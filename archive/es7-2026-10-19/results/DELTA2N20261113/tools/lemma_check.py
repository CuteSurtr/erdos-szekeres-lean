"""Exact checks of the PROVED lemmas of README section 6 on the certificate sets of ETVTHY20261113
(real 5-cap-free sets without convex octagon / heptagon), pure Python (pyexact of that record).
 L1  helper: if p starts a 4-cap (p,d,..) then (o,p,d) is a cup for every o < p   [checked through its consequences]
 L2  layers L^(0)=S, L^(i+1) = points of L^(i) starting a 4-cap inside L^(i):
       every cup of S ending in L^(i) has <= n-1-i points;  L^(3) contains no convex (n-1)-gon;
       every right end of a convex (n-1)-gon lies outside L^(3).
 L3  M = (starts of 4-caps) & (ends of 4-caps):  S minus (Q u Q' u Q(M)) = M minus Q(M) contains no convex (n-1)-gon;
       M contains no (n-2)-cup.
usage: lemma_check.py n certfile.jsonl"""
import sys, json
import pyexact_etvthy as px
W = '/home/jay/research/data/etvthy-20261113/'
def ranks(P):
    """cap_start[p], cap_end[p], cup_end[p] inside the point list P (sorted)."""
    n = len(P)
    if n == 0: return [], [], [], {}
    O = px.otable(P) if n >= 3 else {}
    capE = {}; cupE = {}
    for j in range(n):
        for i in range(j):
            bc = bu = 2
            for h in range(i):
                if O[h, i, j] < 0: bc = max(bc, capE[h, i] + 1)
                else: bu = max(bu, cupE[h, i] + 1)
            capE[i, j] = bc; cupE[i, j] = bu
    capS = {}
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, i, -1):
            bc = 2
            for k in range(j + 1, n):
                if O[i, j, k] < 0: bc = max(bc, capS[j, k] + 1)
            capS[i, j] = bc
    cs = [max([1] + [capS[i, j] for j in range(i + 1, n)]) for i in range(n)]
    ce = [max([1] + [capE[i, j] for i in range(j)]) for j in range(n)]
    ue = [max([1] + [cupE[i, j] for i in range(j)]) for j in range(n)]
    return cs, ce, ue, cupE
def maxgon(P):
    if len(P) < 3: return len(P)
    capE, cupE, capB, cupB = px.chains(P)
    return max(capB[k] + cupB[k] - 2 for k in capB)
n = int(sys.argv[1]); cache = {}; cnt = 0
for line in open(sys.argv[2]):
    rec = json.loads(line); fn = rec['file']
    if fn not in cache: cache[fn] = [json.load(open(W + fn))] if fn.endswith('.json') else [json.loads(l)['P'] for l in open(W + fn)]
    P = sorted(tuple(p) for p in cache[fn][rec['index']]); m = len(P)
    cs, ce, ue, cupE = ranks(P)
    assert max(cs) <= 4 and maxgon(P) <= n - 1
    # right ends of (n-1)-gons
    capE_, cupE_, capB, cupB = px.chains(P)
    ER = {t for (s, t) in capB if capB[s, t] + cupB[s, t] - 2 >= n - 1}
    # L2
    layer = list(range(m)); lay_of = {}
    for i in range(4):
        sub = [P[p] for p in layer]
        if sub:
            cs_i, _, _, _ = ranks(sub)
            for idx, p in enumerate(layer):
                assert ue[p] <= n - 1 - i, ('L2 cup bound', fn, rec['index'], i)       # cups of S ending at p in L^(i)
            nxt = [p for idx, p in enumerate(layer) if cs_i[idx] >= 4]
        else: nxt = []
        for p in layer:
            if p not in nxt: lay_of[p] = i
        layer = nxt
        if i == 2:
            assert maxgon([P[p] for p in layer]) < n - 1 or len(layer) < n - 1, 'L2: gon inside L^(3)'
            assert not (ER & set(layer)), 'L2: right end inside L^(3)'
    # L3
    M = [p for p in range(m) if cs[p] >= 4 and ce[p] >= 4]
    subM = [P[p] for p in M]
    if len(subM) >= 2:
        csM, ceM, ueM, _ = ranks(subM)
        assert max(ueM) <= n - 3, 'L3: (n-2)-cup inside M'
        rest = [subM[i] for i in range(len(subM)) if csM[i] >= 4]
        assert len(rest) < n - 1 or maxgon(rest) < n - 1, 'L3: gon inside M minus Q(M)'
    cnt += 1
print(sys.argv[2].split('/')[-1], 'n =', n, ':', cnt, 'sets, lemmas L2, L3 hold in all', flush=True)
