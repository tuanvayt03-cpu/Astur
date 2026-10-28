# Astur VI — Software Design Document

State: DESIGN PROPOSAL · Source of truth for implementation: .omx/plans/2026-10-28-astur-vietnamese-and-notification-fix.md · Last grounded: 2026-10-28.

## Architecture
- Upstream baseline: Page011/Astur main b60500f (2.4.0). Fork: tuanvayt03-cpu/Astur.
- Retain crates/astur, crates/astur-config, crates/astur-settings boundaries. Do not translate raw IPC keys, shortcuts, persisted value names, exe/class/window titles or user content.
- Candidate: shared pure-Rust localization crate (or small module) with canonical English message IDs, Vietnamese catalog, interpolation, fallback to English, compile/test validation of key inventory and placeholder compatibility. Choose resources such as Fluent/FTL or static Rust maps only after measuring runtime and dependency cost; do not assume JSON runtime parsing.
- Locale preference: independent of window rules and appearance settings, stored atomically in user config (prefer a small locale preference/config key with backwards-compatible default en); no locale-related write to astur.conf/navbar.conf unless intentional, reversible and tested. Switching language never changes managed-window ownership.
- Settings (egui): add language chooser; translate all 14 pages, home/quick-setup, search, help, tooltips, validation, table editor, undo/redo, and system messages. Support Vietnamese glyph fallback and dynamic-length labels, with Ctrl+F matching VI labels, EN labels and stable config keys.
- Native manager: translate first-party launcher, status bar widget names/tooltips, power menu, tray text and confirm prompts. Keep dynamically generated user/system values untouched. Resolve visible translated strings in UI/update paths only, never in global keyboard/mouse hooks.
- Installer: separate identity for fork release, preserve Apache-2.0 and THIRD_PARTY_NOTICES; no silent overwrite or auto-run of active Astur.

## Notification popup defect — diagnosis-first
Observed user symptom: transient notifications/popups from Zalo, Telegram and screenshot workflows appear combined into a tab/managed tile instead of independently overlaying the desktop. Root cause is not yet proven; not every toast is the same Windows surface class.

Relevant upstream filter: crates/astur/src/main.rs lines 4994-5035 defines BLOCK_CLASSES; 5042-5150 filters app surfaces by PID/visibility/ROOT/style/tool/noactivate/DWM cloak/blocked class, then checks GW_OWNER and title, integrity, user ignore_classes and rules. These gates may misclassify third-party transients if they use ordinary-looking root titled windows. Existing source warning explicitly says broad class exclusions caused apps to become unmanageable; do not repeat.

Proposed minimal discriminating predicate, implementation deferred until evidence:
1. Observe window-creation/show and target tab grouping events. Capture exe, process, HWND/class, style/exstyle, owner, title, rect/size, event lifetime and UI role; compare against genuine main window of same app.
2. Reproduce with standard Windows toasts, Telegram/Zalo notifications, Win+Shift+S / Snipping Tool screenshot overlay and at least one arbitrary real child/dialog window.
3. Add failing non-GUI predicate tests with fixtures and, if possible, deterministic harness exercising actual event pipeline before code.
4. Exclude *only* confirmed notification/overlay HWNDs early in adoption; preserve normal main-window tiling and minimize fullscreen/bar impact. Prefer behavioral style/ownership rules and narrowly scoped confirmed app-specific class signature only where necessary; no title-only language-specific heuristic.
5. Test lifecycle: create/update/dismiss, focus changes, multiple monitors, DPI, screen capture, fullscreen, rapid toast burst, app restart and normal quit; no lost notification, auto focus steal or orphaned window.

## Source responsibilities and constraints
- Primary writer integrates shared files and all changes; workers may review isolated surfaces only.
- Document visual changes in upstream plan/ files as per CLAUDE.md.
- Prefer Rust unit tests for pure translators and window metadata classification, and fresh Windows build and manual proof on real Desktop.
- Do not run test window manager over user's current live Astur without safe isolation and recovery plan.

## Decision log
2026-10-28: Separate fork and bilingual switch, not wholesale rewriting English literals. Keep English fallback. Diagnose notification behavior before introducing exclusions. Keep original Astur installed and untouched until release QA.
