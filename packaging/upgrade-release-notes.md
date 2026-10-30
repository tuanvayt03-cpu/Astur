# Astur VI Update 2.4.0.9 — experimental in-place upgrade

**This installer updates the existing English Astur instead of installing a second copy.** It preserves the upstream installer GUID, remembers the existing installation folder and startup shortcut choice, and leaves normal window layout/configuration files in place.

## Changes
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
