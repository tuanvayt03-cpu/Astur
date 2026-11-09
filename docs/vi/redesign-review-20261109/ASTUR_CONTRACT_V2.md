# ASTUR | PRODUCT AND ENGINE CONTRACT V2 | 2026-11-09

**Status:** `REVIEW COMPLETE / AWAIT PRODUCT APPROVAL / IMPLEMENTATION NOT STARTED`

This is the approval boundary. It defines visible behavior and evidence gates, not the final internal architecture.

## 1. Core product invariants

### C01 — Window ownership
Every HWND is in exactly one effective category:
- ManagedTile
- ManagedFloat
- NativeIndependent
- Modal/OwnedTransient
- Ignored

The effective category must have a reason/source that diagnostics can show.

### C02 — Physical truth beats intended geometry
A focus/activation operation is successful only when the target's actual Win32 state satisfies the action:
- expected visible;
- expected non-iconic;
- actual RECT intersects the intended monitor/slot;
- no unrelated managed window was displaced without contract authority.

An intended slot or successful focus API call alone is insufficient.

### C03 — CS1 background mode
Inside the approved overlay mode:
- CS1 is the full-screen/full-width managed background;
- foreground slots exist independently above it;
- opening foreground windows does not shrink CS1;
- explicit native-maximized backgrounds remain Windows-native and are not resized/parked by Astur.

### C04 — Automatic foreground admission
1. Fill a physically empty foreground slot first.
2. If full, replace the N-1 slot that is not focused.
3. Keep the previous occupant recoverable as history.
4. Automatic history must not silently enable the manual tab UI.

### C05 — Explicit activation
Taskbar, Alt+Tab, bar/app button and explicit selection use the same visible outcome:
- select the requested HWND;
- switch to its workspace/monitor if required;
- restore if appropriate;
- reveal/reconcile its physical slot;
- focus after geometry is correct.

### C06 — Minimize and restore
Minimize:
- preserves the HWND's slot/history reservation;
- removes it from active visible presentation;
- chooses a deterministic live successor when needed;
- does not shift unrelated slots.

Restore:
- returns the HWND to its reserved physical slot/history context;
- does not require repeated taskbar clicks.

### C07 — Close/destroy/hide
- Destroy removes ownership and membership.
- App-driven close-to-tray/hide is not mistaken for destroy.
- Closing an active history member can reveal the previous valid member without moving unrelated slots.
- No ghost HWND remains in active slot state.

### C08 — Manual drag
Native-titlebar, custom-titlebar when reliably detectable, and Alt-drag fallback are adapters to the same drop contract.

Cross-monitor transfer is direct and atomic from the user's perspective. No intermediate CS1 placement is committed.

### C09 — Utilities, modal and transient UI
Utilities/toasts/progress/modal windows do not receive normal tile ownership unless explicitly eligible. They must not reflow the layout or steal foreground merely by appearing.

### C10 — Maximize/fullscreen
Native maximize/F11 remains native. Intentional top-edge maximize is honored. Restore-to-normal is the point at which a window may re-enter managed geometry.

### C11 — Monitor topology
Hotplug, RDP, primary changes, negative-X and mixed-DPI changes must:
- preserve surviving window/workspace ownership;
- re-home only when needed;
- reconcile slot/history membership;
- recompute physical geometry;
- leave no active HWND outside all monitors unless intentionally hidden/iconic.

### C12 — Exit and rescue
Once exit restore starts:
- later manager commands may not hide/park/move windows;
- all managed/parked/hidden-by-Astur windows are recovered;
- crash-rescue data remains usable if graceful exit cannot finish.

### C13 — Cosmetic isolation
Animation, bar and visual effects are never correctness dependencies. Failure or disablement must reveal already-correct physical windows.

### C14 — GUI parity
No Settings redesign is accepted until every retained old control/action has a V2 destination and persistence/Undo/hot-reload behavior is accounted for.

### C15 — Provenance
About/diagnostics and release artifacts must identify source commit/build/package provenance sufficiently to map a runtime binary back to source.

## 2. Event transition truth table

| Event/action | Required transition | Required postcondition |
|---|---|---|
| SHOW/ADD managed | classify → assign owner → admit to workspace/slot | ownership unique; no focus steal unless user foreground action |
| SHOW transient/utility | classify native/modal/ignored | no tile/slot allocation; no reflow |
| FOREGROUND/FOCUS | reject stale event or reconcile target | target physically visible if action requires visibility |
| TASKBAR / ALT_TAB / BAR_FOCUS | activate through common outcome | one action recovers exact requested HWND |
| MINIMIZESTART | keep reservation, clear active presentation if needed | iconic HWND not recorded as active visible focus |
| MINIMIZEEND / RESTORE | restore → reveal/reconcile reserved slot | correct RECT and focus; no neighbor shift |
| APP HIDE | preserve or untrack according to actual current visibility/ownership | close-to-tray remains app-owned |
| DESTROY/CLOSE | remove membership and stale state | no ghost slot/history entry |
| DRAG START | acquire drag ownership/context | one active owner/generation |
| DRAG MOVE | preview/track without unrelated retile | source ownership preserved |
| DRAG END | commit only if event owns active drag context | stale END cannot clear another HWND's context |
| CROSS-MONITOR DROP | transactional source/destination update | no intermediate CS1 landing |
| LAYOUT CHANGE | explicitly migrate/dissolve overlay semantics | no stale hidden/overlay state |
| MONITOR REFRESH | snapshot → rebuild → rehome → reconcile → retile | final actual RECT belongs to new topology |
| EXIT | set exit fence → stop new mutation → restore | no post-restore Astur placement/hide |

## 3. Behavioral acceptance matrix

### B01 — CS1 background
CS1 remains full-screen background while CS2/CS3/CS4 are introduced and focused in different orders.

### B02 — 1/2/4/5 geometry
Must be tested only after UD-01 is approved with explicit diagrams/RECTs. No source-derived definition is accepted.

### B03 — Empty then N-1
Open windows until slots fill, then add one more. The focused slot remains untouched; the chosen N-1 occupant becomes history and can be called back.

### B04 — One-click recovery
Alternate taskbar and Alt+Tab among visible and history/park candidates at least 30 times. No foreground, non-iconic HWND may remain outside monitor bounds after settle.

### B05 — Native/custom/Alt drag
Test Notepad/Explorer/browser plus a custom-titlebar app and Alt-drag fallback. No app-specific lock at CS1.

### B06 — Cross-monitor direct transfer
Test 1→3, 1→4, 4→2, 3→2 with monitor positions including negative X and vertical offset.

### B07 — Utilities
Calculator, Snipping Tool, Task Manager and representative small utilities keep native size/mobility and do not consume slots.

### B08 — Background tool/progress
Spawn safe dummy CMD/PowerShell and progress/dialog windows. They must not force foreground or reflow.

### B09 — Toast/input
Representative toast/notification overlays do not tile and do not leave a click-blocking Astur layer.

### B10 — Native maximize
Maximize/F11/top-edge intentional maximize, restore and then re-adopt normal geometry. No snap-back while native-maximized.

### B11 — Minimize lifecycle
Minimize active/nonactive slot members in different orders; other physical slots do not shift.

### B12 — Monitor/RDP lifecycle
Refresh topology, unplug/replug simulated/test monitor, mixed DPI and RDP/session transition. No ghost ownership or offscreen active window.

### B13 — GUI parity
Exercise every retained control path, conditional section, table add/remove/reorder, picker, reset, Undo/Redo, hot reload and EN/VI render.

### B14 — Exit/rescue
Quit while windows are parked/hidden and while an app is slow/hung. Recovery must leave user windows reachable.

### B15 — Native-drag stale END regression
Fail-first event model:
START(A) → START(B) → END(A) → END(B).
END(A) must not erase B's drag context.

### B16 — Provenance
Installed/test binary exposes build/source identity and package checksum mapping.

## 4. 1/2/4/5 approval sheet

This contract intentionally does not guess the final visible geometry.

Before implementation, approve one diagram set defining:
- meaning of 1, 2, 4, 5;
- whether CS1 is counted;
- physical slot rectangles;
- behavior with fewer windows;
- overflow behavior;
- two-monitor mapping.

Until approved, `scroll_default_width`, `pinned_slot_count` or any existing implementation is **not** the product definition.

## 5. Manual drop approval sheet

Automatic N-1 is already fixed. Manual drag onto an occupied slot still needs one choice:

- **Swap:** source and target exchange physical slots.
- **Replace/history:** source becomes active in target slot; target stays in that slot's history.
- **Other explicit operation:** must define where both HWNDs end up.

No implementation may choose this silently.

## 6. Settings IA approval sheet

All candidates must satisfy `GUI_CONTROL_MANIFEST_V2.md`.

- A: current 14 pages improved;
- B: grouped navigation + Advanced;
- C: task-oriented navigation + search/Advanced.

Decision is UX-only; it may not change retained backend features by accident.

## 7. Future baseline recommendation

`BASELINE_COMPARISON_V2.md` recommends, as a **PROPOSAL**, upstream main plus selective reconstruction. Approval is still required before creating the implementation fork/branch.

## 8. Engineering strategy after approval

The contract does **not** mandate one exact class/module design. It does mandate these properties:

- one primary writer for shared state;
- manager remains authoritative for window/workspace state;
- hooks remain fast and queue work;
- every lifecycle path shares the same postconditions;
- stale event ownership/generation is explicit;
- physical placement is verified;
- cosmetics cannot own correctness.

A centralized transition helper is a strong candidate, not a product requirement.

## 9. Verification and release gates

### Code gate
Fresh after the final code change:
- rustfmt;
- clippy with warnings denied;
- unit/property/model tests;
- Win32 integration tests;
- Settings/config regression tests;
- release build;
- packaging/checksum/rollback smoke.

### Desktop gate
On an isolated Windows session/PC/VM with disposable apps:
- B01-B16 applicable desktop cases;
- 1 and 2 monitors;
- negative X / offset / mixed DPI;
- repeated taskbar/Alt+Tab;
- native/custom/Alt drag;
- utilities/modal/toasts;
- maximize/minimize/restore;
- topology refresh.

No active trading windows.

### Promotion gate
No desktop E2E = no stable/user promotion, regardless of CI.

## 10. Product decisions still requiring approval

Only these materially open choices remain:

1. **UD-01:** exact 1/2/4/5 visible geometry.
2. **UD-02:** which contexts enable CS1-background mode.
3. **UD-03:** manual drop onto occupied slot.
4. **UD-04:** utility-policy allowlist and override edges.
5. **UD-05:** Settings information architecture.
6. **UD-06:** approve/reject the proposed future baseline.

Everything else above is either a fixed requirement, evidence, or an engineering verification obligation.

**Terminal state:** `REVIEW COMPLETE / AWAIT PRODUCT APPROVAL`.
