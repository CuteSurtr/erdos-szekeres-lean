#!/usr/bin/env python3
"""Independent re-derivation of the variable numbering of C7UPPER/gen.py Enc(6,8,10) (reviewer code).

Triple variables: combinations of range(60) in lexicographic order; each triple's rotation orbit under
(i,k) -> (i,k+1 mod 6); canonical representative = lexicographically least sorted rotated triple; a new variable
number is assigned the first time a canonical representative is met (1, 2, ...).
Y(i,j), 1 <= i < j <= 9: numbered consecutively after the triple variables in (i,j) lexicographic order.

Only used to translate variable numbers to triples; cross-checked against gen.py once (see selftest)."""
import itertools

M, T = 6, 10
N = M * T


def rot(x, s):
    return (x // M) * M + (x % M + s) % M


def canon(tr):
    return min(tuple(sorted(rot(x, s) for x in tr)) for s in range(M))


def build():
    var_of = {}
    nv = 0
    for tr in itertools.combinations(range(N), 3):
        c = canon(tr)
        if c not in var_of:
            nv += 1
            var_of[c] = nv
    ntrip = nv
    Y = {}
    for i in range(1, T):
        for j in range(i + 1, T):
            nv += 1
            Y[(i, j)] = nv
    triple_of = {v: c for c, v in var_of.items()}
    Yinv = {v: k for k, v in Y.items()}
    return var_of, triple_of, Y, Yinv, ntrip


VAR_OF, TRIPLE_OF, Y, YINV, NTRIP = build()


def selftest():
    import importlib.util
    R = '<results-dir>'
    s = importlib.util.spec_from_file_location('g', R + '/C7UPPER/gen.py')
    G = importlib.util.module_from_spec(s)
    s.loader.exec_module(G)
    E = G.Enc(6, 8, 10)
    assert E.tvar == VAR_OF, 'triple numbering differs'
    assert E.Y == Y, 'Y numbering differs'
    assert E.ntriplevars == NTRIP == 5710
    return True


if __name__ == '__main__':
    print('ntriple', NTRIP, 'nY', len(Y), 'last var', max(YINV))
    print('selftest vs gen.py:', selftest())
