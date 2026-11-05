# Astur: slot-anchor admission, free drag and top-edge maximize (2026-11-05)

## Scope and baseline

- Source: `feat/window-policy-engine-v1-20261104` at `de2de5e`, draft PR #7.
- Isolated worktree: `D:\Project\Astur-slot-anchor-20261105`.
- Implementation branch: `feat/slot-anchor-placement-20261105`.
- Existing release/update worktree `D:\Project\Astur` remains unchanged.
- No live desktop inputs, installer, registry, user config or running window are mutated for automated tests.

## UX contract

1. A user's current focused window is the **slot anchor**. Adding a primary tile must never force the anchor off the visible scrolling viewport.
2. **Free slot first**: when a default-width column fits the viewport's unused area, insert it there (e.g., 1/2 and 1/5 layouts). This is per monitor, using that monitor's work area.
3. **Occupied viewport**: prefer the last-used *other* visible column (layer N-1 from the window MRU), otherwise the nearest non-anchor visible column. Put the newcomer into that column as its active tab, preserving the anchor and the displaced window's managed membership. Do not minimize, close, or independently recreate the old window. Switching focus back to the older tab restores it.
   - A in left slot is active, B right: C replaces the displayed tab of B's slot.
   - B in right slot is active, A left: C replaces the displayed tab of A's slot.
   - If only one full-width scrolling column exists, do not silently shrink it; retain the legacy insertion contract.
4. **Drag between slots**: Alt+left-drag or a genuine native title-bar drag can reorder existing windows. A center-drop onto another independent column **swaps** those two slots, including non-adjacent ones. On a multi-tile/tabbed column, keep existing explicit left/right/below drop behavior instead of splitting it.
5. **Top-edge drag to maximize**: releasing a genuine move at the *physical top edge of the destination monitor* maximizes when `WS_MAXIMIZEBOX` is supported. Tiny or stationary clicks never trigger it. A native Windows maximize/F11 remains independent from tiling; restoration can re-adopt it. This is Windows maximize, not synthetic F11.
6. Floating windows and non-scrolling layouts preserve their existing drag and layout contracts. Background/utility/modal/notification exclusions of the Window Policy Engine remain first.
7. Never act on the mouse hook by calling a foreign window's `ShowWindow`. Actual maximize, detachment and retiling are done only on the manager thread.

## Dependency DAG and verification gates

- P0 baseline/ownership -> DONE: clean independent worktree at source SHA.
- P1 pure geometry/admission policy -> P2 integration in `Cmd::Add`.
- P3 native/Alt drag routing + top-edge maximize -> P4 regression tests.
- P5 format/compile/full Rust tests on Windows CI -> P6 review/preview.
- P7 **live 1/2 monitor acceptance** is an independent gate; never claim it passed from synthetic tests or CI alone.

### Acceptance matrix (manual desktop)

- 1 monitor scrolling at half-width: A -> B visible; focus A -> open C: A stays, C in B slot; select B -> open D: B stays, D fills the opposite slot.
- 1 monitor width 0.2: A..D then E fills unused fifth position; sixth enters a non-anchor tab.
- 2 displays: each window is owned and placed on its actual physical monitor; move by title bar and Alt-drag between monitors, including negative virtual-screen coordinates.
- Drag from slot 1 to slot 2/3/4 or back, center-drop, verify swap and focused status, then use edge-drop to verify Niri before/after/consume unaffected.
- Drag any eligible normal tile to the physical top edge -> native maximize; drag a maximized app down, minimize/restore, and check no phantom tile or lost HWND.
- Windows-native Snap, F11 media, Zalo toast and focus-follows-mouse remain usable. No new overlays may intercept mouse input.
- Quit/relaunch Astur and check parked tabs and rescue behavior, including unexpected termination.

## Safety boundaries

- No process kills, launch into the user's live desktop, release promotion, UI toggle creation, or blanket class/process exemptions.
- No force push, remote rewrite, or touch to other user projects.
- Report CI and live evidence separately. Package a preview only with fresh format/test/build evidence.

## Session handoff

Update with final branch HEAD, commit, CI URL/result, worktree status and remaining live acceptance after verification.
