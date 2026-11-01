"""Referee's own implementation of the construction exactly as WRITTEN in PROOF.md Section 3
(not the author's integer variant in construct.py):

  B_j     = q_j + (eps*g_x, eps^2*g_y), g in G_j = G(j+2, k-j)      (j < n/2)
  B_{n-j} = -B_j
  B_{n/2} = eps^2 * M_0     (M_0 from Lemma 2 with m = k/2)
  q_j = (x_j, x_j^3), x = -(n-1),...,-3,-1,0,1,3,...,n-1

eps = 1/E (E integer).  Everything is multiplied by E^4 * D (D a common denominator) so that all
coordinates are integers; this is a uniform positive scaling, so it changes no orientation, slope,
cup, cap or convexity, and it maps x(p)+x(r)=0 to itself.
"""
from fractions import Fraction
from math import comb, lcm
from rg import orient, longest_cup_cap, collinear_triples


def slopes(P):
    out = []
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            dx = P[j][0] - P[i][0]
            assert dx != 0
            out.append(Fraction(P[j][1] - P[i][1], dx))
    return out


def G(a, b):
    """No a-cup, no b-cap, C(a+b-4, a-2) points; integer coordinates, distinct x (Lemma 1)."""
    if a == 2 or b == 2:
        return [(0, 0)]
    L = G(a - 1, b)
    R = G(a, b - 1)
    sx = max(p[0] for p in L) + 1 - min(p[0] for p in R)
    R = [(x + sx, y) for (x, y) in R]
    s = max(slopes(L) + slopes(R) + [Fraction(0)])          # largest inside slope
    need = max(s * (x2 - x1) - (y2 - y1) for (x1, y1) in L for (x2, y2) in R)
    D = int(need // 1) + 1                                  # D > need
    R = [(x, y + D) for (x, y) in R]
    out = sorted(L + R)
    return out


def check_G(a, b, P):
    lc, lk = longest_cup_cap(P)
    assert len(P) == comb(a + b - 4, a - 2), (a, b, len(P))
    assert len(set(p[0] for p in P)) == len(P)
    assert not collinear_triples(P)
    assert lc <= a - 1 and lk <= b - 1, (a, b, lc, lk)
    return lc, lk


def middle_set(m):
    """Lemma 2: returns (M0 as list of Fraction points, t used)."""
    X = G(m, m + 1)
    check_G(m, m + 1, X)
    T = 1
    while True:
        t = Fraction(1, T)
        Xt = [(-4 + t * gx, -1 + t * t * gy) for (gx, gy) in X]
        M0 = Xt + [(-x, -y) for (x, y) in Xt]
        if not all(x < 0 for (x, y) in Xt):
            T *= 2
            continue
        ins = slopes(Xt)
        btw = [Fraction(q[1] - p[1], q[0] - p[0]) for p in Xt for q in [(-x, -y) for (x, y) in Xt]]
        ok = (all(-Fraction(1, 8) < s < Fraction(1, 8) for s in ins)
              and all(Fraction(1, 8) < s < Fraction(3, 8) for s in btw)
              and all(x < 0 for (x, y) in Xt)
              and all(abs(v) < abs(u) / 2 for (u, v) in M0))
        if ok:
            return M0, t
        T *= 2


def verify_middle(m, M0):
    """Re-verify every claimed property of M0 directly (independently of how it was built)."""
    S = set(M0)
    rep = {}
    rep['symmetric'] = all((-x, -y) in S for (x, y) in M0)
    rep['zero_not_in'] = (0, 0) not in S
    rep['size_ok'] = len(M0) == comb(2 * m - 2, m - 1) == len(S)
    rep['distinct_x'] = len(set(p[0] for p in M0)) == len(M0)
    rep['general_position'] = not collinear_triples(M0)
    lc, lk = longest_cup_cap(M0)
    rep['longest_cup_cap'] = (lc, lk)
    rep['no_m+1_cup_cap'] = lc <= m and lk <= m
    sl = slopes(sorted(M0))
    rep['slopes_in_(-1/2,1/2)'] = all(-Fraction(1, 2) < s < Fraction(1, 2) for s in sl)
    rep['|v|<|u|/2'] = all(abs(v) < abs(u) / 2 for (u, v) in M0)
    return rep


def base_abscissae(k):
    n = k - 2
    xs = []
    for j in range(n + 1):
        if j < n // 2:
            xs.append(2 * j - n + 1)
        elif j == n // 2:
            xs.append(0)
        else:
            xs.append(2 * j - n - 1)
    return xs


def to_int(clusters):
    D = 1
    for B in clusters:
        for (x, y) in B:
            D = lcm(D, Fraction(x).denominator, Fraction(y).denominator)
    return [[(int(x * D), int(y * D)) for (x, y) in B] for B in clusters], D


def build(k, E, mid_scale_pow=2, normalize=True, base=None, mid_factor=1):
    """Clusters of S_eps with eps = 1/E.  mid_scale_pow=2 is the written construction (eps^2 M0);
    mid_scale_pow=1 puts the middle cluster at the outer clusters' scale (negative control).
    base: optional list of base abscissae (default: the proof's odd-plus-zero abscissae)."""
    n = k - 2
    m = k // 2
    xs = base_abscissae(k) if base is None else base
    eps = Fraction(1, E)
    Gs = {}
    for j in range(n // 2):
        P = G(j + 2, k - j)
        check_G(j + 2, k - j, P)
        if normalize and len(P) > 1:
            w = max(p[0] for p in P) - min(p[0] for p in P)
            h = max(p[1] for p in P) - min(p[1] for p in P)
            x0 = min(p[0] for p in P); y0 = min(p[1] for p in P)
            P = [(Fraction(x - x0, w), Fraction(y - y0, h) if h else Fraction(0)) for (x, y) in P]
        Gs[j] = P
    M0, t = middle_set(m)
    clusters = [None] * (n + 1)
    for j in range(n // 2):
        q = (Fraction(xs[j]), Fraction(xs[j]) ** 3)
        Bj = [(q[0] + eps * gx, q[1] + eps * eps * gy) for (gx, gy) in Gs[j]]
        clusters[j] = Bj
        clusters[n - j] = [(-x, -y) for (x, y) in Bj]
    sc = eps ** mid_scale_pow * mid_factor
    clusters[n // 2] = [(sc * x, sc * y) for (x, y) in M0]
    clusters, D = to_int(clusters)
    return clusters, dict(k=k, E=E, t=t, D=D, xs=xs, M0=M0, Gs=Gs)
