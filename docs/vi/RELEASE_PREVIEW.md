# Astur VI Preview — Packaging and Release Contract

Status: **Preview package published and install/uninstall tested on isolated GitHub Windows runner; no user-desktop installation or runtime execution performed**. Source branch: `feat/vi-notifications` (fork `tuanvayt03-cpu/Astur`). Preview version: `2.4.0-preview.1`.

## Objective
Ship an actual Windows x64 `.exe` installer and a portable `.zip`, without replacing or shutting down the original Astur. The installer must carry both `Astur.exe` and `astur-settings.exe`, licensed notices and a clear first-run warning.

## Isolation boundary
- Preview installer Inno Setup `packaging/astur-vi-preview.iss`: distinct `AppId`, `%LOCALAPPDATA%\Programs\Astur VI Preview` installation path, Start Menu and independent uninstall.
- Never autostart or launch at completion. Never close running applications or replace original Astur binaries.
- **Not fully isolated at runtime.** Both versions still read/write `%USERPROFILE%\.astur` and can install global low-level keyboard/mouse hooks. Do **not** run them simultaneously. Exit the original and back up the configuration before trying Preview.
- No runtime GUI or native Zalo/Telegram popup E2E was performed, so label `Preview`, not `Stable`.

## Build DAG
Source tests -> Windows cargo release workspace -> verify both executables and license -> Inno Setup compiler -> portable ZIP + SHA-256 -> **isolated GitHub runner** silent install / file assertions / silent uninstall -> portable ZIP extraction assertions -> pre-release publication.

Release workflow `.github/workflows/preview-release.yml` triggers once when introduced on the feature branch and can be manually dispatched after it is available on the default branch. Tag `astur-vi-preview-2.4.0.1` intentionally does not match upstream `v*` production-release workflow. No existing release is overwritten; duplicate tag/release is an explicit error.

## Machine verification
- `python scripts/test_preview_packaging.py`: asserts separate GUID and path, no startup or automatic launch, no original-app close, bundled two binaries/legal notices, checksum and smoke steps.
- CI includes Rust fmt, Clippy (warnings denied), workspace unit tests, source localization contract, and Windows release build.
- Preview package workflow smoke-installs on disposable GitHub Windows runner, **not** the user's PC; verifies installed files, then uninstalls. Portable ZIP is extracted and validated.
- Published `SHA256SUMS.txt` supports user-side checksum verification.
- Unsigned binaries may trigger SmartScreen. Never recommend disabling antivirus or security protections.

## Known unverified behavior
Actual Zalo, Telegram, Snipping Tool and Windows notification classification is still not E2E confirmed. Only a bounded classifier and synthetic tests have passed. Native GUI display at varying DPI, exact translations for every first-party string, concurrent process behavior, and settings conflicts are not fully tested.

## User recovery
1. In original Astur's tray menu, choose Quit before running Preview.
2. Back up `%USERPROFILE%\.astur`.
3. Install Preview. It does **not** auto-launch.
4. Start Preview from its Start Menu entry to test.
5. Before returning to original, quit Preview and restore the backup if its configuration was changed; uninstall Preview via its own entry.

## Verified pre-release checkpoint
- Source commit: `af9b52b56a308fc090b1cea38bf76599fd9bf4d3`.
- Release: https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-preview-2.4.0.1
- Windows packaging workflow: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40667462157 — **SUCCESS** for fmt, catalog, probe syntax, Clippy, unit tests, release build, Inno compilation, sandboxed installer install/uninstall and ZIP extraction checks.
- Verified GitHub release assets: setup EXE (4,426,196 bytes, SHA-256 `793b166ebae3baf1e4e1650fd41a4487f2e8e3fb0150e14a78d3d434c67bc99a`), portable ZIP (3,358,773 bytes, SHA-256 `3f72ce1a620e70857e8ffea7891d1b920a9f7063df7af791bef08144a6b171dc`), `SHA256SUMS.txt`.
- Source tag intentionally differs from upstream stable tag pattern; release is explicitly marked pre-release.
