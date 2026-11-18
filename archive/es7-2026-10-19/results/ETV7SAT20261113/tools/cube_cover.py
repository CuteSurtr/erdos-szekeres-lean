#!/usr/bin/env python3
"""cube_cover.py -- script check that the two cases of rung N = 36 cover everything.

Uncubed CNF: owner model (3,5,7,36) + rows S1<=25, S2<=25, B1<=16, B2<=16, ALL<=36 (exactly 36 occupied).
Case A = the same with B2<=13 (at most 13 occupied states with f1 = 5).
Case B = the same with S1<=22 (at most 22 occupied states with f1 <= 4).
The families S1 = {f1 <= 4} and B2 = {f1 = 5} partition the 56 states.  With exactly 36 occupied
states, r = #occupied in B2 and t = #occupied in S1 satisfy r + t = 36, so r <= 13 or t <= 22.
The script (1) re-derives the two families and checks that they partition the states, (2) checks the
arithmetic for all (r, t), (3) reads the row specifications actually written into the two cube CNFs
(their .names.pkl) and checks that they differ from the uncubed specification only in the stated bound.
"""
import sys, pickle
sys.path.insert(0, '.')
import cat_common, addrows
states = cat_common.make(3, 5)[0]
S1 = set(addrows.family('S1', 3, 5)); B2 = set(addrows.family('B2', 3, 5))
assert S1 | B2 == set(range(len(states))) and not (S1 & B2), 'families do not partition'
N = 36
for r in range(0, len(B2) + 1):
    t = N - r
    if 0 <= t <= len(S1):
        assert r <= 13 or t <= 22, (r, t)
base = {'S1': 25, 'S2': 25, 'B1': 16, 'B2': 16, 'ALL': 36}
ok = True
for name, changed in (('c36_rle13', {'B2': 13}), ('c36_tle22', {'S1': 22})):
    meta = pickle.load(open(f'run/{name}.cnf.names.pkl', 'rb'))
    rows = {k: v[1] for k, v in meta['rows'].items()}
    want = dict(base); want.update(changed)
    assert rows == want, (name, rows, want)
    assert meta['N'] == 36 and (meta['CA'], meta['CB'], meta['G']) == (3, 5, 7)
    for k, (fam, K) in meta['rows'].items():
        assert fam == addrows.family(k, 3, 5)
    print(name, 'rows', rows, 'OK')
print('COVER OK: every assignment with exactly 36 occupied states satisfies the rows of case A or of case B')
