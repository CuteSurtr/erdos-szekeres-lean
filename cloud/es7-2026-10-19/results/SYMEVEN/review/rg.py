"""Referee's own exact plane-geometry routines (written from scratch; no code shared with the author).

All arithmetic is on Python ints (or Fractions); nothing is floating point.
Points are tuples (x, y).
"""
from itertools import combinations
from functools import cmp_to_key


def orient(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def sgn(v):
    return (v > 0) - (v < 0)


def collinear_triples(pts, stop_at_first=True):
    bad = []
    n = len(pts)
    for i in range(n):
        pi = pts[i]
        for j in range(i + 1, n):
            pj = pts[j]
            for l in range(j + 1, n):
                if orient(pi, pj, pts[l]) == 0:
                    bad.append((i, j, l))
                    if stop_at_first:
                        return bad
    return bad


def strictly_inside_triangle(p, a, b, c):
    s1 = sgn(orient(a, b, p))
    s2 = sgn(orient(b, c, p))
    s3 = sgn(orient(c, a, p))
    return s1 != 0 and s1 == s2 == s3


def convex_position_bf(P):
    """Brute force (Caratheodory): a set in general position is in convex position iff no point
    lies strictly inside a triangle spanned by three other points."""
    m = len(P)
    if m <= 3:
        return True
    for i in range(m):
        others = P[:i] + P[i + 1:]
        for a, b, c in combinations(others, 3):
            if strictly_inside_triangle(P[i], a, b, c):
                return False
    return True


def max_convex_bf(pts):
    n = len(pts)
    for s in range(n, 0, -1):
        for sub in combinations(pts, s):
            if convex_position_bf(list(sub)):
                return s, list(sub)
    return 0, []


def count_convex_bf(pts, maxsize=None):
    n = len(pts)
    maxsize = n if maxsize is None else maxsize
    cnt = {}
    for s in range(3, maxsize + 1):
        c = 0
        for sub in combinations(pts, s):
            if convex_position_bf(list(sub)):
                c += 1
        cnt[s] = c
    return cnt


def sign_table(P):
    n = len(P)
    T = [[[0] * n for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if j == i:
                continue
            Tij = T[i][j]
            for l in range(n):
                if l != i and l != j:
                    Tij[l] = sgn(orient(P[i], P[j], P[l]))
    return T


def max_convex_cupcap(pts, want_witness=True):
    """Method 1: a convex polygon with leftmost a and rightmost b is a cup a->b plus a cap a->b
    (and conversely every such pair is a convex polygon). Requires distinct x-coordinates."""
    P = sorted(pts)
    n = len(P)
    assert len(set(p[0] for p in P)) == n, "distinct x required"
    if n <= 2:
        return n, list(P)
    T = sign_table(P)
    best, bestw = 2, [P[0], P[1]]
    for a in range(n):
        cup = [[0] * n for _ in range(n)]
        cap = [[0] * n for _ in range(n)]
        pcup = [[-1] * n for _ in range(n)]
        pcap = [[-1] * n for _ in range(n)]
        for j in range(a + 1, n):
            cup[a][j] = 2
            cap[a][j] = 2
        for i in range(a + 1, n):
            for j in range(i + 1, n):
                Tij = None
                bc = 0; bk = 0; ac = -1; ak = -1
                for h in range(a, i):
                    s = T[h][i][j]
                    v = cup[h][i]
                    if v and s > 0 and v + 1 > bc:
                        bc = v + 1; ac = h
                    v = cap[h][i]
                    if v and s < 0 and v + 1 > bk:
                        bk = v + 1; ak = h
                cup[i][j] = bc; pcup[i][j] = ac
                cap[i][j] = bk; pcap[i][j] = ak
        for b in range(a + 1, n):
            ic = max(range(a, b), key=lambda i: cup[i][b])
            ik = max(range(a, b), key=lambda i: cap[i][b])
            tot = cup[ic][b] + cap[ik][b] - 2
            if tot > best:
                best = tot
                if want_witness:
                    def chain(tab, ptab, i, j):
                        out = [j]
                        while True:
                            out.append(i)
                            if i == a:
                                break
                            i, j = ptab[i][j], i
                        return out[::-1]
                    w = set(chain(cup, pcup, ic, b)) | set(chain(cap, pcap, ik, b))
                    bestw = [P[t] for t in sorted(w)]
    return best, bestw


def max_convex_angular(pts):
    """Method 2: fix the lowest vertex p (lexicographically least (y,x)), sort the points above it by
    angle, and run a DP over the last edge of a counter-clockwise convex chain. Does not need
    distinct x."""
    n = len(pts)
    if n <= 2:
        return n
    best = 2
    for p in pts:
        above = [q for q in pts if (q[1], q[0]) > (p[1], p[0])]
        above.sort(key=cmp_to_key(lambda q1, q2: -sgn(orient(p, q1, q2))))
        m = len(above)
        if m < 2:
            continue
        f = [[3 if i < j else 0 for j in range(m)] for i in range(m)]
        for j in range(m):
            aj = above[j]
            for i in range(j):
                fij = f[i][j]
                ai = above[i]
                for l in range(j + 1, m):
                    if fij + 1 > f[j][l] and orient(ai, aj, above[l]) > 0:
                        f[j][l] = fij + 1
        mm = max(max(r) for r in f)
        if mm > best:
            best = mm
    return best


def count_convex_cupcap(pts, maxlen=None):
    """Method 3: exact number of subsets in convex position of each size s>=3, as the sum over
    (a,b) of (#cups a->b with i points) x (#caps a->b with j points), i+j-2=s."""
    P = sorted(pts)
    n = len(P)
    assert len(set(p[0] for p in P)) == n
    if maxlen is None:
        maxlen = n
    T = sign_table(P)
    total = {}
    for a in range(n):
        # cups[i][j] = dict length->count of cups starting at a with last edge (i,j)
        cups = [[None] * n for _ in range(n)]
        caps = [[None] * n for _ in range(n)]
        for j in range(a + 1, n):
            cups[a][j] = {2: 1}
            caps[a][j] = {2: 1}
        for i in range(a + 1, n):
            for j in range(i + 1, n):
                dc = {}; dk = {}
                for h in range(a, i):
                    s = T[h][i][j]
                    if s > 0 and cups[h][i]:
                        for L, c in cups[h][i].items():
                            dc[L + 1] = dc.get(L + 1, 0) + c
                    elif s < 0 and caps[h][i]:
                        for L, c in caps[h][i].items():
                            dk[L + 1] = dk.get(L + 1, 0) + c
                cups[i][j] = dc; caps[i][j] = dk
        for b in range(a + 1, n):
            CU = {}; CA = {}
            for i in range(a, b):
                for L, c in (cups[i][b] or {}).items():
                    CU[L] = CU.get(L, 0) + c
                for L, c in (caps[i][b] or {}).items():
                    CA[L] = CA.get(L, 0) + c
            for L1, c1 in CU.items():
                for L2, c2 in CA.items():
                    s = L1 + L2 - 2
                    if s >= 3:
                        total[s] = total.get(s, 0) + c1 * c2
    return dict(sorted(total.items()))


def longest_cup_cap(pts):
    P = sorted(pts)
    n = len(P)
    assert len(set(p[0] for p in P)) == n
    if n <= 2:
        return n, n
    cup = [[2] * n for _ in range(n)]
    cap = [[2] * n for _ in range(n)]
    bc = bk = 2
    for j in range(n):
        for i in range(j):
            for h in range(i):
                o = orient(P[h], P[i], P[j])
                if o > 0 and cup[h][i] + 1 > cup[i][j]:
                    cup[i][j] = cup[h][i] + 1
                elif o < 0 and cap[h][i] + 1 > cap[i][j]:
                    cap[i][j] = cap[h][i] + 1
            bc = max(bc, cup[i][j]); bk = max(bk, cap[i][j])
    return bc, bk


def read_points(path):
    pts = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            t = line.split()
            pts.append(tuple(int(v) for v in t))
    return pts
