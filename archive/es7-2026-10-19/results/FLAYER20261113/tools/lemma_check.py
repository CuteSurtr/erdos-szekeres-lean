"""Exact checks of the PROVED lemmas of README section 2 on real (6,6;8)-sets (all pools)."""
import sys, json, glob
import fl
from fl import *
from esgeo import Analysis
def check(P):
    S = Set66(P); assert S.ok
    A = S.A; n = S.n; bad = []
    beta = A.cup_end; cm = A.cap_end; om = A.cup_start; cp = A.cap_start
    # catalog facts: injectivity, beta = f1 + 1, c_- = 1 + number of nonempty columns
    if len(set(S.in_state)) != n or len(set(S.out_state)) != n: bad.append('injectivity')
    for v in range(n):
        f = S.in_f[v]
        if beta[v] != f[0] + 1 or cm[v] != 1 + sum(1 for x in f if x > 0): bad.append('rank identities')
    # Lemma 1 (junction), cell form
    for v in range(n):
        ci = ec.CELLS[S.in_state[v]]; co = ec.CELLS[S.out_state[v]]
        if not all(a + a2 <= 4 or b + b2 <= 4 for (a, b) in ci for (a2, b2) in co): bad.append('junction')
        if beta[v] == 5 and cp[v] == 5: bad.append('junction E/A2')
        if cm[v] == 5 and om[v] == 5: bad.append('junction A/E2')
    # Lemma 2: pairs inside a beta-level have E_- >= 3
    for v in range(n):
        for u in range(v):
            if beta[u] == beta[v] and beta[u] >= 2 and A.capE[u, v] < 3: bad.append('level pairs')
    # Lemma 3: E has no 5-cap; a 4-cap inside E ends in X; E \ X has no 4-cap (and the mirror statements for A)
    for name, lev, other, key in (('E', [v for v in range(n) if beta[v] == 5], cm, 'cap'), ('A', [v for v in range(n) if cm[v] == 5], beta, 'cup')):
        if len(lev) >= 2:
            Q = [S.P[v] for v in lev]; B = Analysis(Q)
            arrE = B.capE if key == 'cap' else B.cupE
            if arrE.max() >= 5: bad.append('5-chain in ' + name)
            for j in range(len(lev)):
                if arrE[:, j].max() >= 4 and other[lev[j]] != 5: bad.append('4-chain in %s not ending in X' % name)
        rest = [v for v in lev if other[v] != 5]
        if len(rest) >= 2:
            B = Analysis([S.P[v] for v in rest])
            if (B.capE if key == 'cap' else B.cupE).max() >= 4: bad.append('4-chain in %s minus X' % name)
    # Lemma 4: X empty => nothing to check; octagon-free is part of S.ok
    return bad
if __name__ == '__main__':
    tot = 0; nbad = 0; sizes = []
    for fn in sys.argv[1:]:
        for line in open(fn):
            P = [tuple(p) for p in json.loads(line)['P']]
            for tr in (lambda p: p, lambda p: (-p[0], p[1]), lambda p: (p[0], -p[1]), lambda p: (-p[0], -p[1])):
                b = check([tr(p) for p in P]); tot += 1; sizes.append(len(P))
                if b: nbad += 1; print('VIOLATION', fn, b)
    print(f'lemma checks: {tot} oriented sets (4 symmetric images each), sizes {min(sizes)}..{max(sizes)}, violations: {nbad}')
