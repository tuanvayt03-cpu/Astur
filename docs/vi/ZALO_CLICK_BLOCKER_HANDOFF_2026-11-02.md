# Astur 2.4.0.11: Zalo popup still steals clicks — evidence gate

Date: 2026-11-02.
Branch: `fix/zalo-notification-maximize-input`.
Known published installer: `astur-vi-update-2.4.0.11`, based on `ef970ea`.

## Latest real-world report

User's screenshot shows a group notification window at the very top edge of
the desktop. User initially thought click-through improved, then confirmed
the mouse/input lock **still occurs** below the popup. Therefore 2.4.0.11
does NOT pass the Zalo mouse-blocking acceptance requirement. Do not claim
otherwise or publish another speculative installer.

The prior patch makes only **Astur's own** cosmetic overlays click-through
and filters several toast HWND shapes from tiling adoption. It does not modify
a Zalo-owned or other app-owned input-catching overlay, or guarantee that a
different process controls popup placement.

## Live instrumentation availability

CodeLocal workstation `WIN-TJ713VSM6AJ`, session `rdp-tcp#27` ID 2, was
inspected. `tasklist`, `computer.list_windows` and Win32 read-only HWND
sampler showed **no active Astur.exe or Zalo.exe in the accessible session**.
This is not a valid reproduction of the user's screenshot, so exact popup
HWND, ownership, mouse capture and position remain unproven.

## Safe actual-session reproduction

1. Open the Windows interactive desktop **where Astur and Zalo are running**.
2. Double-click `scripts/run_zalo_click_probe.cmd` from this checkout, or run
   `python scripts/capture_zalo_click_blocker.py --seconds 45`.
3. While it samples, trigger one Zalo group notification and move the mouse
   across the area below it where clicks appear blocked. Do not click if the
   desktop feels stuck; cursor and HWND samples are enough initially.
4. Inspect/share ONLY the resulting `astur_zalo_mouse_*.jsonl` log from
   Desktop\Astur_Zalo_Mouse_Diagnostics (there are no message bodies,
   screenshots, titles, keystrokes or clicks in it).
5. Compare `hits[0].root_exe` and `root_rect` against `suspects` and
   `capture_state.ui_thread_capture` while the popup exists. Determine
   if the blocker is `Zalo.exe`, `Astur.exe`, a browser/shell process,
   or an entirely different overlay.
6. To isolate app attribution, repeat once with Astur exited **only after
   preserving the workspace context**. If lock survives, Astur is not the
   sole cause. Never forcibly set WS_EX_TRANSPARENT on Zalo's entire main
   window or hide/relocate arbitrary HWNDs.

## Release gates

- Windows Python probe `--self-test` and `--smoke`: PASS in CodeLocal session.
- `git diff --check`: PASS on diagnostic changes.
- New live sample with the bug reproduced: **MISSING**.
- Screen-level input behavior Zalo and NCPC after fix: **NOT VERIFIED**.
- Next fix must be scoped to the *identified blocking HWND and lifecycle*
  with regression tests, with a new prerelease version and rollback-safe
  installer only after fresh CI and an actual-session acceptance test.

No new Astur binary or installer is built by this diagnostic-only change.
