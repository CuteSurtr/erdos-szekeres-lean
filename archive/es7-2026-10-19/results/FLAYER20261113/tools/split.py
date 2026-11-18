"""Strong (Pascal) split test for first-layer sets (FLAYER20261113).

Given an FL(a,b)-configuration S (no a-cap, no b-cup, no ((a-1),(b-1))-gon), is S = S1 + S2 (disjoint) with
  S1 in FL(a-1,b):  no (a-1)-cap and no ((a-2)-cap,(b-1)-cup)-gon      (no b-cup is inherited)
  S2 in FL(a,b-1):  no (b-1)-cup and no ((a-1)-cap,(b-2)-cup)-gon      (no a-cap is inherited) ?
If yes for every S, then N1(a,b) <= N1(a-1,b) + N1(a,b-1) (the Pascal recursion of the first-layer ETV value).
Exact: all chains are enumerated on the signotope; one SAT call (pysat Cadical153).
"""
import sys, itertools, json, os
from pysat.solvers import Cadical153

def chains(n, sgn_of, sgn, L):
    """all chains (tuples of indices) with exactly L points whose consecutive triples have sign sgn"""
    out = []
    if L == 2: return [(i, j) for i in range(n) for j in range(i + 1, n)]
    def ext(ch):
        if len(ch) == L: out.append(tuple(ch)); return
        for q in range(ch[-1] + 1, n):
            if sgn_of(ch[-2], ch[-1], q) == sgn:
                ch.append(q); ext(ch); ch.pop()
    for i in range(n):
        for j in range(i + 1, n):
            ext([i, j])
    return out

def split(n, sgn_of, a, b, want_model=True, weak=False):
    """returns (ok, S1 list) ; variables 1..n : True = S1"""
    nv = [n]
    def new():
        nv[0] += 1; return nv[0]
    cl = []
    x = lambda p: p + 1
    caps_a1 = chains(n, sgn_of, -1, a - 1) if a - 1 >= 2 else []
    cups_b1 = chains(n, sgn_of, 1, b - 1) if b - 1 >= 2 else []
    for ch in caps_a1: cl.append([-x(p) for p in ch])              # S1 has no (a-1)-cap
    for ch in cups_b1: cl.append([x(p) for p in ch])               # S2 has no (b-1)-cup
    # S1: no ((a-2)-cap, (b-1)-cup)-gon
    if a - 2 >= 2:
        aux = {}
        def get(kind, u, v):
            if (kind, u, v) not in aux: aux[kind, u, v] = new()
            return aux[kind, u, v]
        caps_a2 = chains(n, sgn_of, -1, a - 2)
        ends1 = set((ch[0], ch[-1]) for ch in caps_a2) & set((ch[0], ch[-1]) for ch in cups_b1)
        for ch in caps_a2:
            if (ch[0], ch[-1]) in ends1: cl.append([-x(p) for p in ch] + [get('c1', ch[0], ch[-1])])
        for ch in cups_b1:
            if (ch[0], ch[-1]) in ends1: cl.append([-x(p) for p in ch] + [get('d1', ch[0], ch[-1])])
        for u, v in ends1: cl.append([-get('c1', u, v), -get('d1', u, v)])
    if b - 2 >= 2 and not weak:      # weak: S2 only has to be free of (b-1)-cups
        aux2 = {}
        def get2(kind, u, v):
            if (kind, u, v) not in aux2: aux2[kind, u, v] = new()
            return aux2[kind, u, v]
        cups_b2 = chains(n, sgn_of, 1, b - 2)
        ends2 = set((ch[0], ch[-1]) for ch in cups_b2) & set((ch[0], ch[-1]) for ch in caps_a1)
        for ch in cups_b2:
            if (ch[0], ch[-1]) in ends2: cl.append([x(p) for p in ch] + [get2('d2', ch[0], ch[-1])])
        for ch in caps_a1:
            if (ch[0], ch[-1]) in ends2: cl.append([x(p) for p in ch] + [get2('c2', ch[0], ch[-1])])
        for u, v in ends2: cl.append([-get2('c2', u, v), -get2('d2', u, v)])
    so = Cadical153(bootstrap_with=cl)
    ok = so.solve()
    S1 = None
    if ok:
        m = set(l for l in so.get_model() if l > 0); S1 = [p for p in range(n) if x(p) in m]
    so.delete()
    return ok, S1, len(cl)

def check_split(n, sgn_of, a, b, S1):
    """independent verification of a split by exact DP on the two classes"""
    def analyze(pts):
        m = len(pts); Em = {}; Ep = {}
        for vi in range(m):
            for ui in range(vi):
                em = ep = 2
                for ti in range(ui):
                    if sgn_of(pts[ti], pts[ui], pts[vi]) < 0: em = max(em, Em[ti, ui] + 1)
                    else: ep = max(ep, Ep[ti, ui] + 1)
                Em[ui, vi] = em; Ep[ui, vi] = ep
        mc = max([1] + list(Em.values())) if m >= 2 else m; mu = max([1] + list(Ep.values())) if m >= 2 else m
        types = set()
        for s in range(m):
            Dc = {}; Du = {}
            for j in range(s + 1, m): Dc[s, j] = 2; Du[s, j] = 2
            for j in range(s + 1, m):
                for i in range(s + 1, j):
                    bc = bu = 0
                    for h in range(s, i):
                        if sgn_of(pts[h], pts[i], pts[j]) < 0:
                            if Dc[h, i]: bc = max(bc, Dc[h, i] + 1)
                        else:
                            if Du[h, i]: bu = max(bu, Du[h, i] + 1)
                    Dc[i, j] = bc; Du[i, j] = bu
            for t in range(s + 1, m):
                types.add((max(Dc[i, t] for i in range(s, t)), max(Du[i, t] for i in range(s, t))))
        return mc, mu, types
    S1 = sorted(S1); S2 = [p for p in range(n) if p not in set(S1)]
    mc1, mu1, ty1 = analyze(S1); mc2, mu2, ty2 = analyze(S2)
    ok1 = mc1 <= a - 2 and not any(c >= a - 2 and u >= b - 1 for c, u in ty1)
    ok2 = mu2 <= b - 2 and not any(c >= a - 1 and u >= b - 2 for c, u in ty2)
    return ok1 and ok2

def sig_fn(n, sig):
    idx = {t: i for i, t in enumerate(itertools.combinations(range(n), 3))}
    return lambda i, j, k: (1 if sig[idx[i, j, k]] == '+' else -1)

def pts_fn(P):
    P = sorted(P)
    def f(i, j, k):
        d = (P[j][0] - P[i][0]) * (P[k][1] - P[i][1]) - (P[j][1] - P[i][1]) * (P[k][0] - P[i][0])
        return 1 if d > 0 else -1
    return f

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'maximal':      # split.py maximal maximal_5_5_14.json
        d = json.load(open(sys.argv[2])); a, b = d['a'], d['b']; bad = 0; tot = 0
        for M, m, sig in d['maximal']:
            f = sig_fn(m, sig); ok, S1, ncl = split(m, f, a, b); tot += 1
            if ok: assert check_split(m, f, a, b, S1)
            else: bad += 1; print('NO SPLIT', m, sig)
        print(f'FL({a},{b}) witnesses: {tot} tested, {bad} without strong split')
    elif mode == 'pools':      # split.py pools 6 6 file1.jsonl ...
        a, b = int(sys.argv[2]), int(sys.argv[3]); bad = tot = 0
        for fn in sys.argv[4:]:
            for line in open(fn):
                P = sorted(tuple(p) for p in json.loads(line)['P']); f = pts_fn(P); n = len(P)
                ok, S1, ncl = split(n, f, a, b); tot += 1
                if ok:
                    assert check_split(n, f, a, b, S1)
                    print(os.path.basename(fn), 'n', n, 'split', len(S1), n - len(S1), 'clauses', ncl, flush=True)
                else: bad += 1; print('NO SPLIT', fn, n, P, flush=True)
        print(f'FL({a},{b}) real sets: {tot} tested, {bad} without strong split')
    elif mode == 'samples':    # split.py samples 6 6 samples.jsonl ...   (abstract signotopes of sample_fl.py)
        a, b = int(sys.argv[2]), int(sys.argv[3]); bad = tot = 0
        for fn in sys.argv[4:]:
            seen = set()
            for line in open(fn):
                d = json.loads(line)
                if d['sig'] in seen: continue
                seen.add(d['sig']); n = d['n']; f = sig_fn(n, d['sig'])
                ok, S1, ncl = split(n, f, a, b); tot += 1
                if ok:
                    assert check_split(n, f, a, b, S1)
                    print(os.path.basename(fn), 'n', n, 'info', d.get('info'), 'split', len(S1), n - len(S1), 'clauses', ncl, flush=True)
                else: bad += 1; print('NO SPLIT', fn, n, d['seed'], flush=True)
        print(f'FL({a},{b}) abstract samples: {tot} tested, {bad} without strong split')
