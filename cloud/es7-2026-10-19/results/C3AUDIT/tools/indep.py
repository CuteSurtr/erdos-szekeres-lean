"""Independent exact test of the C3-S node cover.  Own generator (integer lattice, R = A of order 3,
A = [[0,-1],[1,-1]], conjugate to +120 deg by an orientation-preserving linear map), own frames
(all 2n positions/orientations of l), own labelling, sigma, convex layers, node names.
Uses from the repo only: C3Enc literal maps (E.ccw / E.sig / E.T / E.s), and for comparison
hullcase.tree_children / layer_clauses (the thing under test)."""
import sys, random, itertools, json
sys.path.insert(0, "/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3a")
sys.path.insert(0, "/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3-S/tools")
from c3cnf import C3Enc
import hullcase as HC

A = lambda p: (-p[1], p[0] - p[1])
Mref = lambda p: (p[1], p[0])            # M A M = A^-1, det -1
cross = lambda a, b: a[0] * b[1] - a[1] * b[0]
def orient(p, q, r): return cross((q[0]-p[0], q[1]-p[1]), (r[0]-p[0], r[1]-p[1]))

def gen(m, rng, scale):
    pts = []
    for _ in range(m):
        rad = rng.choice(scale)
        p = (rng.randint(-rad, rad), rng.randint(-rad, rad))
        pts += [p, A(p), A(A(p))]
    return pts

def general(S):
    if any(p == (0, 0) for p in S) or len(set(S)) != len(S): return False
    for p, q in itertools.combinations(S, 2):
        if cross(p, q) == 0: return False          # collinear with c
    for p, q, r in itertools.combinations(S, 3):
        if orient(p, q, r) == 0: return False
    return True

def hull(P):
    P = sorted(P)
    def half(P):
        h = []
        for p in P:
            while len(h) >= 2 and orient(h[-2], h[-1], p) <= 0: h.pop()
            h.append(p)
        return h
    lo, up = half(P), half(P[::-1])
    return lo[:-1] + up[:-1]

def layers(S):
    P = list(S); out = []
    while P:
        H = hull(P) if len(P) > 2 else P
        out.append(set(H)); P = [p for p in P if p not in out[-1]]
    return out

def frames(S):
    """all frames: direction d of the upward y-axis strictly between lines through c.  Directions:
    the 2n rays +-p sorted by angle; d = bisector-ish of consecutive rays (exact: sum of unit-free
    representatives works since consecutive rays span < 180 deg)."""
    rays = [p for p in S] + [(-p[0], -p[1]) for p in S]
    import functools
    def half_(v): return 0 if (v[1] > 0 or (v[1] == 0 and v[0] > 0)) else 1
    rays.sort(key=functools.cmp_to_key(lambda a, b: (half_(a) - half_(b)) or (-1 if cross(a, b) > 0 else 1)))
    out = []
    for i in range(len(rays)):
        a, b = rays[i], rays[(i + 1) % len(rays)]
        # direction strictly between a and b (ccw from a): a*|b|^2-ish not exact; use a+b scaled ints
        na, nb = a[0]**2 + a[1]**2, b[0]**2 + b[1]**2
        # a*nb^.5 + b*na^.5 is the true bisector; any positive combination works: use a*nb + b*na
        out.append((a[0]*nb + b[0]*na, a[1]*nb + b[1]*na))
    return out

def labelling(S, d):
    """sigma = [x<0] = point left of the upward axis d; labels by ccw order of q = +-p in the right half."""
    import functools
    sig = {p: int(cross(d, p) > 0) for p in S}
    q = {p: (p if not sig[p] else (-p[0], -p[1])) for p in S}
    order = sorted(S, key=functools.cmp_to_key(lambda a, b: -1 if cross(q[a], q[b]) > 0 else 1))
    lab = {p: i for i, p in enumerate(order)}
    return lab, sig, order

def node_of(S, d, m):
    lab, sig, order = labelling(S, d)
    n = 3 * m
    for p in S:  # check R convention
        assert lab[A(p)] == (lab[p] - m) % n, "R convention"
    s = [sig[order[r]] for r in range(m)]
    for i, p in enumerate(order):  # sigma convention
        r, w = i % m, i // m
        assert sig[p] == (1 - s[r] if w == 1 else s[r]), "sigma convention"
    if s[0] != 0: return None, lab, sig, order
    Ls = layers(S); name = []
    for j, L in enumerate(Ls):
        res = sorted({lab[p] % m for p in L})
        if len(L) not in (3, 6): return "BIG", lab, sig, order
        if j == 0:
            if 0 not in res: return None, lab, sig, order
            if len(res) == 2:
                a = res[1]
                if a > m // 2: return None, lab, sig, order
                name.append(f"0s0-{a}s{s[a]}")
            else: name.append("0s0")
        else:
            name.append(str(res[0]) if len(res) == 1 else f"{res[0]}s{s[res[0]]}-{res[1]}s{s[res[1]]}")
    return "_".join(name), lab, sig, order

def in_tree(m, k, name, kept):
    L = HC.parse_layers(name); cur = []
    for j in range(len(L)):
        ch = [HC.layers_name(c) for c in HC.tree_children(m, k, cur, mirror=True)]
        nm = HC.layers_name(L[:j + 1])
        if nm not in ch: return False, nm
        cur = L[:j + 1]
    return True, None

def truth(E, lab, sig, order, m):
    """true value of each T and s variable; checks orbit consistency of the T literal map."""
    val = {}
    for t, l in E.T.items():
        o = orient(order[t[0]], order[t[1]], order[t[2]]) > 0
        v, b = abs(l), (o if l > 0 else not o)
        assert val.setdefault(v, b) == b, "T orbit inconsistent"
    for r in range(m):
        val[E.s[r]] = bool(sig[order[r]])
    return val

def lit_true(val, l): return val[abs(l)] if l > 0 else not val[abs(l)]

def has_kgon(S, k):
    for Q in itertools.combinations(S, k):
        if len(hull(list(Q))) == k: return True
    return False
