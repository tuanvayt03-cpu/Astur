# Research: Zalo / notification popup moves to monitor top and steals clicks

Date: 2026-11-02. Branch: `fix/zalo-notification-maximize-input`.
Evidence: user screenshot shows a compact notification at screen top; user confirmed mouse still blocked after `2.4.0.11`. **Originating executable and exact HWND not yet proven**. Connected CodeLocal RDP session `rdp-tcp#27` had no live Astur/Zalo processes at inspection time. Do NOT claim fixed or publish another installer without live evidence.

## Sources (primary and comparable implementations)

1. Microsoft: Layered window hit-testing / zero alpha / `WS_EX_TRANSPARENT`, and distinction between visual alpha and input. https://learn.microsoft.com/en-us/windows/win32/winmsg/window-features
2. Microsoft: recommended `WS_EX_LAYERED | WS_EX_TRANSPARENT` together for top-level input passthrough. https://learn.microsoft.com/en-us/windows/win32/dwm/bestpractices-ovw
3. Microsoft: `LowLevelMouseProc` returning nonzero discards input / does not call the next hook. https://learn.microsoft.com/en-us/windows/win32/winmsg/lowlevelmouseproc
4. Microsoft: `GetCapture` only observes current thread; `GetGUIThreadInfo` for another GUI thread, and `hwndCapture`. https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getcapture and https://learn.microsoft.com/windows/win32/api/winuser/ns-winuser-guithreadinfo
5. Microsoft: `GetWindowRect` can include invisible/DPI-scaled borders; compare `DWMWA_EXTENDED_FRAME_BOUNDS` and actual `WindowFromPoint`. https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getwindowrect
6. Microsoft: `SetWindowPos` controls geometry AND z-order; can propagate topmost to owned windows. https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwindowpos
7. Microsoft: `SetWinEventHook` OUTOFCONTEXT queues lifecycle events asynchronously, which can produce race windows. https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setwineventhook
8. komorebi: composite application-specific `ignore` vs `floating` rules; popups that only need to exist briefly should be ignored, not managed. https://github.com/LGUG2Z/komorebi-application-specific-configuration
9. GlazeWM: declarative window rules with process/class/title match and `ignore`; beware blanket `WS_POPUP` classification: release notes reverted WS_POPUP-floating because Telegram and Steam main windows regressed. https://github.com/glzr-io/glazewm and https://github.com/glzr-io/glazewm/releases
10. Microsoft: `HTTRANSPARENT` is scoped to windows in the same thread; **not** a universal cross-process mouse passthrough recipe. https://learn.microsoft.com/en-us/windows/win32/inputdev/wm-nchittest

## Concrete Astur code evidence

- `crates/astur/src/main.rs`: `is_notification_overlay` (combined generic shape heuristic and Zalo executable fallback) is only used to **refuse adoption/foreground**, not change popup input behavior. Its position-dependent classification may fail for a notification whose HWND size/position differs from the visible pixels, host process isn't `Zalo.exe`, or layout events arrive before geometry settles.
- `mouse_proc` installs `WH_MOUSE_LL` and returns `LRESULT(1)` to suppress events under several conditions: launcher/system-menu outside click, wheel over bar, Alt-wheel scrolling, Alt-drag down/up. If a UI-open/drag state gets stale, the geometry may be perfectly clear yet clicks are swallowed.
- `overlay_ex_style` changes only **Astur's** slide/glide overlays to layered/transparent. It cannot make a foreign popup's transparent input shield disappear.
- Earlier `2.4.0.11` synthetic tests and CI pass cannot prove popup placement/input in user's target desktop.

## Root cause matrix (differentiate, do not assume)

A. **Unmanaged foreign topmost HWND or invisible input shield**: `WindowFromPoint` at blocked point resolves to owner process (Zalo, browser, shell or another notification host) and its `GetWindowRect` overlaps the blocked region. `DWMWA_EXTENDED_FRAME_BOUNDS` may be much smaller than true input rect. Full ignore in Astur does not solve external hit-test. Fix should first seek originating app/OS setting, and only consider verified, narrowly scoped shape/input treatment; never edit Zalo's primary HWND wholesale.

B. **Mouse capture**: `WindowFromPoint` may indicate the expected underneath app, but `GetGUIThreadInfo` of suspected app reports a live `hwndCapture`. Capture delivers mouse input outside window boundaries. Analyze owner, foreground, capture start/end. Do not steal/release another process's mouse capture globally.

C. **Astur's own low-level hook suppresses**: `WindowFromPoint` resolves to the correct underneath app, no foreign capture, but click still disappears. Instrument `mouse_proc` return paths with integer reason codes and a bounded, lock-free in-memory counter/ring (no content/text/coordinates beyond what is necessary); identify stale `LAUNCHER_OPEN`, `SYSMENU_OPEN`, `ANY_DRAG`, `main_held`, bar hit boxes. Ensure every exceptional close/destroy/minimize path clears stale states and returns `CallNextHookEx` for ordinary clicks. Never bypass legitimate Alt-drag or popup dismiss actions indiscriminately.

D. **Astur or another actor moves/topmosts popup**: Snapshot the popup HWND `GetWindowRect`, `DWMWA_EXTENDED_FRAME_BOUNDS`, z-order/exstyle and owner immediately at SHOW and at LOCATIONCHANGE/REORDER. `SetWindowPos` may affect position and owned window Z-order. Track Astur-managed HWND mutations with low-cost internal telemetry; the OS event itself does not identify which process invoked SetWindowPos. Different DPI/monitor and shell notifications need separate cases.

E. **Wrong process identity**: the screenshot alone does NOT prove the popup is produced by `Zalo.exe`; it might be a desktop/browser notification host. Process-only blacklists will fail. Capture exe/class/owner/style before selecting ignore rule.

## Optimal solution architecture (in order)

1. **Read-only A/B attribution** within the same desktop session: capture while Astur on + real toast, then one comparison with Astur exited and toast on. Record `WindowFromPoint` at user cursor/blocked region, HWND root/owner/pid/class/style/rect, DWM frame rect, foreground, topmost, GUI-thread mouse capture, GetClipCursor. The repo already has `scripts/run_zalo_click_probe.cmd` and `scripts/capture_zalo_click_blocker.py` for preliminary probes (some metadata still missing).
2. **Instrument Astur mouse hook**, NOT the foreign app: reason-coded return `LRESULT(1)` counters, only when diagnostic flag is enabled, with bounded samples; correlate with popup lifecycle. Add stale launcher/menu/drag-state recovery tests and verify ordinary click pass-through. This is critical because a hook can swallow clicks despite an empty hit-test layer.
3. **Robust popup admission state machine**: mark suspected transient HWND as PENDING without styling/focus/tiling while geometry is unstable; evaluate process/path+class+owner+style+size+monitor+DWM bounds and short-lived lifecycle. Use explicit `ignore` for confirmed transient handles from SHOW through DESTROY, not only one-shot edge-position filtering. Ensure normal chat windows are still tileable. Never forcibly reposition, topmost, hide or restyle the toast.
4. **Input ownership**: If process-verified foreign HWND blocks a region outside the visible toast and Astur exited still reproduces it, the reliable root fix is at notification framework/app layer (settings, replacement OS notifications, or upstream fix). Do NOT blindly set `WS_EX_TRANSPARENT` on all Zalo HWNDs or inject input, as this can break intended notification clicks and main chat.
5. **Release gate**: GitHub Windows fmt/clippy/tests/build/installer backup/rollback, PLUS real on/off A/B with target monitors and DPI and genuine notifications, 20+ click/scroll cases under/to the side of popup, no focus/tiling changes, NCPC maximize regression independent. Only publish a new preview if empirical cases pass.

## Decision after one trace

- Bad `WindowFromPoint` -> identify owner and input rect; resolve foreign-window shield or shell host.
- Correct `WindowFromPoint` + live `hwndCapture` -> isolate capture owner/lifecycle.
- Correct `WindowFromPoint` + no capture + Astur enabled only -> instrument and fix swallowed hook path.
- Mouse works when Astur off, popup moves to top only when Astur on -> audit Astur window mutations and z-order.
- Mouse fails even with Astur off -> report external app/OS responsibility, avoid unsafe Astur cross-process patches.

Status: **RESEARCH_COMPLETE / IMPLEMENTATION_BLOCKED_ON_REAL_HITTEST**, not application fix; do not label `2.4.0.11` resolved.
