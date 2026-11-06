# Astur VI 2.4.0.18 release checkpoint | 2026-11-06

## Origin and scope
- Source branch: `feat/astur-pinned-overlay-20261106`, exact baseline `86a95b7954379bd788bbe56bb6b76643a24167d9`, which is 15 commits ahead of `astur-vi-update-2.4.0.17` with zero missing base commits.
- New release branch: `release/astur-vi-update-2.4.0.18`; source PR #13 remains draft.
- This branch owns **release metadata, preview installer, release notes, and workflow** only. No new overlay code.
- Prior GitHub tag `astur-vi-update-2.4.0.17` and published files must remain unchanged.
- New version/tag: `2.4.0.18` / `astur-vi-update-2.4.0.18` (preview only).

## Verification and release gate
1. Verify pre-existing release/tag/branch collision absent and baseline source CI green.
2. Lock release workflow to new branch, update installer with original Astur AppId and first-original plus immediate pre-2.4.0.18 rollback snapshots.
3. Run Windows rustfmt, translation, upgrade packaging contract, CI Clippy/tests, bilingual Settings renders, release build, seed-install + in-place-upgrade + backup + uninstall smoke, SHA256.
4. Publish new prerelease with installer and checksum only after smoke PASS. If publication fails, report failure and retain upload artifact without pretending publication succeeded.
5. Verify release asset, SHA256, tag commit, CI and branch head.
6. **Desktop acceptance A01–A14 remains pending** until safe isolated Windows desktop is available. Do not run preview against active MT5/SignalOps or another running Astur process.

## Current safety boundaries
No auto install, no modifying user desktop/config, no changing broker status, no force push, no overwrite of a tag or existing release. PR #13 and previous release stay intact. Runtime desktop acceptance not verified by GitHub CI.
