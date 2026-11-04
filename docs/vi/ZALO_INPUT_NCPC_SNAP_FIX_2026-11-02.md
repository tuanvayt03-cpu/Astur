# Astur: Zalo notification, mouse hit-testing, and NCPC maximize

Date: 2026-11-02
Branch: `fix/zalo-notification-maximize-input`
Base: `feat/vi-full-update-popup-v2` at `f9a3b87`.

## Baseline and evidence

- D:\Project\Astur is clean at `f9a3b87` before branch creation, equal to origin feature branch. It is ahead of GitHub **main**, but not origin's feature branch.
- Prior `app_window_reject` filtered generic compact overlay shapes, yet Zalo still caused a layout jump on a user's machine. No real Zalo popup HWND metadata is currently available; do not claim this is proven fixed in production.
- Native `EVENT_SYSTEM_MOVESIZEEND` queued `DragResized`, which re-tiled a managed app. `independent_fullscreen_popups` defaults to false, so the existing `IsZoomed` detachment was bypassed in ordinary configurations.
- Overlay styles for animations longer than 250 ms deliberately accepted input; an Astur slide/glide could cover screen controls for the duration.

## Implemented code changes

1. Zalo-specific fallback only after executable identity **and** compact/top-bottom edge shape are both verified. Zalo's ordinary main chat window remains tileable; popup is excluded from adoption, workspace membership, tab and focus bookkeeping. Never move, hide or mutate Zalo's HWND.
2. Astur animation overlays are always layered and transparent to input, including long animations. Input follows actual Windows geometry even when animated pixels lag it.
3. Any native Win32 maximized surface is treated as independent regardless of `independent_fullscreen_popups`. Native drag end reconciles before `DragResized`, and the placement loop refuses a newly maximized HWND even when an old retile was queued. A normal-size restore re-enters tiling.
4. Extended bounded read-only diagnostic `scripts/capture_zalo_popup_episodes.py` with six `WindowFromPoint` hit-tests across the bottom of the active screen, plus 1.2-second comparison. Records HWND/process/class/geometry only. No titles, message content, screenshots, click injection, foreground changes or window manipulation.

## Automated evidence and limitations

- Python native-probe self-test: PASS (10 assertions).
- `git diff --check`: PASS (Windows LF/CRLF conversion warning, not a whitespace error).
- Windows Rust fmt/clippy/test/build: MUST RUN in GitHub CI; `cargo` and `rustc` are not on the accessible machine's PATH.
- No installed Astur binary replaced. No live Zalo/NCPC HWND reproduction recorded yet.
- Astur cannot guarantee another process's **own** invisible/click-capturing HWND is nonblocking by merely refusing to tile it. Read-only hit-test data is required to distinguish and address that separate cause safely.

## Manual acceptance matrix (must pass before release/installation)

- Zalo message toast on each display: no tile contraction, no reflow, no top-of-screen relocation, no workspace/tab/focus change; toast renders and dismisses normally.
- With Zalo toast visible, click/drag/scroll controls in lower screen regions repeatedly. `WindowFromPoint` should identify the expected underlying app (not `astur_slide`). If Zalo itself owns the top hit HWND far outside the toast, classify as an app-owned input shield and capture its class/styles before any additional change.
- NCPC Remote Desktop Control: from a half-screen Astur tile, drag the caption to screen top to invoke Windows Snap maximize. Confirm `IsZoomed`, no tile revert at 0.2s/1s/5s, and mouse/keyboard usable. Native restore-down should rejoin tiling without orphaning.
- Repeat NCPC with secondary monitor, mixed DPI, workspaces, minimize/restore, Alt-drag and Windows Maximize button. Check that deliberate F11/independent media and normal tiling are unaffected.
- Test long animations (251–2000 ms): overlays remain click-through, including popup-driven layout activity. Review that click targets follow real window geometry, not delayed animation imagery.
- Only after all checks and a successful CI build: produce a new reversible prerelease installer using the existing AppId/backups. Never auto-install over the active Astur instance without explicit instruction.
