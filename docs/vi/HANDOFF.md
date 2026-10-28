# Astur VI — Handoff after in-place updater V2 (2026-10-28)

## Current project state
- GitHub fork: https://github.com/tuanvayt03-cpu/Astur
- Local repo: `D:\Project\Astur`, branch `feat/vi-full-update-popup-v2`; draft PR #3 https://github.com/tuanvayt03-cpu/Astur/pull/3 remains unmerged.
- **NEW PREVIEW UPDATE release**: https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-update-2.4.0.1
- The **immutable release source commit** is `425fe151d0697a4a4d5a885cd7de5d958d8f98d3`. Later docs-only commits may be ahead on the branch.
- Windows GitHub Actions **SUCCESS**: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40680404202, including source fmt, 543-key translation contract, safe-upgrade static contract, Win32 probe syntax, Clippy, Rust workspace unit tests, release build, Inno compile and a simulated in-place upgrade from an already installed Astur using the same AppId.
- User's running original and separate VI Preview on their PC were **not changed**. No install or process kill on user's computer.

## Verified release assets
- `Astur-VI-Update-Setup-2.4.0.1.exe` (4,445,026 bytes), SHA-256 `0d969b989e735d072e033563cbb71a97521757471aa12de383f5c5317f4ede39`.
- `SHA256SUMS.txt` published with the release.
- Release is marked **pre-release**, not stable. `AppId` and installation directory match the original upstream `packaging/astur.iss`, unlike earlier VI Preview which has separate identity.
- Setup backs up current installed `Astur.exe`, `astur-settings.exe`, `astur.conf`, `navbar.conf` (if they exist), first-copy preserved under `%LOCALAPPDATA%\Astur\UpgradeBackup\before-vi-update-2.4.0.1`. Setup preserves a custom existing install path, shortcut/startup task selections, existing config, and can optionally open app afterward. Simulated Windows runner seed-install -> update -> file/config/backup checks -> uninstall all PASS.

## Technical changes and independent audit
- Shared `astur-config::i18n` catalog, **543** unique EN/VI mappings (prior 367), and use in both Settings UI and native manager tray/power menu. Missing locale preference defaults VI; explicit English remains selectable. Program identifiers, user text, process/window names and config values never translated.
- Previous overlay filter required `WS_EX_TOPMOST`. Broadened **tiling-adoption-only** exclusion for compact borderless corner / layered notification-like windows, even if not topmost. Does not hide, close, silence, reposition or eat input from notifications. Synthetic positive and negative tests pass.
- Debugging finding: first upgrade smoke failed because installer Pascal script used unsupported `ExpandConstant('{userprofile}')`; Windows log showed `Internal error: Unknown constant "userprofile"`. Replaced with `{%USERPROFILE}` and added static guard against regression. Fresh end-to-end run `40680404202` PASSED.
- Audit findings and acceptance gates: `docs/vi/AUDIT_UPDATE_V2.md`; upgrade user instructions: `packaging/upgrade-install-notice.txt` and `upgrade-release-notes.md`.

## Outstanding limitations (do NOT claim COMPLETE Stable)
1. **Real Zalo, Telegram, Snipping Tool native popup E2E still UNVERIFIED**. User screenshot of previous Preview shows tiles resized, but actual offending HWND class/style had not been captured. Need real popup and before/after 2/4/6 window geometry + confirm popup animation/dismissal and main Zalo tileability.
2. **Localization NOT proven 100%**. 543 static mappings plus UI wrappers and native tray/power items compile/test, but some dynamic strings/native launcher/status bar and user-facing text may remain English. Need screenshot-by-screenshot visual audit on user machine, various DPI/scales and light/dark modes.
3. Setup is **unsigned**, may trigger SmartScreen; do not advise bypassing security. Separate installed VI Preview may remain on PC: **exit it** before installing/updating original to avoid two simultaneous managers. For rollback, quit updated Astur and reinstall original upstream installer, using saved binaries/config as needed. Keep original config backup until acceptance.
4. Current update published only as Preview pre-release, draft PR unmerged, no source history rewritten.

## Recovery protocol
Refresh `git status --short --branch`, current HEAD, release asset API, and CI run. Preserve release source tag and current user config. Use a new version/tag for further code changes; do NOT overwrite 2.4.0.1 published binaries. Do not claim bug fixed for real native toasts until observed.
