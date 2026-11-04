# Window Policy Engine v1 — 2026-11-04

Baseline: Astur VI Update 2.4.0.13 (`baee7b6`).

## Objective

Stop treating every newly visible top-level window as a full tiling participant.
Primary work windows should tile; utility/progress/settings surfaces should stay
free; background agent/tool windows should not disturb the active desktop; owned
modal windows should remain with their application; hard shell/overlay surfaces
remain outside Astur.

## Policy model

The manager classifies a candidate into exactly one of:

- `Tile` — normal primary work window; insert into the active workspace layout.
- `Float` — managed but free-sized/free-positioned; does not consume a tile.
- `Background` — leave to Windows; no Astur registry/focus/layout mutation.
- `Modal` — owned application surface; leave placement/focus relationship to
  Windows/the owner instead of consuming a tile.
- `Ignore` — shell/toast/elevated/native-independent or explicit hard opt-out.

The decision also carries a reason and confidence for debug logging.

## Inputs and precedence

1. Hard surface/security/native/notification exclusions.
2. Legacy ignore class.
3. Explicit app rule: auto/tile/float/background/ignore.
4. Owned top-level window -> modal.
5. Untitled surface -> ignore.
6. Background-spawn protection -> background when the window is not foreground.
7. Legacy float class / built-in settings utility.
8. Generic utility shape -> float.
9. Otherwise -> tile.

Explicit app rules can override automatic utility/modal heuristics, but cannot
override hard shell/security/native safety exclusions.

## Utility heuristic

The classifier never floats a window merely because it is small. A window is a
utility candidate when it is a standard dialog class/modal frame, or when it is
both compact and fixed-size with normal caption/system-menu chrome. A small
resizable Chrome/Explorer/main app window therefore remains tileable.

Built-in utility defaults include `astur-settings.exe` and
`SystemSettings.exe`.

## User intent

A real foreground transition or Astur-launched app is treated as foreground
intent. A SHOW/UNCLOAK candidate that is still background remains protected.
When the user later selects a normal background window through taskbar/Alt+Tab,
its foreground event can adopt it normally.

No PowerShell/CMD executable blacklist is used.

## Performance boundary

The global WinEvent hook keeps the cheap background SHOW prefilter from 2.4.0.13.
Full policy collection (class, rule, integrity, geometry) runs on the manager
thread. No new heavy work is added to the mouse/keyboard hooks.

## Configuration

`window_rules` accepts:

`auto | tile | float | background | ignore`

Old tile/float/ignore rules remain valid. New Settings rows default to `auto`.

## Acceptance matrix

- Agent/CLI PowerShell or CMD scan: no focus/layout change.
- User-selected terminal: normal adoption/tiling.
- WinRAR main: tile.
- WinRAR extraction/progress dialog: float/modal/background, never tile.
- Astur Settings and Windows Settings: float.
- Chrome/Explorer main: tile, even when manually resized small.
- File Open/Save dialog: modal/free, no layout reflow.
- Existing Zalo notification host: ignore.
- Native maximize/F11: independent behavior unchanged.
- One and two monitors: no unrelated focused-monitor movement.
- Startup adoption and post-start window adoption use the same policy.
- Old app rules parse and behave unchanged.

Release remains Preview until live Windows acceptance.
