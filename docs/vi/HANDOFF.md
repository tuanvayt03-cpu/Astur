# Astur VI — Durable Handoff

Updated: 2026-10-28 11:19 ICT (approximate session time). Lifecycle: PLAN_CHECKPOINT / IMPLEMENTATION_PENDING.

## Repository/identity
- Owned fork: https://github.com/tuanvayt03-cpu/Astur (verified admin/push).
- Original: https://github.com/Page011/Astur; upstream default main baseline b60500f0155c1d817936b869989718299cbd3f14, tagged source version 2.4.0 in Cargo.
- Branch: docs/vi-localization-plan, tracking origin/docs/vi-localization-plan; base fork main remains at upstream commit. PR: https://github.com/tuanvayt03-cpu/Astur/pull/1 (open; plan only).
- CodeLocal authorized workspace: D:\Project; local clone: D:\Project\Astur. Do not modify other repos or current Astur installation.

## Scope and artifacts
1. .omx/plans/2026-10-28-astur-vietnamese-and-notification-fix.md — execution DAG, acceptance criteria, dispatch responsibilities.
2. docs/vi/SDD.md — Vietnamese i18n proposal, popup diagnosis-first architecture.
3. docs/vi/CONTRACT.md — invariants, exact test matrix.
4. This handoff checkpoint.
These are documentation-only; **no i18n implementation nor notification popup fix yet**.

## Fresh evidence from this session
- Fork created by gh repo fork Page011/Astur --clone=false, exit 0; GitHub get_repo confirmed fork owner/admin rights.
- Local clone via git clone completed exit 0; git fetch planning branch exit 0, git switch --track completed exit 0.
- At the docs-only checkpoint, git status --short --branch was clean on docs/vi-localization-plan; git diff --check origin/main...HEAD returned 0.
- GitHub fetched docs/vi/CONTRACT.md from planning branch and verified contents.
- GitHub Actions workflow results were not present for planning branch at last check; `gh pr checks 1 --repo tuanvayt03-cpu/Astur` returned 'no checks reported'. Do not claim CI pass.
- `cargo --version` failed in CodeLocal shell ('cargo' not recognized). Rust toolchain availability elsewhere not yet ruled out.
- OS window list was available, but no target toast shown/captured; root cause of grouping remains unconfirmed.
- Fork's Issues API returned HTTP 410 (Issues disabled). Track notification regression inside plan/PR rather than creating phantom issue.

## Code inspection evidence
crates/astur/src/main.rs:4994-5035 BLOCK_CLASSES; 5042-5150 app_surface_reject, app_window_reject, manage_reject; style and owner exclusions already exist. Broader app-class exclusions previously broke main app management per source comment. No code edits to these paths until real transient HWND identity/geometry/lifetime is observed.

## Next actions — exact order
A. Set up/verify Rust toolchain or CI; baseline fmt/clippy/test/build on Windows; capture exact source SHA and failed checks.
B. Reproduce Telegram + Zalo + Windows/Snipping Tool notifications and screenshots without changing their current settings. Capture sanitized HWND metadata, no message content, owner/class/style/rect/event trace and compare app main HWND.
C. Add regression fixtures; implement narrow exception at correct adoption gate. Re-run tests, manual stress and genuine main-window tiling.
D. Inventory and implement en/vi catalogs, native font/geometry tests, locale preference and UI switch according to SDD.
E. Verify full matrix, release separate installer with legal notices and rollback. Only mark COMPLETE after fresh evidence.
Do not run an experimental window manager over current desktop or uninstall/change existing Astur without a safe recovery plan.

## Pending
- Notification bug: UNVERIFIED root cause; UNFIXED.
- i18n: PLANNED only.
- CI: NOT RUN / no checks reported; local compiler PATH missing.
- Release binaries: NOT BUILT.
- Last verified before this checkpoint: clean local planning branch at commit 78c281af39c2c0ea131ebd1707704fef4f54aa2c. This file commit becomes the new remote head; refresh SHA and local branch after writing.

## Recovery
Open the PR and documents, re-check GitHub branch HEAD and CodeLocal git status/diff before any edits. One primary writer. No secret, no unscoped repo edits, no force-push.
