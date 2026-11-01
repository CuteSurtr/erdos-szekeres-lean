"""Independent exact replay of the 446 balanced V2 rounded cover cuts (math.md (3.2)):
for derived row (T, q) with capacity C >= 0 and nonnegative integer weights w_r on EARLIER rows,
  L_i = sum_{r: i in S_r} w_r,  D = sum_r w_r d_r,
  E_T = sum_{i in T} (L_i - C)_+ + sum_{i not in T} L_i,
  require C*(q-1) + E_T < D.
Then every Boolean h satisfying the parent rows has h(T) >= q. By induction every Boolean h
satisfying the 2,685 base rows satisfies all 3,131 rows; hence the Boolean feasible set of the
3,131-row catalog equals that of the base rows, which is <T,C>-invariant.
Integer arithmetic only.
"""
import json, sys
src = json.load(open(sys.argv[1])); cuts = json.load(open(sys.argv[2]))
rows = [(c['support'], c['rhs']) for c in src['constraints']]
assert cuts['base_rows'] == 2685 and len(cuts['proofs']) == 446 == len(rows) - 2685
bad = 0
for k, p in enumerate(cuts['proofs']):
    idx = 2685 + k
    assert p['row'] == idx, (k, p['row'])
    T = set(p['support']); q = p['rhs']; C = p['capacity']
    if (sorted(T), q) != (sorted(rows[idx][0]), rows[idx][1]):
        print('row mismatch at', idx); bad += 1; continue
    assert isinstance(C, int) and C >= 0 and isinstance(q, int) and q >= 1
    L = {}; D = 0
    for r, w in p['weights']:
        assert isinstance(r, int) and isinstance(w, int) and w >= 0 and 0 <= r < idx, (idx, r, w)
        S, dr = rows[r]
        D += w * dr
        for i in S: L[i] = L.get(i, 0) + w
    E = sum(max(L.get(i, 0) - C, 0) for i in T) + sum(v for i, v in L.items() if i not in T)
    if not (C * (q - 1) + E < D):
        print('FAILED margin at row', idx, C, q, E, D); bad += 1
print('replayed', len(cuts['proofs']), 'cuts; failures:', bad)
