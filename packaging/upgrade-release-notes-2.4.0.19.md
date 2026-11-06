# Astur VI Update 2.4.0.19 (Preview) | Calculator and Windows utilities no longer fullscreen

**Experimental unsigned Windows x64 in-place update**, based on 2.4.0.18. Keeps previous fullscreen-background CS1 and CS2/CS3/CS4 overlays.

## Fixed
- Windows **Calculator** is no longer treated as a tiled fullscreen window when opened under Astur. The native Windows window stays freely sized and movable. Covers modern `Calculator.exe`, `CalculatorApp.exe`, `calc.exe` names, plus legacy Calculator UWP application-frame identity.
- Similar small **utilities are not tiled by default**: Snipping Tool, Character Map, Task Manager, Magnifier, On-Screen Keyboard, Sticky Notes, Clock/Alarms, Sound Recorder, Windows version/cleanup/configuration/diagnostic tools.
- Uses **unmanaged `Ignore`** rather than managed `Float` for these built-ins. Astur does not resize, reposition, style or allocate a CS slot to them. User-defined `window_rules` can explicitly opt a particular tool back into managed `tile` or `float` behavior.
- Main apps (Chrome, Explorer, Notepad, Paint, Telegram, MT5, Windows Terminal) keep their ordinary configurable tiling behavior.
- Narrow exact executable matching and UWP Calculator host/class/title matching avoid a blanket exclusion for WinUI apps or small resizable windows.

## Installation and rollback
- Quit Astur before running the installer. **Never run two window managers.** Prefer an isolated test session without active trading windows.
- Installer uses the same original Astur AppId and install directory. Existing user configuration is preserved.
- Current installed binaries and available configuration are backed up under `%LOCALAPPDATA%\Astur\UpgradeBackup\before-vi-update-2.4.0.19`. Previous first-original backup remains intact. The prior [2.4.0.18 update](https://github.com/tuanvayt03-cpu/Astur/releases/tag/astur-vi-update-2.4.0.18) stays available.
- Verify the release SHA256 manifest. This executable is **unsigned**; do not bypass Windows security warnings for an untrusted binary.

## Verification limits
- Windows CI gates: Rustfmt, Clippy with `-D warnings`, tests, bilingual Settings renders, x64 build, in-place upgrade/backup/uninstall smoke and SHA256.
- Live Calculator / Snipping Tool / Task Manager test on the user's one-/two-monitor desktop remains **PENDING**. Passing CI is not a claim of real desktop acceptance.
- Implementation and acceptance: [Small utilities policy](https://github.com/tuanvayt03-cpu/Astur/blob/fix/astur-small-utilities-unmanaged-20261106/docs/vi/SMALL_UTILITIES_NATIVE_UNMANAGED_20261106.md); source review [PR #14](https://github.com/tuanvayt03-cpu/Astur/pull/14).
