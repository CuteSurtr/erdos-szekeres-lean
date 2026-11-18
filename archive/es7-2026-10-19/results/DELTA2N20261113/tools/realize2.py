"""Second realizer: coordinate-wise max-margin LP (each point in turn is moved to the position maximizing the
smallest normalized orientation margin over all triples through it, all other points fixed; the constraints are
linear in the moved point).  Start: output of realize.py-style gradient descent or random.  HiGHS (scipy linprog) is
used only as a heuristic: the result is rounded to integers and every sign is re-checked exactly.
usage: realize2.py cex/file.json [rounds] -> updates the file in place if a realization is found"""
import sys, json, itertools, random
import numpy as np
from scipy.optimize import linprog
comb = itertools.combinations
def exact_ok(P, s, m):
    if any(P[i][0] >= P[i + 1][0] for i in range(m - 1)): return False
    for (i, j, k), c in zip(comb(range(m), 3), s):
        d = (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
        if d == 0 or (d > 0) != (c == '+'): return False
    return True
def polish(m, s, X, rounds=60, rng=None):
    sg = {t: (1.0 if c == '+' else -1.0) for t, c in zip(comb(range(m), 3), s)}
    X = np.array(X, dtype=float); best = -1e9
    for r in range(rounds):
        order = list(range(m)); (rng or random).shuffle(order)
        for k in order:
            # variables (x, y, t): maximize t s.t. sign * det(p_i, p_j, p) >= t * |p_i - p_j|  (distance of p from line ij)
            A = []; b = []
            for i, j in comb([q for q in range(m) if q != k], 2):
                tr = tuple(sorted((i, j, k))); sgn = sg[tr]
                # orientation of the sorted triple as a function of p = p_k; det(a,b,c) is alternating:
                a_, b_, c_ = tr
                pos = tr.index(k)
                (x1, y1), (x2, y2) = X[i], X[j]          # i < j
                # det(p_i, p_j, p) = (x2-x1)(y-y1) - (y2-y1)(x-x1); position parity: k last -> +, k middle -> -, k first -> +
                par = 1.0 if pos != 1 else -1.0
                cx = -(y2 - y1) * par * sgn; cy = (x2 - x1) * par * sgn; c0 = ((y2 - y1) * x1 - (x2 - x1) * y1) * par * sgn
                nrm = np.hypot(x2 - x1, y2 - y1)
                A.append([-cx, -cy, nrm]); b.append(c0)          # cx x + cy y + c0 >= t nrm
            lo = X[k - 1][0] if k > 0 else X[0][0] - 10 * (X[-1][0] - X[0][0] + 1)
            hi = X[k + 1][0] if k < m - 1 else X[-1][0] + 10 * (X[-1][0] - X[0][0] + 1)
            A.append([-1, 0, 1]); b.append(-lo); A.append([1, 0, 1]); b.append(hi)          # x - lo >= t, hi - x >= t
            span = 20 * (np.abs(X).max() + 1)
            res = linprog([0, 0, -1], A_ub=np.array(A), b_ub=np.array(b), bounds=[(-span, span), (-span, span), (None, None)], method='highs')
            if res.status == 0 and res.x is not None: X[k] = res.x[:2]
        # exact test on a rounded copy
        for sc in (10**3, 10**5, 10**7):
            sc2 = sc / max(1e-9, np.abs(X).max())
            P = [(int(round(x * sc2 * 1000)), int(round(y * sc2 * 1000))) for x, y in X]
            if exact_ok(P, s, m): return P
    return None
if __name__ == '__main__':
    fn = sys.argv[1]; rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    rec = json.load(open(fn))
    if rec.get('realized'): print(fn, 'already realized'); sys.exit(0)
    m, s = rec['m'], rec['signs']; rng = random.Random(5); P = None
    for attempt in range(6):
        X = [(i + rng.uniform(-0.2, 0.2), rng.uniform(-2, 2)) for i in range(m)]
        P = polish(m, s, X, rounds, rng)
        if P: break
    if P:
        rec['realized'] = True; rec['P'] = P; rec['realizer'] = 'realize2.py (coordinate-wise max-margin LP)'
        json.dump(rec, open(fn, 'w'))
    print(fn, 'REALIZED by LP polish' if P else 'not realized by LP polish', flush=True)
