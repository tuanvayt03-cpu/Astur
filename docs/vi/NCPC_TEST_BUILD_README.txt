ASTUR / NCPC — ZALO POPUP & MOUSE INPUT TEST BUILD
=================================================

THIS IS A PORTABLE TEST BUILD, NOT AN INSTALLER OR A STABLE RELEASE.
Built by GitHub Windows CI from the exact commit recorded in
NCPC_BUILD_INFO.txt. It does not automatically replace Astur on the PC.

Safe test procedure on the PC that exhibits the problem:
  1. Save a copy of %USERPROFILE%\.astur (config and backup state) before testing.
  2. Quit the currently running Astur from its system tray. Do not force kill
     the window manager unless normal Quit fails and you know how to recover.
  3. Extract the GitHub Actions ZIP into a NEW EMPTY folder. Run astur.exe
     from that folder. If Windows reports an existing Astur instance, stop:
     do not launch two window managers simultaneously.
  4. Trigger several real Zalo notifications on each monitor; verify no
     layout jump, no entire-screen flash, no underlying-click blockage.
     Verify normal Zalo chat can still be tiled; test NCPC drag-to-maximize.
  5. Quit this test Astur using its tray menu and relaunch the PREVIOUS
     installed Astur through its normal Start Menu shortcut.

This test build adds a narrow ignore rule for Zalo.exe / ZaloPC.exe window
surfaces that are TOPMOST, have no APPWINDOW, and have no caption, system
menu or thickframe. The matching second Zalo HWND captured in the user logs
was 960x1040 pixels; normal Zalo chat uses APPWINDOW and window chrome.
The code never changes Zalo's actual HWND style, z-order, hit testing or focus.

IMPORTANT LIMITATION: Original logs prove that Zalo itself had transient
mouse capture and that WindowFromPoint hit the oversized Zalo HWND during
31/37 popup samples. Astur ignoring that HWND cannot by itself force
Zalo's native input layer to become click-through. If click blocking remains,
reproduce once with the previous Astur exited and Zalo still running, so
the cause can be attributed without blindly mutating another process.

Do not install this over the active Astur binary. Do not delete any config.
No secrets, content of messages or screenshots are required for the test.
See docs/vi/NCPC_ZALO_HWND_EVIDENCE_2026-11-03.md for engineering detail.
