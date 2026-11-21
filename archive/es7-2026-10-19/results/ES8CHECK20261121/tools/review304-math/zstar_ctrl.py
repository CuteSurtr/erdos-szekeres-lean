"""Independent exact control of Lemma Z and Lemma Z* (review304-math).
Own code from the Lean definitions: labels(u,v) = (rankCap(u,v)-1, rankCup(u,v)-1),
column(v,i) = max{cupLabel(u,v) : u<v, capLabel(u,v) >= i+1} (0 if none).
Exact integer orientation; points sorted by x (distinct x required)."""
import random, sys, json
from fractions import Fraction

def orient(p, q, r):
    return (q[0]-p[0])*(r[1]-p[1]) - (q[1]-p[1])*(r[0]-p[0])

def build(k, l, memo={}):
    # S(k,l): no k-cup, no l-cap, C(k+l-4,k-2) points
    if (k, l) in memo: return memo[(k, l)]
    if k <= 2 or l <= 2:
        res = [(0, 0)]
    else:
        L = build(k-1, l); R = build(k, l-1)
        X = max(p[0] for p in L) - min(p[0] for p in R) + 1
        Y = 1
        while True:
            Rs = [(p[0]+X, p[1]+Y) for p in R]
            ok = True
            # a<b in L, r in Rs: cup turn; l in L, r1<r2 in Rs: cap turn
            for i in range(len(L)):
                for j in range(i+1, len(L)):
                    for r in (Rs[0], Rs[-1]) if len(Rs) > 1 else Rs:
                        pass
            # exact check of all needed turns (small sizes at each level are fine for k,l<=7)
            for i in range(len(L)):
                for j in range(i+1, len(L)):
                    for r in Rs:
                        if orient(L[i], L[j], r) <= 0: ok = False; break
                    if not ok: break
                if not ok: break
            if ok:
                for a in L:
                    for i in range(len(Rs)):
                        for j in range(i+1, len(Rs)):
                            if orient(a, Rs[i], Rs[j]) >= 0: ok = False; break
                        if not ok: break
                    if not ok: break
            if ok: break
            Y *= 4
        res = L + Rs
    memo[(k, l)] = res
    return res

def tables(P):
    n = len(P)
    S = {}
    for i in range(n):
        for j in range(i+1, n):
            for k in range(j+1, n):
                o = orient(P[i], P[j], P[k])
                assert o != 0, "collinear"
                S[(i, j, k)] = 1 if o > 0 else -1
    return S

def ranks(idx, S, sgn):
    # E[(a,b)] = max number of points of a chain of the given sign ending with edge (a,b); idx sorted
    E = {}; pred = {}
    for bi in range(len(idx)):
        for ci in range(bi+1, len(idx)):
            b, c = idx[bi], idx[ci]
            best, arg = 2, None
            for ai in range(bi):
                a = idx[ai]
                if S[(a, b, c)] == sgn and E[(a, b)] + 1 > best:
                    best, arg = E[(a, b)] + 1, a
            E[(b, c)] = best; pred[(b, c)] = arg
    return E, pred

def longest(idx, S, sgn):
    E, pred = ranks(idx, S, sgn)
    return max(E.values()) if E else min(len(idx), 1)

def chain_of(E, pred, pair):
    out = [pair[1], pair[0]]; cur = pair
    while pred[cur] is not None:
        a = pred[cur]; out.append(a); cur = (a, cur[0])
    return out[::-1]

def make_balanced(idx, S, rng):
    idx = sorted(idx)
    while True:
        Ecup, pcup = ranks(idx, S, 1)
        Ecap, pcap = ranks(idx, S, -1)
        bad = [(pr, Ecup, pcup) for pr, v in Ecup.items() if v >= 7] + [(pr, Ecap, pcap) for pr, v in Ecap.items() if v >= 7]
        if not bad: return idx, Ecup, Ecap
        pr, E, pd = rng.choice(bad)
        ch = chain_of(E, pd, pr)
        idx.remove(rng.choice(ch))

def states(idx, Ecup, Ecap):
    st = {}
    for vi, v in enumerate(idx):
        f = []
        for i in range(5):
            m = 0
            for u in idx[:vi]:
                cap, cup = Ecap[(u, v)] - 1, Ecup[(u, v)] - 1
                if cap >= i+1: m = max(m, cup)
            f.append(m)
        st[v] = tuple(f)
    return st

def check(P, idx_all, rng, tag, out):
    S = tables(P)
    idx, Ecup, Ecap = make_balanced(idx_all, S, rng)
    st = states(idx, Ecup, Ecap)
    assert all(st[v][i] >= st[v][i+1] for v in idx for i in range(4)), "not antitone"
    assert all(0 <= x <= 5 for v in idx for x in st[v]), "range"
    inj = len(set(st.values())) == len(idx)
    first = st[idx[0]] == (0,0,0,0,0) and (len(idx) < 2 or st[idx[1]] == (1,0,0,0,0))
    Z = [v for v in idx if st[v][0] <= 4 and st[v][4] == 0]
    Zs = [v for v in idx if st[v][0] == 5 and st[v][4] >= 1]
    cupend = [v for v in idx if st[v][0] == 5]
    capend = [v for v in idx if st[v][4] >= 1]
    r = dict(tag=tag, n=len(idx), inj=inj, first=first, Z=len(Z), Zs=len(Zs),
             Zcup=longest(Z, S, 1), Zcap=longest(Z, S, -1),
             Zscup=longest(Zs, S, 1), Zscap=longest(Zs, S, -1),
             neg_cupend_cup=longest(cupend, S, 1), neg_capend_cap=longest(capend, S, -1))
    r['ok'] = inj and first and r['Zcup'] < 6 and r['Zcap'] < 6 and r['Zscup'] < 6 and r['Zscap'] < 6
    out.append(r); print(json.dumps(r), flush=True)
    return r

def main():
    seed = int(sys.argv[1]); nsets = int(sys.argv[2]); sub = int(sys.argv[3])
    rng = random.Random(seed)
    base = build(7, 7)
    assert len(base) == 252 and len(set(p[0] for p in base)) == 252
    out = []
    # 1) the construction itself (no rotation)
    P = sorted(base)
    check(P, list(range(len(P))), rng, "S77", out)
    # 2) random rational rotations (Pythagorean triples) of random subsets, then greedy deletion of 7-cups/7-caps
    triples = [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29),(12,35,37),(9,40,41),(28,45,53),(11,60,61),(33,56,65)]
    for t in range(nsets):
        a, b, c = rng.choice(triples)
        if rng.random() < 0.5: a, b = b, a
        if rng.random() < 0.5: b = -b
        sel = rng.sample(base, sub)
        Q = [(a*x - b*y, b*x + a*y) for (x, y) in sel]
        if len(set(q[0] for q in Q)) < len(Q): continue
        Q.sort()
        check(Q, list(range(len(Q))), rng, f"rot{t}:{a},{b}", out)
    print("SUMMARY", json.dumps(dict(sets=len(out), all_ok=all(r['ok'] for r in out),
          max_Zs=max(r['Zs'] for r in out), sum_Zs=sum(r['Zs'] for r in out),
          neg_cupend_has6cup=sum(r['neg_cupend_cup'] >= 6 for r in out),
          neg_capend_has6cap=sum(r['neg_capend_cap'] >= 6 for r in out))))

main()
