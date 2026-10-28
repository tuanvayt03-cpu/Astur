# Astur VI — Fresh Handoff / Recovery Checkpoint

Date: 2026-10-28. State: **PARTIAL — CODE AND WINDOWS CI PASS; APP-SPECIFIC POPUP E2E AND INSTALLER NOT VERIFIED**.

## Baseline
- Upstream `Page011/Astur@b60500f` v2.4.0; owned fork https://github.com/tuanvayt03-cpu/Astur.
- Active branch `feat/vi-notifications` at `D:\Project\Astur`, tracking `origin/feat/vi-notifications`. Parent planning branch `docs/vi-localization-plan`, PR #1.
- Draft feature PR: https://github.com/tuanvayt03-cpu/Astur/pull/2. Overlay-source checkpoint `1091d22` pushed; follow-up Windows CI run https://github.com/tuanvayt03-cpu/Astur/actions/runs/40659722010. Resolve Git status and final SHA after any documentation update.
- Installed Astur on Windows user desktop was not touched. One primary writer; other repositories outside scope are untouched.

## Delivered code
1. Settings English/Vietnamese selection and separate persisted `ui-language.txt`, English fallback; no mutation of layout/window rules/action identifiers.
2. `crates/astur-settings/src/i18n.rs` contains **367 unique translated strings**; direct Settings nav, sections, row metadata, various buttons, hover hints and drop-downs are translated at display boundaries. English and Vietnamese row query both searchable. Some first-party strings, native launcher/status/tray/installer remain English.
3. `scripts/test_i18n_inventory.py` statically checks navigation/metadata coverage, duplicate keys and EN/VI placeholder preservation. `scripts/capture_notification_windows.py` reads Win32 metadata only (no messages/secrets); callback signature unified during audit.
4. GitHub Actions CI enabled on fork; workflow includes Rust format/clippy/test/release and Python catalog/probe guards on next commit.

## Fresh evidence available
- `python scripts/test_i18n_inventory.py`: exit 0; 367 translations, 75 literal metadata tuples, 0 missing in covered groups, no duplicate/placeholder defect.
- `python -m py_compile` for diagnostic script and localization test: exit 0.
- CI run https://github.com/tuanvayt03-cpu/Astur/actions/runs/40645288503 for Rust commit `4efaf42`: **Format PASS, Clippy PASS, Test PASS, Release build PASS** (overall success). Audit/QA checkpoint `5db2584` also passed full Windows CI, including translation and probe steps: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40646010315. CI/release workflow action versions were then updated to Node24 majors, requiring a fresh CI result.
- Windows CI for overlay source commit `1091d22`: **PASS Format, catalog checks, probe syntax, Clippy, workspace Test and Release build**: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40659722010. CodeLocal `where cargo` still fails; CI is the authoritative compiler evidence.
- Added non-suppressing overlay-adoption guard: compact captionless topmost WS_POPUP windows without WS_EX_APPWINDOW stay visible and OS-managed while excluded from Astur tiling/tabs. Normal main application windows, captioned popups and fullscreen windows stay eligible. New synthetic geometry/style regression tests were added. Actual Zalo/Telegram HWND popups were not available to capture; **app-specific runtime behavior remains UNVERIFIED**.

## Critical open work
P0: Capture an actual offending Zalo/Telegram/Windows toast HWND (style/class/owner/size) and normal main windows; verify the new narrow overlay classifier catches it and its appearance/dismissal remain normal. Expand test cases only from evidence. Run OS screenshot and 2/4/6 tiled-window geometry E2E without touching installed production Astur.
P1: Complete native/secondary locale coverage, Windows visual snapshot and layout QA.
P1: Build isolated installer, preserve Apache-2.0 notices, run install/update/rollback smoke without interfering with original running Astur.
P1: Keep draft PR #2 unmerged; update final CI status after the handoff docs checkpoint, and do not mark C07–C09 as E2E PASS without real notification samples and unchanged grid geometry.

## Next session recovery
Check `git status --short --branch`, `git rev-parse HEAD`, remote HEAD, PR #2 and latest GitHub run, read `docs/vi/SDD.md`, `CONTRACT.md` and `AUDIT_2026-10-28.md`. Run QA, fix failures without weakening tests, checkpoint commit and push without force. No release until notification and runtime E2E pass.
