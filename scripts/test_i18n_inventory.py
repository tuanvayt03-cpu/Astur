#!/usr/bin/env python3
"""Deterministic coverage gate for first-party Vietnamese UI strings.

This is a source inventory and rendering-boundary check, not proof that every
pixel is translated. User data, machine identifiers and shortcut tokens are
explicitly outside the catalog by contract.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
GUI = (ROOT / "crates/astur-settings/src/main.rs").read_text("utf-8")
WM = (ROOT / "crates/astur/src/main.rs").read_text("utf-8")
CONFIG = (ROOT / "crates/astur-config/src/lib.rs").read_text("utf-8")
LOCALE = (ROOT / "crates/astur-config/src/i18n.rs").read_text("utf-8")


def norm(value: str) -> str:
    return re.sub(
        r"\\u\{([0-9a-fA-F]+)\}",
        lambda match: chr(int(match.group(1), 16)),
        value,
    )


entries = re.findall(r'(?ms)^\s*"((?:[^"\\]|\\.)*)"\s*=>\s*"((?:[^"\\]|\\.)*)"', LOCALE)
keys = {norm(english) for english, _ in entries}
assert len(keys) == len(entries), "Duplicate translation keys generate unreachable Rust arms"

placeholder = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")
for english, vietnamese in entries:
    assert sorted(placeholder.findall(english)) == sorted(placeholder.findall(vietnamese)), english


def literals(pattern: str, text: str) -> set[str]:
    return {norm(value) for value in re.findall(pattern, text, flags=re.S)}


static_tr = literals(r'\btr\(\s*"((?:[^"\\]|\\.)*)"\s*\)', GUI + "\n" + WM)
static_tr_missing = sorted(static_tr - keys)
trf_literals = literals(r'\btrf\(\s*"((?:[^"\\]|\\.)*)"', GUI + "\n" + WM + "\n" + CONFIG)
trf_missing = sorted(trf_literals - keys)

# These helpers are render boundaries: their literal arguments are owned UI,
# while the values in the fields remain user data or stable config values.
settings_source = GUI.rsplit("\n#[cfg(test)]\nmod tests {", 1)[0]
assert "fn home(&mut self" in settings_source and "fn row_noted(" in settings_source, "Settings source scan truncated before UI helpers"
sections = literals(r'\bsection\(\s*ui\s*,\s*f\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)', settings_source)
notes = literals(r'\b(?:note|warn_note)\(\s*ui\s*,\s*"((?:[^"\\]|\\.)*)"\s*\)', settings_source)
meta = re.findall(
    r'(?s)\(\s*"((?:[^"\\]|\\.)*)"\s*,\s*"((?:[^"\\]|\\.)*)"\s*,\s*"([a-z][a-z0-9_, ]*)"\s*,?\s*\)',
    settings_source,
)
meta_labels = {norm(label) for label, _, _ in meta}
meta_descriptions = {norm(description) for _, description, _ in meta if description}

tips = {
    "Move a window: hold the key and drag anywhere on it",
    "Resize a window from its nearest corner",
    "Go to a workspace (add Shift to take the window along)",
    "Focus the next or the previous window",
    "Focus the window in that direction (add Shift to move it)",
    "Find and open apps, files and more",
    "Open your terminal",
    "Float the window, or tile it again",
    "Close the window",
    "Lock, sleep, restart, and Astur's own menu",
}

owned_dynamic = {
    "Tile windows when Astur starts",
    "Space between windows",
    "Hold {key}, the Astur key, for every shortcut below.",
    "Off: Astur starts with tiling off, so every window floats as on plain Windows until you press {key}{toggle}. Takes effect the next time Astur starts.",
    "App launcher ({key}Space)",
    "New Astur key: {new}. Keep it? Going back to {old} in {seconds} s.",
    "Not saved: {error}",
    "Couldn't write {path}: {error}",
    "Couldn't save display language: {error}",
    "Saved, but Astur reads a different value for {keys}: another line sets it again (later in the file, or in the other file), or the value is not valid.",
    "Read-only: {error}",
    "Read-only: {error}. Showing built-in defaults and writing nothing, so the file stays as it is. Save it as UTF-8 (or close the program holding it), then press Retry.",
    "{count} config line{s} not understood, so {verb} nothing",
    "No settings match {query}.",
    "{held} + a workspace's key switches to it; with Shift it takes the active window there. Set them in the Workspaces table.",
    "What {key}Enter runs, typed out: for an app with options, e.g. wt -p Ubuntu. Put a path with spaces in quotes when options follow it.",
    "What {key}Shift+Enter runs. Empty: the system default browser.",
    "Monitor {n}",
    "Column widths ({width})",
    "The widths {width} steps through, as a share of the screen.",
    "Window heights ({height})",
    "The heights {height} steps through, for a window sharing a column.",
    "The tab strip of a tabbed column ({tab}).",
    "An app (a terminal by default) that drops down over everything with {key} and hides again with the same key. Change the key under Shortcuts > Extra hotkeys.",
    "Not added: {path} has a , or ; and this list is split at those. Type the end of its path instead, e.g. {tail}",
    "Window class: {class}",
    "No key: Astur keeps {key}",
    "The app's file name, or its full path. {wild} app.",
    "Any {what}",
    "{action} (default)",
    "Workspace {n} doesn't exist (you have {ws}), so this does nothing.",
    "Custom: {value}",
    "Astur can't read {chord}: set its key again",
    "{chord} has no Astur key, Alt or Win, so it does nothing. Set its key again to add the Astur key.",
    "Astur has no action {action}",
    "No {what}: the {what}s after it would move up a workspace (the file can't skip one). Set one, or clear the later ones.",
    "{value} is not a key Astur can use here",
    "A {what} can't contain , or ;",
}

format_labels = {
    "24-hour",
    "12-hour",
    "24-hour with seconds",
    "12-hour with seconds",
    "Window title",
    "App name",
    "App and window title",
    "language",
    "language and country",
    "country",
    "Every second",
    "Every 5 seconds",
    "Every 10 seconds",
    "Every 30 seconds",
    "Every minute",
    "Every 5 minutes",
    "Every 15 minutes",
    "Every hour",
}

# Audit dynamic labels actually shown in offscreen screenshots. These boundaries
# used to escape the old prefix scan, despite appearing in native controls.
bar_presets = re.findall(
    r'(?s)\blabel:\s*"([^"]+)"\s*,\s*blurb:\s*"([^"]+)"', CONFIG
)
layout_region = GUI.split("fn layout_label(", 1)[1].split("/// Themeable", 1)[0]
layout_text = literals(r'=>\s*(?:\{\s*)?"((?:[^"\\]|\\.)*)"', layout_region)
desc_region = CONFIG.split("pub fn description(self)", 1)[1].split("pub fn bits(self)", 1)[0]
key_descriptions = literals(
    r'MainKey::\w+\s*=>\s*\{\s*"((?:[^"\\]|\\.)*)"', desc_region
)
assert len(bar_presets) >= 9 and len(layout_text) >= 12 and len(key_descriptions) == 5

missing = {
    "static_tr": sorted(static_tr_missing),
    "trf_literals": sorted(trf_missing),
    "sections": sorted(sections - keys),
    "notes": sorted(notes - keys),
    "metadata_labels": sorted(meta_labels - keys),
    "metadata_descriptions": sorted(meta_descriptions - keys),
    "tips": sorted(tips - keys),
    "dynamic_templates": sorted(owned_dynamic - keys),
    "format_labels": sorted(format_labels - keys),
    "bar_preset_labels": sorted({name for name, _ in bar_presets} - keys),
    "bar_preset_descriptions": sorted({desc for _, desc in bar_presets} - keys),
    "layout_labels_and_help": sorted(layout_text - keys),
    "main_key_descriptions": sorted(key_descriptions - keys),
}

nav_region = settings_source.split("const NAV:", 1)[1].split("const ICON_UNDO", 1)[0]
nav_items = set(re.findall(r'Page::\w+,\s*"([^"]+)"', nav_region, flags=re.S))
nav_groups = set(re.findall(r'\(Page::\w+,\s*"[^"]+",\s*[^,]+,\s*"([^"]*)"', nav_region))
navigation = nav_items | (nav_groups - {""}) | {"Astur Settings", "Language", "Find a setting  (Ctrl+F)"}

for name, values in missing.items():
    print(f"{name}: missing {len(values)}; {values}")

assert not any(missing.values()), "owned first-party strings are absent from the catalog"
assert len(nav_items) == 14, f"expected 14 Settings pages, found {len(nav_items)}"
assert not (navigation - keys), sorted(navigation - keys)

render_boundary_guards = {
    "settings runtime localization": "fn localize_runtime(text: &str) -> String",
    "settings runtime saved-value localization": 'Saved, but Astur reads a different value for {keys}',
    "settings runtime preset localization": 'Preset not applied: couldn\'t back up navbar.conf: {error}',
    "settings runtime toast localization": 'Files changed outside Settings; Undo restarted',
    "settings motion warning localization": 'tr("An old setting (workspace_slide = false) turns workspace animation off.")',
    "dynamic settings interpolation": 'trf(\n                        "Hold {key}, the Astur key, for every shortcut below."',
    "native launcher prompt": 'tr("Search apps, files and commands…")',
    "native launcher web row": 'trf(\n                        "Search the web for {query}"',
    "native power built-ins": 'sys_action(tr("Lock")',
    "native status layout": 'format!("[{}]", tr(label))',
    "locale-aware date formatter": 'if i18n::language() == "vi"',
    "date locale regression": 'format_date("ddd dd MMM", 2026, 10, 4, 0), "CN 04 Th10"',
}
for name, fragment in render_boundary_guards.items():
    assert fragment in (GUI + "\n" + WM + "\n" + CONFIG + "\n" + LOCALE), (
        f"render boundary guard missing ({name}): {fragment}"
    )

# Regression guards for the observed screenshot and the render boundaries that
# make those strings visible in Vietnamese.
for needle in (
    'trf(\n                        "Hold {key}, the Astur key, for every shortcut below."',
    'fn tile_hint(c: &Config) -> String',
    '"Space between windows"',
    '"Move a window: hold the key and drag anywhere on it"',
    'tr("Name")',
    'tr("Up/Down  •  Enter open  •  Esc close")',
    'config::i18n::{self, tr, trf}',
):
    assert needle in (GUI + "\n" + WM), f"render regression guard missing: {needle}"

# Explicit contract exceptions: these are deliberately not catalog entries.
# The scan does not silently swallow them; their boundaries are documented so
# a future change must choose a display wrapper or update this inventory.
exceptions = {
    "user_data": "window titles, app/file/path names, workspace names, clipboard, emoji and custom command output",
    "machine_data": "config keys, action IDs, process/exe names, window classes and persisted values",
    "shortcut_tokens": "Alt/Win/Ctrl/key names and user-entered shortcut text",
}
print(f"Catalog entries: {len(keys)}; Settings pages: {len(nav_items)}; explicit exceptions: {len(exceptions)}")
print("Vietnamese localization inventory/render-boundary gate: PASS")
