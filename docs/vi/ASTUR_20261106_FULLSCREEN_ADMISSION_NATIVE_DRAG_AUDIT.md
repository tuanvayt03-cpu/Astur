# Astur 2026-11-06: Full-width admission, inconsistent native drag and real desktop video

## Baseline / owner

- Current released baseline `astur-vi-update-2.4.0.17` -> `384dbebe31e0ef3e98f443541673c4b510931cea`.
- Isolated single-writer fix `fix/astur-native-drag-admission-20261106`, CodeLocal worktree `D:\Project\Astur-native-drag-admission-20261106`.
- Video privately supplied by the user on 2026-11-06: `2026-11-06 09-18-43.mp4`, 1536x864, 30fps, 23.533s. The recording and unredacted screenshots shall never be committed to GitHub. Contact-sheet observations: 0–3s chat windows side by side, 3–7s MT5/chat and Calculator briefly appear, 10–11s Calculator in left slot, 20–23s TradingView/MT5/Control Hub. Rapid replacements occur in both halves. The video does NOT encode WinEvent, layout-col IDs, mouse hooks or foreground IDs and cannot alone prove which handler ran.
- Additional user symptom: while moving CS1 to CS2 some windows swap, others remain anchored in CS1; new CS3 sometimes steals CS2 even when user considers an overlay slot empty; CS1 full background must persist unless manually minimized.
- The currently installed Astur/process must not be stopped, modified or restarted during source/CI work; MT5 and chat content untouched.

## Confirmed source-level causes/constraints

**Admission gap:** `scroll_anchor_admission` reads only nonfloating scrolling columns and considers free space solely at the two ends of a *packed* strip. A lone full-width scrolling column occupies the full viewport: no free physical slot is reported and no other visible column exists, so the function returns `(None,None)`. `Cmd::Add` then falls back to insert-new-column and calls `ensure_visible`, which can scroll the old full-width column off screen. This directly conflicts with the user-requested persistent fullscreen background + side-by-side front overlay slots.

**Fullscreen is overloaded:** native maximized `IsZoomed`/independent HWND is a separate lifecycle from `MaximizeColumn` (a managed scrolling column with width ~1.0). The two should not be collapsed without a clear model. User video alone does not establish which state the failed attempt used.

**Inconsistent native drag:** `EVENT_SYSTEM_MOVESIZEEND` in the released baseline dispatches `DragMoved` only when a captured source exists AND the start point passes `native_caption_drag_origin` (requires `WS_CAPTION`, restrictive position). A custom title bar can enter genuine native move/resize and change the actual window rectangle yet be routed to `DragResized`, which retiles to its old slot. Some UIs never send native Win32 MOVESIZE events for their own drag interactions. Therefore no universal mouse-titlebar guarantee can be claimed without real event evidence. The explicit `Alt+left-drag` fallback is supported independently.

**Drop-zone ambiguity:** same-monitor swaps are accepted only in the central 50% of the target rectangle; dropping near its first/last 25% follows before/after/Below insertion, which may scroll the viewport and make a successful drag appear to have failed. Configurable edge-zone semantics and explicit diagnostics are necessary.

## Implemented low-risk code patch on this branch

1. Capture the starting HWND rectangle on `EVENT_SYSTEM_MOVESIZESTART` with atomic data only (no blocking call in low-level mouse hook).
2. At MOVESIZEEND, classify a native move by actual translation, approximately unchanged dimensions, and actual cursor travel, even if `WS_CAPTION` and fixed Y-zone tests fail. Keep native resize, real snap/maximize, click and drag semantics untouched. Does not spoof drag for an app that never emits MOVESIZE events.
3. Widen centre-drop swap area from 50% to 75% of the target window, retaining narrow 12.5% edges for explicit insertion; add independent regression assertions for native custom-titlebar move, native resize, no movement, negative monitor coordinates and slot threshold.
4. Debug-only, privacy-safe admission and native-drag outcome telemetry: HWND, monitor/workspace, offset, full-width flag, action and boolean gate results. Never capture window title, contact, chat content, broker account or screenshot in GitHub logs.

## Next mandatory architecture change (not included in low-risk patch)

**One coherent monitor presentation model** rather than extending the scrolling strip's ad-hoc `tabbed/auto_stack`:
- Separate `PinnedBackground` from `OverlaySlot` occupancy and `active/focus`.
- When CS1 is full-width and user opens CS2: CS1 remains background full-screen, CS2 fills front slot 1/2 (or chosen region) without becoming a second scrolling column.
- CS3 fills the other visible front slot; CS4 reuses the non-anchor front slot per layer N-1. CS1 is never minimized/parked or replaced merely because a newer window appears.
- Explicit minimize/close/unpin/restore transitions promote/demote background and slots deterministically. Fullscreen native/Win32 and full-width Astur column must have separate transition contracts.
- Empty/front slot selection uses geometry of *actually occupied presented slots*, not width of background, MRU alone, or hidden tabs. Inter-monitor drag targets explicit slot IDs.
- Persistent stable slot IDs, a deterministic policy precedence, one writer/one transition per event, and a post-transition invariant check (no window lost, no duplicate HWND, no non-anchor displacement, no unwanted workspace switch).
- Required E2E: fullscreen CS1 + CS2 → CS3 → CS4; focus either overlay; 1/2, 1/4, 1/5; 2 monitors including negative coordinates; native/custom titlebars, Alt+drag, taskbar Telegram once, minimize/restore and Zalo notification safety.

## Execution DAG and gate

1. Baseline and source audit COMPLETE; no source of private data added.
2. Native drag classification + drop tolerance + non-sensitive logging IMPLEMENTED.
3. Rustfmt, Clippy -D warnings, Windows full tests, x64 build: **must pass on fresh commit**, no weakened tests.
4. Review one pass, fix any same-lifecycle defect and rerun fresh CI.
5. Deliver a branch and draft PR for inspection; **do not publish another auto-updater yet**.
6. Fullscreen pinned-background model is a separate major transition, BLOCKED for stable rollout until desktop event evidence establishes whether the active case is native maximize or scrolling full-width column. Do not fake acceptance from a passing source CI.
7. Actual Windows desktop QA using disposable windows with no MT5 order/control interaction; no second Astur window manager on an active trading desktop. Collect only event-code / HWND style bits / geometry / monitor / slot IDs with bounded retention, then re-evaluate.

## Recovery

Previous 2.4.0.17 release remains unchanged. Record exact branch HEAD, CI URL/status, Git clean state, draft PR and remaining E2E gate at checkpoint.
