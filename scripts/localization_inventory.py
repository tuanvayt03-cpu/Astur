#!/usr/bin/env python3
"""Read-only Rust UI string inventory for Astur Vietnamese localization."""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
text = (ROOT / 'crates/astur-settings/src/main.rs').read_text(encoding='utf-8')
names = ['toggle','section','section_title','row','nav_item','num','color','pick','choice','text','font_row','header','status','page_ui','label','hint']
for name in names:
    hits=[(text.count('\n',0,m.start())+1, text[m.start():m.start()+140].splitlines()[0]) for m in re.finditer(r'(?m)^\s*(?:pub\s+)?fn\s+'+re.escape(name)+r'\s*\(', text)]
    print(name, hits[:8])
for pat in ['ui.button(', 'ui.label(', 'RichText::new(', 'on_hover_text(', 'hint_text(', 'section(', 'toggle(', 'num(']:
    print(pat, text.count(pat))
