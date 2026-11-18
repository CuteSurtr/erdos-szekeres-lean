#!/usr/bin/env python3
"""Extra-row file for capacity C from an existing capacity file.

Usage: make_capx.py IN_EXTRA.json C OUT.json

Keeps every demand-one row of IN_EXTRA.json (the cake_lpr-certified coupled rows) in the same order
and replaces the capacity row (the single row whose support is F, the 84 states with f1 >= 5) by
h(F) >= 84 - C.  The capacity row is written FIRST, so that rows appended later (witness kills) never
move it: fastbb's closed contexts stay valid as long as rows are only appended.
"""
import gzip, json, sys

SRC = 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz'


def main():
    inp, c, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    src = sys.argv[4] if len(sys.argv) > 4 else SRC
    states = json.load(gzip.open(src))['states']
    F = [i for i, s in enumerate(states) if s[0] >= 5]
    assert len(F) == 84
    rows = json.load(open(inp))
    cap = [r for r in rows if sorted(r['support']) == F]
    assert len(cap) == 1, 'expected exactly one capacity row'
    coupled = [r for r in rows if sorted(r['support']) != F]
    assert all(r['rhs'] == 1 for r in coupled)
    assert 0 <= 84 - c <= 84
    new = [{'support': F, 'rhs': 84 - c}] + coupled
    json.dump(new, open(out, 'w'))
    print(json.dumps({'capacity': c, 'capacity_row_rhs': 84 - c, 'coupled_rows': len(coupled), 'out': out}))


if __name__ == '__main__':
    main()
