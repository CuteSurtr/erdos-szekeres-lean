#!/usr/bin/env python3
"""Second, independently written exact checker for BFP certificates (cross-check of check_bfp.py).

Differences from check_bfp.py: literal semantics come from the reference encoder C7UPPER/gen.py (E.o), not from a
re-implementation; the identity is re-derived by expanding the 3x3 bracket determinants symbolically (sympy) once at
start; term signs are computed as products of bracket signs times the identity's coefficients as found by the
expansion; exponent cancellation is checked on the multiset of (orbit, exponent) pairs with Python integers.
Usage: check_bfp2.py CERT.json [--model MODEL.json]"""
import sys, json, os, importlib.util
from collections import defaultdict
import sympy
GEN = os.environ.get('GEN', '<results-dir>/C7UPPER/gen.py')
sp_ = importlib.util.spec_from_file_location('gen', GEN); G = importlib.util.module_from_spec(sp_); sp_.loader.exec_module(G)
E = G.Enc(6, 8, 10)
# derive the coefficients of the 3 products in the GP identity on symbolic points 0..4 (pivot 0)
X = sympy.symbols('x0:5'); Y = sympy.symbols('y0:5')
def br(i, j, k): return sympy.Matrix([[X[i], Y[i], 1], [X[j], Y[j], 1], [X[k], Y[k], 1]]).det()
PRODS = [((0, 1, 2), (0, 3, 4)), ((0, 1, 3), (0, 2, 4)), ((0, 1, 4), (0, 2, 3))]
COEF = None
for c in [(a, b, d) for a in (1, -1) for b in (1, -1) for d in (1, -1)]:
    if sympy.expand(sum(ci * br(*p) * br(*q) for ci, (p, q) in zip(c, PRODS))) == 0: COEF = c; break
assert COEF is not None and COEF[0] == 1
def main():
    args = sys.argv[1:]; model = None
    if '--model' in args:
        i = args.index('--model'); model = set(json.load(open(args[i + 1]))); del args[i:i + 2]
    cert = json.load(open(args[0])); clause = cert['clause']; comps = cert['comparisons']
    assign = {}
    for l in clause:
        assert abs(l) not in assign, 'repeated variable'
        assign[abs(l)] = (l < 0)        # value under the clause-falsifying assignment
    used = set(); expo = defaultdict(int)
    assert comps, 'empty'
    for cp in comps:
        q = cp['quintuple']; w = cp['weight']; m = cp['minority']; j = cp['other']
        assert isinstance(w, int) and w > 0 and m != j and {m, j} <= {0, 1, 2}
        assert len(set(q)) == 5 and all(0 <= x < 60 for x in q)
        sig = []; orb = []
        for ci, (p, r) in zip(COEF, PRODS):
            s = ci; o = []
            for t in (p, r):
                lit = E.o(*[q[k] for k in t]); v = abs(lit); used.add(v)
                assert v in assign, 'bracket variable missing from clause'
                s *= (1 if lit > 0 else -1) * (1 if assign[v] else -1); o.append(v)
            sig.append(s); orb.append(o)
        assert sig.count(sig[m]) == 1, 'claimed minority is not the unique odd sign'
        for v in orb[m]: expo[v] += w
        for v in orb[j]: expo[v] -= w
    assert used == set(assign), 'clause has variables not used by any identity'
    assert all(e == 0 for e in expo.values()), 'exponents do not cancel'
    if model is not None:
        assert all((l > 0) != (abs(l) in model) for l in clause), 'model does not falsify clause'
    print(json.dumps({'file': args[0], 'ok': True, 'comparisons': len(comps), 'clause_len': len(clause), 'gp_coefficients': COEF}))
if __name__ == '__main__':
    try: main()
    except AssertionError as ex:
        print(json.dumps({'file': sys.argv[1], 'ok': False, 'error': str(ex)})); sys.exit(1)
