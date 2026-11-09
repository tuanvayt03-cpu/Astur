# ASTUR | WIN32 ENGINE AUDIT V2 | 2026-11-09

**Audited ref:** PR #15 HEAD `69944546258e30bd9de761803999e9767dbf0101`
**Mode:** source/read-only audit; no live desktop test
**Verdict:** `ONE NEW CONFIRMED SOURCE GAP / THREE R2 RISKS MITIGATED BUT E2E UNPROVEN`

## 1. Ground rules

A source finding is not automatically a runtime incident. Runtime assertions require trace or a fail-first reproduction. Conversely, a deterministic code counterexample can establish a source gap even before the event ordering has been seen on the user's machine.

## 2. H1 — restore_all_windows 500 ms exit race

### Evidence
`restore_all_windows` around L7881:
- sets `EXITING=true` with SeqCst before the wait;
- unhooks input;
- waits at most 500 ms while `MGR_BUSY`;
- restores tracked windows.

Manager loop around L20574 sets `MGR_BUSY=true` before checking `EXITING`; commands arriving after exit are dropped.

`set_pos_raw` around L1197 returns immediately while `EXITING` is true.
`switch_plain` around L12739 also returns while `EXITING` is true.

### Assessment
**MITIGATED / no confirmed bug.**

The 500 ms bound alone is not proof that an old command can re-park a restored window. The code deliberately blocks the main placement and workspace-hide paths after `EXITING`.

### Residual test
Still test:
- a command already inside a synchronous Win32 call when EXITING flips;
- a hung app;
- posted `SWP_ASYNCWINDOWPOS` requests already in the foreign app queue;
- exit during workspace switch/motion teardown.

Expected invariant: after exit restore reaches its safe boundary, no Astur action may hide or park a user window again.

## 3. H2 — minimize / foreground permutations

### Evidence
PR #15 adds several targeted mitigations:

- `focused_follow_allowed` checks that a queued `Cmd::Focused(h)` still owns the root foreground at processing time.
- `synthetic_reveal_guard` prevents a minimize-induced foreground echo from pulling a scrolling survivor into a different column.
- Pinned overlays bypass that guard and reconcile active member on foreground.
- `PinnedOverlay::minimize_successor` keeps the minimized HWND reserved in its slot and selects a live successor.
- `Cmd::ActivateWindow` restores, switches workspace when needed, then calls `strip_reveal` and forces placement for iconic targets.

### Assessment
**MITIGATED / HYPOTHESIS remains for event ordering.**

The source directly addresses the earlier failure classes. There is no evidence here that the remaining permutations currently break state. The missing evidence is an exhaustive event-order test for sequences such as:

`MINIMIZESTART(A) → FOREGROUND(B) → MINIMIZEEND(A) → RetileFor(A)`

and rapid taskbar toggle/restore sequences.

## 4. H3 — monitor refresh versus posted placement

### Evidence
`refresh_monitors` around L13092 now:
- snapshots tracked HWND ownership;
- takes strips, overlays and old focus;
- rebuilds monitor topology;
- re-homes windows;
- restores pinned overlay only after re-home via `reconcile_members`;
- restores focus where the old focused HWND is still valid.

Placement uses `SWP_ASYNCWINDOWPOS` by default. The source documents the consequence that a posted request has not necessarily landed when the manager continues. It also documents that requests sent to one HWND are intended to remain FIFO when placement mode is not mixed.

### Assessment
**MITIGATED / HYPOTHESIS.**

The overlay-loss defect from the older source is repaired in PR #15. The remaining concern is physical stale placement from a pre-refresh topology landing before the newest post-refresh request. FIFO-per-HWND should make the newer request win, but this needs an actual topology-change harness because HMONITOR/work-area identity changes are precisely the hard edge here.

### Required test
A deterministic fake/Win32 harness should enqueue old placement, refresh monitor topology, enqueue the new placement, then assert the final RECT belongs to the new topology. Add negative-X, vertical offset, mixed DPI and unplug/replug cases.

## 5. H4 — stale MOVESIZEEND can clear another HWND's native drag

### Source counterexample
At `EVENT_SYSTEM_MOVESIZESTART`, the global `NATIVE_DRAG` atomic is set to the current HWND.

At `EVENT_SYSTEM_MOVESIZEEND` around L21464:
```text
source = NATIVE_DRAG.swap(0)
...
as_move = source == h && ...
```

The HIDE/DESTROY/MINIMIZE cleanup path already uses a safer pattern:
```text
NATIVE_DRAG.compare_exchange(h, 0, ...)
```

Counterexample:

1. START(A) stores A.
2. Before a delayed END(A), START(B) stores B.
3. delayed END(A) executes `swap(0)`, obtaining B and clearing the global active state.
4. `source == h` is false, so A is not accepted as B's move.
5. END(B) later sees `source=0`; B has lost its native-drag context and can fall into the resize/reconcile path.

### Assessment
**CONFIRMED_SOURCE_GAP, runtime occurrence UNKNOWN.**

The equality check protects the wrong HWND from being committed as the move, but it does not protect the actual current HWND's state from being erased.

### Future repair requirement
Do not implement in this docs-only branch. The implementation phase should first add a fail-first test for the ordering above, then either:
- clear with `compare_exchange(h, 0)` and consume metadata only when ownership matches; or
- store a per-HWND/generation drag context if overlapping native move loops must be represented.

No test may be weakened to make the race disappear.

## 6. Activation/park audit

PR #15 improves `strip_reveal` so that a pinned overlay activation:
- checks whether the HWND is physically parked or hidden by Astur;
- repairs missing overlay membership for managed tiled targets;
- updates `ws.focused`;
- unhides Astur-hidden targets;
- performs a forced instant retile for a parked correctness repair.

`Cmd::BarFocus` routes managed targets through `Cmd::ActivateWindow`, reducing path divergence.

**Source verdict:** the historic parked-foreground symptom has a plausible direct repair in PR #15. It is still **desktop-unverified**.

## 7. Exit/async placement note

The source explicitly states that:
- default async placement posts `SetWindowPos` to foreign window queues;
- a read may see old geometry before a posted placement lands;
- changing async mode while an older posted move is still queued can produce one stale landing until the next retile.

This is an accepted implementation caveat, not permission for V2 to use a requested future RECT as proof that a HWND is physically visible.

## 8. Required V2 engine invariants

1. Activation PASS requires physical monitor intersection, not just model state or foreground API success.
2. One HWND has one owner/category at a time.
3. A foreground slot has one active visible member; hidden history is not active presentation.
4. Minimize preserves reservation but not false focus.
5. Stale events may not mutate another HWND's active drag/activation generation.
6. Monitor refresh must invalidate/reconcile geometry against the new topology.
7. Exit makes every later placement/hide a no-op.
8. Window animation is cosmetic; losing animation must never lose physical correctness.

## 9. Verification gate

Before a V2 release:
- pure model tests for all event permutations;
- Win32 integration tests for real HWND geometry and iconic/visible state;
- rapid taskbar/Alt+Tab loops;
- native/custom-titlebar drag;
- dual monitor, negative X, vertical offsets, mixed DPI and display refresh;
- isolated desktop acceptance.

CI alone does not satisfy this gate.
