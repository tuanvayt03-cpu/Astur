# Astur scrolling: Stable slots, tab drag and minimize (2026-11-05)

## Baseline / ownership

- Reference: `Astur VI Update 2.4.0.14`, release commit `1b665143a8bf15d831d8191fb57f9ff3f5668544`; https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-update-2.4.0.14
- Isolated primary-writer worktree: `D:\Project\Astur-slot-stability-20261105`, branch `fix/astur-stable-slots-20261105`. Other worktrees/installed Astur remain untouched.
- Evidence: real desktop screenshot on 2026-11-05 showing Chrome TradingView left, MT5 behind and MT5 Control Hub on right; user reports CS1→CS2 tab dragging fails, CS3 inserts at CS1/displaces CS2, minimizing CS1 relocates CS2 into CS1.
- Problem is not a Settings toggle. The prior 2.4.0.14 unit tests passed but did not exercise multi-stage viewport/focus/Win32 drop/minimize interactions.

## Root causes

1. `Cmd::Add` called `Manager::insert_window` which immediately invoked `ensure_visible`, **before** `col.tabbed=true` and `col.active=new`. The newly focused tab was allowed to shift the viewport and push the old slot out.
2. `window_under_point` read real `GetWindowRect` during a drag; those rectangles can be stale, animated or dragged, not the intended layout slots. Further, the old center-swap allowed only single-window columns, so swapping an active tab out of a tabbed column was blocked.
3. `tiled_windows` removed iconic HWNDs from the scrolling strip. Minimizing CS1 deleted its geometric column and immediately shifted all later slots left. The MINIMIZE event also ran `ensure_visible`, possibly inducing another scroll.
4. A delayed synthetic `Focused` event after add/minimize could call `strip_reveal` again and reverse a stable layout. A bounded one-use guard is necessary for this specific automatic focus transition, without disabling ordinary user clicks/taskbar focus. The old reveal also scrolled a half-width column that was 98% visible merely because its last 2% clipped at the edge; automatic focus now keeps slots that are at least 75% visible stationary, but still reveals mostly-offscreen/parked tiles. Explicit scrolling keys retain their previous semantics.

## Implementation contract

- Scrolling layout geometry includes live minimized HWNDs as **reserved occupants**. Actual Win32 placement continues to skip iconic surfaces. Other layouts retain existing minimize-and-compact semantics.
- A new window keeps the previous focus anchor's strip X position. Reconcile the saved offset after insertion/tab metadata commits; only a column added *before* the anchor may adjust the offset by its exact span.
- Resolve dragging via Astur's layout rectangles and visibility classification, not animation-dependent `GetWindowRect`. A center drop swaps the two selected occupants, even across nonadjacent columns and a tabbed slot. Reassign the column IDs and last-active tabs to preserve grouping and width by position. Edge drops still use before/after/below rules.
- On minimizing a focused tile: reserve its slot, select a live tab in the same column or nearest live column, and do not call viewport-recentering. Drop the automatic follow/reveal exactly once within 900 ms after minimize or admission; explicit later interactions still reveal normally.
- Keep F11, native maximize, top-edge drag, notification exemptions, Window Policy Engine, and two-monitor boundaries unchanged.

## Verification DAG

- B0: base Git/status, owner/worktree and release integrity -> PASS prior to implementation.
- B1: pure layout/slot/minimize/drag correction -> IMPLEMENTED on feature worktree.
- B2: local `git diff --check`, bilingual inventory and installer contract -> run.
- B3: Windows CI Rustfmt, Clippy (-D warnings), full Rust tests, release workspace build -> **must PASS on fresh commit**.
- B4: review and fix compile/test regressions (max two repairs for a root cause, then re-diagnose).
- B5: portable preview GitHub Actions artifact for acceptance; do not automatically alter installed Astur on the user's desktop.
- B6: real desktop E2E (1/2, 1/4, 1/5, 2 monitors including negative coordinates, Chrome/MT5 and generic windows, open C while A/B focused, minimize/restore each, native title-bar drag and Alt+drag, F11/maximize, Zalo click-through) -> **PENDING** until real evidence.
- B7: only then release/promotion with version bump after stable behavior proven.

## Acceptance scenarios

- Two slots: focus CS1 at slot 1, add CS3 -> CS1 unchanged, CS3 visible at slot 2 with CS2 still recoverable as an inactive tab. Focus CS2 at slot 2, add CS3 -> CS2 remains slot 2, CS3 appears in slot 1.
- Five slots: fill empty slots first; adding the sixth reuses a non-anchor tab, not forced insertion into the focus column.
- Drag from CS1 to CS2/3/4, also from a tabbed slot, center-drop swaps and leaves unrelated columns fixed. Edge drops preserve explicit insert/group semantics.
- Minimize CS1 while CS2 is at slot 2: CS2 keeps its X position and remains managed. Restore CS1 recovers its original slot without duplication.
- Cross-monitor drag and maximize do not reassign an unrelated window's monitor or disturb MT5 orders, pointer, or popup focus.

## External research

- Niri scrolling implementation maintains separate `columns`, `active_column_idx` and `view_offset`, and retains prior activation/offset information on removal: https://github.com/niri-wm/niri/blob/main/src/layout/scrolling.rs
- Niri layout configuration offers explicit center-on-focus modes: https://niri-wm.github.io/niri/Configuration:-Layout.html
- PaperWM documents window navigation and automatic focus visibility as distinct mechanisms: https://github.com/paperwm/PaperWM
- These are comparable design approaches, not claims that their Linux compositor code can directly run in Win32 Astur.

## Recovery point (update after CI)

- Source release 2.4.0.14 is preserved and not modified. No new installer should be advertised as production-ready before B3+B6.
- Record branch HEAD, PR, CI URL/outcome, Git status, remaining acceptance, possible defects; only claim PASS with fresh evidence.
