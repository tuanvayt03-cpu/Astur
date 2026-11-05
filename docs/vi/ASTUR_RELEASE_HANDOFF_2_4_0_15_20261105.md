# Astur VI 2.4.0.15 — release/handoff

## Baseline & ownership

- Date: 2026-11-05, Asia/Bangkok.
- Prior published release `astur-vi-update-2.4.0.14` tag -> commit `1b665143a8bf15d831d8191fb57f9ff3f5668544`; untouched.
- Source fix branch `fix/astur-stable-slots-20261105` HEAD `1be70f95f376ece2ad6bb2f8f893cb6591c3d5fc`; PR #9 (draft). Source CI run https://github.com/tuanvayt03-cpu/Astur/actions/runs/41996637086 **SUCCESS**, including Format, Clippy, tests and release build.
- Release branch `release/astur-vi-update-2.4.0.15`, isolated worktree `D:\Project\Astur-update-2.4.0.15`. A single primary writer owns release files.
- Other worktrees (original `D:\Project\Astur`, 2.4.0.14 release and source fix) remain unchanged. No local installer launch, process stop, registry/config mutation or MT5 interference.

## Scope

- Use fixes in `docs/vi/STABLE_SLOT_ROOT_CAUSE_FIX_20261105.md`: stable slot geometry for minimized windows, focus-safe admission, group-aware drag swaps, geometry-driven target detection and bounded automatic reveal.
- Bump only `.github/workflows/upgrade-release.yml`, `packaging/astur-vi-update.iss`, `packaging/upgrade-install-notice.txt`, release notes and this handoff to 2.4.0.15.
- Keep installer `AppId` and original destination/config, original 2.4.0.1 backup, and newly retained `before-vi-update-2.4.0.15` snapshot. Preserve all existing GitHub tags/releases; do not rewrite history.
- Publication mode: GitHub **prerelease**, never stable/latest. It is unsigned and not automatically installed.

## Gates / critical path

1. Verify target branch and tag are absent; source branch clean and source CI PASS.
2. Update release metadata and notes; local `py scripts/test_upgrade_packaging.py`, `py scripts/test_preview_packaging.py`, `py scripts/test_i18n_inventory.py`, `git diff --check`.
3. Commit/push only scoped release changes; run dedicated Windows upgrade workflow.
4. Gate on rustfmt, Clippy, unit tests, EN/VI Settings render, x64 build, Inno Setup, in-place upgrade/rollback/uninstall smoke and checksum.
5. Confirm GitHub prerelease tag matches release SHA, installer asset present, SHA256SUMS.txt matches actual downloaded installer, source worktree clean, local original worktree unchanged. Record exact CI and release links.
6. **Live desktop QA still PENDING**: test 1/2, 1/4, 1/5 slots and two monitors, drag/tab swap, add CS3 from both anchors, minimize/restore, native maximize, Zalo popup and MT5 interactions. Do not mark LIVE PASS based on CI. No uncontrolled second WM instance.

## Remaining safety

- Limit fixes to in-scope branch. Maximum two repairs per root cause before re-diagnosis.
- No release overwrite, force-push, unauthorized installer execution, or destructive changes to workstations.
- If publishing fails, preserve the existing release and note blocking gate; do not invent a successful download link.

## Final checkpoint

Pending release workflow and asset verification. After publication update PR #9 with source/release SHA, workflow result, exact hashes, clean git status and outstanding desktop QA.
