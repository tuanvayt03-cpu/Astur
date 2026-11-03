# Background Spawn Protection — 2026-11-03

Branch: `feat/background-window-protection`
Base: Astur VI Update 2.4.0.12 release branch, commit `a3fee38`.

## User requirement

A PowerShell/CMD/terminal/tool window created by an agent, scan or other
background process must not steal the current desktop, take a tile, move
existing windows, or interrupt a maximized/fullscreen user app merely because
the new HWND became visible. It should remain under normal Windows foreground
policy; when Windows refuses background activation its taskbar button may flash.
If the user deliberately selects that window later, Astur may then adopt/tile it
normally.

Do NOT solve this with a permanent powershell.exe/cmd.exe blacklist: a terminal
the user opens or selects must remain a normal Astur-managed application.

## Root causes in the prior default

1. `foreground_lock_disable=true` was the generated/default configuration.
   Astur therefore set Windows' system-wide ForegroundLockTimeout to zero while
   running, weakening the OS focus-stealing protection for every process.
2. `EVENT_OBJECT_SHOW` immediately queued `Cmd::Add` for any otherwise
   manageable top-level window even when it was not the Windows foreground.
   `Cmd::Add` inserts the window and retiles the monitor, so a short-lived
   background console can visibly move the user's existing layout.

## Implemented policy

- New config key `background_spawn_protection=true` by default.
- A newly shown, untracked background HWND is not queued to `Cmd::Add`.
  Astur does not tile/style/focus/hide/move it.
- The same handle is adopted normally when it later becomes the actual Windows
  foreground (taskbar click, Alt+Tab, direct user selection, or another genuine
  foreground transition).
- Deferred SHOW handles are not placed into the UNCLOAK retry path, preventing
  a background DWM uncloak from bypassing the protection.
- Tracked windows retain existing SHOW/follow semantics.
- A new foreground app shown while a retile has SUPPRESS set is still adopted;
  this preserves the prior 1-of-4 burst regression fix.
- While background protection is enabled, Astur never disables Windows'
  foreground-lock globally, even if an old config still contains
  `foreground_lock_disable=true`. This makes the update effective for existing
  installations without rewriting the user's config file.
- New/default configs set `foreground_lock_disable=false`. The old aggressive
  behavior remains available only by turning background protection off and
  explicitly enabling foreground-lock disable.

## Safety boundary

The implementation does NOT inspect command lines, process parents, window
titles, agent identity or application-specific executable names. It also does
not call ShowWindow/SetWindowPos/minimize on the deferred window. This avoids
misclassifying a manually opened PowerShell and avoids fighting a taskbar
restore SHOW/FOREGROUND ordering race.

## Acceptance matrix before release

1. One monitor, tiled desktop: background agent spawns PowerShell/CMD for a
   short scan then exits. Existing windows never resize or change focus.
2. Two monitors: same test while typing on either monitor; neither monitor
   retiles and `focused_mon` stays unchanged.
3. Maximized and borderless/fullscreen current app: background spawn does not
   detach/restore/change the current app.
4. User launches terminal using Astur Alt+Enter: normal foreground terminal is
   adopted and lands on the intended cursor monitor.
5. User launches/selects PowerShell from Start/taskbar/Alt+Tab: it becomes
   foreground, is adopted, and tiles normally.
6. App opens a legitimate background window without foregrounding it: it remains
   unmanaged until selected; no layout jump.
7. Existing managed app re-shows itself on its active/hidden workspace: tracked
   SHOW behavior and workspace-follow rules remain unchanged.
8. Re-run Zalo popup and NCPC native-titlebar/maximize regressions from 2.4.0.12.
9. Fresh Windows CI: fmt, clippy, workspace tests and release build.

## Limitation

This prevents Astur from disturbing the layout for background SHOWs and restores
Windows' normal foreground protection. A third-party process that explicitly
creates a TOPMOST overlay or is legitimately granted foreground rights can still
present its own UI. Such an application-level behavior needs its own evidence;
Astur should not blindly restyle or minimize foreign HWNDs.
