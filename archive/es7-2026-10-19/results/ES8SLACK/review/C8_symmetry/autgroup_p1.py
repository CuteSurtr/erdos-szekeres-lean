"""Exact symmetry group of the Boolean feasible set F_P1 = {h in {0,1}^252 :
2,685 base rows, h0 = h1 = 0, h2 + h3 <= 1}.

Occupied sets O = {i : h_i = 0}. Base rows <=> O in Delta, the simplicial complex whose
minimal non-faces are K = all 8-subsets of base supports (every row is "|O cap S| <= 7").
F_P1 <=> Psi = {O in Delta : {0,1} <= O, O cap {2,3} nonempty}.
Lemma: sigma(Psi) = Psi  iff  sigma{0,1} = {0,1}, sigma{2,3} = {2,3} and
sigma(N_x) = N_sigma(x) for x in {2,3}, where N_x = minimal elements of
{k minus {0,1,x} : k in K} (minimal non-faces of the link of {0,1,x}).
(The intersection of all members of Psi is {0,1}; its minimal members are {0,1,2},{0,1,3};
Psi_x = {O in Psi : x in O} corresponds to the link of {0,1,x}.)
Encoded as a coloured graph: states (0,1 coloured 'occ', 2,3 coloured 'pair'), anchors a_2,a_3
(a_x adjacent to state x), one vertex per (e, x) with e in N_x adjacent to e's states and to a_x.
Exhaustive individualization-refinement as in autgroup.py; every automorphism found is
verified directly on (N_2, N_3).
"""
import json, sys, itertools, time
from collections import Counter

SRC = sys.argv[1]
d = json.load(open(SRC))
cons = d['constraints']
NS = 252
K = set()
for c in cons[:2685]:
    S = sorted(c['support']); assert len(S) - c['rhs'] == 7
    for sub in itertools.combinations(S, 8):
        K.add(frozenset(sub))
print('|K| =', len(K))


def minimal(fam):
    fam = set(fam)
    out = []
    for s in fam:
        m = len(s); ok = True
        for r in range(1, m):
            for sub in itertools.combinations(sorted(s), r):
                if frozenset(sub) in fam:
                    ok = False; break
            if not ok: break
        if ok: out.append(s)
    return set(out)


N = {}
for x in (2, 3):
    fam = {k - {0, 1, x} for k in K}
    N[x] = minimal(fam)
    print('N_%d: %d sets, size histogram %s' % (x, len(N[x]), dict(sorted(Counter(len(s) for s in N[x]).items()))))

# graph
vcol = []
adj = []
def addv(col):
    vcol.append(col); adj.append([]); return len(vcol) - 1
for i in range(NS):
    addv(('state', 'occ' if i in (0, 1) else 'pair' if i in (2, 3) else 'plain'))
anchor = {x: addv(('anchor',)) for x in (2, 3)}
def adde(a, b):
    adj[a].append(b); adj[b].append(a)
for x in (2, 3):
    adde(anchor[x], x)
    for e in N[x]:
        h = addv(('nf',))
        adde(h, anchor[x])
        for i in e: adde(h, i)
n = len(vcol)
cn = sorted(set(vcol), key=repr)
init = [cn.index(c) for c in vcol]
print('graph vertices', n, 'edges', sum(len(a) for a in adj) // 2)


def relabel(sigs):
    keys = sorted(set(sigs)); m = {k: t for t, k in enumerate(keys)}
    return [m[s] for s in sigs], len(keys)


def refine(colors):
    colors, k = relabel(colors)
    while True:
        new, k2 = relabel([(colors[v], tuple(sorted(colors[u] for u in adj[v]))) for v in range(n)])
        if k2 == k: return new, k
        colors, k = new, k2


def cells_of(colors):
    cl = {}
    for v in range(NS): cl.setdefault(colors[v], []).append(v)
    return cl


Nset = {x: set(N[x]) for x in (2, 3)}
def is_aut(sig):
    if {sig[0], sig[1]} != {0, 1} or {sig[2], sig[3]} != {2, 3}: return False
    for x in (2, 3):
        y = sig[x]
        img = {frozenset(sig[i] for i in e) for e in N[x]}
        if img != Nset[y]: return False
    return True


t0 = time.time()
c0, _ = refine(init)
cl0 = cells_of(c0)
print('equitable partition on states: %d cells, sizes %s' % (len(cl0), dict(sorted(Counter(len(v) for v in cl0.values()).items()))))
leaves = []; nodes = [0]
def search(colors, path):
    nodes[0] += 1
    if nodes[0] > 50000: raise RuntimeError('node limit')
    cl = cells_of(colors)
    ns = [c for c in sorted(cl) if len(cl[c]) > 1]
    if not ns:
        leaves.append(colors); return
    for v in cl[ns[0]]:
        nc, _ = refine([(colors[x], 1 if x == v else 0) for x in range(n)])
        search(nc, path + [v])
search(c0, [])
L0 = leaves[0]
auts = set()
for L in leaves:
    inv = {L[v]: v for v in range(NS)}
    sig = [inv[L0[v]] for v in range(NS)]
    if is_aut(sig): auts.add(tuple(sig))
print('nodes', nodes[0], 'leaves', len(leaves), '| |Aut(F_P1)| =', len(auts), '| time %.1fs' % (time.time() - t0))
T = json.load(open(sys.argv[2]))['T']
print('Aut(F_P1) == {id, T}:', auts == {tuple(range(NS)), tuple(T)})
