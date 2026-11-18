"""LO33 (13 Nov 2026): shared helpers for the two-capacity residual question.
Pair (c, c2): rows  h(F) >= 84 - c  and  h(Lo) >= 70 - c2  on the 154 residual states
(F = 84 states with f1 >= 5, Lo = 70 states with f1 <= 4), together with h0 = 0, the 2,650 Lean rows and
the cake_lpr-certified coupled rows of certified.jsonl (work directory copy)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from common import N, STATES, ROWS, check
F = [i for i in range(N) if STATES[i][0] >= 5]
LO = [i for i in range(N) if STATES[i][0] <= 4]
assert len(F) == 84 and len(LO) == 70 and sorted(F + LO) == list(range(N))

def certified_supports(path=None):
    out = set()
    for line in open(path or os.path.join(HERE, 'certified.jsonl')):
        r = json.loads(line)
        if r['verdict'] == 's VERIFIED UNSAT': out.add(tuple(sorted(r['support'])))
    return [list(s) for s in sorted(out)]

def cap_rows(c, c2):
    rows = []
    if 84 - c > 0: rows.append({'support': F, 'rhs': 84 - c})
    if 70 - c2 > 0: rows.append({'support': LO, 'rhs': 70 - c2})
    return rows

def extra_rows(c, c2, cert=None):
    cert = certified_supports() if cert is None else cert
    return [{'support': s, 'rhs': 1} for s in cert] + cap_rows(c, c2)

def pooled():
    pool = [r['support'] for r in json.load(open(os.path.join(HERE, 'newrows.json')))]
    fp = os.path.join(HERE, 'fnewrows.json')
    if os.path.exists(fp): pool += [r['support'] for r in json.load(open(fp))]
    lp = os.path.join(HERE, 'lonewrows.json')
    if os.path.exists(lp): pool += [r['support'] for r in json.load(open(lp))]
    return [list(s) for s in sorted({tuple(sorted(s)) for s in pool})]
