#!/usr/bin/env python3
"""Optional cup-cap cardinality lemmas for the hull frame (UNVERIFIED encoding; experiments only).

In the hull frame (gen_cnf.py --hull), the points P' = {2..N} contain no (K-1)-cup (point 1
prepends to every cup) and no K-cap. Erdos-Szekeres cup-cap: a set with no a-cap and no u-cup
has at most f(a,u) = C(a+u-4, a-2) points. Hence, for the N-1 points of P':
  * the points that END no r-cup inside P' form a set with no r-cup and no K-cap:
        #{v : v ends an r-cup in P'} >= (N-1) - C(K+r-4, r-2)            (cup, end)
  * the points that END no r-cap form a set with no r-cap and no (K-1)-cup:
        #{v : v ends an r-cap in P'} >= (N-1) - C(r+K-5, r-2)            (cap, end)
  * the same two bounds for points that START an r-cup / r-cap (reverse the order).
Only bounds with a positive right-hand side are added. f is computed from (a, u) here, not
hard-coded (critique item 11).

Encoding (new variables, one direction only, which is all a lower bound needs):
  L(a,b,r) -> OR_w Z(w,a,b,r);  Z(w,a,b,r) -> L(w,a,r-1) & T(w,a,b)       ("ends" chains)
  with T(w,a,b) = X(w,a,b) for cups and -X(w,a,b) for caps, L(a,b,2) = true, and
  E(v,r) -> OR_a L(a,v,r);   sequential counter "at least t of E(.,r)" (justification direction).
Soundness: any assignment of the base variables extends by giving every new variable its exact
meaning; all new clauses are implications that then hold, and the counter holds because of the
cup-cap theorem. So a model of the original CNF is never excluded. Completeness is not needed.
"""
import argparse
import itertools
import json
from math import comb


def f_capcup(a, u):
    """Max size of a point set (signotope) with no a-cap and no u-cup."""
    return comb(a + u - 4, a - 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('case_cnf')
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--families', default='cup_end,cap_end,cup_start,cap_start')
    args = ap.parse_args()
    info = json.load(open(args.case_cnf + '.json'))
    N, K = info['N'], info['K']
    Xi = {}
    n = 0
    for t in itertools.combinations(range(1, N + 1), 3):
        n += 1
        Xi[t] = n
    header = None
    comments = []
    body = []
    with open(args.case_cnf) as f:
        for line in f:
            if line.startswith('c'):
                comments.append(line)
            elif line.startswith('p'):
                header = line.split()
            else:
                body.append(line)
    nv, nc = int(header[2]), int(header[3])
    cls = []
    nxt = [nv]

    def new():
        nxt[0] += 1
        return nxt[0]

    P = list(range(2, N + 1))
    M = len(P)
    added = []
    for fam in args.families.split(','):
        kind, side = fam.split('_')
        for r in range(3, K + 1):
            if kind == 'cup':
                bound = f_capcup(K, r)      # no r-cup and no K-cap
                if r >= K - 1:
                    continue                 # P' has no (K-1)-cup anyway
            else:
                bound = f_capcup(r, K - 1)  # no r-cap and no (K-1)-cup
                if r >= K:
                    continue
            t = M - bound
            if t <= 0:
                continue
            # order: 'end' uses P in increasing order; 'start' uses the reversed order
            order = P if side == 'end' else list(reversed(P))
            pos = {v: i for i, v in enumerate(order)}

            def T(w, a, b):
                # w,a,b are consecutive in a cup (cap) iff the x-sorted triple is CCW (CW);
                # this does not depend on the reading direction, so 'start' reuses it.
                lit = Xi[tuple(sorted((w, a, b)))]
                return lit if kind == 'cup' else -lit

            L = {}
            for i, j in itertools.combinations(range(M), 2):
                for rr in range(3, r + 1):
                    L[(i, j, rr)] = new()
            for (i, j, rr), var in L.items():
                ors = [-var]
                for w in range(0, i):
                    z = new()
                    ors.append(z)
                    prev = L.get((w, i, rr - 1)) if rr - 1 >= 3 else None
                    if prev is not None:
                        cls.append([-z, prev])
                    cls.append([-z, T(order[w], order[i], order[j])])
                cls.append(ors)
            E = []
            for j in range(M):
                e = new()
                E.append(e)
                cls.append([-e] + [L[(i, j, r)] for i in range(0, j) if (i, j, r) in L])
            # at least t of E: S(i,c) -> S(i-1,c) | (S(i-1,c-1) & E_i)  (justification direction)
            S = {}
            for i in range(1, M + 1):
                for c in range(1, min(i, t) + 1):
                    S[(i, c)] = new()
            for (i, c), s in S.items():
                prev_c = S.get((i - 1, c))
                prev_c1 = S.get((i - 1, c - 1)) if c - 1 >= 1 else True
                e = E[i - 1]
                # s -> prev_c | e   and   s -> prev_c | prev_c1
                c1 = [-s, e] + ([prev_c] if prev_c else [])
                cls.append(c1)
                if prev_c1 is not True:
                    c2 = [-s, prev_c1] + ([prev_c] if prev_c else [])
                    cls.append(c2)
            cls.append([S[(M, t)]])
            added.append({'family': fam, 'r': r, 'f': bound, 'at_least': t, 'of': M})
    with open(args.out, 'w') as f:
        for c in comments:
            f.write(c)
        f.write('c lemma_cnf ' + json.dumps(added) + '\n')
        f.write(f'p cnf {nxt[0]} {nc + len(cls)}\n')
        for line in body:
            f.write(line)
        for c in cls:
            f.write(' '.join(map(str, c)) + ' 0\n')
    info2 = dict(info)
    info2.update({'lemmas': added, 'vars': nxt[0], 'clauses': nc + len(cls), 'out': args.out})
    json.dump(info2, open(args.out + '.json', 'w'))
    print(json.dumps({'out': args.out, 'lemmas': added, 'vars': nxt[0], 'clauses': nc + len(cls)}))


if __name__ == '__main__':
    main()
