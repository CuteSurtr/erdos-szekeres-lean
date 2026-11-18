"""Canonical candidates for the Pascal split of an FL(a,b)-configuration (abstract signotope or real set).
D_greedyL : left-to-right greedy transversal of the (b-1)-cups: v in D iff a (b-1)-cup ends at v whose other points
            are outside D.   (S \\ D has no (b-1)-cup;  D is contained in E, hence has no (a-1)-cap.)
D_E       : E = all ends of (b-1)-cups.
Reports whether D is free of ((a-2)-cap,(b-1)-cup)-gons (then D is in FL(a-1,b)), and whether S \\ D is free of
((a-1)-cap,(b-2)-cup)-gons (then S \\ D is in FL(a,b-1)): 'strong' = both."""
import sys, json, itertools, os, random
from split import sig_fn, pts_fn

def cup_ends(n, f, L, allowed):
    """Ep over allowed points only; returns dict v -> longest cup ending at v within allowed (v in allowed)"""
    pts = [p for p in range(n) if allowed[p]]
    Ep = {}; best = {p: 1 for p in pts}
    for vi, v in enumerate(pts):
        for u in pts[:vi]:
            e = 2
            for t in pts:
                if t >= u: break
                if f(t, u, v) > 0 and Ep[t, u] + 1 > e: e = Ep[t, u] + 1
            Ep[u, v] = e
            if e > best[v]: best[v] = e
    return best

def greedy_left(n, f, b):
    inD = [False] * n
    # incremental: Ep over non-D points; when v is processed all earlier decisions are final
    Ep = {}
    for v in range(n):
        longest = 1
        for u in range(v):
            if inD[u]: continue
            e = 2
            for t in range(u):
                if inD[t]: continue
                if f(t, u, v) > 0 and Ep[t, u] + 1 > e: e = Ep[t, u] + 1
            Ep[u, v] = e
            longest = max(longest, e)
        if longest >= b - 1: inD[v] = True
    return [v for v in range(n) if inD[v]]

def types(pts, f):
    m = len(pts); out = set()
    for s in range(m):
        Dc = {}; Du = {}
        for j in range(s + 1, m): Dc[s, j] = 2; Du[s, j] = 2
        for j in range(s + 1, m):
            for i in range(s + 1, j):
                bc = bu = 0
                for h in range(s, i):
                    if f(pts[h], pts[i], pts[j]) < 0:
                        if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                    else:
                        if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                Dc[i, j] = bc; Du[i, j] = bu
        for t in range(s + 1, m):
            out.add((max(Dc[i, t] for i in range(s, t)), max(Du[i, t] for i in range(s, t))))
    return out

def test(n, f, a, b):
    res = {}
    full = [True] * n
    be = cup_ends(n, f, b, full)
    E = [v for v in range(n) if be[v] >= b - 1]
    G = greedy_left(n, f, b)
    for nm, D in (('E', E), ('greedyL', G)):
        Dset = set(D); R = [p for p in range(n) if p not in Dset]
        tD = types(D, f); tR = types(R, f)
        okD = not any(c >= a - 2 and u >= b - 1 for c, u in tD) and not any(c >= a - 1 for c, u in tD)
        okR = not any(u >= b - 1 for c, u in tR)
        strong = okD and okR and not any(c >= a - 1 and u >= b - 2 for c, u in tR)
        res[nm] = (len(D), okD, okR, strong)
    return res

if __name__ == '__main__':
    mode = sys.argv[1]; stats = {}
    def tally(r):
        for nm, (sz, okD, okR, strong) in r.items():
            st = stats.setdefault(nm, [0, 0, 0, 0]); st[0] += 1; st[1] += okD; st[2] += okR; st[3] += strong
    if mode == 'maximal':
        d = json.load(open(sys.argv[2])); a, b = d['a'], d['b']
        for M, m, sig in d['maximal']: tally(test(m, sig_fn(m, sig), a, b))
    elif mode == 'pools':
        a, b = int(sys.argv[2]), int(sys.argv[3])
        for fn in sys.argv[4:]:
            for line in open(fn):
                P = sorted(tuple(p) for p in json.loads(line)['P']); r = test(len(P), pts_fn(P), a, b); tally(r)
                print(os.path.basename(fn), len(P), r, flush=True)
    for nm, (tot, okD, okR, strong) in stats.items():
        print(f'{nm}: {tot} configurations; D in FL(a-1,b): {okD}; S-D has no (b-1)-cup: {okR}; strong split by D: {strong}')
