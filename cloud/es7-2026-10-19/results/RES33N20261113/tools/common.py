"""Residual budget-33 CEGAR (13 Nov 2026). Discovery only; nothing here is a proof."""
import gzip, hashlib, json, itertools, os, sys
REPO = '/home/jay/research/lean/erdos-szekeres-lean'
SRC = REPO + '/experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'
raw = gzip.decompress(open(SRC, 'rb').read())
assert hashlib.sha256(raw).hexdigest() == 'e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6'
CAT = json.loads(raw)
STATES = CAT['states']
N = len(STATES)
ROWS = [(tuple(sorted(r['support'])), int(r['rhs'])) for r in CAT['constraints']]
def cells(s):
    return frozenset((i + 1, y) for i, h in enumerate(s[:4]) for y in range(1, h + 1))
CELLS = [cells(s) for s in STATES]
def check(holes, rows):
    H = set(holes)
    return [k for k, (s, d) in enumerate(rows) if len(H.intersection(s)) < d]
