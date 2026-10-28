# Astur VI — Durable Handoff / Recovery Checkpoint

Date: 2026-10-28. Lifecycle: **PREVIEW_RELEASED** (installer and portable artifacts published; **NOT STABLE**, runtime popup E2E remains unverified).

## Source identity
- Upstream: `Page011/Astur@b60500f` (v2.4.0).
- User-owned fork: https://github.com/tuanvayt03-cpu/Astur
- Local checkout: `D:\Project\Astur`; branch `feat/vi-notifications`; remote `origin/feat/vi-notifications`.
- Release source commit: **`af9b52b56a308fc090b1cea38bf76599fd9bf4d3`**.
- Released tag: `astur-vi-preview-2.4.0.1` (pre-release, never matches the official `v*` stable workflow).
- Draft feature PR #2 remains unmerged: https://github.com/tuanvayt03-cpu/Astur/pull/2
- Primary integrator owned all writes. Original Astur installation, window process, configuration and other local repositories were not modified.

## Verified assets
Release: https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-preview-2.4.0.1

1. `Astur-VI-Preview-Setup-2.4.0-preview.1.exe`, 4,426,196 bytes, SHA-256 `793b166ebae3baf1e4e1650fd41a4487f2e8e3fb0150e14a78d3d434c67bc99a`.
2. `Astur-VI-Preview-Portable-2.4.0-preview.1.zip`, 3,358,773 bytes, SHA-256 `3f72ce1a620e70857e8ffea7891d1b920a9f7063df7af791bef08144a6b171dc`.
3. `SHA256SUMS.txt`, uploaded as a release asset.

Verified with GitHub Release API: `isPrerelease=true`, all three assets `state=uploaded`; target commit `af9b52b56a308fc090b1cea38bf76599fd9bf4d3`.

## Build and package fresh machine evidence
GitHub Actions release job **SUCCESS**: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40667462157

All completed successfully: Windows checkout, Rust stable, `cargo fmt --all --check`, preview installation safety test, localization catalog test, diagnostics syntax check, `cargo clippy --workspace --all-targets -- -D warnings`, workspace unit tests, `cargo build --release --workspace`, both executable/legal-file assertions, Inno Setup installation, preview installer generation, portable ZIP + checksum, isolated Windows runner **silent install/uninstall smoke**, ZIP extraction and file validation, and pre-release publication.

Local `python scripts/test_preview_packaging.py` and `python scripts/test_i18n_inventory.py` also EXIT 0. Local Cargo PATH remains unavailable; GitHub Windows CI is build evidence. No full GUI or native Zalo/Telegram real popup E2E evidence.

## Preview safety boundary
- Installer GUID is distinct from upstream, directory is `%LOCALAPPDATA%\Programs\Astur VI Preview`, independent Start Menu shortcuts and uninstall.
- No automatic launch, autostart, closure of other processes, or replacement of the installed original. Actual Preview has not been launched on the user's desktop.
- **Critical runtime limitation:** Both installations currently share `%USERPROFILE%\.astur` configuration and rescue data, plus global window hooks. Users must EXIT original Astur and BACK UP `%USERPROFILE%\.astur` before running the Preview; never run the two simultaneously.
- Unsigned installer may prompt SmartScreen; user must evaluate provenance/checksum rather than disable protection.
- Includes 367 EN/VI translations and notification classifier that excludes compact notification-like HWNDs from tiling/tabs while letting them pop normally. **Partial localization and class-specific popup behavior still unverified**.

## Remaining work for Stable
P0: Reproduce real Zalo/Telegram/Windows toast and Snipping Tool overlay; capture sanitized HWND metadata and verify toast appearance, dismissal, unchanged 2/4/6 tile geometry, app main-window tiling.
P1: Finish complete first-party localization incl. native launcher, tray, status bar, popups and installer, visual QA for light/dark and DPI.
P1: Better runtime config isolation for side-by-side execution if required; until then no concurrent launch.
P2: Separate user-acceptance test and appropriately signed stable release if applicable. Do not merge draft PR or announce Stable prematurely.

## Recovery protocol
After this handoff edit, refresh final HEAD, branch, local dirty state, remote and CI. This documentation commit may be ahead of the released artifact's immutable source commit. Do not force-push or rewrite tag/release. Preserve existing binaries and original user configuration.
