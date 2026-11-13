#!/usr/bin/env python3
"""Compare the two found small sets with the printed literature sets.
Usage: python3 -I compare_printed.py PATH/verify_small.py C4PTS C5PTS

(1) found 4-fold 8-point set vs Eppstein / Wikipedia 8-point figure (symmetrised integer version, typed in by hand
    from the symmetrised copy made in the literature check): exact order-type isomorphism test (backtracking over
    bijections, both orientations).
(2) SMQH arXiv:2506.00224 Table 2 (orbits of (-12,-17), (-15,2), (-13,0) under rotation by 2pi/5, plus (0,0)):
    rigorous rational-interval orientations, brute-force convex k-subset counts; compared with the found 5-fold set.
    Also an isomorphism test between the two 5-fold sets.
"""
import sys, importlib.util, itertools, math
from fractions import Fraction as Fr

spec = importlib.util.spec_from_file_location('vs', sys.argv[1])
vs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(vs)


def table_from_sign(n, f):
    O = [[[0] * n for _ in range(n)] for _ in range(n)]
    for a, b, c in itertools.permutations(range(n), 3):
        O[a][b][c] = f(a, b, c)
    return O


def counts(O, n, K):
    res = {}
    for k in range(3, K + 1):
        res[k] = sum(1 for S in itertools.combinations(range(n), k) if vs.convex_T1(O, S))
    return res


def isomorphic(O1, O2, n):
    """exists bijection pi and eps in {+1,-1} with O1[a][b][c] == eps * O2[pi a][pi b][pi c] for all triples."""
    for eps in (1, -1):
        pi = [None] * n
        used = [False] * n

        def bt(i):
            if i == n:
                return True
            for v in range(n):
                if used[v]:
                    continue
                ok = True
                for a in range(i):
                    for b in range(a + 1, i):
                        if O1[a][b][i] != eps * O2[pi[a]][pi[b]][v]:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    pi[i] = v
                    used[v] = True
                    if bt(i + 1):
                        return True
                    used[v] = False
                    pi[i] = None
            return False
        if bt(0):
            return eps, list(pi)
    return None


# ---------------------------------------------------------------- (1)
_, W4 = vs.read_pts(sys.argv[2])
P4 = [vs.canon4(w) for w in W4]
O4 = table_from_sign(8, lambda a, b, c: vs.orient4(P4, a, b, c))
EPP = [(18, 18), (342, 18), (18, 342), (126, 99), (261, 126), (234, 261), (342, 342), (99, 234)]
assert all(vs.orient4(EPP, a, b, c) != 0 for a, b, c in itertools.combinations(range(8), 3))
OE = table_from_sign(8, lambda a, b, c: vs.orient4(EPP, a, b, c))
print('(1) Eppstein/Wikipedia 8-point set (symmetrised): counts', counts(OE, 8, 5), '; found c4 set:', counts(O4, 8, 5))
r = isomorphic(O4, OE, 8)
print('    order-type isomorphic to the found 4-fold set:', r is not None, '' if r is None else '(eps=%d, map %s)' % r)

# ---------------------------------------------------------------- (2)
ROT = [(vs.iv(Fr(1)), vs.iv(Fr(0))), (vs.COS72, vs.SIN72), (vs.COS144, vs.SIN144),
       (vs.COS144, vs.iscale(-1, vs.SIN144)), (vs.COS72, vs.iscale(-1, vs.SIN72))]
pts = []
for (x, y) in [(-12, -17), (-15, 2), (-13, 0)]:
    for k in range(5):
        c, s = ROT[k]
        X = vs.isub(vs.iscale(x, c), vs.iscale(y, s))
        Y = vs.iadd(vs.iscale(x, s), vs.iscale(y, c))
        pts.append((X, Y))
pts.append((vs.iv(Fr(0)), vs.iv(Fr(0))))
n = len(pts)
und = 0


def sgnC(a, b, c):
    global und
    s = vs.orient5_C(pts, a, b, c)
    if s is None:
        und += 1
        return 0
    return s


OS = table_from_sign(n, sgnC)
print('(2) SMQH Table 2: n =', n, ' undecided orientations (interval):', und)
cS = counts(OS, n, 6)
print('    SMQH Table 2 convex k-subset counts:', cS)
_, W5 = vs.read_pts(sys.argv[3])
O5 = table_from_sign(16, lambda a, b, c: vs.orient5_A(W5, a, b, c))
c5 = counts(O5, 16, 6)
print('    found c5 set convex k-subset counts:', c5)
print('    same counts:', cS == c5, '-> isomorphism (eps, map) or None:', isomorphic(O5, OS, 16) if cS == c5 else None)
