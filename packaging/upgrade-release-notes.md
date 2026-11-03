# Astur VI Update 2.4.0.12 — experimental in-place upgrade

**Build source:** `release/astur-vi-update-2.4.0.12`, based on `950dbd7`, includes the Zalo HWND classifier and native title-bar monitor transfer.

## 2.4.0.12 changes
- Native title-bar drag of an Astur-managed tiled window across physical monitors now rehomes it to the target monitor's active workspace on release, without requiring Left Alt. Existing Alt+drag, keyboard monitor move, tiling order, native maximize and floating behavior remain available.
- The Zalo-specific ignore rule now includes TOPMOST borderless windows without APPWINDOW/caption/frame, including the observed 960×1040 transient Zalo HWND on NCPC; normal Zalo chat remains tileable. Only Astur management is bypassed: no Zalo window visibility, z-order or input flags are changed.
- Diagnostic mouse hook guard and Win32 HWND sampling from intervening fixes remain included.
- In addition to the original first-upgrade backup, this installer saves the **immediately pre-2.4.0.12** binaries and `astur.conf`/`navbar.conf` under `%LOCALAPPDATA%\Astur\UpgradeBackup\before-vi-update-2.4.0.12`. Neither backup is overwritten by a reinstall.
- Windows CI enforces formatting, static analysis, unit tests, bilingual Settings renders, and an isolated original-AppId-to-updater installation/backup/uninstall smoke test.

**PREVIEW / acceptance limitation:** NCPC multi-monitor title-bar movement and real Zalo input-blocking have not yet been verified after this build on the affected desktop. Do not classify this as a proven live fix. The oversized Zalo popup itself may intercept mouse events even when Astur ignores it. Quit Astur before comparing the app's native behavior. This is not an official upstream Astur release.

---

## Previous 2.4.0.11 changes

**Historical note for 2.4.0.11:** Built from `fix/zalo-notification-maximize-input`, with the earlier popup and maximize fixes. That version did not resolve the live NCPC Zalo issue.

## 2.4.0.11 changes
- Zalo-specific, process-verified compact edge-popup fallback in Astur's window admission path. The goal is to let Zalo show its own notifications without Astur converting them into tiles or taking focus; normal chat windows stay manageable.
- Astur slide/glide animation overlays pass mouse input through at every animation duration, including >250 ms. This removes Astur's intentional full-monitor click shield during long animations.
- Honor Windows native maximization regardless of the optional `independent_fullscreen_popups` toggle (OFF by default). Native end-of-drag now reconciles maximize before a pending tile resize; queued placement also refuses already-maximized windows. Restored windows can return to tiling.
- Extend the privacy-safe Zalo diagnostics with read-only `WindowFromPoint` tests for lower-screen input targets; no message text, screenshots, injected clicks or window-position modification.
- Rust Windows CI: format, Clippy, tests and release build gate this updater; installer tests validate backup, custom install path, configuration preservation and uninstall on an isolated runner.


**This installer updates the existing English Astur instead of installing a second copy.** It preserves the upstream installer GUID, remembers the existing installation folder and startup shortcut choice, and leaves normal window layout/configuration files in place.

## Changes
- **Ignore compact desktop notification banners immediately**: top/bottom-edge messaging toasts with short geometry and no actual resize/minimize/maximize controls are never adopted as Astur tiles or tabs, even when their host sets cosmetic APPWINDOW/caption/window-menu flags. SHOW/FOREGROUND/UNCLOAKED events are ignored before they enter the layout/focus queue. Normal Zalo/Telegram/Chrome windows remain managed; notification presentation and dismissal remain owned by the originating app. Regression tests cover the exact 350x80 top-edge screenshot shape, style variants, normal main-window counterexamples and event boundary.
- Fix lifecycle race: minimize and temporary hide of an independent fullscreen window no longer erase its tracking marker before a normal-size restore can be re-adopted by Astur. The marker is removed after successful normal window adoption or destruction.
- Fix scrolling focus: when a managed tile becomes an independent fullscreen window, Astur no longer forces focus to the next tile. The fullscreen surface keeps its Windows Z-order until the user explicitly selects another window.
- Added synthetic regression tests for minimize/restore re-adoption, delayed visibility and focus behavior.
- Regression guard: even if native maximize/F11 occurs before the queued WinEvent reconciliation, the layout engine will not send a tile resize/restore to the native fullscreen surface.
- Optional **Keep fullscreen and media popups independent** setting under Windows & rules (OFF by default). Native maximize/Windows square button, F11 borderless fullscreen and unowned borderless media viewer surfaces are excluded from Astur's tile/tab registry. Restored normal-size main windows may return to normal tiling. Other tiled windows retain ordinary per-window focus/Z-order; no global Always on Top.
- Compact EN/VI language switcher moved from left navigation to the header; dropdown offers only the other language. Vietnamese catalog expands to 821 mapped strings.
- Expanded English/Vietnamese translation catalog to 821 mapped first-party strings across 14 Settings pages, native launcher/power menus, status-bar labels, key help, validation/search hints and dynamic messages. Vietnamese is the default when no language preference exists; original English remains available in Settings. Source-level coverage does not guarantee pixel-level 100% translation.
- Additional translations for Settings choices, help, preset descriptions, advanced rule controls, and the manager's first-party tray and power menu items.
- Extended notification-overlay classification for **very shallow banners flush with the top/bottom screen edge**, even when the app omits `WS_POPUP`, `TOPMOST` and `LAYERED`. Compact framed banners are excluded only with a second overlay signal (`TOPMOST`/`LAYERED`); resizable app windows and ordinary dialogs remain manageable. This skips **tiling and tab adoption only**; it does not block, mute, close, move or suppress notifications. Synthetic tests cover the observed banner dimensions and nearby counterexamples.
- Original executable, settings executable, `astur.conf` and `navbar.conf` are backed up on first upgrade under `%LOCALAPPDATA%\Astur\UpgradeBackup\before-vi-update-2.4.0.1`.

## Before running
Exit the separately installed **Astur VI Preview** if open. Do not run two Astur processes simultaneously. The installer may ask to close the existing English Astur to replace its files. It offers an optional launch on completion.

## Rollback
The pre-update executables and configuration are copied to the backup location above. If you want a normal upstream installation again, exit Astur and run the original Astur installer. Do not remove the backup until the new build is verified.

## Verification and limitations
Windows CI validates Rust fmt/clippy/tests/release build, translation contract, same-AppID upgrade contract, an isolated Windows runner install of the original installer followed by this updater, preservation of a custom install path and user settings, original-binary backup checks, and an uninstall smoke.

**This is a pre-release and not a fully verified stable update.** Real Zalo/Telegram/Snipping Tool notification HWND behavior is not yet proven in a live desktop session, and some dynamic strings/native surfaces may remain English. App/window titles and user data are intentionally not translated. The unsigned installer can raise a Windows SmartScreen warning; do not disable security protections.

Source: https://github.com/tuanvayt03-cpu/Astur
