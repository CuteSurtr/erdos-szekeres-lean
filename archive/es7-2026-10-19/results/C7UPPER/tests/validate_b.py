#!/usr/bin/env python3
"""Validate a gen_b.py CNF against real configurations (float64).
usage: validate_b.py CNF (pts FILE | random N seed)"""
import sys, json, math, random
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from validate import orient_f, layers_to_points, read_pts, random_layers


def assignment(mp, layers):
    m, t = mp['m'], mp['t']
    pts, lay = layers_to_points(m, layers)          # pts[i*m+k]
    A = {}
    mind = float('inf')
    for c, v in mp['orb']:
        P = [pts[i * m + k] for (i, k) in c]
        d = orient_f(*P)
        mind = min(mind, abs(d))
        A[v] = d > 0
    psi = [th % (math.pi / m) for (_, th) in lay]
    for i, j, v in mp['Y']:
        A[v] = psi[i] < psi[j]
    for i, v in mp['H']:
        A[v] = lay[i][1] < math.pi / m
    return A, mind


def check(cnf, mp, A):
    base = len(mp['orb']) + len(mp['Y']) + len(mp['H'])
    bad_chain = 0; bad_other = 0
    def lv(l):
        x = A.get(abs(l), False)
        return x if l > 0 else not x
    with open(cnf) as f:
        f.readline()
        for line in f:
            cl = list(map(int, line.split()))[:-1]
            if any(lv(l) for l in cl):
                continue
            pos = [l for l in cl if l > base]
            if pos:
                A[pos[0]] = True
                continue
            if any(abs(l) > base for l in cl):
                bad_chain += 1
            else:
                bad_other += 1
    return bad_other, bad_chain


if __name__ == '__main__':
    cnf = sys.argv[1]
    mp = json.load(open(cnf + '.map.json'))
    if sys.argv[2] == 'pts':
        layers = read_pts(sys.argv[3], mp['m'])[:mp['t']]
        A, mind = assignment(mp, layers)
        print(sys.argv[3].rsplit('/', 1)[-1], 'min|det| %.3g' % mind, 'unsat (geometric, chain):', check(cnf, mp, A))
    else:
        N = int(sys.argv[3]); rng = random.Random(int(sys.argv[4]))
        tot_o = 0; tot_c = 0; n = 0
        for s in range(N):
            layers = random_layers(mp['m'], mp['t'], rng, 'needle' if s % 2 else 'free')
            A, mind = assignment(mp, layers)
            if mind < 1e-9:
                continue
            o, c = check(cnf, mp, A)
            n += 1; tot_o += (o > 0); tot_c += (c > 0)
            if o:
                print('VIOLATION geometric', o, layers)
        print('random configs', n, 'with geometric violations', tot_o, 'with chain violations', tot_c)
