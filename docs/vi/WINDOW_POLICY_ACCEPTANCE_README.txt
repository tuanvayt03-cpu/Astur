ASTUR WINDOW POLICY ENGINE V1 - PORTABLE ACCEPTANCE BUILD

This is a portable preview for live desktop acceptance. It does not install or
overwrite the current Astur installation.

SOURCE
- Branch: feat/window-policy-engine-v1-20261104
- Exact commit and CI run are in target/release/WINDOW_POLICY_BUILD_INFO.txt.

SAFE TEST
1. Back up %USERPROFILE%\.astur if it contains important custom configuration.
2. Quit the currently installed Astur from its tray icon.
3. Extract this ZIP to a new folder.
4. Run target\release\astur.exe from that extracted folder.
5. Run the acceptance cases below.
6. Quit the portable Astur, then start the installed Astur again.

ACCEPTANCE CASES
- Agent/tool starts PowerShell or CMD in the background:
  it must not steal a tile, focus, or reflow the active desktop.
- Select that terminal yourself from taskbar/Alt+Tab:
  a normal terminal may then be adopted/managed normally.
- WinRAR main window:
  should still behave as a primary app.
- WinRAR extraction/progress/dialog:
  must remain free/modal/background and must not consume half the screen.
- Astur Settings and Windows Settings:
  should remain floating/free rather than taking a tile.
- Chrome and Explorer main windows:
  should still tile normally, including when manually resized small.
- Open/Save/confirmation dialogs:
  should stay with their owner and must not reflow the layout.
- Re-test Zalo notification, native maximize/F11 and title-bar cross-monitor drag.

IMPORTANT
A third-party app that Windows legitimately grants foreground may still appear
in front. This build does not blindly minimize, hide, restyle, or make foreign
windows click-through. The goal is to stop Astur itself from adopting the wrong
surface and reshuffling the desktop.
