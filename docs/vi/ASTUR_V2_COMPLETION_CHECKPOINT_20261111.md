# Astur V2 runtime completion checkpoint — 2026-11-11

## Baseline

- Source baseline: `astur-vi-update-2.4.0.19` at `4dedce4`.
- Working branch: `feat/astur-v2-completion-20261111`.
- Worktree was clean before this change.
- No Astur process, installation, user configuration, MT5 or SignalOps session
  was started or modified.

## Runtime repair

The shared native title-bar drag snapshot is now owned by the HWND that started
the move loop:

- all geometry is written before the active HWND is published;
- `MOVESIZEEND` uses an acquire/CAS ownership check;
- an out-of-order `END(A)` cannot consume the newer `START(B)` snapshot;
- a matching `END(B)` still consumes B's snapshot exactly once;
- the regression covers empty, mismatched and matching ownership decisions.

This closes the confirmed source gap recorded in the 2026-11-06 native-drag
audit without changing Alt-drag, resize, maximize or custom-titlebar policy.

## Fresh verification

- `cargo fmt --all -- --check`: PASS.
- `git diff --check`: PASS.
- `cargo test -p astur-config --locked`: PASS, 73 passed / 0 failed.
- `python scripts/test_i18n_inventory.py`: PASS, 824 catalog entries / 14
  Settings pages.
- `python scripts/test_upgrade_packaging.py`: PASS.
- `python scripts/test_preview_packaging.py`: PASS.
- Full `cargo test -p astur --locked`: BLOCKED on this host because the bundled
  GNU toolchain's `dlltool.exe` cannot create the Windows import library for
  `bcryptprimitives.dll`. This is an environment/toolchain limitation, not a
  test result.

## Acceptance boundary

The source-level runtime repair is ready for fresh Windows CI. Desktop E2E for
native/custom titlebars, two monitors, DPI, taskbar recovery and notification
ownership remains a separate required proof and must not be reported as PASS
until run on a disposable Windows desktop. No installer or release tag is
created by this checkpoint.
