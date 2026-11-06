# Astur Pinned Background + Foreground Slots — implementation / handoff

Date: 2026-11-06. Main writer: CodeLocal. Baseline: `fix/astur-native-drag-admission-20261106` at `6bf0a2cffc20a868dea9a7e7aa2a3e1850353fed`; previous release `astur-vi-update-2.4.0.17` at `384dbebe31e0ef3e98f443541673c4b510931cea`. Isolated branch `feat/astur-pinned-overlay-20261106`, worktree `D:\Project\Astur-pinned-overlay-20261106`. Do not modify original installed Astur or desktop MT5/Chatwoot sessions. No private video, account data or window titles committed.

## User contract

- CS1 is full-width/fullscreen and must stay fullscreen unless the user intentionally restores/minimizes it. A managed Astur full-width column and a Windows-native maximized HWND are distinct, both supported as backgrounds by explicit state instead of by implicit scrolling width.
- CS2 appears in a foreground slot without resizing/parking CS1. With 1/2 width, it fills right; CS3 fills the vacant left half. No unnecessary replacement, horizontal slide or new manual tab bar.
- When every foreground slot is occupied, the next CS4 fills the previously used OTHER slot (N-1), not the focused slot. Previous occupants remain managed, and can be restored from taskbar/Alt+Tab. Closing CS4 reveals the prior occupant of that slot.
- For 1/4 and 1/5 widths, foreground slots derive from `scroll_default_width`; fill vacancies before replacing the previous other slot. The active slot remains stable.
- Same-monitor drag targets physical slot geometry (including gaps), not the underlying strip index. Dragging fullwidth *managed* background into a slot exchanges it with the active foreground occupant. An independent Windows-native maximized background is not resized or exchanged by the WM.
- Cross-monitor occupied-slot moves exchange HWND ownership and slot membership atomically, with no transient insertion through destination column 1. Source and destination stay managed; no duplicate HWND or lost slot.
- Foreground focus on a prior hidden overlay member must activate it and physically place it into its original reserved slot on the same taskbar action; inactive stacked members are parked offscreen, not Windows-minimized. When a native fullscreen background gets taskbar focus, it may cover overlays until they are selected again.
- On native maximize restore/close, the external overlay presentation is dissolved before ordinary tiling/adoption. On managed background close, ordinary strip layout resumes. On minimized background, front-slot positions remain stable.
- No automatic window-policy arm, no registry edits, no broker write, no UI restart while working on source.

## Architecture / machine state

The workspace owns an optional `PinnedOverlay` containing `background` HWND, `external_background` flag, physical slots, active occupant per slot, selected/previous slot. It is independent from `Strip.col_of`, `tabbed`, `auto_stack` and `strip.offset`. A managed background participates in workspace membership/layout; a native independent background is **not** managed/repositioned by Astur. A native maximized candidate is selected only when no other managed tile occupies that workspace, it is already marked independent, visible/maximized, not a tool window and on the exact monitor. This conservative gate deliberately avoids app popups and unrelated MT5 windows.

Critical paths: `Cmd::Add` detects and commits admission once; `workspace_layout` calculates background + front-slot rectangles; `PlaceMap` parks only inactive overlay members; `retile_monitor_opts` places front windows and adjusts non-topmost z-order without activation or touching native BG; `strip_reveal` activates a previously parked member; `Cmd::Focused/ActivateWindow` follow actual taskbar/window foreground; `detach_window` repairs membership and foreground focus; `DragMoved` and cross-monitor exchange use slot IDs and protect native fullscreen. `process_strip` handles focus/move in the overlay and explicitly unpins for incompatible layout-edit actions. Tab bars are suppressed in overlay mode.

## Verification gates and DAG

P0: baseline/worktree ownership, source audit, user-video frame evidence (the video has no WinEvent trace).
P1: pure slot-state tests: CS1 full, 2/right, 3/left, 4 other; hidden member taskbar activation; close/restore; 1/4 and 1/5 width; direct background/slot exchange; external native BG excluded from managed geometry.
P2: source integration: Add/Focus/Minimize/Close/Drag/Cross-monitor/Reload/Tab-bar.
P3: Windows CI fresh rustfmt, Clippy with `-D warnings`, full Rust tests, x64 release build plus translation/upgrade/Zalo regression. Must PASS after the FINAL code change; never weaken/remove tests.
P4: independent code review, repair in-scope defects, then fresh CI again.
P5: portable preview, user-active desktop acceptance with disposable non-MT5 apps on one/two screens (including negative coordinates). Check standard/custom caption, Alt+drag, Telegram one-click taskbar recovery, native maximize/restoration, overlay occupancy and Zalo popup click-through. **No claim of live PASS without new runtime event/visual evidence.**
P6: Only after P5 acceptance publish new installer with in-place backup/rollback smoke and checksum, retain release 2.4.0.17.

## Risk / recovery

This changes focus, z-order and layout on a live desktop. Never silently install, never run two WMs, never take over active MT5 or sensitive windows for E2E. On failure leave the existing 2.4.0.17 release untouched, retain branch/CI evidence and correct the current lifecycle. When native independent candidate is uncertain, do not pin it. Do not upload private desktop recording to GitHub. Checkpoint exact SHA, PR, build, Git clean state and remaining desktop acceptance after each commit.
