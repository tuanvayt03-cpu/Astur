# Astur VI Update 2.4.0.14 — release controller/handoff

## Baseline and scope

- Date: 2026-11-05 (Asia/Bangkok)
- Repository: https://github.com/tuanvayt03-cpu/Astur
- Parent source: `feat/slot-anchor-placement-20261105` at `af4fd2d48f79a194c3c4793180486df9d8a247c6`, Windows CI https://github.com/tuanvayt03-cpu/Astur/actions/runs/41968150301 **SUCCESS**.
- Development PRs: #7 Window Policy Engine and #8 slot-anchor/top-edge maximize (both separate draft reviews; publishing this opt-in prerelease does not merge them).
- Release branch/worktree: `release/astur-vi-update-2.4.0.14`, `D:\Project\Astur-update-2.4.0.14`.
- Existing local installation source worktree remains `D:\Project\Astur`, branch `release/astur-vi-update-2.4.0.12` at `a3fee38`, unchanged.
- Previous existing GitHub release: `astur-vi-update-2.4.0.13` (published 2026-11-04), immutable. New tag `astur-vi-update-2.4.0.14` must not be present before the release.
- No live desktop modifications or installer execution on the user's machine. Installer smoke only in disposable Windows GitHub runner.

## Scope

1. Retain all features from slot-anchor preview and Window Policy Engine: focus-anchored new windows, free slots first, N-1 tab reuse, nonadjacent dragging/swapping, native top-edge maximize and prior notification safety.
2. Bump ONLY the dedicated upgrade-release workflow, installer metadata, per-version rollback path and preview release notes to `2.4.0.14`. Preserve older 2.4.0.13 release/tag and historical change notes.
3. Preserve the upstream AppId and remembered install directory, startup task, original first-upgrade backup, new prior-2.4.0.14 backup and user config.
4. Publish **GitHub prerelease**, not stable/latest. Do not push over an existing tag, install locally, or merge draft PRs.

## DAG and gates

- S0 resolve release version, tags, branch, workspace, ownership -> DONE before editing.
- S1 update installer/workflow/notes -> done on release branch.
- S2 local contract checks: `py scripts/test_upgrade_packaging.py`, `py scripts/test_i18n_inventory.py`, `py scripts/test_preview_packaging.py`, `git diff --check` -> PASS before CI trigger.
- S3 single-writer commit and push dedicated release branch -> triggers `.github/workflows/upgrade-release.yml`.
- S4 Windows CI: fmt + Clippy + unit tests + EN/VI Settings renders + release build + Inno Setup + custom-dir upgrade/backup/uninstall smoke + SHA256 and artifact -> must PASS.
- S5 GitHub prerelease `astur-vi-update-2.4.0.14` with `Astur-VI-Update-Setup-2.4.0.14.exe` and `SHA256SUMS.txt` -> verify source SHA/tag, manifest and asset size/digest.
- S6 refresh both worktree statuses, remote, release URL and Git commit; final handoff.
- S7 live one/two-display acceptance remains **PENDING** and does not become PASS from CI.

## Safety / recovery

- Workflow is limited to dedicated release branch and rejects an existing tag.
- Never force-push, rewrite history, overwrite old release assets, disturb unrelated local work, launch Astur next to an active instance, or change the user's live registry/config/processes.
- If Windows CI fails, fix root cause on this branch, keep old released artifact intact and fresh-verify.
- If publication fails, preserve Actions installer artifact and note release gate FAILED; do not claim GitHub release exists.
- The installer is unsigned: don't instruct users to bypass Windows security warnings.
- Checkpoint after release: record final commit/tag, Actions run IDs/status, released asset/checksum, outstanding live acceptance and clean Git state.

## Verification status

On branch before push: upgrade package contract PASS, preview contract PASS, Vietnamese i18n inventory PASS, `git diff --check` PASS. All Windows CI checks and publication PENDING until run completes.
