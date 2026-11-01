#!/usr/bin/env python3
"""Exact realization of the one-cluster rule set: points in Z[zeta_p] as integer coefficient vectors (length p, basis
zeta^0..zeta^{p-1}, not reduced). Sector-0 representatives: X_0-cluster leaves  S + sum over tree nodes on the path of
+-round(S*lam*mu^depth/2 * e^{i delta}) (each node offset rounded to the lattice Z + Z zeta), plus the centre.
Node angles are re-spaced: within each class, nodes get evenly spaced angles in an order that is a linear extension of
the comparisons fixed by the rule (each 'max' root above its subtree, each 'min' root below), so every relevant
angular gap is >= 1/(n_class+1) class units.
usage: gen_points.py h lam mu log10S out.pts"""
import sys, math, cmath
from fractions import Fraction as F
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from rule import rule_tree
def respace(T):
    """T: nested (L, R, Fraction angle). Re-space angles within each class by rank of the original angle (ties broken by
    the recursion order), preserving every strict comparison between a node and its ancestors."""
    nodes = []
    def rec(t, path):
        if t is None: return
        nodes.append(t); rec(t[0], path); rec(t[1], path)
    rec(T, ())
    # ranking: original angle, ties by order of appearance (preorder) -- ties only occur between unrelated nodes
    order = sorted(range(len(nodes)), key=lambda i: (nodes[i][2], i))
    by_class = {}
    for i in order: by_class.setdefault(int(nodes[i][2]), []).append(i)
    newang = {}
    for k, lst in by_class.items():
        for r, i in enumerate(lst): newang[id(nodes[i])] = F(k) + F(r + 1, len(lst) + 1)
    def rebuild(t):
        if t is None: return None
        return (rebuild(t[0]), rebuild(t[1]), newang[id(t)])
    return rebuild(T)
def check_order_preserved(T, U):
    """every node vs each ancestor: same strict comparison in T and U"""
    ok = True
    def rec(t, u, anc_t, anc_u):
        nonlocal ok
        if t is None: return
        for at, au in zip(anc_t, anc_u):
            if (t[2] < at) != (u[2] < au) or (t[2] > at) != (u[2] > au): ok = False
        rec(t[0], u[0], anc_t + [t[2]], anc_u + [u[2]]); rec(t[1], u[1], anc_t + [t[2]], anc_u + [u[2]])
    rec(T, U, [], [])
    return ok
def main():
    h, lam, mu, lS, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    p = 2 * h + 1
    v, desc, T = rule_tree(h)
    U = respace(T)
    assert check_order_preserved(T, U)
    S = 10 ** lS
    z1 = cmath.exp(2j * math.pi / p)
    sn, cs = math.sin(2 * math.pi / p), math.cos(2 * math.pi / p)
    from decimal import Decimal, getcontext
    getcontext().prec = 60
    def lattice(zre, zim):
        """nearest point a + b zeta (exact integers) to the complex number given as Decimals"""
        # z = a + b cos + i b sin -> b = im/sin, a = re - b cos
        SN = Decimal(repr(sn)); CS = Decimal(repr(cs))   # only used to choose the lattice point; exactness not needed
        b = (zim / SN).to_integral_value()
        a = (zre - b * CS).to_integral_value()
        return int(a), int(b)
    leaves = []
    def rec(t, a, b, scale):
        if t is None: leaves.append((a, b)); return
        L, R, ang = t
        d = math.pi / 2 + float(ang) * math.pi / p
        half = scale / 2
        dre = Decimal(half) * Decimal(repr(math.cos(d))); dim = Decimal(half) * Decimal(repr(math.sin(d)))
        da, db = lattice(dre, dim)
        rec(L, a - da, b - db, scale * mu)
        rec(R, a + da, b + db, scale * mu)
    rec(U, S, 0, float(S) * lam)
    with open(out, 'w') as f:
        f.write('# one-cluster rule h=%d p=%d t=%d lam=%g mu=%g S=1e%d ; sector-0 reps as coefficients of zeta^0..zeta^%d, then centre\n' % (h, p, len(leaves), lam, mu, lS, p - 1))
        f.write('%d %d %d\n' % (p, len(leaves), 1))
        for a, b in leaves:
            f.write(' '.join(str(x) for x in [a, b] + [0] * (p - 2)) + '\n')
    print('wrote', out, 'p=%d t=%d n=%d' % (p, len(leaves), p * len(leaves) + 1))
if __name__ == '__main__':
    main()
