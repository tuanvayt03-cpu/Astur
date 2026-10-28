# Astur VI — Implementation Status

2026-10-28 · **Partial implementation; no installer release.** Repo `tuanvayt03-cpu/Astur`, branch `feat/vi-notifications`.

## Verified scope
- `astur-settings` GUI English/Vietnamese chooser, preference in `ui-language.txt`, English fallback and no changes to existing window-management settings.
- 367 unique manual EN→VI translation pairs covering all 19 tracked navigation items/groups, 34 tracked section titles and 75 literal settings-metadata tuples (labels and descriptions). Direct call sites for common controls, dropdown labels, hover texts and shortcuts were also converted. Other direct strings and native `astur` executable UI remain incomplete.
- Static QA: 367 entries, 0 duplicate mapping, no missing tracked metadata, EN/VI interpolation placeholders preserved. CI runs `scripts/test_i18n_inventory.py` and probe syntax checks on next commit.
- Windows CI at https://github.com/tuanvayt03-cpu/Astur/actions/runs/40645288503 passed Format, Clippy, workspace Test and release build (overall conclusion SUCCESS) on code commit `4efaf42`. Checkpoint `5db2584` additionally passed expanded CI: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40646010315. The **new non-suppressing overlay classifier and regression tests** passed full Windows CI on source commit `1091d22`: https://github.com/tuanvayt03-cpu/Astur/actions/runs/40659722010. No manual native popup GUI E2E yet.

## Notification issue
A **non-suppressing compact-overlay classifier** now exists in `crates/astur/src/main.rs`. Captionless, non-resizable, small WS_POPUP windows with WS_EX_TOPMOST but not WS_EX_APPWINDOW are kept visible and positioned by their originating application/Windows, but are excluded from the workspace/tile/tab registry. Tests cover synthetic toasts and non-toasts; no global blacklist by app exe/class. This is **NOT YET E2E-verified for actual Zalo, Telegram, Windows toast or Snipping Tool HWNDs**, which were absent during diagnostics. A sanitized read-only metadata capture utility remains available.

## Remaining to COMPLETE
1. Obtain a real popup window signature and reproduce; match it against the new classifier, add any necessary targeted regression and verify native notification presentation, dismissal, normal main app windows and stable grid geometry.
2. Complete untranslated first-party WM UI (launcher/tray/status/power), Windows DPI/Unicode screenshots and language persistence E2E.
3. Verify final Windows CI full suite and isolated installer/rollback/package notices.
4. Merge/promote and publish only after fresh verified acceptance; update handoff with SHA, PR and machine evidence.

See `docs/vi/AUDIT_2026-10-28.md`, `docs/vi/HANDOFF.md`, `docs/vi/SDD.md`, and `docs/vi/CONTRACT.md`.
