#!/usr/bin/env python3
"""Independent Python port of `ResidualCycleValid` (ResidualCycleGeometry/ResidualBoxes/ResidualDomains with
CycleSigns.CheckTriple) for the 1,164 residual cycle lists extracted from the kernel-checked
ResidualGeometry*.lean sources; also checks cycle i <-> JSON row cycleRow(i) (i<973 ? i : i+1) of
source-2650.json.gz (support = set, demand = length-7), and that the 23 skipped rows are the block rows.
Residual grid: x in 1..4, y in 1..6; Contains(s,(x,y)) := y <= s[x-1].
Usage: python3 -I residual_cycle_check.py
"""
import glob, gzip, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
src = json.loads(gzip.decompress(open(ROOT + '/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz', 'rb').read()))
cat = src['states']
rows = [(frozenset(c['support']), int(c['rhs'])) for c in src['constraints']]
assert len(cat) == 154
GRID = [(x, y) for x in range(1, 5) for y in range(1, 7)]


def contains(s, z):
    x, y = z
    return y <= (s[x - 1] if 0 <= x - 1 < len(s) else 0)


def box(a, b):
    d = [z for z in GRID if contains(cat[b], z) and not contains(cat[a], z)]
    if not d:
        return (False, 0, 0, 0, 0)
    return (True, min(z[0] for z in d), max(z[0] for z in d), min(z[1] for z in d), max(z[1] for z in d))


T = [[box(a, b) for b in range(154)] for a in range(154)]


def safe(ab, bc, ac, want):
    if not ab[0] or not bc[0] or not ac[0]:
        return True
    return bc[2] <= ab[1] if want else bc[4] <= ab[3]


def check_triple(a, b, c):
    return (safe(T[a][b], T[b][c], T[a][c], True) and
            safe(T[a][c], T[c][b], T[a][b], False) and
            safe(T[b][a], T[a][c], T[b][c], False) and
            safe(T[b][c], T[c][a], T[b][a], True) and
            safe(T[c][a], T[a][b], T[c][b], True) and
            safe(T[c][b], T[b][a], T[c][a], False))


cyc = {}
for f in sorted(glob.glob(HERE + '/extract_residual_cycles/ResidualGeometry0*.lean')):
    txt = open(f).read()
    start = int(re.search(r'cycles\[i\.val - (\d+)\]!', txt).group(1))
    body = re.search(r'def cycles : Array \(List \(Fin 154\)\) := #\[(.*?)\n\]', txt, re.S).group(1)
    for j, l in enumerate(re.findall(r'\[[0-9, ]+\]', body)):
        cyc[start + j] = json.loads(l)
assert sorted(cyc) == list(range(1164)), (len(cyc), min(cyc), max(cyc))
cycle_row = lambda i: i if i < 973 else i + 1
bad_valid, bad_row = [], []
for i in range(1164):
    ids = cyc[i]
    k = len(ids)
    if not (len(set(ids)) == k and all(check_triple(ids[a], ids[b], ids[c])
                                       for a in range(k) for b in range(a + 1, k) for c in range(b + 1, k))):
        bad_valid.append(i)
    if rows[cycle_row(i)] != (frozenset(ids), k - 7):
        bad_row.append(i)
skipped = sorted(set(range(1187)) - {cycle_row(i) for i in range(1164)})
skipped_are_blocks = all(rows[r][1] == len(rows[r][0]) - 22 == 6 for r in skipped)
print(json.dumps({'cycles': len(cyc), 'validity_failures': len(bad_valid), 'row_mismatches': len(bad_row),
                  'skipped_rows': [skipped[0], skipped[1], '...', skipped[-1]], 'n_skipped': len(skipped),
                  'skipped_are_demand6_size28_blocks': skipped_are_blocks}))
ok = not bad_valid and not bad_row and len(skipped) == 23 and skipped_are_blocks
print('ALL 1164 RESIDUAL CYCLES SATISFY ResidualCycleValid AND MATCH THE JSON ROWS' if ok else 'FAILURE')
sys.exit(0 if ok else 1)
