# Astur VI — Handoff after in-place updater V2 (2026-10-29)

## Controller checkpoint — 2026-10-29

Source is a verified static/core-test checkpoint, not release-ready. Direct CodeLocal host verification resolved crates.io access and downloaded the locked dependencies. Fresh inventory (749), formatter and diff checks passed; workspace compilation then stopped at `parking_lot_core`: `dlltool.exe` missing (exit 101). Thus earlier missing-serde_json limitation below is superseded for host execution. Full compile/clippy/test/render remain unverified. Controller-created helper scripts were removed; they were not pre-existing user files. No installer was built or installed. Next: supply the GNU binutils toolchain, run full verifiers and inspect VI/EN renders. Commit/push checkpoint only; no release or merge.

## Current authoritative localization wave — 2026-10-29

- Scope is the current dirty checkout on `feat/vi-full-update-popup-v2`, baseline HEAD `72110704faa88859e6f222286d19b1f1b2d9db68`. The primary writer did not launch Astur, write user config, install/release, commit, or push.
- First-party source coverage now includes the shared `astur-config::i18n` catalog, all 14 Settings pages, metadata/sections/notes, search and validation output, key-picker/help text, native launcher/power-menu labels, status layout/mute labels, runtime save/toast errors, and locale-aware date formatting. The catalog has **749 unique entries**; the inventory gate scans both `tr` and `trf` literals and reports zero missing static calls, sections, notes, metadata labels/descriptions, tips, format labels or owned dynamic templates. Three explicit exceptions remain by contract: user data, machine data and shortcut tokens. This is source/render-boundary coverage, not a claim of pixel-level 100% localization.
- Changed source files: `crates/astur-config/src/i18n.rs`, `crates/astur-config/src/lib.rs`, `crates/astur-settings/src/main.rs`, `crates/astur/src/main.rs`, and `scripts/test_i18n_inventory.py`. Existing untracked `scripts/run_localization_audit.ps1` was preserved unchanged.
- The screenshot regressions are covered at the render boundary: `Space between windows`, `Hold Left Alt...`, `Tile windows when Astur starts`, and Alt-drag help. Dynamic strings use named interpolation; config/action IDs, user data, class/exe names and shortcut tokens remain untouched.

### Fresh evidence

| Command | Result |
|---|---|
| `cargo fmt --all -- --check` | exit 0 |
| `git diff --check` | exit 0 |
| `python scripts/test_i18n_inventory.py` | exit 0; 749 entries, 14 pages, `tr`/`trf` and all tracked categories missing 0 |
| `cargo metadata --offline --no-deps --format-version 1` | exit 0 |
| `C:\Program Files\Rust stable GNU 1.99\bin\rustc.exe --edition=2021 --test crates/astur-config/src/lib.rs` | exit 0; direct test binary 71 passed, 0 failed, including screenshot/interpolation and EN/VI date regressions |
| `cargo test --offline -p astur-config --lib --locked` (GNU cargo) | exit 1: Cargo resolver cannot find cached `serde_json` from workspace package `astur` |
| `cargo clippy --offline --workspace --all-targets --locked` | exit 1: cache lacks `serde_json` |
| `cargo test --offline --workspace --all-targets --locked` | exit 1: cache lacks `serde_json` |
| `cargo build --offline --release --workspace --locked` | exit 1: cache lacks `serde_json` |
| `cargo test --offline -p astur-settings -- --ignored render_pages --locked` | exit 1: cache lacks `serde_json` |

The online Cargo test was also attempted and could not reach `index.crates.io`; no dependency or network workaround was installed. Full workspace compile, clippy, release build and offscreen Settings render remain UNVERIFIED for this machine. Exact next action: provide a Windows GNU toolchain (or MSVC Build Tools) and the locked dependency cache/network, rerun the four Cargo commands above, then inspect both VI and EN `render_pages` artifacts before any controller-owned commit/push. The pre-existing untracked `scripts/run_localization_audit.ps1` remains untouched; its `workspace-write` setting is a residual audit risk, not part of this localization change.

One real test defect found and fixed in this wave: locale-sensitive date golden tests raced the global locale tests. A test-only shared lock now makes EN/VI assertions deterministic; it does not alter runtime locale semantics.

The release/installer and notification sections below are historical context from 2026-10-28, not fresh evidence for this checkout.

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
