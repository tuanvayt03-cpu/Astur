# ASTUR | GUI CONTROL MANIFEST V2 | 2026-11-09

**Source baseline:** release `.19`, `crates/astur-settings/src/main.rs` blob `ad4f8567070dbd5d421991ea21d77ecf398e54ab`
**Source length:** 11842 lines
**Status:** `CONTROL-SURFACE INVENTORY COMPLETE ENOUGH FOR PARITY GATE / DESKTOP INTERACTION NOT VERIFIED`

A static scan found **209 page-local helper/direct control call sites** across the 14 page bodies. This number is not a user-visible control count because helpers expand into rows/tables and some calls are structural. The manifest below records the behavior surfaces a redesign must preserve.

## 1. Global Settings behavior

Must preserve:
- 14-page navigation and page search;
- EN/VI language selection;
- instant apply/hot reload behavior;
- Undo/Redo and Undo all;
- per-row reset-to-default;
- conditional groups and More options;
- safe external config read/reload behavior;
- temporary main-key trial with **Keep / Undo** and timed automatic rollback;
- validation messages and conflict notes;
- native app/file/folder/window pickers.

Reusable source helpers include:
`row_core`, `row_noted`, `row`, `toggle`, `text`, `num`, `pct`, `pick`, `seg_row`, `choice_row`, `path_row`, `table`, `ws_table`, `rule_ui`, `hotkey_ui`, `window_picker`, `more`, `when`, `reset_button`.

## 2. Page parity manifest

### P01 Home — `home` around L1224
Required surfaces:
- Review action.
- Theme.
- Layout.
- Status-bar style quick picker.
- Animations.
- Gap quick setup.
- main-key Change link.
- See every shortcut link.
- Quick switches.

### P02 Shortcuts — `shortcuts` around L1352
Required surfaces:
- fixed Windows/focus/window-management key rows;
- workspace key summary and Edit cross-link;
- terminal picker/command;
- browser picker/command;
- Extra hotkeys editable table;
- chord capture and conflict validation;
- scrolling-layout keys;
- Copy cheat sheet;
- main-key picker and 15-second rollback semantics.

### P03 Layout — `layout` around L1546
Required config/actions:
- layout picker;
- `master_ratio`;
- `outer_gap`;
- `inner_gap`;
- per-monitor `monitor_layouts`;
- scrolling `scroll_default_width`;
- `scroll_center`;
- `scroll_width_presets`;
- `scroll_height_presets`;
- Advanced `tab_bar_height`.

A V2 overlay preset must not silently overload `scroll_default_width` as the product meaning of 1/2/4/5.

### P04 Workspaces — `workspaces` around L1694
Required:
- shared vs per-monitor `workspace_mode`;
- editable workspace table;
- count, name, icon, key and wallpaper;
- add/remove behavior;
- wallpaper native picker;
- validation for workspace-targeted actions.

### P05 Windows & rules — `windows` around L1724
Required:
- `start_tiled`;
- `focus_follows_mouse`;
- `cursor_follows_focus`;
- `alt_tab_replacement`;
- `independent_fullscreen_popups`;
- App rules table;
- rule action and precedence;
- exe/class/title match fields;
- choose an actual open window;
- workspace/monitor routing;
- Advanced `async_window_pos`;
- `background_spawn_protection`;
- `foreground_lock_disable`.

The redesign must expose the **effective rule and reason** for a window; preserving a config key without a discoverable UI path is not parity.

### P06 Appearance — `appearance` around L1847
Required:
- theme;
- inactive-window opacity;
- DWM border enable;
- active/unfocused border colors;
- launcher/menu text size;
- popup radius;
- popup opacity;
- acrylic/blur;
- Advanced popup font weight and border width;
- popup/theme color roles.

### P07 Motion — `motion` around L2012
Required:
- preset/current-state presentation and Fix action;
- animations on/off;
- duration;
- workspace switch mode `off/slide/spring/fade`;
- window move mode `off/glide/spring`;
- easing/curve;
- safe behavior when animation is unavailable.

Motion must remain cosmetic; disabling or failing it cannot alter layout correctness.

### P08 Status bar — `bar` / `bar_body` around L2111/L2164
This is the largest parity surface.

Required top-level behavior:
- Astur bar / YASB / no bar;
- cross-link to Integrations;
- preset gallery with preview, nearest-preset/diff behavior, Apply and reset;
- palette;
- shape: strip/floating/islands/pills;
- floating margin;
- corner radius;
- island/pill padding;
- separator style;
- hover highlight;
- height;
- edge padding;
- text size;
- pill/widget colors;
- three-zone left/center/right editor;
- drag-and-drop widgets;
- click a widget chip to open its settings;
- stats icon/label mode;
- active workspace style;
- workspace label mode;
- workspace app icons;
- hide empty workspaces;
- per-widget left/right/middle click actions;
- monitor targeting;
- behavior switches;
- Advanced text weight, outline, widget gap and workspace mark width.

The source defines about 20 widget types, including workspace/app/title/layout/stat/media/time/disk/keyboard/uptime/custom/logo/separator/spacer families. Widget-specific settings and custom-command interval/format must remain accessible.

### P09 Launcher — `launcher` around L2542
Required:
- launcher enable;
- installed-app source;
- file source;
- file scope native folder picker;
- excluded folders;
- calculator source;
- web search source and provider;
- open-window source;
- clipboard history + history size + prefix;
- emoji + prefix;
- custom launcher entries table;
- entry target kind/value/icon and browse path;
- raw custom web search URL;
- monitor placement;
- max results;
- MRU boost;
- launcher size controls.

Do not confuse launcher calculator with Windows Calculator unmanaged policy.

### P10 Power menu — `power` around L2857
Required:
- system/power menu enable;
- built-in action checklist;
- custom actions table;
- target/action kind;
- icon;
- confirmation requirement;
- Advanced menu width.

Dangerous actions must preserve explicit confirmation semantics.

### P11 Desktop extras — `extras` around L2937
Required:
- Scratchpad enable;
- detected app picker;
- actual open-window/class picker;
- scratchpad command;
- scratchpad class;
- wallpaper folder;
- workspace/launcher-history persistence.

### P12 Integrations — `integrations` around L3010
Required:
- YASB enable;
- port value;
- Copy address;
- Copy widget YAML;
- Copy example CSS;
- Status bar cross-link;
- IPC enable;
- named-pipe name;
- IPC launch permission.

Security-sensitive `ipc_allow_launch` must not be hidden behind an implicit migration.

### P13 Troubleshooting — `troubleshooting` around L3113
Required:
- parser/problem list;
- Remove line;
- suggested-fix action;
- Open in editor;
- Open folder;
- Reload from disk;
- log level;
- Open log;
- config diagnostics without silently rewriting unreadable files.

### P14 About — `about` around L3249
Required:
- product/version information;
- project links;
- V2 addition: exact source commit/build ID and package provenance.

The provenance addition is a V2 requirement because the current live binary could not be source-mapped reliably.

## 3. Non-page surfaces that remain part of parity

- launcher runtime UI;
- tray Settings/Quit;
- power/system menu;
- status bar click actions and workspace/app buttons;
- tab-bar interactions in scrolling/manual-tab mode;
- native file/folder picker;
- open-window picker;
- temporary main-key confirmation UI;
- Undo/Redo toasts/status;
- validation and troubleshooting surfaces;
- EN/VI rendering and search aliases.

## 4. Persistence and safety parity

Every migrated control must record:
- source page and source symbol;
- config key/backend action;
- default;
- visibility predicate;
- enable predicate;
- validation;
- persistence file;
- hot-reload behavior;
- reset behavior;
- Undo/Redo behavior;
- keyboard path;
- mouse/drag path;
- test;
- V2 destination;
- desktop E2E state.

A new menu structure is **not parity-complete** until every old control/action has one explicit destination or an approved removal decision.

## 5. Existing source-level QA worth preserving

The Settings source includes checks such as:
- every page draw is a no-op unless edited;
- every GUI-written key has a row;
- motion preset mapping;
- hidden workspace behavior;
- EN/VI page render tests;
- picked windows fill rule/scratchpad fields;
- status-bar row width checks.

These are useful regression gates but they do not prove click/drag behavior on a real desktop.

## 6. Candidate information architectures

No winner is selected here.

### Candidate A — current 14 pages, improved
Lowest migration risk. Simplify labels, cross-link common tasks, add V2 mode preview and effective-policy inspection.

### Candidate B — grouped navigation + Advanced
Fewer top-level entries, but requires a strict parity map so Status Bar, Launcher, Power, Extras and Integrations do not disappear into a generic bucket.

### Candidate C — task-oriented
Top-level tasks such as Arrange windows, Control apps, Shortcuts, Bar/appearance, Tools, Diagnostics; full search and Advanced preserve direct access.

Approval should choose using the same core journeys, not aesthetics alone.
