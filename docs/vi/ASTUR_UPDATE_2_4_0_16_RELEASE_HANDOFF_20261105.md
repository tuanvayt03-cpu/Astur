# Astur VI Update 2.4.0.16 — release handoff

Date: 2026-11-05. Main writer owns release worktree `D:\Project\Astur-update-2.4.0.16` on branch `release/astur-vi-update-2.4.0.16`. Baseline is `d857e72fb7a547e6d4559a4e86e45d3220076da7`, source fix branch `fix/astur-auto-slot-separate-20261105` and draft PR #10. The prior public release 2.4.0.15 at `507be759e81c06fe04a122c9d7c6dd8313e5e114` remains immutable and untouched.

## Release contract

- New version/tag: `2.4.0.16` / `astur-vi-update-2.4.0.16`; verify tag and release do not exist before push.
- Preserve original AppId, installer directory, existing settings, dual backups (original first snapshot plus `before-vi-update-2.4.0.16`) and rollback.
- Update only release metadata `.github/workflows/upgrade-release.yml`, `packaging/astur-vi-update.iss`, `packaging/upgrade-install-notice.txt`, `packaging/upgrade-release-notes.md` and this handoff. The source features are inherited from the verified fix branch.
- Behavior: new overflow windows no longer turn on manual tab UI, single-window columns no longer render a black title bar, parked/hidden windows recover on activation, explicit tab toggles have independent semantics, and no early scroll is performed before slot admission finishes.
- A successful installer CI is **not** evidence of real interactive one/two-monitor acceptance. GitHub release is an unsigned experimental prerelease, never stable/latest. Do not install/launch Astur on a busy MT5 desktop automatically.

## Critical path / gates

1. Preflight: clean isolated release worktree, source commit/branch, absent tag/branch and previous live release preserved.
2. Release files and notes version bump, tests: `py scripts/test_upgrade_packaging.py`, `py scripts/test_preview_packaging.py`, `py scripts/test_i18n_inventory.py`, `git diff --check`.
3. Single-writer commit/push dedicated release branch.
4. GitHub Windows release job: rustfmt, Clippy -D warnings, all unit/regression tests, Settings VI/EN rendered offscreen, x64 release build, Inno Setup installer, AppId in-place upgrade/backup/uninstall smoke, SHA-256 file and GitHub asset publish.
5. Verify released tag points exactly to release branch SHA, prerelease=true, installer and checksum exist and are downloaded/verified against GitHub digest.
6. Record final dynamic HEAD/worktree statuses, PR/CI/release links and rollback path.
7. **Unresolved live acceptance**: with disposable non-MT5 windows on a real 1/2 monitor desktop, verify CS1 anchor / CS2 replacement both directions, minimize/restore, title-bar+Alt dragging, tab OFF/ON, tab-less lone Explorer, one taskbar click, F11/maximize and Zalo notifications. Keep PR #10 draft and treat stable rollout BLOCKED until the owner verifies.

## Safety

No force push or existing-tag overwrite. No edits/installation on original `D:\Project\Astur` worktree or active user desktop. No changes to MT5 orders or trading control. Failed CI must block publication; inspect logs and repair on source/release branch then run fresh evidence. Don't bypass OS security warnings.

## Pending update after release

Record final source/release SHA, Windows CI result, release artifact filename, real SHA256, original working tree status, and QA gate.
