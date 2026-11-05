# Astur: Telegram taskbar recovery + direct cross-monitor slot drag

Date: 2026-11-05, timezone ICT. Owner: CodeLocal single primary writer. Baseline `release/astur-vi-update-2.4.0.16` at `9ba362457de7dcc7ad5fe6167314e4375b27dc7c`, GitHub prerelease remains immutable. Isolated worktree `D:\Project\Astur-cross-monitor-telegram-20261105`, branch `fix/astur-cross-monitor-telegram-20261105`.

## Video evidence

User's own Windows desktop recording `2026-11-05 18-09-12.mp4`, 1536x864, 30 fps, 53.633 seconds. The 11-clip storyboard and redacted contact sheet are kept ONLY in the conversation artifact, not in the repository, because the recording contains customer/chat/MT5 information. The source video has NOT been uploaded to GitHub.

- 0–7s: two Chrome windows, stable split.
- 7–9.5s: strong two-region changes to MT5/Telegram and back.
- 15.7–20.3s: left MT5 changes first, then Control Hub in right.
- 28.5–32.6s: Telegram appears at left, then both regions change.
- 32.6–39s: two chat windows side by side.
- 39–42s: both regions change with MT5/Telegram.
- 45.8–51.1s: taskbar/Chrome changes.
- 51.1–53.6s: MT5 and Explorer.
- Frame samples at 3.33 Hz show synchronous changes near 7.2, 8.4, 20.4, 30.0, 32.7, 40.5, 42.0 and 51.3 seconds. These are **observed** pixel/scene changes, not a trace of key/mouse input or proof of which WinEvent path executed.

User independently reported Telegram taskbar clicks sometimes do not raise the window; do not treat one 30fps visual sequence as a full handler trace. Runtime events will need direct evidence.

## Root causes identified in source

1. Cross-monitor `Cmd::DragMoved` goes through `Manager::move_window`. The detach calls `ensure_visible` on source and insertion calls `ensure_visible` on destination *before* final placement. In a two-slot/two-monitor scrolling layout, dropping CS4 onto target slot 2 can visually recenter at slot 1 then move to slot 2.
2. Unlike same-monitor swaps, cross-monitor center drops only inserted the dragged HWND into a destination column; the occupant's original slot was not exchanged atomically. Slots could be split or offset changed. The mouse's destination physical viewport must determine target, not the source window's index or focus.
3. In `EVENT_SYSTEM_FOREGROUND`, repeated HWNDs are ignored by the `LAST_FG` dedup unconditionally. A repeated foreground event is not redundant if the same HWND is still parked/hidden by Astur/iconic. `EVENT_OBJECT_SHOW` could also occur for an already tracked parked window without a new foreground transition; a guarded recovery is needed.
4. A synthetic focus echo from an admitted window is guarded against scrolling to preserve the anchor. When the HWND remains physically parked, the echo must still allow a **retile without recenter**, not permanently skip placement.

## Implemented contract / scope

- On a genuine cross-monitor drop into an **occupied scrolling slot**, exchange the two shown HWNDs as one model mutation. Window order, per-slot column identity, width, tab mode/auto-stack, weights and viewport offsets remain attached to positions. Swap HWND owner monitor, preserve group semantics and place both windows on the new monitors; no transient insertion into monitor destination slot 1.
- A cross-monitor drop without a slot target retains prior before/after scrolling insertion behavior; drops onto occupied non-scrolling layouts retain their existing order contract.
- A repeated foreground event is reprocessed only if a *managed* HWND is still off all monitors, Astur-hidden or minimized. Ordinary duplicate events still skip work. `EVENT_OBJECT_SHOW` for an already managed HWND may request recovery only if the same HWND is current foreground, visibly parked, and no Astur suppression is active. No background app can steal focus through this branch.
- If an admission foreground echo is suppressed but actual recovery is needed, **retile without ensure_visible** to keep the current anchor stationary.
- Log at debug level only minimal HWND, monitor id, workspace and recovery reason, never user chat, account, image or window title. Keep the existing rescue snapshots and AppId behavior unchanged.
- Floating, manually controlled windows and native top-edge maximize retain existing paths.

## DAG and verification

1. Baseline and owner/worktree resolve; preserve the 2.4.0.16 release and unrelated desktop state.
2. Atomic cross-display exchange with precise drop target and no early source/destination recentering. Add model tests for 4→2, 1→3, 3→2, non-adjacent monitor/slot changes and grouped metadata preservation.
3. Foreground, SHOW, parked/hidden/minimized recovery with pure dedup test, runtime debug instrumentation.
4. `git diff --check`, static translations, upgrade/preview contract -> PASS on current source; Windows rustfmt, Clippy -D warnings, full Rust tests and x64 release build -> require fresh CI.
5. Review changes; fix in-scope defects and rerun fresh CI.
6. Publish a **portable preview** only after CI; no automatic user desktop install. Manual acceptance must reproduce: (a) Telegram taskbar one click from park, (b) CS1–CS4 direct cross-display swaps, (c) no auto tab title strip, (d) minimize/restore, two monitors including reversed and negative coordinates, (e) Zalo & MT5 focus safety. Never claim live PASS from source tests.
7. Release installer only after manual acceptance and in-place rollback smoke, else leave draft PR and preview.

## Safety and handoff

No active Astur instance, window, mouse, MT5 order/route, registry or user config changed. No force push, branch rewrite or blind retry. Log and store runtime-safe metadata only. After work, checkpoint exact SHA, CI link, PR, clean Git state and remaining live QA.
