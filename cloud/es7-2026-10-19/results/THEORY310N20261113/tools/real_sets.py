#!/usr/bin/env python3
"""Charts, minimum-slope partitions and level sets of real 64-point octagon-free sets.
Exact rational arithmetic.  For each hull vertex a of S: chart P = Phi_a(S - a),
partition U/L by minimum slope, junctions G (6-cup ending + 5-cap starting inside U),
H = L + G, R = U - G; then level sets H6 (6-cup of H ends), R6 (6-cup of R ends), R7;
checks Lemma A/B and records sizes."""
import sys, glob, itertools, json
from fractions import Fraction as Fr

def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])

def hull(P):
    pts = sorted(set(P))
    def half(seq):
        h = []
        for p in seq:
            while len(h) >= 2 and orient(h[-2], h[-1], p) <= 0:
                h.pop()
            h.append(p)
        return h
    lo = half(pts); up = half(pts[::-1])
    return lo[:-1] + up[:-1]

def chart(S, a):
    others = [p for p in S if p != a]
    # direction d with (p-a).d > 0 for all others: sum of inward normals of the two hull edges
    H = hull(S); k = H.index(a); prev = H[k-1]; nxt = H[(k+1) % len(H)]
    e1 = (prev[0]-a[0], prev[1]-a[1]); e2 = (nxt[0]-a[0], nxt[1]-a[1])
    c = e1[0]*e2[1] - e1[1]*e2[0]
    n1 = (-e1[1], e1[0]) if c > 0 else (e1[1], -e1[0])
    n2 = (-e2[1], e2[0]) if c < 0 else (e2[1], -e2[0])
    d = (n1[0] + n2[0], n1[1] + n2[1])
    assert all((p[0]-a[0])*d[0] + (p[1]-a[1])*d[1] > 0 for p in others), 'bad direction'
    dp = (-d[1], d[0])  # (d, dp) positively oriented
    pts = []
    for p in others:
        x = (p[0]-a[0])*d[0] + (p[1]-a[1])*d[1]
        y = (p[0]-a[0])*dp[0] + (p[1]-a[1])*dp[1]
        pts.append((Fr(y, x), Fr(-1, x)))
    pts.sort()
    assert len({p[0] for p in pts}) == len(pts)
    return pts

def chains(P, idx):
    """For index subset idx (sorted), longest cup/cap ending at / starting with pairs."""
    idx = sorted(idx); n = len(idx)
    cupE = {}; capE = {}; cupS = {}; capS = {}
    for j in range(n):
        for i in range(j):
            u, v = idx[i], idx[j]
            cupE[u, v] = 1 + max([cupE[x, u] for x in idx[:i] if orient(P[x], P[u], P[v]) > 0] + [1])
            capE[u, v] = 1 + max([capE[x, u] for x in idx[:i] if orient(P[x], P[u], P[v]) < 0] + [1])
    for i in range(n-1, -1, -1):
        for j in range(n-1, i, -1):
            u, v = idx[i], idx[j]
            cupS[u, v] = 1 + max([cupS[v, y] for y in idx[j+1:] if orient(P[u], P[v], P[y]) > 0] + [1])
            capS[u, v] = 1 + max([capS[v, y] for y in idx[j+1:] if orient(P[u], P[v], P[y]) < 0] + [1])
    endcup = {v: max([cupE[u, v] for u in idx if u < v] + [1]) for v in idx}
    endcap = {v: max([capE[u, v] for u in idx if u < v] + [1]) for v in idx}
    startcup = {u: max([cupS[u, v] for v in idx if v > u] + [1]) for u in idx}
    startcap = {u: max([capS[u, v] for v in idx if v > u] + [1]) for u in idx}
    longcup = max(list(endcup.values()) + [0]); longcap = max(list(endcap.values()) + [0])
    return endcup, endcap, startcup, startcap, longcup, longcap

def analyse(S):
    out = []
    for a in hull(S):
        P = chart(S, a); n = len(P)
        m = {}
        for u in range(n):
            best = None
            for v in range(n):
                if v == u: continue
                s = (P[v][1]-P[u][1]) / (P[v][0]-P[u][0])
                if best is None or s < best[0]:
                    best = (s, v)
            m[u] = best[1]
        U = [u for u in range(n) if m[u] > u]; L = [u for u in range(n) if m[u] < u]
        ecU, _, _, scU, _, _ = chains(P, U)
        G = [u for u in U if ecU[u] >= 6 and scU[u] >= 5]
        H = sorted(L + G); R = [u for u in U if u not in G]
        ecH, eaH, scH, saH, lcH, laH = chains(P, H)
        ecR, eaR, scR, saR, lcR, laR = chains(P, R)
        assert laH <= 6 and lcH <= 6, 'H not balanced'
        assert laR <= 5, 'R has 6-cap'
        H6 = [v for v in H if ecH[v] >= 6]; Hlow = [v for v in H if ecH[v] < 6]
        R6 = [v for v in R if ecR[v] >= 6]; R7 = [v for v in R if ecR[v] >= 7]; Rlow = [v for v in R if ecR[v] < 6]
        chk = {
            'H6_no6cap': chains(P, H6)[5] <= 5 if H6 else True,
            'Hlow_no6cup': chains(P, Hlow)[4] <= 5 if Hlow else True,
            'R6_no5cap': chains(P, R6)[5] <= 4 if R6 else True,
            'Rlow_no6cup': chains(P, Rlow)[4] <= 5 if Rlow else True,
            'R7_no4cap_start': all(saR[v] <= 3 for v in R7),
        }
        out.append({'root': a, 'n': n, 'U': len(U), 'L': len(L), 'G': len(G), 'H': len(H), 'R': len(R),
                    'H6': len(H6), 'R6': len(R6), 'R7': len(R7), 'longcupH': lcH, 'longcapH': laH,
                    'longcupR': lcR, 'longcapR': laR, 'checks': chk})
    return out

if __name__ == '__main__':
    files = sys.argv[1:]
    allres = {}
    for f in files:
        lines = [l.split() for l in open(f).read().split('\n') if l.strip()]
        if len(lines[0]) == 1:
            lines = lines[1:]
        S = [(int(x), int(y)) for x, y in lines]
        res = analyse(S)
        allres[f] = res
        for r in res:
            print(f.split('/')[-1], {k: v for k, v in r.items() if k != 'checks'}, 'checks ok' if all(r['checks'].values()) else r['checks'], flush=True)
    json.dump(allres, open('real_sets_out.json', 'w'), indent=1, default=str)
