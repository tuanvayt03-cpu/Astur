# Astur small-utility native-window policy | 2026-11-06

## User-visible problem

With Astur fullscreen/scrolling overlay active, opening Windows Calculator can
create a full CS tile. The existing built-in utility list only floated
Astur Settings and Windows Settings; Windows Calculator is often *resizable*
and therefore bypasses the compact fixed-size heuristic. The safe fix is a
**narrow executable-based policy**, not a global "small windows ignore" rule
that would break resized Chrome, Explorer, Telegram or MT5 windows.

## Behavior

- The listed auxiliary utilities are **Ignore**, not **Float**, by default:
  their window sizing, position, z-order and activation remain with Windows.
  Astur does not create a CS slot, append them to its registry, apply Astur
  focus styling, or resize/park them.
- Calculator executable identities: `calc.exe`, `Calculator.exe`,
  `CalculatorApp.exe`, `WindowsCalculator.exe`. Windows 10 UWP
  `ApplicationFrameHost.exe` Calculator frames get an exact host/class/title
  fallback (English and Vietnamese). Other UWP app frames remain tileable.
- Screenshot: `SnippingTool.exe`, `ScreenSketch.exe`,
  `ScreenClippingHost.exe`.
- System mini-tools: `charmap.exe`, `Magnify.exe`, `osk.exe`,
  `taskmgr.exe`, `winver.exe`, `cleanmgr.exe`, `msconfig.exe`,
  `dxdiag.exe`.
- Notes / Clock / Sound Recorder: `StikyNot.exe`, `StickyNotes.exe`,
  `Microsoft.Notes.exe`, `WindowsAlarms.exe`, `Time.exe`,
  `SoundRecorder.exe`, `VoiceRecorder.exe`.
- Astur Settings and Windows Settings retain prior managed-Float defaults;
  owned dialogs, toasts, shell and native fullscreen continue their separate
  structural safeguards.
- User-defined `window_rules` with exact executable/class/title matches
  still win over these built-in small-utility defaults. To force Calculator to
  float-managed or tile, set the relevant app rule to `float` or `tile`.
  Auto returns to native unmanaged behavior.

## Regression and acceptance

The Rust regression covers case-insensitive/exact basename detection,
modern and UWP-host Calculator, nonutility negative controls (Chrome,
Explorer, Notepad, Paint, Telegram, MT5, Terminal), startup/foreground
launch paths, override precedence and modal precedence.

Live A/B acceptance in a disposable Windows desktop remains required:
1. Launch Calculator into a scrolling or pinned-fullscreen CS1 workspace;
   it should appear at its own compact size, **not full screen**, without
   moving or replacing any CS occupant.
2. Drag/resize Calculator, switch taskbar focus, close/reopen; no snapback,
   implicit adoption, lost focus or altered CS slot.
3. Repeat for Snipping Tool, Character Map, Task Manager, Sticky Notes,
   Magnifier/On-screen Keyboard where installed.
4. Launch/rescale Notepad, Chrome, Explorer and Telegram; their configured
   regular tiling behavior must remain intact.
5. Verify a user rule `tile|Calculator.exe||||` intentionally overrides the
   default, and `auto` reverts to native unmanaged.
6. Test on one and two monitors (also negative-X secondary monitor).
7. Never test a new WM over active MT5/SignalOps sessions.

**Scope:** source policy and tests. No automatic installation, no live
desktop acceptance claim, no previous release rewrite.
