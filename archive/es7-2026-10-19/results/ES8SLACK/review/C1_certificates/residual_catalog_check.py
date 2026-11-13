#!/usr/bin/env python3
"""Compare the literal Lean catalog Residual32Bridge2650/Catalog.lean with source-2650.json.gz (JSON used
by the residual tree replay).  Row r of Lean = rowChunks[r/128][r%128]; checks support and demand.
Usage: python3 -I residual_catalog_check.py"""
import gzip, json, re, sys
import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
X = ROOT + '/experiments'
txt = open(X + '/omission-residual32-bridge2650-2026-10-11/Residual32Bridge2650/Catalog.lean').read()
chunks = {}
for start, body in re.findall(r'def rows(\d+) : Array \(Finset \(Fin 154\) × ℕ × ℕ\) := #\[(.*?)\n\]', txt, re.S):
    chunks[int(start)] = [(frozenset(json.loads('[' + s + ']')), int(d))
                          for s, d in re.findall(r'\(\{([0-9, ]*)\}, (\d+), \d+\)', body)]
order = re.search(r'def rowChunks[^=]*:= #\[([a-z0-9, ]*)\]', txt).group(1)
names = [x.strip() for x in order.split(',')]
lean_rows = []
for nm in names:
    lean_rows.extend(chunks[int(nm[len('rows'):])])
src = json.loads(gzip.decompress(open(X + '/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))
js = [(frozenset(c['support']), int(c['rhs'])) for c in src['constraints']]
bad = [r for r in range(max(len(js), len(lean_rows))) if r >= len(js) or r >= len(lean_rows) or js[r] != lean_rows[r]]
print(json.dumps({'chunk_order': names[:3] + ['...'], 'lean_rows': len(lean_rows), 'json_rows': len(js),
                  'mismatches': len(bad), 'first_bad': bad[:5]}))
print('RESIDUAL LITERAL CATALOG == JSON' if not bad and len(js) == 2650 else 'MISMATCH')
sys.exit(0 if not bad else 1)
