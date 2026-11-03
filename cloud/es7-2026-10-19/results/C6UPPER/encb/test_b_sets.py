"""Exact check of encoder B (gen_b2.py) on real sets: the certified 6-fold 54-point set and its mirror image must
satisfy every clause of B's m6K8t9 CNF.  Orientations come from ROT456/tests/rv.py (90-digit arithmetic, cyclotomic
coordinates); B's orbit variables are read through B's own map file; chain variables take their least fixpoint.
usage: python3 test_b_sets.py B_m6K8t9.cnf"""
import os, sys, json, math
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(H, '..', '..', 'ROT456', 'tests')); sys.path.insert(0, os.path.join(H, '..', '..', 'C7UPPER'))
import rv, gen
from test_random_lib import read_reps, CERT
fn = sys.argv[1]; mp = json.load(open(fn + '.map.json'))
m, K, t = mp['m'], mp['K'], mp['t']; assert (m, t) == (6, 9)
E = gen.Enc(m, K, t)
reps, nc = read_reps(m, CERT[m]); mirror = [tuple([w[0]] + list(w[1:])[::-1]) for w in reps]
base = len(mp['orb']) + len(mp['Y']) + len(mp['H'])
def check(reps, label):
    cfg = rv.layered(m, reps); sg = rv.otable(cfg)
    val, _ = rv.assign(E, cfg, sg)                     # true values of A's variables
    A = bytearray(mp['nv'] + 1)
    for c, v in mp['orb']:                             # B orbit var := orient of B's canonical triple
        l = E.o(*[i * m + k for (i, k) in c]); A[v] = 1 if (val[abs(l)] == (l > 0)) else 0
    psi = cfg['psi']
    for i, j, v in mp['Y']: A[v] = 1 if psi[i] < psi[j] else 0
    for pas in (1, 2):
        bad = 0; idx = 0
        with open(fn) as f:
            f.readline()
            for line in f:
                idx += 1
                cl = [int(x) for x in line.split()[:-1]]
                if not any((l > 0 and A[l]) or (l < 0 and not A[-l]) for l in cl):
                    pos = [l for l in cl if l > base]
                    if pas == 1 and len(pos) == 1: A[pos[0]] = 1
                    else: bad += 1
        assert idx == mp['ncl']
    y12 = next(v for i, j, v in mp['Y'] if (i, j) == (1, 2))
    print('%s: clauses=%d nviol=%d Y(1,2)=%d' % (label, idx, bad, A[y12]), flush=True)
    return bad
assert check(reps, 'original') == 0 and check(mirror, 'mirror') == 0
print('OK: both sets satisfy every clause of', os.path.basename(fn))
