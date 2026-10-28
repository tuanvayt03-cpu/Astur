#!/usr/bin/env python3
"""Inventory user-facing metadata in the Settings GUI, excluding machine keys."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
s=(root/'crates/astur-settings/src/main.rs').read_text('utf-8')
loc=(root/'crates/astur-settings/src/i18n.rs').read_text('utf-8')
translated=set(re.findall(r'(?m)^\s*"([^"]+)"\s*=>\s*"',loc))
pattern=re.compile(r'\(\s*"([^"\n]+)"\s*,\s*"([^"\n]*)"\s*,\s*"([a-z][a-z0-9_, ]+)"\s*\)')
meta={(m.group(1),m.group(2),m.group(3)) for m in pattern.finditer(s) if ('_' in m.group(3) or m.group(3).startswith('key'))}
labels=sorted({a for a,_,_ in meta if a not in translated and len(a)<120})
descs=sorted({b for _,b,_ in meta if b and b not in translated})
print(f"Metadata tuples: {len(meta)}, missing label translations: {len(labels)}, missing descriptions: {len(descs)}")
for x in labels: print('LABEL:',x)
for x in descs: print('DESC:',x)
