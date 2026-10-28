#!/usr/bin/env python3
"""Deterministic static coverage gate for translation-rendering boundaries.

This is not Rust compilation or proof of 100% localization.
"""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
gui = (ROOT / 'crates/astur-settings/src/main.rs').read_text('utf-8')
locale = (ROOT / 'crates/astur-settings/src/i18n.rs').read_text('utf-8')
normalize=lambda s:s.replace(r'\u{2026}', '…')
entries = re.findall(r'(?m)^\s*"([^"]+)"\s*=>\s*"([^"]+)"', locale)
keys = set(en for en, _ in entries)
assert len(keys) == len(entries), "Duplicate translation keys generate unreachable Rust arms"
placeholder = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")
for english, vietnamese in entries:
    assert sorted(placeholder.findall(english)) == sorted(placeholder.findall(vietnamese)), english
nav_src = gui.split('const NAV:', 1)[1].split('const ICON_UNDO', 1)[0]
nav_items = set(re.findall(r'\(Page::\w+,\s*"([^"]+)"', nav_src))
nav_groups = set(re.findall(r'\(Page::\w+,\s*"[^"]+",\s*[^,]+,\s*"([^"]+)"', nav_src))
navigation = nav_items | (nav_groups - {''}) | {'Astur Settings', 'Language', 'Find a setting  (Ctrl+F)'}
sections = set(re.findall(r'\bsection\(ui,\s*f,\s*"([^"]+)"\)', gui))
pattern=re.compile(r'\(\s*"([^"\n]+)"\s*,\s*"([^"\n]*)"\s*,\s*"([a-z][a-z0-9_, ]+)"\s*\)')
meta={(normalize(m.group(1)),normalize(m.group(2)),m.group(3)) for m in pattern.finditer(gui) if '_' in m.group(3) or m.group(3).startswith('key')}
labels={x for x,_,_ in meta}
descs={x for _,x,_ in meta if x}
coverage={
    'navigation':sorted(navigation-keys),
    'section_headings':sorted(sections-keys),
    'metadata_labels':sorted(labels-keys),
    'metadata_descriptions':sorted(descs-keys),
}
print(f'Localized entries: {len(keys)}; tracked metadata tuples: {len(meta)}')
for part,missing in coverage.items():print(f'{part}: missing {len(missing)}; {missing[:8]}')
assert not coverage['navigation'] and not coverage['section_headings']
assert not coverage['metadata_labels'] and not coverage['metadata_descriptions']
assert 'mod i18n;' in gui and 'i18n::load' in gui and 'i18n::save' in gui
assert 'tr(label)' in gui and 'tr(desc)' in gui
