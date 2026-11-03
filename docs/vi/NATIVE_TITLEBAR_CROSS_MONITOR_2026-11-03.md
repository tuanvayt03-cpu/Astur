# Astur: native title-bar transfer between monitors

Date: 2026-11-03
Branch: `feat/native-titlebar-cross-monitor`, branched from `fix/zalo-notification-maximize-input` (e497379).
Scope: Rust WinEvent native drag release, test and README. No config migration or running Astur installation changed.

## Original behavior and user report

The upstream Astur documentation and current fork both support Left Alt + left-drag from any point and MOD+Shift+arrows to move a tiled window to another display. `main_key=lalt` (default) exclusively accepts Left Alt. Settings > Shortcuts > Astur key can change to `alt` (either Left/Right Alt), `win` or other supported modifiers.

A native titlebar drag without Alt emitted `EVENT_SYSTEM_MOVESIZEEND` and only queued `Cmd::DragResized(h, None)`. That reconciled native fullscreen and re-tiled the *original* monitor; it did not re-home tiling ownership even if the user dragged the window across physical displays. An Alt-drag followed the separate `Cmd::DragMoved` path which already handled moving tiled and floating windows, scrolling columns, drop zones and monitor focus.

## Implementation

- On native `EVENT_SYSTEM_MOVESIZESTART`, capture the window origin monitor and whether the mouse started in a conservative non-client caption strip (within horizontal 16px insets, vertical 8..96px, regular WS_CAPTION). No low-level hook or injected mouse messages.
- On `EVENT_SYSTEM_MOVESIZEEND`, if the source is still the tracked native drag, the drop pointer is on another physical monitor, the original grab was on the title bar, and Windows hasn't maximized the app, enqueue the **existing** `Cmd::DragMoved` with the final Win32 rect and release cursor. This transfers tiling ownership and re-tiles both monitors using the already-proven drop logic.
- Otherwise, preserve existing `Cmd::DragResized` behavior for same-monitor titlebar movement, border resizing, Windows Snap maximize/restore-down and unrelated Win32 popups. On HIDE/DESTROY/MINIMIZESTART reset the native drag baseline.
- No separate "disable Alt" feature is needed; Alt remains available as an alternate move-anywhere action.
- No new setting yet. This behavior ships in the experimental branch only, not stable.

## Verification and acceptance

- Unit test exercises caption vs top/left resize vs app content and borderless popup. Monitor decision covers left/right, missing origin, same-screen, non-caption and maximized cases.
- Require fresh Windows Rust format/clippy/test/release build and portable artifact from this SHA.
- On real NCPC use titlebar to move a managed tile across display 1->2 and back, release near corners/middle and check gap closure on source and correct tiling/focus on destination. Repeat with normal resize on both edges, floating tiles, minimized/restore, different DPI/scale and Snap maximize on both monitors. Alt+left-drag and MOD+Shift+arrows must remain working.
- Existing Zalo popup no-blink / click-through E2E remains a separate release gate. Do not claim it passed from CI.
