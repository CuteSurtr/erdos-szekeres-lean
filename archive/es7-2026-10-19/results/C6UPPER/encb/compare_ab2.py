#!/usr/bin/env python3
"""Semantic comparison of the non-chain parts of encoders A (gen.py) and B (gen_b.py).
For every triple orbit and every phase pattern of its layers (psi-order consistent, H bits), compute the
orientation literals forced by each encoder's clauses (A: families angle+nest; B: all clauses without chain
variables), with B's variables translated into A's, and compare.  Also compares the unconditional units.
usage: compare_ab.py A.cnf B.cnf
"""
import sys, json, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0] + '/../../C7UPPER')
import gen


def main():
    fa, fb = sys.argv[1], sys.argv[2]
    ma = json.load(open(fa + '.json')); mb = json.load(open(fb + '.map.json'))
    m, K, t = ma['m'], ma['K'], ma['t']
    E = gen.Enc(m, K, t)
    # variable translation B -> A literal
    tr = {}
    for c, v in mb['orb']:
        ids = [i * m + k for (i, k) in c]
        tr[v] = E.o(*ids)
    for i, j, v in mb['Y']:
        tr[v] = E.Y[(i, j)]
    for i, v in mb['H']:
        tr[v] = E.H[i]
    baseB = len(mb['orb']) + len(mb['Y']) + len(mb['H'])
    def tl(l):
        x = tr[abs(l)]
        return x if l > 0 else -x
    # collect clauses
    A = []
    a0, a1 = ma['ranges']['angle'][0], ma['ranges']['nest'][1]
    with open(fa) as f:
        f.readline()
        for idx, line in enumerate(f):
            if idx >= a1:
                break
            if idx >= a0:
                A.append(list(map(int, line.split()))[:-1])
    B = []
    with open(fb) as f:
        f.readline()
        for line in f:
            cl = list(map(int, line.split()))[:-1]
            if any(abs(l) > baseB for l in cl):
                continue
            cl = [tl(l) for l in cl]
            # skip B's psi-transitivity clauses (only Y literals, 3 of them)
            if all(abs(l) in E.Y.values() for l in cl):
                continue
            B.append(cl)
    nt = E.ntriplevars
    def group(cls):
        g = {}
        for cl in cls:
            o = [l for l in cl if abs(l) <= nt]
            assert len(o) == 1, cl
            g.setdefault(abs(o[0]), []).append(cl)
        return g
    gA, gB = group(A), group(B)
    print('clauses A', len(A), 'B', len(B), 'orbits with clauses A', len(gA), 'B', len(gB))
    inv = {v: C for C, v in E.tvar.items()}
    mism = 0; checked = 0
    for v in set(gA) | set(gB):
        C = inv[v]
        Ls = sorted(set(x // m for x in C))
        free = [L for L in Ls if L != 0]
        for perm in itertools.permutations(free):
            rk = {L: r for r, L in enumerate(perm)}
            for hb in itertools.product([True, False], repeat=len(free) if E.odd else 0):
                val = {}
                for a, b in itertools.combinations(free, 2):
                    y = E.Y[(min(a, b), max(a, b))]
                    val[y] = rk[min(a, b)] < rk[max(a, b)]
                for L, h in zip(free, hb):
                    val[E.H[L]] = h
                def fired(cls):
                    out = set()
                    for cl in cls:
                        prem_false = True
                        olit = None
                        for l in cl:
                            if abs(l) <= nt:
                                olit = l
                            else:
                                x = val.get(abs(l))
                                if x is None:
                                    raise RuntimeError('premise var outside pattern')
                                if (x if l > 0 else not x):
                                    prem_false = False
                        if prem_false:
                            out.add(olit)
                    return out
                fa_ = fired(gA.get(v, [])); fb_ = fired(gB.get(v, []))
                checked += 1
                if fa_ != fb_:
                    mism += 1
                    if mism < 5:
                        print('MISMATCH', C, perm, hb, fa_, fb_)
    print('orbit-pattern pairs checked', checked, 'mismatches', mism)


main()
