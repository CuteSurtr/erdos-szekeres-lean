"""Independent pure-Python check of a real (6,6;8)-set and of its level sets E (ends of 5-cups), A (ends of
5-caps), X: integers only, no C library.  usage: verify_levels.py <points.json | jsonl line index file> """
import sys, json, itertools
def check(P):
    P = sorted(tuple(p) for p in P); n = len(P)
    assert len({p[0] for p in P}) == n
    det = lambda i, j, k: (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
    sg = {}
    for t in itertools.combinations(range(n), 3):
        d = det(*t); assert d != 0; sg[t] = 1 if d > 0 else -1
    Em = {}; Ep = {}
    for v in range(n):
        for u in range(v):
            em = ep = 2
            for t in range(u):
                if sg[t, u, v] < 0: em = max(em, Em[t, u] + 1)
                else: ep = max(ep, Ep[t, u] + 1)
            Em[u, v] = em; Ep[u, v] = ep
    assert max(Em.values()) <= 5 and max(Ep.values()) <= 5, 'has a 6-cap or a 6-cup'
    # octagon test: 5-cap and 5-cup with common endpoints
    for s in range(n):
        Dc = {}; Du = {}
        for j in range(s + 1, n): Dc[s, j] = 2; Du[s, j] = 2
        for j in range(s + 1, n):
            for i in range(s + 1, j):
                bc = bu = 0
                for h in range(s, i):
                    if sg[h, i, j] < 0:
                        if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                    else:
                        if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                Dc[i, j] = bc; Du[i, j] = bu
        for t in range(s + 1, n):
            assert not (max(Dc[i, t] for i in range(s, t)) >= 5 and max(Du[i, t] for i in range(s, t)) >= 5), 'octagon'
    E = {v for v in range(n) if any(Ep[u, v] >= 5 for u in range(v))}; A = {v for v in range(n) if any(Em[u, v] >= 5 for u in range(v))}
    return n, len(E), len(A), len(E & A), len(E | A)
if __name__ == '__main__':
    for fn in sys.argv[1:]:
        P = json.load(open(fn)); P = P['P'] if isinstance(P, dict) else P
        n, e, a, x, ea = check(P)
        print(f'{fn}: valid (6,6;8)-set, n = {n}, |E| = {e}, |A| = {a}, |X| = {x}, |E u A| = {ea}')
