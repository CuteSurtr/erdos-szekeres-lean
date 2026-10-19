#!/usr/bin/env python3
"""Hull-size case split on top of the hull-frame signotope CNF from tools/trackB/gen_cnf.py --hull.

Frame (gen_cnf.py --hull): points 1..N, X(i,j,k) for i<j<k numbered 1..C(N,3) in lexicographic
order, X true = counterclockwise = "cup" triple, and the unit clauses X(1,i,j) for all 1<i<j.

Hull indicators (new variables, appended after the base CNF's variables)
  H_v for v = 3..N-1:   H_v <-> AND_{2<=a<v<b<=N} X(a,v,b)
  (full equivalence: (-H_v | X(a,v,b)) for each a,b, and (H_v | OR -X(a,v,b)).)
  Points 1, 2 and N are always extreme in the frame; v in 3..N-1 is extreme iff H_v
  (proof in results/G/README.md, section "Soundness and exhaustiveness").
  So hull size h = 3 + m with m = #{v : H_v}.

Counter (new variables): sequential counter with full equivalence
  S(i,c) <-> S(i-1,c) | (S(i-1,c-1) & H_{v_i}),  S(0,c) = false (c>=1), S(i,0) = true,
  over the list v_1..v_L = 3..N-1 (L = N-3), for c = 1..C.  Every total assignment of the base
  variables extends uniquely to H and S, and then S(L,c) holds iff m >= c.

Cases
  --case m        exactly m (unit S(L,m) if m>=1, unit -S(L,m+1))         [hull size m+3]
  --case ge:M     at least M (unit S(L,M))                                   [hull size >= M+3]
  The cases m = 0..M-1 together with ge:M partition all assignments (exhaustive, disjoint).
  With M = K-3 the last case is the "hull has >= K vertices" case, which the base CNF already
  forbids (K hull vertices form a K-cup with point 1); it is run as a sanity check, not assumed.

Output: the base CNF clauses unchanged and in the same order (so clause ids of the base CNF are
preserved), followed by the new clauses. A JSON sidecar records the variable map.
"""
import argparse
import itertools
import json


def read_cnf(path):
    nv = nc = None
    clauses = []
    comments = []
    with open(path) as f:
        cur = []
        for line in f:
            if line.startswith('c'):
                comments.append(line.rstrip('\n'))
                continue
            if line.startswith('p'):
                _, _, a, b = line.split()
                nv, nc = int(a), int(b)
                continue
            for t in line.split():
                x = int(t)
                if x == 0:
                    clauses.append(cur)
                    cur = []
                else:
                    cur.append(x)
    assert nc == len(clauses), (nc, len(clauses))
    return nv, clauses, comments


def xindex(N):
    X = {}
    n = 0
    for t in itertools.combinations(range(1, N + 1), 3):
        n += 1
        X[t] = n
    return X


def hull_clauses(N, K, nv, case):
    X = xindex(N)
    nxt = [nv]

    def new():
        nxt[0] += 1
        return nxt[0]

    cls = []
    H = {}
    for v in range(3, N):
        H[v] = new()
    for v in range(3, N):
        big = [H[v]]
        for a in range(2, v):
            for b in range(v + 1, N + 1):
                cls.append([-H[v], X[(a, v, b)]])
                big.append(-X[(a, v, b)])
        cls.append(big)
    hs = [H[v] for v in range(3, N)]
    L = len(hs)
    if case.startswith('ge:'):
        M = int(case[3:])
        C = M
    else:
        m = int(case)
        C = m + 1
    # S[(i,c)] for 1<=i<=L, 1<=c<=min(i,C); S(i,c) with c>i is constant false
    S = {}
    for i in range(1, L + 1):
        for c in range(1, min(i, C) + 1):
            S[(i, c)] = new()

    def s(i, c):  # returns literal, or True/False constant
        if c <= 0:
            return True
        if i <= 0 or c > i:
            return False
        return S[(i, c)]

    def clause(lits):
        out = []
        for l in lits:
            if l is True:
                return
            if l is False:
                continue
            out.append(l)
        cls.append(out)

    def neg(l):
        if l is True:
            return False
        if l is False:
            return True
        return -l

    for i in range(1, L + 1):
        h = hs[i - 1]
        for c in range(1, min(i, C) + 1):
            sic = S[(i, c)]
            p_c = s(i - 1, c)
            p_c1 = s(i - 1, c - 1)
            # S(i-1,c) -> S(i,c)
            clause([neg(p_c), sic])
            # S(i-1,c-1) & h -> S(i,c)
            clause([neg(p_c1), -h, sic])
            # S(i,c) -> S(i-1,c) | S(i-1,c-1)
            clause([-sic, p_c, p_c1])
            # S(i,c) -> S(i-1,c) | h
            clause([-sic, p_c, h])
    units = []
    if case.startswith('ge:'):
        M = int(case[3:])
        lit = s(L, M)
        assert lit not in (True, False)
        units.append([lit])
    else:
        m = int(case)
        if m >= 1:
            lit = s(L, m)
            assert lit not in (True, False)
            units.append([lit])
        lit = s(L, m + 1)
        if lit is not False:
            assert lit is not True
            units.append([-lit])
    cls += units
    info = {'H': {str(v): H[v] for v in H}, 'S_top': {str(c): S[(L, c)] for c in range(1, min(L, C) + 1)},
            'case': case, 'units': units}
    return nxt[0], cls, info


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('base', help='CNF from gen_cnf.py N K --hull')
    ap.add_argument('N', type=int)
    ap.add_argument('K', type=int)
    ap.add_argument('--case', required=True, help="m (exactly m extra hull vertices; h=m+3) or ge:M")
    ap.add_argument('-o', '--out', required=True)
    args = ap.parse_args()
    nv, clauses, comments = read_cnf(args.base)
    from math import comb
    nX = comb(args.N, 3)
    assert any(f'N={args.N} K={args.K} hull=True' in c for c in comments), 'base must be gen_cnf.py N K --hull'
    nv2, extra, info = hull_clauses(args.N, args.K, nv, args.case)
    with open(args.out, 'w') as f:
        for c in comments:
            f.write(c + '\n')
        f.write(f'c hull_split case={args.case} (h = case+3) base_vars={nv} base_clauses={len(clauses)}\n')
        f.write(f'p cnf {nv2} {len(clauses) + len(extra)}\n')
        for c in clauses:
            f.write(' '.join(map(str, c)) + ' 0\n')
        for c in extra:
            f.write(' '.join(map(str, c)) + ' 0\n')
    info.update({'N': args.N, 'K': args.K, 'nX': nX, 'base_vars': nv, 'base_clauses': len(clauses),
                 'vars': nv2, 'clauses': len(clauses) + len(extra), 'out': args.out})
    with open(args.out + '.json', 'w') as f:
        json.dump(info, f)
    print(json.dumps({k: info[k] for k in ('N', 'K', 'case', 'vars', 'clauses', 'out')}))


if __name__ == '__main__':
    main()
