"""Global sparse symmetric-BFP certificate on one abstract 56-point model, by column generation.
Columns: every comparison row of every 3-term GP relation (a; b,c,d,e) with a in layer-representatives {4l} (rotations
give the same orbit rows). LP: min c.y s.t. M y = 0, sum y = 1, y >= 0, cost c_r = sum of orbit weights over the six
brackets of the relation; reweighted-L1 rounds as in bfp_cegar3.sparse_support. Pricing over all columns with numpy.
The final support is turned into an exact certificate by bfpcert.find_cert and re-checked by check_cert.
Output: orbits and layers used, compared with the local (5-layer) sparse certificates of the same model."""
import sys, os, json, time, itertools
import numpy as np
sys.path.insert(0, '.')
import bfp_cegar2 as B
from bfpcert import find_cert, check_cert
from modeltest import chi_from_model
from scipy.optimize import linprog
from scipy.sparse import csr_matrix, vstack

t0 = time.time()
model = sys.argv[1]; out = sys.argv[2]
chi = chi_from_model(model); n = 56; ids = B.ids
OID = np.full((n, n, n), -1, dtype=np.int32)
for tr, v in ids.items():
    for p in itertools.permutations(tr):
        OID[p] = v
NORB = int(OID.max()) + 1
P = lambda *a: print('%6.0fs' % (time.time() - t0), *a, flush=True)
P('orbits', NORB)

# all relations with a = 4l
rels = []
for l in range(14):
    a = 4 * l; oth = np.array([x for x in range(n) if x != a], dtype=np.int16)
    Q = np.array(list(itertools.combinations(range(n - 1), 4)), dtype=np.int16)
    R = np.empty((len(Q), 5), dtype=np.int16); R[:, 0] = a; R[:, 1:] = oth[Q]
    rels.append(R)
REL = np.concatenate(rels); del rels
a, b, c, d, e = (REL[:, k].astype(np.int64) for k in range(5))
s = np.stack([chi[a, b, c] * chi[a, d, e], -chi[a, b, d] * chi[a, c, e], chi[a, b, e] * chi[a, c, d]], 1).astype(np.int8)
assert not np.any((s[:, 0] == s[:, 1]) & (s[:, 1] == s[:, 2]))
j = np.where((s[:, 0] != s[:, 1]) & (s[:, 0] != s[:, 2]), 0, np.where((s[:, 1] != s[:, 0]) & (s[:, 1] != s[:, 2]), 1, 2))
TERM = [(OID[a, b, c], OID[a, d, e]), (OID[a, b, d], OID[a, c, e]), (OID[a, b, e], OID[a, c, d])]
BR = np.stack([OID[a, b, c], OID[a, d, e], OID[a, b, d], OID[a, c, e], OID[a, b, e], OID[a, c, d]], 1)
cols = []
for kk in (1, 2):
    k = (j + kk) % 3
    G = np.stack([np.choose(j, [TERM[0][0], TERM[1][0], TERM[2][0]]), np.choose(j, [TERM[0][1], TERM[1][1], TERM[2][1]])], 1)
    L = np.stack([np.choose(k, [TERM[0][0], TERM[1][0], TERM[2][0]]), np.choose(k, [TERM[0][1], TERM[1][1], TERM[2][1]])], 1)
    G.sort(1); L.sort(1)
    cols.append((G, L, k))
G = np.concatenate([cols[0][0], cols[1][0]]); L = np.concatenate([cols[0][1], cols[1][1]])
KK = np.concatenate([cols[0][2], cols[1][2]]); RI = np.concatenate([np.arange(len(REL)), np.arange(len(REL))])
keep = ~np.all(G == L, 1)
G, L, KK, RI = G[keep], L[keep], KK[keep], RI[keep]
P('relations', len(REL), 'columns', len(G))

def bracket_cost(w):
    return w[BR].sum(1)[RI]

def solve_restricted(idx, c):
    rows = np.concatenate([G[idx, 0], G[idx, 1], L[idx, 0], L[idx, 1]])
    vals = np.concatenate([np.ones(2 * len(idx)), -np.ones(2 * len(idx))])
    cc = np.tile(np.arange(len(idx)), 4)
    M = csr_matrix((vals, (rows, cc)), shape=(NORB, len(idx)))
    A = vstack([M, csr_matrix(np.ones((1, len(idx))))]).tocsr(); bb = np.zeros(NORB + 1); bb[-1] = 1
    res = linprog(c[idx], A_eq=A, b_eq=bb, bounds=(0, None), method='highs')
    return res

# initial columns: all columns inside the 5-layer subset given on the command line (known infeasible), else layers 0..4
LS = json.loads(sys.argv[3]) if len(sys.argv) > 3 else [0, 1, 2, 3, 4]
EPS = float(sys.argv[4]) if len(sys.argv) > 4 else 1e-4
ROUNDS = int(sys.argv[5]) if len(sys.argv) > 5 else 6
inS = np.zeros(n, bool); inS[[l * 4 + k for l in LS for k in range(4)]] = True
# a column is inside S if its relation's five points are (up to rotation they all start at a=4l, so test directly)
idx = np.nonzero(inS[REL[RI]].all(1))[0]
P('initial columns', len(idx), 'eps', EPS)
w = np.ones(NORB); best = None; hist = []
for rnd in range(ROUNDS):
    c = bracket_cost(w)
    for it in range(200):
        res = solve_restricted(idx, c)
        if res.status != 0:
            P('LP status', res.status, res.message); sys.exit(1)
        lam = res.eqlin.marginals; lv = lam[:NORB]; lt = lam[-1]
        rc = c - (lv[G[:, 0]] + lv[G[:, 1]] - lv[L[:, 0]] - lv[L[:, 1]]) - lt
        neg = np.nonzero(rc < -1e-9)[0]
        if len(neg) == 0:
            break
        add = neg[np.argsort(rc[neg])[:4000]]
        idx = np.union1d(idx, add)
    y = res.x; supp = idx[y > 1e-9]
    used = np.unique(BR[RI[supp]]); lay = sorted({int(x) // 4 for x in np.unique(REL[RI[supp]])})
    hist.append((rnd, len(supp), len(used), len(lay), it, len(idx)))
    P('round', rnd, 'support', len(supp), 'orbits used', len(used), 'layers', lay, 'cg iters', it, 'columns', len(idx))
    if best is None or len(used) < best[0]:
        best = (len(used), supp.copy())
    u = np.zeros(NORB); np.add.at(u, BR[RI[supp]].ravel(), np.repeat(y[y > 1e-9], 6))
    w = 1.0 / (EPS + u)

# exact certificate on the best support
supp = best[1]
Rlist = []
for r in supp:
    Rlist.append(dict(rel=tuple(int(x) for x in REL[RI[r]]), j=int(j[RI[r]]), k=int(KK[r]),
                      G=tuple(int(x) for x in G[r]), L=tuple(int(x) for x in L[r])))
cert = find_cert(Rlist)
if not isinstance(cert, list):
    P('exact extraction failed', cert); sys.exit(1)
ok, msg = check_cert(chi, cert, ids)
used = sorted({int(OID[x]) for r, _ in cert for x in [tuple(r['rel'][i] for i in t) for t in ((0, 1, 2), (0, 3, 4), (0, 1, 3), (0, 2, 4), (0, 1, 4), (0, 2, 3))]})
lay = sorted({v // 4 for r, _ in cert for v in r['rel']})
P('exact certificate:', ok, msg, 'relations', len(cert), 'orbits used', len(used), 'layers', lay)
json.dump(dict(model=model, hist=hist, cert=[dict(rel=r['rel'], j=r['j'], k=r['k'], w=w_) for r, w_ in cert],
               orbits=used, layers=lay, check=ok), open(out, 'w'))
