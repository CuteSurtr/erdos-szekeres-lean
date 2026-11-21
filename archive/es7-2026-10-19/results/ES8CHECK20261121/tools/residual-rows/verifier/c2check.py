#!/usr/bin/env python3
"""Independent exact controls for candidate C2 (forward-cap lemma).

All geometric predicates use Python integers only (orientation determinants and
cross-multiplied slope comparisons).  Definitions follow math.md 2.1-2.2 and
ResidualStates.column / ResidualRanks.labels:
  d1(u,v) = 6 - F-(u,v)   (F- = longest cap STARTING with the pair (u,v))
  d2(u,v) = E+(u,v) - 1   (E+ = longest cup ENDING with the pair (u,v))
  f_a(v)  = max{ d2(u,v) : u < v, d1(u,v) >= a }  (0 if empty), a = 1..4
Checks, for every configuration with no 6-cap and no 8-cup:
  (P1) v = first point: state (0,0,0,0)
  (P2) v > first: #{a : f_a(v) >= 1} == 6 - m(v), m(v) = min_{u<v} F-(u,v)
  (P3) longest cap ending at v <= 7 - m(v)   (and record equality = sharpness)
  (P4) owners of {f4 = 0} have no 5-cap; owners of {f3 = 0} have no 4-cap
  (P5) states lie in the 154-state catalog (antitone, f1<6 or f2=6) -- only if no junction
"""
import sys, json, random
from math import lcm
from fractions import Fraction


def orient(p, q, r):
    return (q[0] - p[0]) * (r[1] - p[1]) - (q[1] - p[1]) * (r[0] - p[0])


def tables(P):
    n = len(P)
    capE, cupE, capS, cupS = {}, {}, {}, {}
    for v in range(n):
        for u in range(v):
            bc = 1
            bu = 1
            for x in range(u):
                o = orient(P[x], P[u], P[v])
                if o < 0:
                    if capE[x, u] > bc:
                        bc = capE[x, u]
                elif o > 0:
                    if cupE[x, u] > bu:
                        bu = cupE[x, u]
                else:
                    raise ValueError('collinear triple')
            capE[u, v] = bc + 1
            cupE[u, v] = bu + 1
    for u in range(n - 1, -1, -1):
        for v in range(n - 1, u, -1):
            bc = 1
            bu = 1
            for y in range(v + 1, n):
                o = orient(P[u], P[v], P[y])
                if o < 0:
                    if capS[v, y] > bc:
                        bc = capS[v, y]
                elif o > 0:
                    if cupS[v, y] > bu:
                        bu = cupS[v, y]
            capS[u, v] = bc + 1
            cupS[u, v] = bu + 1
    return capE, cupE, capS, cupS


def longest(P, which):
    if len(P) < 2:
        return len(P)
    capE, cupE, _, _ = tables(P)
    t = capE if which == 'cap' else cupE
    return max(t.values())


def find_chain(P, k, which):
    """return index list of a k-chain (cap or cup) if one exists, else None"""
    n = len(P)
    capE, cupE, _, _ = tables(P)
    t = capE if which == 'cap' else cupE
    sgn = -1 if which == 'cap' else 1
    for (u, v), L in t.items():
        if L >= k:
            # backtrack a chain of length L ending (u,v), then keep the last k
            ch = [v, u]
            a, b = u, v
            while t[a, b] > 2:
                for x in range(a):
                    if orient(P[x], P[a], P[b]) * sgn > 0 and t[x, a] == t[a, b] - 1:
                        ch.append(x)
                        a, b = x, a
                        break
                else:
                    raise RuntimeError('backtrack failed')
            ch.reverse()
            return ch[-k:]
    return None


def analyse(P, tag, stats, want_catalog=True):
    n = len(P)
    assert all(P[i][0] < P[i + 1][0] for i in range(n - 1)), 'x not strictly increasing'
    capE, cupE, capS, cupS = tables(P)
    longcap = max(capE.values()) if n > 1 else 1
    longcup = max(cupE.values()) if n > 1 else 1
    assert longcap <= 5 and longcup <= 7, (tag, longcap, longcup)
    endcup = [max([cupE[u, v] for u in range(v)] + [1]) for v in range(n)]
    startcap = [max([capS[u, w] for w in range(u + 1, n)] + [1]) for u in range(n)]
    junction = any(endcup[v] >= 6 and startcap[v] >= 5 for v in range(n))
    st = []
    fails = []
    for v in range(n):
        f = [0, 0, 0, 0]
        for u in range(v):
            d1 = 6 - capS[u, v]
            d2 = cupE[u, v] - 1
            assert 1 <= d1 <= 4 and 1 <= d2 <= 6
            for a in range(1, d1 + 1):
                if d2 > f[a - 1]:
                    f[a - 1] = d2
        st.append(tuple(f))
        if v == 0:
            if tuple(f) != (0, 0, 0, 0):
                fails.append(('P1', v, f))
            continue
        m = min(capS[u, v] for u in range(v))
        cnt = sum(1 for x in f if x >= 1)
        stats['points'] += 1
        stats['m_hist'][m] = stats['m_hist'].get(m, 0) + 1
        if cnt != 6 - m:
            fails.append(('P2', v, f, m))
        capend = max(capE[u, v] for u in range(v))
        if capend > 7 - m:
            fails.append(('P3', v, capend, m))
        if capend == 7 - m:
            stats['P3_equal'] += 1
            stats['P3_equal_by_m'][m] = stats['P3_equal_by_m'].get(m, 0) + 1
    if want_catalog and not junction:
        for f in st:
            if not (f[0] >= f[1] >= f[2] >= f[3] and (f[0] < 6 or f[1] == 6)):
                fails.append(('P5', f))
        if len(set(st)) != n:
            fails.append(('P5-injective',))
    O4 = [v for v in range(n) if st[v][3] == 0]
    O3 = [v for v in range(n) if st[v][2] == 0]
    c4 = longest([P[v] for v in O4], 'cap')
    c3 = longest([P[v] for v in O3], 'cap')
    if c4 >= 5:
        fails.append(('P4-O4', c4))
    if c3 >= 4:
        fails.append(('P4-O3', c3))
    stats['configs'] += 1
    stats['residual_like'] += (0 if junction else 1)
    stats['maxcap_O4_hist'][c4] = stats['maxcap_O4_hist'].get(c4, 0) + 1
    stats['maxcap_O3_hist'][c3] = stats['maxcap_O3_hist'].get(c3, 0) + 1
    stats['longcap_hist'][longcap] = stats['longcap_hist'].get(longcap, 0) + 1
    if fails:
        stats['fail_configs'] += 1
        stats['fail_examples'].append((tag, fails[:5]))
    return dict(n=n, junction=junction, longcap=longcap, longcup=longcup, O4=len(O4), O3=len(O3),
                maxcap_O4=c4, maxcap_O3=c3, fails=len(fails), states=st)


def newstats():
    return dict(configs=0, residual_like=0, points=0, m_hist={}, P3_equal=0, P3_equal_by_m={},
                maxcap_O4_hist={}, maxcap_O3_hist={}, longcap_hist={}, fail_configs=0, fail_examples=[])


# ---------------- real sets: charts and min-slope partition (integer version) ----------------

def hull(S):
    pts = sorted(set(S))

    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h
    lo = half(pts)
    up = half(pts[::-1])
    return lo[:-1] + up[:-1]


def chart_int(S, a):
    """Same chart as THEORY310N tools/real_sets.py chart(): point (y/x, -1/x), scaled by
    L = lcm of all x > 0 so that all coordinates are integers (positive scaling keeps
    every orientation sign and the x-order)."""
    others = [p for p in S if p != a]
    H = hull(S)
    k = H.index(a)
    prev = H[k - 1]
    nxt = H[(k + 1) % len(H)]
    e1 = (prev[0] - a[0], prev[1] - a[1])
    e2 = (nxt[0] - a[0], nxt[1] - a[1])
    c = e1[0] * e2[1] - e1[1] * e2[0]
    n1 = (-e1[1], e1[0]) if c > 0 else (e1[1], -e1[0])
    n2 = (-e2[1], e2[0]) if c < 0 else (e2[1], -e2[0])
    d = (n1[0] + n2[0], n1[1] + n2[1])
    xs = []
    for p in others:
        x = (p[0] - a[0]) * d[0] + (p[1] - a[1]) * d[1]
        y = (p[0] - a[0]) * (-d[1]) + (p[1] - a[1]) * d[0]
        assert x > 0
        xs.append((x, y))
    L = 1
    for x, _ in xs:
        L = lcm(L, x)
    pts = sorted(((y * (L // x), -(L // x)) for x, y in xs))
    assert len({p[0] for p in pts}) == len(pts)
    return pts


def slope_less(P, u, v, w, z):
    """slope(u,v) < slope(w,z), exact (denominators made positive)."""
    a1 = P[v][1] - P[u][1]
    b1 = P[v][0] - P[u][0]
    a2 = P[z][1] - P[w][1]
    b2 = P[z][0] - P[w][0]
    if b1 < 0:
        a1, b1 = -a1, -b1
    if b2 < 0:
        a2, b2 = -a2, -b2
    return a1 * b2 < a2 * b1


def residual_part(P):
    n = len(P)
    mnb = {}
    for u in range(n):
        best = None
        for v in range(n):
            if v == u:
                continue
            if best is None or slope_less(P, u, v, u, best):
                best = v
        mnb[u] = best
    U = [u for u in range(n) if mnb[u] > u]
    Q = [P[u] for u in U]
    capE, cupE, capS, cupS = tables(Q)
    m = len(Q)
    endcup = [max([cupE[i, j] for i in range(j)] + [1]) for j in range(m)]
    startcap = [max([capS[i, j] for j in range(i + 1, m)] + [1]) for i in range(m)]
    G = [i for i in range(m) if endcup[i] >= 6 and startcap[i] >= 5]
    R = [Q[i] for i in range(m) if i not in G]
    return R, len(U), len(G)


def main():
    out = {}
    base = sys.argv[1]
    # 1. the 57-point residual set of THEORY310N (chart points as rationals)
    d = json.load(open(base + '/archive/es7-2026-10-19/results/THEORY310N20261113/data/residual57_points.json'))
    pts = [(Fraction(x), Fraction(y)) for x, y in d['R_chart_points']]
    Lx = 1
    Ly = 1
    for x, y in pts:
        Lx = lcm(Lx, x.denominator)
        Ly = lcm(Ly, y.denominator)
    P57 = sorted((int(x * Lx), int(y * Ly)) for x, y in pts)
    s57 = newstats()
    r57 = analyse(P57, 'residual57', s57)
    # exhibit a 4-cap among the {f4=0} owners (sharpness) and the cap-length statistics
    O4pts = [P57[v] for v in range(len(P57)) if r57['states'][v][3] == 0]
    ex4 = find_chain(O4pts, 4, 'cap')
    out['residual57'] = dict(n=r57['n'], junction=r57['junction'], longcap=r57['longcap'], longcup=r57['longcup'],
                            O4=r57['O4'], O3=r57['O3'], maxcap_O4=r57['maxcap_O4'], maxcap_O3=r57['maxcap_O3'],
                            fails=r57['fails'], stats=s57, distinct_states=len(set(r57['states'])),
                            O4_4cap_example_found=ex4 is not None)
    print('residual57', {k: v for k, v in out['residual57'].items() if k != 'stats'}, flush=True)
    print('  stats', s57, flush=True)
    # 2. residual parts of every chart of the 64-point octagon-free sets in the repo
    files = [base + '/experiments/es8-lower-bound-search-2026-10-11/saturation/witness8.txt']
    import glob
    files += sorted(glob.glob(base + '/experiments/es8-lower-bound-search-2026-10-11/family/sets/*.txt'))
    sreal = newstats()
    rows = []
    for fn in files:
        S = [tuple(map(int, l.split())) for l in open(fn) if l.strip() and len(l.split()) == 2]
        for a in hull(S):
            P = chart_int(S, a)
            R, nU, nG = residual_part(P)
            r = analyse(R, (fn.split('/')[-1], a), sreal)
            rows.append(dict(file=fn.split('/')[-1], root=a, U=nU, G=nG, R=len(R), junction=r['junction'],
                             O4=r['O4'], O3=r['O3'], maxcap_O4=r['maxcap_O4'], maxcap_O3=r['maxcap_O3'],
                             longcap=r['longcap'], fails=r['fails']))
            print(rows[-1], flush=True)
    out['real_charts'] = dict(charts=len(rows), stats=sreal, rows=rows)
    print('real charts stats', sreal, flush=True)
    json.dump(out, open(sys.argv[2], 'w'), indent=1, default=str)


if __name__ == '__main__':
    main()
