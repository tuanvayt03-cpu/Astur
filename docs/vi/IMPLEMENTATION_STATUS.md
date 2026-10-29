# Astur VI — Implementation Status

## 2026-10-29 localization audit — current checkout

- Baseline: `72110704faa88859e6f222286d19b1f1b2d9db68` on `feat/vi-full-update-popup-v2`; no app launch, config write, install/release, commit or push.
- Source/render-boundary inventory: **749** unique catalog entries, all **14** Settings pages, zero missing static `tr` and `trf` literals, sections, notes, metadata labels/descriptions, tips, format labels and owned dynamic templates; explicit exceptions are user data, machine data and shortcut tokens. This deliberately does not claim pixel-level 100%.
- Localization boundaries completed: screenshot strings and Alt-drag help; named interpolation for dynamic key/help/validation/search strings; key picker and validation; native launcher headers/prompts/web rows; native power built-ins; status layout/mute labels; EN/VI date names. Internal config/action IDs, window identity fields, user content and shortcut tokens remain unchanged.
- Fresh local evidence: `cargo fmt --all -- --check` exit 0; `git diff --check` exit 0; `python scripts/test_i18n_inventory.py` exit 0; `python -m py_compile scripts/test_i18n_inventory.py` exit 0; `cargo metadata --offline --no-deps --format-version 1` exit 0. GNU `rustc` from `C:\Program Files\Rust stable GNU 1.99\bin` compiles and runs the direct `astur-config` test binary: 71 passed, 0 failed. GNU Cargo workspace verifiers still exit 1 at missing cached `serde_json`.
- Required workspace verifiers are blocked by environment dependency resolution, not reported as PASS: offline clippy, workspace tests, release build and ignored `render_pages` all exit 1 because the local cache has no `serde_json`; online Cargo cannot reach crates.io. No dependency was installed or changed.
- Exact next actions: on a machine with a usable Windows linker plus the locked dependency cache/network, rerun fresh `cargo clippy --offline --workspace --all-targets --locked`, `cargo test --offline --workspace --all-targets --locked`, `cargo build --offline --release --workspace --locked`, and `cargo test --offline -p astur-settings -- --ignored render_pages --locked`; inspect both VI/EN render artifacts, then have the current controller re-read HEAD/tree and decide commit/push. Do not treat the pre-existing untracked `scripts/run_localization_audit.ps1` as changed.

2026-10-28 · **In-place Astur VI Update Preview 2.4.0.1 released and upgrade smoke PASSED; NOT Stable.** Repo `tuanvayt03-cpu/Astur`, branch `feat/vi-full-update-popup-v2`. Earlier independent Preview also exists.

## Verified scope
- `astur-settings` GUI English/Vietnamese chooser, preference in `ui-language.txt`, English fallback and no changes to existing window-management settings.
- 367 unique manual EN→VI translation pairs covering all 19 tracked navigation items/groups, 34 tracked section titles and 75 literal settings-metadata tuples (labels and descriptions). Direct call sites for common controls, dropdown labels, hover texts and shortcuts were also converted. Other direct strings and native `astur` executable UI remain incomplete.
- Static QA: 367 entries, 0 duplicate mapping, no missing tracked metadata, EN/VI interpolation placeholders preserved. CI runs `scripts/test_i18n_inventory.py` and probe syntax checks on next commit.
- Windows CI at https://github.com/tuanvayt03-cpu/Astur/actions/runs/40645288503 passed Format, Clippy, workspace Test and release build (overall conclusion SUCCESS) on code commit `4efaf42`. Checkpoint `5db2584` additionally passed expanded CI: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40646010315. The **new non-suppressing overlay classifier and regression tests** passed full Windows CI on source commit `1091d22`: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40659722010. No manual native popup GUI E2E yet.

## Notification issue
A **non-suppressing compact-overlay classifier** now exists in `crates/astur/src/main.rs`. Captionless, non-resizable, small WS_POPUP windows with WS_EX_TOPMOST but not WS_EX_APPWINDOW are kept visible and positioned by their originating application/Windows, but are excluded from the workspace/tile/tab registry. Tests cover synthetic toasts and non-toasts; no global blacklist by app exe/class. This is **NOT YET E2E-verified for actual Zalo, Telegram, Windows toast or Snipping Tool HWNDs**, which were absent during diagnostics. A sanitized read-only metadata capture utility remains available.

## Remaining to COMPLETE
1. Obtain a real popup window signature and reproduce; match it against the new classifier, add any necessary targeted regression and verify native notification presentation, dismissal, normal main app windows and stable grid geometry.
2. Complete untranslated first-party WM UI (launcher/tray/status/power), Windows DPI/Unicode screenshots and language persistence E2E.
3. Preview Windows build and isolated installer install/uninstall PASS at https://github.com/tuanvayt03-cpu/Astur/actions/runs/40667462157. Verify actual user-desktop UI, lifecycle/rollback and release packaging again before Stable promotion.
4. Preview release: https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-preview-2.4.0.1 (installer, portable ZIP, SHA256). Keep draft PR unmerged and publish **Stable only** after fresh verified acceptance; update handoff with SHA, PR and machine evidence.

See `docs/vi/AUDIT_2026-10-28.md`, `docs/vi/HANDOFF.md`, `docs/vi/SDD.md`, and `docs/vi/CONTRACT.md`.

## NEW V2 updater (most recent, authoritative)
- GitHub update pre-release: https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-update-2.4.0.1 ; source commit `425fe151d0697a4a4d5a885cd7de5d958d8f98d3`. This release has the **same AppId** as the English original and is not the old separate VI Preview.
- Windows CI full SUCCESS: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40680404202 ; verified installer build, original seed install, upgrade, config preservation, backup hash, uninstall and checksums. SHA-256 installer `0d969b989e735d072e033563cbb71a97521757471aa12de383f5c5317f4ede39`.
- Shared VI/EN catalog expanded to **543** strings including manager tray/power menus; language defaults VI for first launch. Some native/dynamic UI strings may remain English. User-provided app data, app titles and technical identifiers intentionally stay unchanged.
- Notification-adoption classifier now handles compact non-topmost corner popups and layered popup-like windows; only excludes from tile/tab registration, never suppresses native popup. **Real Zalo/Telegram E2E remains UNVERIFIED**. No unstable blanket process or framework class ignore was installed.
- Previous Preview version remains installable separately but should be **exited** before running this in-place updater; never simultaneously launch two Astur managers. Same user config directory `%USERPROFILE%\.astur` preserved. Installer backup under `%LOCALAPPDATA%\Astur\UpgradeBackup\before-vi-update-2.4.0.1`.
- Stable release, draft PR #3 merge and full first-party translation must wait for screenshot/geometry E2E and user acceptance; do not claim full 100% translation from partial static catalog coverage.
