# Astur VI — Behavioral Contract & QA Matrix

State: CONTRACT (not yet verified); source baseline Page011/Astur b60500f.

## Non-negotiable invariants
C01 Native tiling, mouse/keyboard hooks, workspace switching, focus, Alt-drag, fullscreen and recovery must behave as upstream before and after locale changes.
C02 No translated text affects machine action IDs, configs, Win32 class/exe matching, window labels, user content or keyboard shortcuts.
C03 Locale en or vi, persisted across Settings restart. Invalid/missing key resolves to English safely, never raw placeholder or panic.
C04 EN/VI key and interpolation argument sets are identical. All owned strings are categorized as translated or documented externally owned.
C05 Every Vietnamese glyph renders without blank squares or clipping in Settings, tray, status, launcher, dialogs, warning and help, checked light/dark and 100/125/150/200% DPI.
C06 Existing astur.conf/navbar.conf settings (layout, shortcut, float/ignore rules, status bar, backups) remain byte/semantically unchanged by a locale-only operation, barring explicit dedicated locale field.
C07 A genuine Telegram/Zalo main window remains tiled by default. A transient toast never steals a grid slot, never becomes a 'tabbed column' application, never hijacks focus and retains normal notification behavior.
C08 Standard Windows notifications, Snipping Tool overlay/snips and toast bursts remain usable. If two transients are of different ownership/class, verify independently; no blanket suppression by exe.
C09 On popup exit/dismiss, no ghost tile/tab, empty workspace gap, orphaned window or stuck input hook.
C10 OS/untranslated dynamic content (window titles, user messages) is preserved exactly; UI-only labels translated.
C11 Fresh Windows GitHub Actions passes fmt, clippy, workspace tests and release workspace build; runtime proof recorded separately.
C12 Binary/installer release carries LICENSE and notices, distinct artifact identity, rollback guidance and tested clean install. No modification of active current installation during implementation.

## Regression matrix
| Area | Setup | Expected | Evidence |
| --- | --- | --- | --- |
| Locale | en→vi→en, restart | all visible owned UI responds, saved preference | tests + screenshots |
| Key inventory | catalogs compared | no absent/extra/unbound placeholders | unit tests |
| Search | Vietnamese query, English query, config key | finds same settings | automated test |
| Notifications | Telegram popup alongside tiled Telegram window | popup excluded, app still tileable | HWND trace + screen capture |
| Notifications | Zalo popup alongside tiled Zalo window | popup excluded, app still tileable | HWND trace + screen capture |
| System | Windows Toasts/Notification Center | overlays normal, no tab entry | OS capture |
| Capture | Win+Shift+S, Snipping Tool UI/toast | capture works and no tab | OS capture |
| Layout | 2/4/6 windows, grid/master/scrolling/columns | stable geometry and no phantom tile | OS capture |
| Scope | other app main windows | still tiled; dialog behavior unchanged | OS capture |
| Stress | 10+ successive notifications across workspaces | no focus steal, crash, ghost tile | OS capture + logs |
| Exit | close popup and quit Astur | no stranded/hidden windows | OS capture |
| Build | fresh final commit | fmt/clippy/test/release build green | CI links/exit codes |

## Evidence protocol
A screenshot alone is not evidence of Win32 class identity. Collect HWND+PID+exe+class+styles/owner and a minimal reproduction first. All regression PASS markers must be supported by fresh post-change machine/CI evidence. Unrun checks marked UNVERIFIED, never PASS.

## Handoff template
Branch and commit; upstream baseline; state of notification root cause; files changed; user work untouched; test commands/results + CI URL + images; known defects; exact next actions; push/release state; rollback.
