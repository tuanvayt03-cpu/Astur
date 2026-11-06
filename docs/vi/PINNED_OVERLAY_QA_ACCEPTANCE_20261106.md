# Astur pinned fullscreen + foreground slots | desktop acceptance

Status: **NOT ACCEPTED** until a real desktop capture and events confirm every mandatory case below. This file is a repeatable checklist, not a claim of passing live tests.

## Preconditions / safety

- Use disposable applications (e.g. Notepad, Explorer, test browser windows); no trading terminals, SignalOps, Chatwoot sessions, private messages, accounts or production work.
- Run only **one** Astur instance. Do not start this QA executable alongside the installed Astur window manager. Take a rollback copy of the currently installed version and settings first.
- Check one monitor first, then two monitors, including a monitor with negative X coordinates where available.
- Use a **separate QA desktop/session**. If active MT5/SignalOps windows or other critical apps are present, **do not run the QA binary or manipulate those windows**.
- Artifact is experimental, never an installer or automatic upgrade. GitHub CI success checks Rust functionality, **not** user-desktop behavior.

## Mandatory real-desktop acceptance matrix

| ID | Action / setup | Expected outcome |
| --- | --- | --- |
| A01 | Scrolling layout, CS1 managed column full width; open CS2 | CS1 remains full-width underneath; CS2 occupies right foreground half |
| A02 | With CS2 focused, open CS3 | CS3 fills left free half, CS2 stays right, CS1 remains untouched |
| A03 | With CS3 focused, open CS4 | CS4 reuses the *other* nonfocused slot; CS3 stays visible; CS2 remains recoverable |
| A04 | Click CS2 on taskbar once; focus back to CS4; close CS4 | Click restores CS2 in its reserved slot; closing active stacked occupant restores prior occupant |
| A05 | Minimize / restore / close CS1 | Foreground slots remain stable on minimize; managed overlay dissolves safely on background close |
| A06 | Start a separate independent Windows-native maximized CS1, then open foreground apps | No resize, parking, or Astur positioning of native background; foreground slots overlay correctly |
| A07 | Restore or close native maximized background | External overlay dissolves, windows remain owned by ordinary tiling |
| A08 | Drag managed CS1 into CS2 via standard title bar and Alt+left drag | Direct managed background/foreground swap; no snap-back to CS1 |
| A09 | Drag a custom-title-bar application between CS1 / CS2, including reverse direction | Recognized native move or Alt+drag fallback; correct physical target, not old strip index |
| A10 | Fill 1/4 and 1/5 overlay slots, open one additional window | Fill genuinely vacant slots first; otherwise replace other N-1 slot, preserve focus |
| A11 | Two monitors: cross-monitor drag into occupied physical slot (also negative X) | Atomic exchange, no duplicate HWND, no transient destination CS1 insertion |
| A12 | Minimize/close/reopen a foreground app, switch workspaces, then taskbar-recover Telegram test window | No lost window, no phantom slot, no scroll jump; one click recovers selected app |
| A13 | Zalo-style test popup/dialog and custom control | Mouse click and text input work; no overlay steals clicks, no permanent TOPMOST window |
| A14 | Exit test binary, restore previous Astur/settings and reopen disposable apps | Previous release launches normally; no orphaned offscreen windows or duplicate manager processes |

## Evidence and acceptance record

For each ID record: **PASS / FAIL / NOT RUN**, app class (not user data), monitor geometry, timestamp, exact binary SHA256, session isolation, test action, actual outcome, and screenshot or WinEvent HWND/RECT evidence with private content excluded. Video/screenshots remain private and outside GitHub. Fix any FAIL on the same branch; rerun fresh Windows CI after final change, then repeat affected desktop cases.

Only after A01–A14 are PASS can the branch advance to merge and a new installer. Before publishing: build separate installer + portable package, confirm both SHA256 values, smoke install/uninstall in disposable directory, verify backup/rollback and that released `2.4.0.17` assets stay available. Never silently replace an installed Astur.
