# ASTUR | PRODUCT_INTENT_V2 | 2026-11-09

**Status:** `CORRECTED INPUT CONTRACT / APPROVAL-READY / NO IMPLEMENTATION AUTHORITY`

This document separates user-stated requirements from source evidence, runtime evidence, hypotheses and proposals. It fixes the earlier C-R01..C-R12 classification errors.

## Evidence labels

- `USER_REQUIREMENT`: explicitly required behavior.
- `SOURCE_EVIDENCE`: code or branch shows an attempted implementation.
- `CONFIRMED_BUG`: observed wrong behavior or a source defect with a concrete counterexample.
- `CONFIRMED_SOURCE_GAP`: code permits an invalid transition, while runtime occurrence may still be unproven.
- `HYPOTHESIS`: plausible risk needing a failing test/trace.
- `PROPOSAL`: design choice, not user intent.
- `UNDECIDED`: genuine product choice that still changes UX materially.
- `UNKNOWN`: evidence is insufficient.

## User requirements that are no longer open questions

### UR-01 | CS1 is the background in the described mode
**USER_REQUIREMENT.** CS1 stays full-screen/full-width as the background. CS2/CS3/CS4 occupy foreground physical slots. Opening another CS must not automatically minimize, move or replace the currently focused foreground occupant.

What remains open is only **where this mode applies**: which layout/workspace/monitor presets enable it.

### UR-02 | Empty slot first, then N-1 non-focused
**USER_REQUIREMENT.** A new managed foreground window fills a physically empty slot first. When the foreground slots are full, it replaces the N-1 slot that is not the focused slot. The displaced HWND remains recoverable by taskbar, Alt+Tab or explicit selection.

Minimize, close and manual drag are lifecycle exceptions that need explicit rules, but they do not erase this base rule.

### UR-03 | One action must produce a real visible window
**USER_REQUIREMENT.** A taskbar click, Alt+Tab, bar/app selection or equivalent explicit activation must bring the selected HWND physically onto the intended monitor and slot in one action. `GetForegroundWindow` success while the HWND is still at a park coordinate is failure.

### UR-04 | Direct drag and direct cross-monitor transfer
**USER_REQUIREMENT.** Native titlebar drag when Windows emits a valid move loop, custom-titlebar support when detectable, and Alt-drag fallback must move directly between slots/monitors. Required examples include 1→3, 1→4, 4→2 and 3→2. No intermediate CS1 hop, no snap-back and no app-specific CS1 lock.

### UR-05 | Small utilities and transient windows do not own layout
**USER_REQUIREMENT.** Calculator and similar small utilities stay freely sized/movable. WinRAR progress/dialogs, Settings, Zalo/Telegram toasts, Snipping overlays and agent-spawned CMD/PowerShell must not take a tile slot, reflow the desktop or steal foreground merely because they appeared.

Normal apps can still be managed according to explicit policy.

### UR-06 | Native lifecycle must remain native
**USER_REQUIREMENT.** Native maximize/F11, intentional top-edge maximize, minimize/restore, close/reopen, popup ownership, monitor hotplug/RDP, mixed DPI and animation must not corrupt slot ownership, z-order, focus or physical placement.

### UR-07 | Existing useful product surfaces must remain accessible
**USER_REQUIREMENT.** A redesign may reorganize Settings, but it may not silently drop useful behavior from the 14 Settings pages, launcher, status bar, tray, shortcuts, workspace controls, Undo/Redo, hot reload, animation, i18n, integrations and rule/picker editors.

## Runtime evidence

### RT-01 | Foreground HWND physically parked
**CONFIRMED_BUG at symptom level.** Historic trace recorded Telegram as foreground, visible and non-minimized while its RECT was `(480,1355)`, outside both observed monitors and matching Astur's park geometry.

**UNKNOWN:** the exact live binary-to-source mapping for that trace. Do not assign RT-01 to PR #13, release .19 or PR #15 without a matching binary provenance or equivalent fail-first reproduction.

## Source evidence

| Requirement | Source evidence |
|---|---|
| UR-01 | PR #13 / release .18 pinned background and foreground slots; PR #15 reconcile work |
| UR-02 | PR #8 and PR #13 empty-slot/N-1 models |
| UR-03 | PR #10/#11/#15 taskbar and park recovery paths |
| UR-04 | PR #5 native titlebar, PR #11 cross-monitor exchange, PR #12 custom-titlebar classification |
| UR-05 | PR #6/#7 background/policy work; PR #14 and .19 small-utility unmanaged policy |
| UR-06 | PR #4/#8/#9/#13/#15 maximize/minimize/refresh lifecycle work |
| UR-07 | .19 Settings source: 14 pages and extensive reusable control framework |

Source presence is not desktop PASS.

## Corrections to the previous review pack

- **C-R01:** D01/W02 must not ask whether CS1 background exists; only scope of the mode is open.
- **C-R02:** D02/W05 must not ask whether N-1 exists; lifecycle exceptions are open.
- **C-R03:** implementation-derived `pinned_slot_count` is not the definition of user-visible 1/2/4/5.
- **C-R04:** background tool handling is stronger than `Float`; it needs no focus steal and no reflow.
- **C-R05:** Zalo input behavior and native maximize need their own acceptance journeys.
- **C-R06:** 70 rows are feature families, not all controls.
- **C-R07:** seven Settings groups are one candidate IA only.
- **C-R08:** PR #14/.19 and PR #15 diverge.
- **C-R09:** prerelease is not inherently wrong; promotion without the right evidence is.
- **C-R10:** base branch and architecture are design choices after comparison.
- **C-R11:** live binary provenance remains unmapped.
- **C-R12:** reviewer completion and CI success are not desktop acceptance.

## Genuine open product decisions

### UD-01 | Exact visible geometry of 1/2/4/5
The term must be defined by diagrams and RECT expectations. The current implementation may not be used as the definition.

At minimum the approval must specify:
- whether the number means total visible windows, foreground slots, or a preset family;
- whether CS1 consumes one of those positions;
- expected geometry on one monitor;
- expected mapping on two monitors;
- what happens when fewer/more HWNDs exist than the preset.

### UD-02 | Scope of CS1-background mode
The behavior itself is fixed. The remaining choice is which layout/workspace/monitor contexts opt into it.

### UD-03 | Manual drop onto an occupied slot
Choose and document one visible result: swap, replace-with-history, or another explicit operation. Automatic N-1 replacement is a separate rule and must not silently define manual drag semantics.

### UD-04 | Utility policy edges
The product requirement is fixed; the allowlist/signature and the extent of user override are still implementation/product choices. Safety-critical shell/elevation behavior must remain non-overridable where Windows requires it.

### UD-05 | Settings information architecture
Compare:
1. current 14 pages improved in place;
2. grouped navigation with Advanced;
3. task-oriented navigation with feature-preserving search/cross-links.

No candidate may be selected without control-to-control parity.

### UD-06 | Future source baseline
Main, .13, .19 and selective reconstruction are compared separately in `BASELINE_COMPARISON_V2.md`.

## Proposals, not requirements

- rebuild from upstream main;
- retain .19 as the implementation base;
- centralize all lifecycle logic in one controller;
- use multiple narrow controllers with shared postconditions;
- remove physical parking entirely;
- keep parking but never use it as state truth;
- seven Settings groups;
- a new install identity/config path;
- a Rescue/diagnostic page.

These may be approved later, but none is silently promoted by this document.
