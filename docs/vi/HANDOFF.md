# Astur VI — Handoff after in-place updater V2 (2026-10-29)

## Post-notification screenshot fix — Preview 2.4.0.4 (2026-10-29)

- Checkpoint `7db101f` (818 unique translations) was pushed with a normalized-string duplicate gate. Windows CI `40851884525` PASS (format, Clippy, unit tests, release build). Preview 2.4.0.3 updater workflow `40851884551` was running when 2.4.0.4 work began; do not overwrite any published tag.
- The supplied notification screenshot places a compact banner near the **top middle**, whereas existing `transient_overlay_shape()` recognized popup windows without TOPMOST primarily at **screen corners**. Extended generic Win32 classification for **small borderless WS_POPUP windows near top or bottom monitor edge** even if unlayered/not TOPMOST, without app-specific blacklists. Synthetic Rust tests now cover top-centre and bottom-centre banners plus large borderless windows, small ordinary captioned dialogs and normal app windows as counterexamples.
- **This is a plausible source-level remedy, not a verified Zalo live fix**: two read-only Win32 probes on the user's desktop had no real notification HWND at the time. No native Zalo notification was suppressed and no installed process/config was changed. Must verify real notification appears normally and tile sizes do not change before declaring that case PASS.
- Preview 2.4.0.4 has its own immutable tag/installer version and must pass new Windows CI (Clippy/tests/build, locale render, installer upgrade smoke) and screenshot review before distribution. Preserve original backup directory `before-vi-update-2.4.0.1`, original AppId, and all unrelated user work.

## Post-render visual audit — Preview 2.4.0.3 (2026-10-29)

- `de0c727` Windows CI `40851178202` and updater CI `40851178310` failed on Clippy due **four unreachable translation patterns**: the same MainKey descriptions were declared as multiline Rust literals and again as single-line equivalent strings. The first Rust patterns are valid; removed only four duplicate later arms. Correct catalog count is **818 unique messages**, not 822. Added Rust line-continuation normalized duplicate detection in `scripts/test_i18n_inventory.py` to prevent recurrence; local fresh inventory and updater contract PASS; full CI and installer publication for this follow-on patch remain UNVERIFIED until the new SHA's runs finish.

- `2a5b83a` passed Windows CI `40848088030` (fmt, Clippy, full tests, release build). Preview 2.4.0.2 workflow `40848088119` passed tests, bilingual render, upgrade-over-upstream smoke, and release publication; **do not overwrite this immutable tag**.
- Visually inspected GitHub screenshot artifact `12886910390` (78 EN/VI PNG, 14 main Settings pages and expanded views). It revealed English labels/descriptions still visible in Vietnamese mode, e.g. `Astur key`, `Caps Lock` help, `Status bar style`, `Your own style`, `Outer gap`, `Inner gap`, `Installed apps`, `Open windows`, and bar preset descriptions.
- Root cause of false PASS in the old 749-entry gate: `GUI.split("#[cfg(test)]", 1)[0]` truncated at a test-only `seen` field near line 411, before the full Settings page source; metadata parser also missed trailing commas. Changed scan to stop at the real `mod tests` boundary and parse trailing commas. Gate exposed 40 missing Meta labels plus 3 descriptions, now translated; added 9 bar preset blurbs, 6 layout help texts, 5 multi-line MainKey descriptions, and dynamic display labels. Locale catalog is now **818 entries**, including these screenshot-proven fixes. Static gate also checks preset and key description inventory.
- Preview 2.4.0.3 is the intended next immutable release with full Windows CI and bilingual render verification required. No local installation or user settings were modified. Real Zalo notification E2E is **still unverified**: no live toast HWND appeared during two read-only probes; keep popups allowed and do not blacklist the entire app.

## Controller continuation — Preview 2.4.0.2 (2026-10-29)

- Baseline at start: clean `feat/vi-full-update-popup-v2` at `c1aa69d`, tracking `origin/feat/vi-full-update-popup-v2`. The existing published 2.4.0.1 preview is immutable and must never be overwritten.
- This wave prepares **Preview 2.4.0.2**, preserving the original installer AppId, existing install location/config, and the FIRST original backup directory `before-vi-update-2.4.0.1`. Updater tag/version consistency now has a static regression gate.
- `astur-settings` offscreen render test now generates separate `*-vi.png` and `*-en.png` screenshots for all tracked Settings pages. The Windows upgrade workflow checks for at least 14 per language and uploads the image set as a review artifact before building the installer. A green count gate alone does not prove visual translation completeness.
- Notification diagnosis: a read-only Win32 snapshot observed 33 windows, but **no live Zalo/Telegram toast** to compare class/style/owner/geometry with the existing `transient_overlay_shape` predicate. The current predicate and synthetic tests remain in place; **real Zalo/Telegram/browser notification E2E is NOT verified**, and the running installation is unchanged. Do not suppress toasts or blacklist the whole application.
- Fresh local checks after changes: `python scripts/test_upgrade_packaging.py` exit 0; `python scripts/test_i18n_inventory.py` exit 0 (749 entries, 14 pages, zero missing); `python -m py_compile` for the three diagnostic/contract scripts exit 0; CodeLocal Git diff review completed. Local full Rust checks are **unverified** because `cargo` is not in the permitted execution PATH and an external absolute GNU toolchain path is disallowed by the workspace execution policy. This is not a product/test PASS.
- Post-push CI of `4bd4313` failed Clippy on **nine pre-existing localization compile errors** (seven Rust `String` versus `&str` interpolation mismatches in Settings, two `tr`-function shadowing errors in system-menu painting), confirmed in both the prior `c1aa69d` and new Windows run logs. These are same-lifecycle defects and were patched in the follow-on checkpoint; this remains **UNVERIFIED** until fresh CI against the follow-on commit passes. Never mark the 4bd4313 run PASS.
- Critical path: commit/push only the confirmed Clippy fixes; observe new Windows CI fmt/Clippy/workspace tests/bilingual renders/release build/isolated upgrade; inspect VI/EN PNGs for layout/glyph issues; then allow only a clearly labeled prerelease. For notification acceptance, still obtain real transient HWND metadata during a popup and compare against the main app window and 2/4/6 tile geometry before declaring C07–C09 PASS. No local install, user config mutation or live manager restart authorized or performed.

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
