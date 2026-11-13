"""Baek block rows for the ETV catalog.  For a 2-set K of cap coordinates, a family F of states whose pairwise
refined domains D'(s->t), D'(t->s) only contain labels with cap coordinate in K has owners with no 4-cap
(a 4-cap needs three strictly increasing cap coordinates on its consecutive pairs).  Baek: 23 points in
general position contain a 4-cap or a convex octagon.  So |O cap F| <= 22: row (F, |F| - 22).
Functions: graphs(), max_clique(graph, within), rows for a given occupied set (lazy separation)."""
import itertools
import etv_common as ec
from etv_common import N, A
D = ec.DREF
def graphs():
    G = {}
    for K in itertools.combinations(range(1, A + 1), 2):
        adj = [0] * N
        for s in range(N):
            for t in range(N):
                if s != t and all(z[0] in K for z in D[s][t] | D[t][s]):
                    adj[s] |= 1 << t
        G[K] = adj
    return G
def max_clique(adj, within):
    best = [0]
    def expand(R, P):
        if P == 0:
            if R.bit_count() > best[0].bit_count(): best[0] = R
            return
        if R.bit_count() + P.bit_count() <= best[0].bit_count(): return
        # greedy coloring bound
        Q = P; colors = 0; U = P
        while U:
            colors += 1; avail = U
            while avail:
                v = (avail & -avail).bit_length() - 1; avail &= ~adj[v] & ~(1 << v); U &= ~(1 << v)
        if R.bit_count() + colors <= best[0].bit_count(): return
        while P:
            v = (P & -P).bit_length() - 1
            expand(R | (1 << v), P & adj[v])
            P &= ~(1 << v)
            if R.bit_count() + P.bit_count() <= best[0].bit_count(): return
    expand(0, within)
    return [i for i in range(N) if best[0] >> i & 1]
def extend(adj, C):
    m = 0
    for c in C: m |= 1 << c
    cand = (1 << N) - 1
    for c in C: cand &= adj[c]
    while cand:
        v = (cand & -cand).bit_length() - 1; C = C + [v]; cand &= adj[v]
    return sorted(C)
if __name__ == '__main__':
    G = graphs(); full = (1 << N) - 1
    for K, adj in G.items():
        C = max_clique(adj, full); print('K', K, 'max family', len(C), 'demand', len(C) - 22, C)
