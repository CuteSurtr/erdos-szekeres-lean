#!/usr/bin/env python3
"""Exact, independent check of a WITNESS reported by fastbb (or pbb_strong).

Usage (from the repository root): check_witness.py WITNESS.json EXTRA.json BUDGET [KILLDIR]

Checks with scripts/omission_row_probe.valid_holes (exact integer counts) that the hole set has at most
BUDGET holes and satisfies every row of the 2,650-row source and of EXTRA.json, and that state 0 is
occupied.  Reports how many of the 84 F-states (f1 >= 5) are occupied.  With KILLDIR (a copy of the
res33 tools) it also counts the pooled, not yet certified transported rows that the vector violates
(rows whose support is fully occupied): these are the candidates for the certified kill.
"""
import gzip, json, os, sys
sys.path.insert(0, 'scripts')
from omission_row_probe import read_rows, valid_holes

SRC = 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'


def main():
    wit = json.load(open(sys.argv[1]))
    H = wit['holes']
    budget = int(sys.argv[3])
    src = json.load(gzip.open(SRC))
    states = src['states']
    src['constraints'] += json.load(open(sys.argv[2]))
    n, rows = read_rows(src)
    F = [i for i, s in enumerate(states) if s[0] >= 5]
    out = {'holes': len(H), 'context': wit.get('context'), 'rows_checked': len(rows),
           'valid_witness': bool(valid_holes(n, rows, budget, H) and 0 not in H),
           'F_occupied': len(set(F) - set(H)), 'F_holes': len(set(F) & set(H))}
    if len(sys.argv) > 4:
        occ = set(range(n)) - set(H)
        pool = [r['support'] for r in json.load(open(os.path.join(sys.argv[4], 'newrows.json')))]
        fp = os.path.join(sys.argv[4], 'fnewrows.json')
        if os.path.exists(fp):
            pool += [r['support'] for r in json.load(open(fp))]
        viol = [S for S in pool if set(S) <= occ]
        out['pooled_rows'] = len(pool)
        out['pooled_rows_violated'] = len(viol)
        out['violated_sizes'] = sorted({len(S) for S in viol})
    print(json.dumps(out))


if __name__ == '__main__':
    main()
