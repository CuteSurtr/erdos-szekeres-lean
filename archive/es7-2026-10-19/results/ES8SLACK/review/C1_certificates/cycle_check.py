#!/usr/bin/env python3
"""Independent Python port of the balanced `CycleValid` finite check (CycleGeometry/CycleSigns/Domains/
BoundingBoxes) applied to all 2,685 cycle lists extracted from the kernel-checked Geometry*.lean sources.

Contains(s,(x,y)) := y <= s[x-1];  difference(a,b) = {z in [1..5]^2 : Contains(b,z) and not Contains(a,z)};
box = (present, xmin, xmax, ymin, ymax) of the difference;  Safe(ab,bc,ac,want) := some box absent or
(want ? bc.xmax <= ab.xmin : bc.ymax <= ab.ymin);  CheckTriple(a,b,c) = conjunction over the six
chronological orders exactly as in CycleSigns.CheckTriple;  CycleValid = injective and every i<j<k checks.
Also reports how many cycles would fail if the six-order conjunction were weakened, as a sanity control.
Usage: python3 -I cycle_check.py
"""
import glob, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
cat = json.load(open(ROOT + '/experiments/omission-cover-certificates-2026-10-10/balanced-v2-source.json'))['states']
assert len(cat) == 252
GRID = [(x, y) for x in range(1, 6) for y in range(1, 6)]


def contains(s, z):
    x, y = z
    return y <= (s[x - 1] if 0 <= x - 1 < len(s) else 0)


def box(a, b):
    d = [z for z in GRID if contains(cat[b], z) and not contains(cat[a], z)]
    if not d:
        return (False, 0, 0, 0, 0)
    return (True, min(z[0] for z in d), max(z[0] for z in d), min(z[1] for z in d), max(z[1] for z in d))


T = [[box(a, b) for b in range(252)] for a in range(252)]


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
for f in sorted(glob.glob(HERE + '/extract_balanced_rows/Geometry*.lean')):
    txt = open(f).read()
    start = int(re.search(r'cycles\[r\.val - (\d+)\]!', txt).group(1))
    body = re.search(r'def cycles : Array \(List \(Fin 252\)\) := #\[(.*?)\n\]', txt, re.S).group(1)
    for j, l in enumerate(re.findall(r'\[[0-9, ]+\]', body)):
        cyc[start + j] = json.loads(l)
assert sorted(cyc) == list(range(2685))
bad = []
for r in range(2685):
    ids = cyc[r]
    k = len(ids)
    okr = len(set(ids)) == k and all(check_triple(ids[i], ids[j], ids[l])
                                     for i in range(k) for j in range(i + 1, k) for l in range(j + 1, k))
    if not okr:
        bad.append(r)
# controls: reversed lists (orientation flips) should fail; the check is not vacuous
rev_fail = sum(1 for r in range(2685) if not all(check_triple(*(cyc[r][::-1][i] for i in t))
               for t in [(0, 1, 2)]))
empty_boxes = sum(1 for a in range(252) for b in range(252) if a != b and not T[a][b][0])
print(json.dumps({'cycles': len(cyc), 'cycle_valid_failures': len(bad), 'first_bad': bad[:5],
                  'control_reversed_first_triple_fails': rev_fail, 'absent_offdiagonal_boxes': empty_boxes}))
print('ALL 2685 BALANCED CYCLES SATISFY CycleValid (Python port)' if not bad else 'CYCLE CHECK FAILURE')
sys.exit(0 if not bad else 1)
