#!/usr/bin/env python3
"""Exact stdlib checker for biquadratic final polynomial (BFP) certificates on the sixfold 10-layer encoding.

Certificate JSON: {"clause": [lits], "comparisons": [{"quintuple": [a,b,c,d,e], "minority": m, "other": j,
"weight": w}, ...]}.  Brackets of the 3-term GP identity on (a;b,c,d,e):
  T0 = [abc][ade],  T1 = -[abd][ace],  T2 = [abe][acd],   T0 + T1 + T2 = 0  (polynomial identity).
Semantics of variables: independent re-implementation of C7UPPER/gen.py orbit variables (as in check_gp.py).
Checks:
  (1) the clause's variable set equals the union of the bracket variables of all used identities, no repeats;
  (2) under the unique assignment falsifying the clause, in each used identity exactly two of T0,T1,T2 share a sign
      and the odd one is T_m (so |T_m| = |T_j| + |T_j'| > |T_j|, all nonzero), and j != m;
  (3) weights are positive integers and sum_k w_k * (e(T_m) - e(T_j)) = 0 exactly, where e(T) is the exponent
      vector of the product of the two bracket ORBITS of T (bracket magnitudes are invariant under the rotation).
Then a configuration with the sixfold rotation (generic orientations) falsifying the clause would satisfy
prod |T_m|^w > prod |T_j|^w with both products equal (same monomial in the orbit magnitudes): contradiction.
Optional --model: check that the model falsifies the clause.
"""
import sys, json, itertools
from collections import Counter
N, M = 60, 6
def rot(x, s): return (x // M) * M + (x % M + s) % M
def sortpar(t):
    a = list(t); p = 1
    for i in range(len(a)):
        for j in range(len(a) - 1 - i):
            if a[j] > a[j + 1]: a[j], a[j + 1] = a[j + 1], a[j]; p = -p
    return tuple(a), p
CANON = {}
for T in itertools.combinations(range(N), 3):
    best = None
    for s in range(M):
        srt, par = sortpar([rot(x, s) for x in T])
        if best is None or srt < best[0]: best = (srt, par)
    CANON[T] = best
VARS = {C: i + 1 for i, C in enumerate(sorted({c for c, _ in CANON.values()}))}
assert len(VARS) == 5710
def var_par(t):
    srt, p1 = sortpar(t); C, p2 = CANON[srt]
    return VARS[C], p1 * p2
def terms(q):
    a, b, c, d, e = q
    return [((a, b, c), (a, d, e), 1), ((a, b, d), (a, c, e), -1), ((a, b, e), (a, c, d), 1)]
def check(cert, model=None):
    clause = cert['clause']; comps = cert['comparisons']
    if not comps: return 'no comparisons'
    vs = [abs(l) for l in clause]
    if len(set(vs)) != len(vs): return 'repeated variable'
    need = set()
    for cp in comps:
        q = tuple(cp['quintuple'])
        if len(set(q)) != 5 or not all(isinstance(x, int) and 0 <= x < N for x in q): return 'bad quintuple'
        for x, y, _ in terms(q): need.add(var_par(x)[0]); need.add(var_par(y)[0])
    if set(vs) != need: return 'clause variables != bracket variables'
    val = {abs(l): (l < 0) for l in clause}
    def o(t):
        v, p = var_par(t); return p * (1 if val[v] else -1)
    expo = Counter()
    for cp in comps:
        q = tuple(cp['quintuple']); m = cp['minority']; j = cp['other']; w = cp['weight']
        if not (isinstance(w, int) and w > 0): return 'nonpositive weight'
        if m not in (0, 1, 2) or j not in (0, 1, 2) or m == j: return 'bad term indices'
        tt = terms(q); s = [co * o(x) * o(y) for x, y, co in tt]
        if s.count(s[m]) != 1: return 'term m is not the minority (or GP violation)'
        for t in tt[m][:2]: expo[var_par(t)[0]] += w
        for t in tt[j][:2]: expo[var_par(t)[0]] -= w
    if any(expo.values()): return 'exponents do not cancel'
    if model is not None and any((l > 0) == (abs(l) in model) for l in clause): return 'model does not falsify clause'
    return None
if __name__ == '__main__':
    args = sys.argv[1:]; model = None
    if '--model' in args:
        i = args.index('--model'); model = set(json.load(open(args[i + 1]))); del args[i:i + 2]
    cert = json.load(open(args[0]))
    err = check(cert, model)
    print(json.dumps({'file': args[0], 'comparisons': len(cert['comparisons']), 'clause_len': len(cert['clause']),
                      'model_bound': model is not None, 'ok': err is None, 'error': err}))
    sys.exit(0 if err is None else 1)
