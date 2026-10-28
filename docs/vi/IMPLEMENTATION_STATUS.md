# Astur VI — Implementation State (2026-10-28)

The original SDD in the planning branch defined the full scope. This feature branch now implements a **partial Settings-localization slice**, not the full project.

## Implemented in `feat/vi-notifications`
- `crates/astur-settings/src/i18n.rs`: display-only en/vi translator with safe English fallback, language preference read/write to `ui-language.txt` beside `astur.conf`, no modification to existing window-manager config keys.
- `crates/astur-settings/src/main.rs`: Settings navigation language dropdown and display-boundary localization for navigation, status, core setting rows, descriptions, section headings, Undo notification, and search in both EN/VI. English remains default and the selected language is restored when Settings is reopened.
- 320 manual first-party translation mappings; static inventory shows full coverage of the 19 tracked navigation/heading strings, 34 tracked section headings, 75 literal setting metadata tuples. **This does not mean every GUI string is translated**: other direct buttons, secondary panels, first-party native manager menus, dynamically formatted dialogs and installer may still be English.
- Python read-only metadata scanner and translation inventory QA scripts.
- `scripts/capture_notification_windows.py`: diagnostic-only HWND style/class/executable sampler, intentionally does not capture title/message contents. This is **not** a notification handling fix.

## Verification evidence
- `python Astur\scripts\test_i18n_inventory.py`: exit 0; 320 entries, 0 missing navigation, section, tracked metadata label and metadata description.
- `python -m py_compile ...`: exit 0 for QA/probe scripts.
- `git -C Astur diff --check`: exit 0 (line-ending advisory only).
- `where cargo`: exit 1; despite Rustup 1.29.1 installer being installed through winget, a callable Rust/Cargo toolchain was not available from the CodeLocal shell.
- No fresh Rust cargo fmt/test/clippy/build, nor successful runtime notification reproduction. No Windows GUI visual QA, so no PASS claimed on those points.

## Notification popup behavior
Original report: Zalo/Telegram/screenshot notification becomes a managed tile/tab. Relevant source `crates/astur/src/main.rs` near lines 4994–5150 already rejects unowned? It rejects owned/noactivate/tool window classes, but the exact notification HWND metadata is unknown. A class-wide ignore risks disabling legitimate Telegram/Zalo main windows; avoid speculative modifications. The separate read-only inspector is available for a future authorized reproduction, but collection was not executed successfully in this session.

## Required next work
1. Acquire a working Windows Rust toolchain with cargo, compile the new settings implementation, fix compiler/lint/runtime faults.
2. Complete first-party labels in native manager status bar, launcher, tray, power menu, installer, and all remaining dialogs and tooltips; add display/render snapshots and dynamic placeholder consistency tests.
3. Capture actual offending HWND metadata for a Zalo/Telegram/screenshot popup and a genuine app window, add failing regression, implement minimal safe exclusion and verify with live Windows UI without disturbing the user's installed Astur.
4. After all tests pass, build a separately identified fork installer and provide rollback, checksums and release artifacts.
5. Only then mark C01–C12 contract PASS and release.

This file and HANDOFF remain the source of truth until implementation catches up with SDD and CONTRACT.
