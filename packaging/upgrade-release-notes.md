# Astur VI Update 2.4.0.17 (Preview) — Direct cross-monitor slots + taskbar recovery

**Source baseline:** `ff315dd497efd9a26d657713c4b81467ce6e2e06`, branch `fix/astur-cross-monitor-telegram-20261105`, draft PR #11. Release branch/tag must resolve to one exact commit. Prior release 2.4.0.16 and its assets must remain unchanged.

## New in 2.4.0.17

- **Cross-monitor, slot-to-slot direct drag:** In a two-display four-slot layout, drop 4→2, 1→3, 1→4, or 3→2 using the mouse location on the target screen. Occupied scrolling slots exchange both HWND owners together, maintaining both monitor offsets and column metadata, without transiently recentering the destination on slot 1. Existing insertion rules remain for vacant/edge destinations.
- **Telegram taskbar activation:** A repeated foreground event for a managed HWND still physically parked, Astur-hidden, or minimized is now handled as recovery rather than blindly filtered out. A guarded SHOW on an already tracked, parked foreground HWND also invokes recovery; synthetic foreground echo can retile without recentering.
- **No new auto-tab UI:** This builds on the automatic slot stack / manual tab separation delivered in 2.4.0.16. User-requested tab mode and single Explorer tab bar visibility remain independent.
- **Additional source tests:** two monitors with four windows and nonadjacent swaps, tabbed column metadata, no window loss/duplication, duplicate foreground recovery.
- **Private evidence:** a 53.63-second screen recording was analyzed within the user conversation but not uploaded to GitHub.

## Gates and rollout

- Source CI on exact `ff315dd` commit: https://github.com/tuanvayt03-cpu/Astur/actions/runs/42020494791 (PASS: rustfmt, Clippy, all Rust unit tests, release build, portable preview).
- Dedicated 2.4.0.17 Windows update workflow must PASS bilingual Settings render, original-AppId update/backup/uninstall smoke, installer build, checksum and prerelease publication on the release commit before the update can be distributed.
- **Live desktop acceptance still PENDING:** source and isolated Windows CI cannot establish one-click Telegram recovery or smooth cross-monitor dragging on the user's physical displays. This is a prerelease, not stable. Quit running Astur before installing, do not run two managers together, never bypass OS warnings, and avoid testing with active MT5 trading windows.
- Version 2.4.0.16 remains available for rollback. Preserve first-original backup and the immediately previous installation snapshot.

Implementation, reproduction and acceptance: `docs/vi/TELEGRAM_TASKBAR_CROSS_MONITOR_SLOT_20261105.md`. Draft PR: https://github.com/tuanvayt03-cpu/Astur/pull/11

---

## Previous release: 2.4.0.16

# Astur VI Update 2.4.0.16 (Preview) — Auto Slot Stack without unwanted tabs

Source baseline: `d857e72fb7a547e6d4559a4e86e45d3220076da7` on `fix/astur-auto-slot-separate-20261105`, building on Astur VI 2.4.0.15. Final release tag must point to the exact committed release branch head.

## Fixes in 2.4.0.16

- **No unsolicited black tab strip:** Opening CS3 when the visible slots are full now uses a separate automatic slot-stack state. Only `Alt+Shift+T` explicitly switches Manual Tab Mode on/off. A single File Explorer or Chrome window does not get an Astur tab bar.
- **CS3 respects the active anchor:** An auto-admitted window uses a free viewport slot first, or the previous N-1/non-anchor slot when the view is full. It no longer scrolls the strip prematurely before the slot membership is committed.
- **One activation should recover the prior occupant:** Taskbar/Alt+Tab activation detects the previously parked member or an actual HWND parked outside all monitors. Astur performs a real retile/unpark instead of trusting the future layout's `Vis::Full` state. Astur-owned stale SW_HIDE on an active workspace can be repaired without undoing app-owned hide/scratchpad semantics.
- **Minimized window recovery:** App-bar actions and manually clicked tabs restore an iconic HWND before placing it into its reserved slot; hidden-workspace activations retain switch-before-restore order. TabClick uses the same minimized-placeholder list as the tab bar.
- **Explicit Tab OFF is real OFF:** Manual toggles clear automatic state. When a stack shrinks to one member, stale auto state is cleared and no tab bar/title space is rendered.
- Existing 2.4.0.15 scrolling slot geometry, flexible drag/swaps, Zalo notification exclusions, native top-edge maximize and previous backup contract remain.

## Verification and rollout boundary

- Source CI includes rustfmt, Clippy with warnings denied, regression/unit tests (implicit stack, visible tab bar, focused previously parked occupant, manual ON/OFF and singleton) and Windows release build.
- Dedicated installer CI must pass bilingual Settings rendering, original-AppId in-place update, backup/uninstall smoke, SHA256SUMS generation and GitHub prerelease publication before publication is claimed.
- **Live one/two-display desktop QA is still PENDING**. Do not claim production/full UI PASS or silently install over a running Astur instance with MT5.
- The installer is UNSIGNED and preview-only. Quit Astur before a user-initiated upgrade. Never bypass Defender/SmartScreen security warnings to run an untrusted file. Version 2.4.0.15 remains available for rollback.

Detailed development order and acceptance: `docs/vi/AUTO_SLOT_TAB_VISIBILITY_REPAIR_20261105.md`. Draft implementation PR #10: https://github.com/tuanvayt03-cpu/Astur/pull/10

---

## Previous release 2.4.0.15

# Astur VI Update 2.4.0.15 (Preview) — Stable scrolling slots

**Source:** `release/astur-vi-update-2.4.0.15`, based on verified fix commit `1be70f95f376ece2ad6bb2f8f893cb6591c3d5fc` and the earlier 2.4.0.14 release. The release tag must match the final release branch commit exactly.

## Fixes in 2.4.0.15

- **Keep CS2 in its own slot when CS1 is minimized:** minimized windows remain geometric placeholders in scrolling mode. Win32 placement skips their minimized surfaces, but no longer collapses later columns to the left. Focus is reassigned to a live tab/column without forced viewport recentering.
- **CS3 opens in a non-anchor slot:** preserve the original focused slot's strip-space location during admission; finalize the new tab before reconciling viewport offset. A short one-use guard prevents delayed automatic foreground events from moving the anchor again.
- **Freely drag across CS1/CS2/CS3/CS4:** target selection uses Astur's stable layout rectangles rather than live Win32 animation rectangles. Center-drop swaps independently positioned or tabbed-window occupants, preserves column identity, per-slot width, tab memberships and last-active window; edge-drop still inserts before/after/below.
- **Prevent focus jumps from tiny clipped edges:** a column still at least 75% visible is not automatically recentered simply because a few pixels are clipped by the viewport. Explicit scroll/focus hotkeys continue to work.
- Retains 2.4.0.14 top-edge maximize, native title-bar drag, 1/2 and 1/5 width settings, Window Policy Engine, background spawn and Zalo exclusions.

## Verification and risk

- Fresh source Windows CI: https://github.com/tuanvayt03-cpu/Astur/actions/runs/41996637086 — PASS rustfmt, bilingual inventory, Clippy (-D warnings), all unit and new regression tests, x64 release build.
- The dedicated update workflow must PASS the Windows installer compilation, upstream AppId in-place upgrade, preserved first and immediate pre-2.4.0.15 backups, uninstall smoke, checksum and GitHub prerelease publication.
- **Real desktop UI acceptance is still pending:** unit tests and an isolated Windows runner do not establish that Chrome/MT5/Zalo, fullscreen, mouse drag, minimize and restore work in the user's active one/two-display environment. This is an unsigned experimental prerelease, not stable. Exit Astur before installing. Do not bypass Windows security warnings.
- Previous GitHub releases and their assets are not overwritten; 2.4.0.14 remains a rollback option.

Source issue & model/test contract: `docs/vi/STABLE_SLOT_ROOT_CAUSE_FIX_20261105.md`. Review: https://github.com/tuanvayt03-cpu/Astur/pull/9

---

## Previous release: 2.4.0.14

# Astur VI Update 2.4.0.14 (Preview) — In-place Windows update

**Source branch:** `release/astur-vi-update-2.4.0.14`, built from `feat/slot-anchor-placement-20261105` at `af4fd2d` (Window Policy Engine PR #7 + slot-anchor PR #8). The release tag is immutable and must match the precise build SHA.

## New in 2.4.0.14

- **Focus-anchored scrolling admission:** a newly opened window fills a free viewport slot first. When the viewport is occupied, it uses a tab in the previously focused **other** visible slot (N-1); the currently focused slot stays anchored. Existing windows remain managed and can be selected again, not forcibly minimized or closed.
- **Freely drag windows across slots:** Alt+left-drag or native title-bar drag works within a monitor, not just across monitors. Dropping at the center of an independent column swaps positions, including non-adjacent columns; left/right/below drop zones retain their established behavior.
- **Drag to top edge to maximize:** a real drag ending at the physical top edge of the destination display invokes Windows maximize for eligible windows, even on displays with negative virtual-screen coordinates. A stationary click, resize or unsupported window does not trigger it. Windows-native F11/maximized windows remain separate from tiling.
- Retains **Window Policy Engine v1**, background-spawn protections, Zalo notification exclusions, click-through overlays, VI/EN Settings, and the existing single-monitor/multi-monitor functionality.
- **In-place update with rollback:** same AppId and original installation directory. Preserve the first-upgrade snapshot and create a new before-2.4.0.14 backup of existing binaries and available user configuration. Neither backup is overwritten on a repeat installation.

## Verification and limitations

- Windows CI must pass Rustfmt, Clippy with warnings denied, full unit tests, bilingual Settings offscreen renders, x64 release build, Inno Setup, original-AppId upgrade/rollback/uninstall smoke, and SHA256 generation **before** GitHub prerelease publication.
- **Desktop live acceptance still pending.** Synthetic unit tests and isolated runner tests are not proof that one/two-monitor dragging, 1/2 or 1/5 slot placement, native maximize/F11 and actual Zalo/MT5 behavior work without regression on the user's own desktop.
- This is an **unsigned experimental prerelease**, not an official upstream stable release. Close the running Astur before upgrading. Do not disable Windows Defender/SmartScreen to run the installer.
- Source: https://github.com/tuanvayt03-cpu/Astur
- Follow-up source reviews: PR #7 and PR #8.

---

## Previous 2.4.0.13 release notes

# Astur VI Update 2.4.0.13 — experimental in-place upgrade

**Build source:** `release/astur-vi-update-2.4.0.13`, based on `d55ca1a`.

## 2.4.0.13 changes
- Adds **Background Spawn Protection**, enabled by default. Newly shown background windows are left outside Astur's tiling registry until Windows actually foregrounds them, preventing short-lived agent/CLI PowerShell/CMD scan windows from taking a tile and reflowing the active desktop.
- Keeps Windows' normal foreground-stealing protection enabled while Background Spawn Protection is active, including live config reloads. Existing configs that still contain `foreground_lock_disable=true` cannot silently disable the Windows guard while protection is enabled.
- Adds a Windows & rules Settings toggle with English/Vietnamese UI. User-selected terminals still enter Astur normally through the existing foreground path; there is no permanent PowerShell/CMD blacklist and no forced minimize/restyle of foreign HWNDs.
- Retains all 2.4.0.12 changes: native title-bar cross-monitor drag, Zalo topmost-borderless host bypass, native maximize fixes, click-through Astur overlays, dual rollback backups and bilingual Settings.
- The installer preserves the original first-upgrade backup and also captures the immediately pre-2.4.0.13 installation under `%LOCALAPPDATA%\Astur\UpgradeBackup\before-vi-update-2.4.0.13`.

**PREVIEW / acceptance limitation:** CI verifies the code and isolated upgrade/rollback path, but the new background-spawn behavior still requires live desktop confirmation on the affected one/two-monitor machines. A third-party process that is legitimately granted foreground or creates its own TOPMOST UI may still present itself; Astur does not blindly minimize or restyle foreign windows.

---

## Previous 2.4.0.12 changes

**Historical note for 2.4.0.12:** Built from `release/astur-vi-update-2.4.0.12`, based on `950dbd7`, including the Zalo HWND classifier and native title-bar monitor transfer.

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
