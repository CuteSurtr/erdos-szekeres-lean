#!/usr/bin/env python3
"""Own-parser check: the 2,650 rows of Residual32Bridge2650/Catalog.lean (support2650/demand2650) equal, in order,
the constraints of source-2650.json.gz that every slice tree uses as rows 0..2649 (res118-lean, read-only)."""
import gzip, hashlib, json, re, sys
from pathlib import Path
CAT = Path('/home/jay/research/lean/erdos-szekeres-lean/experiments/omission-compact-checker-2026-11-05/build/chain311/src/Residual32Bridge2650/Catalog.lean')
SRC = Path('/home/jay/research/data/es308-20261114/inputs/source-2650.json.gz')
text = CAT.read_text()
order = re.search(r'def rowChunks := #\[(.*?)\]', text).group(1).split(', ')
rows = []
for name in order:
    body = re.search(rf'def {name} : Array \(Finset \(Fin 154\) × ℕ × ℕ\) := #\[(.*?)\n\]', text, re.S).group(1)
    for sup, dem in re.findall(r'\(\{([0-9, ]*)\}, (\d+), \d+\)', body):
        rows.append((frozenset(int(t) for t in sup.split(',')), int(dem)))
src = json.loads(gzip.decompress(SRC.read_bytes()))
want = [(frozenset(c['support']), c['rhs']) for c in src['constraints']]
dups = sum(len(c['support']) != len(set(c['support'])) for c in src['constraints'])
res = {'catalog_lean_sha256': hashlib.sha256(CAT.read_bytes()).hexdigest(), 'lean_rows': len(rows),
       'json_rows': len(want), 'json_rows_with_repeated_states': dups, 'equal_in_order': rows == want,
       'source_hash_comment_in_lean': 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6' in text}
print(json.dumps(res, indent=1))
sys.exit(0 if res['equal_in_order'] and res['lean_rows'] == 2650 and dups == 0 else 1)
