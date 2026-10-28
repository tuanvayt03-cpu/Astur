# Astur VI — Session Handoff / Recovery Point

Updated: 2026-10-28, current lifecycle: **PARTIAL IMPLEMENTATION — NOT COMPLETE / NOT VERIFIED FOR RELEASE**.

## Baseline/ownership
- User GitHub fork: https://github.com/tuanvayt03-cpu/Astur; upstream Page011/Astur main at `b60500f0155c1d817936b869989718299cbd3f14`.
- Prior docs checkpoint: `9813d9269ce04b9d897958c18897a46a72189a0f` on branch `docs/vi-localization-plan` (PR #1).
- Active feature branch: `feat/vi-notifications` at `D:\Project\Astur`. Parent contains prior docs checkpoint. The local installed Astur application was NOT altered, stopped, restarted or replaced.
- One primary writer; no other repositories modified by this task.

## Implemented
1. `crates/astur-settings/src/i18n.rs`: 320 EN→VI manually translated display strings, English fallback and locale preference `ui-language.txt` next to astur.conf; unit tests for language toggling, fallback and persistence.
2. `crates/astur-settings/src/main.rs`: UI selector, locale loading, translated settings navigation and headers, row label/description, status, notes and some actions, plus bilingual search for translated rows.
3. `scripts/localization_inventory.py`, `scripts/metadata_inventory.py`, `scripts/test_i18n_inventory.py`: static inventory and QA (not Rust tests).
4. `scripts/capture_notification_windows.py`: read-only native HWND diagnostics probe. Tool execution against current desktop was blocked; NO notification root cause has been confirmed, NO notification behavior fixed.
5. `docs/vi/IMPLEMENTATION_STATUS.md` and controller prompt/checkpoint documentation.

## Fresh verification (final source state)
- `python Astur\scripts\test_i18n_inventory.py` EXIT 0: 320 translations, 0 missing tracked navigation, section, metadata labels and descriptions (75 tracked metadata tuples).
- `python -m py_compile` for four diagnostic/QA Python scripts EXIT 0.
- `git -C Astur diff --check` EXIT 0 (CRLF advisory on Windows).
- `where cargo` EXIT 1. Rustup installer from winget installed, but cargo/rustc not on accessible PATH; no Rust compilation.
- GitHub CI: no workflow registered for fork at planning checkpoint; new feature-branch status must be refreshed after push.
- UI/Windows notification E2E: UNVERIFIED.

## Remaining defects/blockers
- **Full localization remains incomplete**: only tracked Settings UI metadata and main navigation have guaranteed translations; native menus/installer and dynamic content need further work.
- **Notification regression remains UNFIXED/ROOT CAUSE UNKNOWN**: do not blindly ignore apps/classes. No user messages or secrets are recorded in diagnostic probe.
- **Build/installer unverified**: no release. Existing Astur remains the safe rollback.
- Source check likely needs rustfmt and Rust compiler adjustments after toolchain availability.

## Next actions
1. Verify branch and latest SHA, Git status/diff, configure Rust compiler and run cargo fmt/test/clippy/release build.
2. Cover first-party UI remaining strings and visual QA at 100/125/150/200% DPI.
3. With explicit safe OS reproduction, inspect HWND class/exstyle/owner/size and add precise failing popup test; fix and E2E test Telegram, Zalo, Windows toast, Snipping Tool.
4. Review/test/fix → fresh machine evidence → commit/push new checkpoint → independent installer/release (only after PASS).

Do not describe the current code as ready for installation. Fork GitHub branch is a recovery point, not a production release. Never destroy or overwrite current user configuration.
