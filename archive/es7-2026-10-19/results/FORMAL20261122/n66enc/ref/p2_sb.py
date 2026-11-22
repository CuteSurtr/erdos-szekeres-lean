"""Phase 2 (21:10 KST): lex-leader symmetry breaking for the mirror map tau on the selectors (README section 6.7).
TAU is recomputed here from the profiles (conjugate partition via cell sets), independently of sym66.py.
pairs: a list of (s, TAU[s]) with s != TAU[s], one per tau-orbit at most.
LEX(x): at the first listed pair (s, t) with x_s != x_t, x_s = 0 (hole) and x_t = 1 (occupied).
For every selection x exactly one of x, x o tau satisfies LEX unless they agree on all listed pairs (then both do);
x o tau is the selection of the mirror image (Occ(rho S) = tau Occ(S), section 2.8), so adding LEX keeps every
"some set of the class has at most L holes" model.
Encoding (aux e_j = "the first j pairs are equal", numbered from top+1):
  pair j: [-e_{j-1}] -x_s  x_t ;  [-e_{j-1}] -x_s -x_t e_j ;  [-e_{j-1}] x_s x_t e_j   (no e for the last pair)."""
import json
import etv_common as ec
assert ec.A == 4 and ec.B == 4 and ec.N == 70
_cells = [frozenset((a + 1, y) for a in range(4) for y in range(1, f[a] + 1)) for f in ec.STATES]
_cellidx = {c: i for i, c in enumerate(_cells)}
TAU = [_cellidx[frozenset((b, a) for a, b in c)] for c in _cells]
def check_pairs(pairs):
    seen = set()
    for s, t in pairs:
        assert TAU[s] == t and s != t, (s, t)
        o = frozenset((s, t)); assert o not in seen, (s, t); seen.add(o)
    return True
def default_pairs(freqfile='mono/freq.json'):
    """one pair per non-trivial orbit, the more frequent hole state first, orbits by decreasing hole frequency"""
    hf = json.load(open(freqfile))['hole_freq']
    orbits = sorted({tuple(sorted((s, TAU[s]))) for s in range(ec.N) if TAU[s] != s}, key=lambda o: (-(hf[o[0]] + hf[o[1]]), o))
    pairs = [(o[0], o[1]) if hf[o[0]] >= hf[o[1]] else (o[1], o[0]) for o in orbits]
    check_pairs(pairs); return [list(p) for p in pairs]
def sb_clauses(sel_of_state, pairs, top):
    check_pairs([tuple(p) for p in pairs])
    out = []; e_prev = None
    for j, (s, t) in enumerate(pairs):
        xs, xt = sel_of_state[s], sel_of_state[t]
        g = [] if e_prev is None else [-e_prev]
        out.append(g + [-xs, xt])
        if j < len(pairs) - 1:
            top += 1; e = top
            out.append(g + [-xs, -xt, e]); out.append(g + [xs, xt, e]); e_prev = e
    return out, top
if __name__ == '__main__':
    import itertools
    p = default_pairs(); print(len(p), p[:6], sum(1 for s in range(70) if TAU[s] == s), 'fixed')
    # brute-force check of the claim on random selections: exactly one of x, x o tau satisfies LEX unless equal on pairs
    import random
    rnd = random.Random(1)
    def lex(x):
        for s, t in p:
            if x[s] != x[t]: return x[s] == 0 and x[t] == 1
        return True
    for _ in range(20000):
        x = [rnd.random() < 0.8 for _ in range(70)]; y = [x[TAU[s]] for s in range(70)]
        eq = all(x[s] == x[t] for s, t in p)
        assert (lex(x) != lex(y)) or eq
        assert lex(x) or lex(y)
    # the CNF encoding agrees with lex() on random selections (unit propagation from the selectors decides it)
    from pysat.solvers import Solver
    sel = list(range(1, 71)); cl, top = sb_clauses({s: sel[s] for s in range(70)}, p, 70)
    for _ in range(3000):
        x = [rnd.random() < 0.85 for _ in range(70)]
        with Solver(name='cadical153', bootstrap_with=cl) as S:
            r = S.solve(assumptions=[sel[s] if x[s] else -sel[s] for s in range(70)])
        assert r == lex(x)
    print('lex checks ok')
