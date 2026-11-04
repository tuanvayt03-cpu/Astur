# Astur: NCPC real notification HWND evidence and narrow policy correction

Date: 2026-11-03
Branch: `fix/zalo-notification-maximize-input`
Source: two user-supplied read-only Windows probe files, 166 JSONL samples each, approximately 45 s each. Do not commit raw logs.

## What was actually observed

### astur_input_20261103_114156.jsonl
- Normal Zalo chat HWND 329116, PID 19680, `Chrome_WidgetWin_1`, style `0x14c70000`, exstyle `0x00000100` (APPWINDOW), non-topmost, rect `0,0,960,1040`, visible throughout. Preserve its normal tiling.
- SECOND Zalo HWND **2033224**, same PID/class but **style `0x14030000`, exstyle `0x00000008` (TOPMOST)**, no APPWINDOW/caption/thickframe/system-menu, rect `1920,75,2880,1115` (960 x 1040, half a monitor/work area). Seen from approx 13.51 s to 23.28 s, foreground from ~14.61 s; becomes invisible by ~23.54 s.
- `GetGUIThreadInfo` reported `hwndCapture=2033224` in five discrete samples between 14.61 s and 19.77 s. This is transient capture, not evidence of capture held permanently.
- `clip_rect` remains desktop-wide `0,0,3840,1155`; no system cursor clip observed.

### astur_input_20261103_113816.jsonl
- At ~11.20 s Zalo chat HWND 329116 changed from `480,1355,1440,2395` (outside visible screens) to `0,0,960,1040`; Telegram main HWND 66496 changed from `0,0,960,1040` to `-32000,-32000,-31840,-31972` (canonical minimized placement). These are real visibility/placement changes, consistent with observed monitor flash.
- The logs record resulting geometry and focus, NOT which process issued the underlying ShowWindow/SetWindowPos; do not assert Astur alone caused those calls.
- Other observed mouse capture samples on Explorer.exe thread may correspond to normal user interactions, not a confirmed cause of the Zalo blocking symptom.

## Root cause hypothesis and code-level correction

`transient_overlay_shape` and existing `zalo_notification_shape` reject a full-height, half-monitor HWND based on size, even if TOPMOST and unframed. `WinEvent` can then queue Add/Focused, allowing Astur to adopt the temporary window or react to its focus.

Add `zalo_topmost_borderless_surface` under **exact Zalo executable identity only**. Require `WS_EX_TOPMOST`, no `WS_EX_APPWINDOW`, and no WS_CHILD/CAPTION/THICKFRAME/SYSMENU. Unlike a toast geometry filter, this matches the 960x1040 trace and leaves Zalo's normal chat window manageable. The classifier does not call SetWindowPos, ShowWindow, ReleaseCapture or change foreign styles/input; it only refuses Astur's adoption/focus tracking.

## Verification and remaining limitations

- Pure Rust unit test covers the exact two logged style tuples, location, out-of-bounds transient size, hidden variation, and normal chat exclusion.
- Require fresh Windows CI fmt, Clippy, tests and release build after the final changes. No local Cargo on CodeLocal host PATH.
- A release is NOT approved until the user's actual NCPC desktop replays several Zalo notifications with no layout/visible flicker or blocked mouse input and remote desktop maximize still works.
- The Zalo HWND itself briefly called mouse capture in the original logs; ignoring it in Astur cannot ensure a Zalo-owned capture/input shield is fixed. If the click lock remains when Astur is not controlling the HWND, compare with Astur exited and investigate the originating app.
- Existing installed Astur must not be overwritten automatically. Explicitly scoped reversible preview only after live acceptance.
