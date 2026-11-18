"""Describe the real no-split FL(5,5) sets: states (3x3 box), levels, weak (one-sided) splits, symmetric images."""
import sys, json, itertools
def describe(P):
    P = sorted(tuple(p) for p in P); n = len(P)
    det = lambda i, j, k: (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
    sg = {t: (1 if det(*t) > 0 else -1) for t in itertools.combinations(range(n), 3)}
    Em = {}; Ep = {}; st = []
    for v in range(n):
        f = [0, 0, 0]
        for u in range(v):
            em = ep = 2
            for t in range(u):
                if sg[t, u, v] < 0: em = max(em, Em[t, u] + 1)
                else: ep = max(ep, Ep[t, u] + 1)
            Em[u, v] = em; Ep[u, v] = ep
            for c in range(em - 1): f[c] = max(f[c], ep - 1)
        st.append(tuple(f))
    E = {v for v in range(n) if st[v][0] == 3}; A = {v for v in range(n) if st[v][2] >= 1}
    def chains(L, s): return [idx for idx in itertools.combinations(range(n), L) if all(sg[idx[q], idx[q+1], idx[q+2]] == s for q in range(L - 2))]
    caps4 = chains(4, -1); cups4 = chains(4, 1); caps3 = chains(3, -1); cups3 = chains(3, 1)
    m = lambda s: sum(1 << p for p in s)
    def gons(caps, cups):
        by = {}
        for c in cups: by.setdefault((c[0], c[-1]), []).append(c)
        return [m(set(c) | set(u)) for c in caps for u in by.get((c[0], c[-1]), [])]
    cap1 = [m(c) for c in caps4]; cup1 = [m(c) for c in cups4]; g1 = gons(caps3, cups4); g2 = gons(caps4, cups3)
    full = (1 << n) - 1; inside = lambda S, L: any(x & S == x for x in L)
    strong = w1 = w2 = 0
    for S1 in range(1 << n):
        S2 = full ^ S1
        f1 = not inside(S1, cap1) and not inside(S1, g1); f2 = not inside(S2, cup1) and not inside(S2, g2)
        strong += f1 and f2; w1 += f1 and not inside(S2, cup1); w2 += (not inside(S1, cap1)) and f2
    return {'states': ' '.join(''.join(map(str, f)) for f in st), 'E': len(E), 'A': len(A), 'X': len(E & A), 'EuA': len(E | A),
            'strong_splits': strong, 'one_sided_S1_in_FL45': w1, 'one_sided_S2_in_FL54': w2}
for line in open(sys.argv[1]):
    d = json.loads(line); r = describe(d['P']); print('record', d.get('record'), r, flush=True)
