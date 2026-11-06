# Astur VI update 2.4.0.19 — release handoff (2026-11-06)

## Baseline
- Source: `fix/astur-small-utilities-unmanaged-20261106` at `126cd9ecf550941dd8e1819a985ab01c7b39f8de`, based on previous release 2.4.0.18 commit `c64f8347c69b0a624ad807a30331699c04f99118`.
- Release branch: `release/astur-vi-update-2.4.0.19` (dedicated, one-shot).
- Scope: packaging workflow, version, installer notice, release notes, handoff. No source Rust edits on this release branch.
- Source PR #14 draft; previous 2.4.0.18 GitHub tag/asset preserved.

## Required verification
- Source branch fresh Windows CI rustfmt/Clippy/tests/build.
- Release branch fresh CI plus dedicated updater workflow. Windows screenshot renders, original AppId in-place installer smoke, two rollback backups, config preservation/uninstall, installer SHA256, GitHub prerelease publish.
- Verify exactly one tag `astur-vi-update-2.4.0.19` at final release commit, prerelease and installer+manifest asset checksums.
- No installed user Astur instance touched. Real one/two-monitor UI E2E on disposable apps pending.

## Recovery
- Backup first original: `before-vi-update-2.4.0.1`.
- Backup immediately previous: `before-vi-update-2.4.0.19`.
- Prior 2.4.0.18 installer remains available.
- Do not claim live acceptance from CI. If a required check fails, fix on the release branch, fresh verify, and publish only after green.
