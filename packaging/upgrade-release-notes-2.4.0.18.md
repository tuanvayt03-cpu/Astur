# Astur VI Update 2.4.0.18 (Preview) | Fullscreen background and deterministic foreground slots

**Windows x64 experimental in-place update.** Not an upstream stable release. Built from the pinned overlay and native drag fixes on [draft PR #13](https://github.com/tuanvayt03-cpu/Astur/pull/13), including the previously published 2.4.0.17 changes.

## What's new
- **Pinned CS1 fullscreen background:** keep CS1 at full width behind independent foreground overlays instead of treating it as a scrolling column that consumes all slots.
- **Deterministic slots:** CS2 opens into the empty right half, CS3 the left, CS4 replaces the other nonfocused (N-1) slot; previous occupants remain recoverable without creating an unsolicited manual tab bar.
- **Window lifecycle:** preserve overlay state for taskbar/Alt+Tab recovery, minimize, close/restore, and hidden-workspace admissions.
- **Dragging:** improved native/custom title-bar drag detection, Alt+drag fallback and direct same-/cross-monitor slot exchanges, including negative monitor coordinates.
- **Windows-native maximized CS1:** treated as a separate background that Astur does not resize/park.
- Retains previous 2.4.0.17 Telegram taskbar recovery, Zalo popup protections and prior scrolling/layout behavior.

## Installation and rollback
- This **updates Astur in place**, using the same installer AppId and existing install directory. It does **not** silently install or launch from GitHub.
- Exit Astur before updating, and **do not run two window managers at the same time**. Back up important desktop work first.
- Previous installed executables and `astur.conf`/`navbar.conf` (when present) are saved in `%LOCALAPPDATA%\Astur\UpgradeBackup\before-vi-update-2.4.0.18`. The original first-upgrade backup is retained.
- [Previous preview 2.4.0.17](https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-update-2.4.0.17) stays available for rollback.
- The unsigned installer may prompt Windows security warnings. Verify checksum/source; **do not bypass system security protections** to run an untrusted installer.

## Verification boundary
Windows CI must pass Rustfmt, `cargo clippy -- -D warnings`, all Rust tests, VI/EN Settings renders, x64 build, isolated same-AppId upgrade/backup/uninstall smoke and published SHA256. **No real desktop E2E acceptance has been claimed.** Real CS1–CS4 focus/drag/taskbar, multi-monitor and Zalo input still require isolated acceptance with disposable apps, not active MT5/SignalOps windows.

[Acceptance checklist](https://github.com/tuanvayt03-cpu/Astur/blob/feat/astur-pinned-overlay-20261106/docs/vi/PINNED_OVERLAY_QA_ACCEPTANCE_20261106.md).
