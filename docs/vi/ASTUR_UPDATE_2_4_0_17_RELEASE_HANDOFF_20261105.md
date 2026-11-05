# Astur 2.4.0.17 preview release handoff

Date: 2026-11-05 (ICT). Isolated primary-writer worktree `D:\Project\Astur-update-2.4.0.17`, branch `release/astur-vi-update-2.4.0.17`. Source baseline `ff315dd497efd9a26d657713c4b81467ce6e2e06` on `fix/astur-cross-monitor-telegram-20261105`, draft PR #11. Previous published 2.4.0.16 release `9ba362457de7dcc7ad5fe6167314e4375b27dc7c` is preserved.

## Objective / scope

- Publish an UNSIGNED experimental 2.4.0.17 Windows x64 *in-place update* for the source changes already independently built in CI (PR + push), with the original Astur AppId, installation path and backup/rollback identity.
- Cross-screen direct slot exchange (1↔3, 1↔4, 4↔2, 3↔2), no interim jump to column 1, preserve slot widths, tab grouping, offsets and ownership.
- Telegram/taskbar recovery: accept repeated foreground only when a managed window is still physically parked, iconic or Astur-hidden, plus guarded SHOW and retile recovery; avoid arbitrary focus stealing.
- Preserve 2.4.0.16 Manual Tab versus Auto Slot separation and previous Zalo exemptions.
- Only release packaging metadata, install notice, notes and handoff may be changed here. No installer launch, MT5 automation, user config mutation, forced commit or overwritten prior releases.

## DAG / gates

1. Verify source branch SHA, clean worktrees, no tag/branch/release collision. Keep prior 2.4.0.16 untouched.
2. Set workflow, ISS and installer notice to 2.4.0.17. Keep original AppId unchanged and first-original backup preserved; change immediate snapshot to `before-vi-update-2.4.0.17`.
3. Source-local: `py scripts/test_upgrade_packaging.py`, `py scripts/test_preview_packaging.py`, `py scripts/test_i18n_inventory.py`, `git diff --check`.
4. Commit scoped changes, push release branch. Windows release CI: rustfmt, Clippy `-D warnings`, full Rust tests, bilingual Settings render, x64 binary, Inno Setup, AppId in-place upgrade/backup/uninstall smoke, SHA256SUMS and GitHub prerelease publication.
5. Verify tag points exactly to final release SHA; prerelease status, asset, file size, checksum and independently downloaded hash.
6. Check all worktrees, record remote branch/HEAD, evidence, blockers in PR #11. Keep PR draft.
7. **Live UI E2E pending**: safe disposable windows on the user's real two displays; Telegram once from taskbar, all cross-screen 4-slot drags, negative monitor coords, minimize/restore, no tab strip on singleton Explorer, native maximize and Zalo popup. No stable promotion until actual acceptance.

## Recovery / safeguards

Prior 2.4.0.16 remains a downloadable rollback candidate. Stop one Astur manager before upgrading; do not operate two window managers. No silent install. No Windows Defender/SmartScreen bypass. All evidence about private Telegram/MT5 chats stays outside the repository.

## Dynamic checkpoint after release

To fill with exact release SHA, CI workflow IDs and conclusions, asset SHA-256, and status of pending desktop QA. CI PASS must not be described as live GUI acceptance.
