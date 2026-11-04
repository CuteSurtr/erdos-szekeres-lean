"""[m=4 copy of ROT456/tests/test_reflect.py: 4-fold 52-point set, m4K8t13] Reflection check for the even-m unit Y(1,2): the certified 6-fold 54-point set and its mirror image (complex
conjugation, weight vector (a0,a1,...,a5) -> (a0,a5,...,a1)) both satisfy every clause of m6K8t9, and their
Y(1,2) values differ.  Exact arithmetic (rv.py, 90 digits).  CNFDIR = directory with m6K8t9.cnf and .json."""
import os, sys, json, time
sys.path[:0] = ['<worktree>/cloud/es7-2026-10-19/results/ROT456/tests', '<worktree>/cloud/es7-2026-10-19/results/C7UPPER']
import rv, gen
from test_random_lib import read_reps, CERT
m, K, t = 4, 8, 13
fn = os.path.join(os.environ.get('CNFDIR', '.'), 'm4K8t13.cnf'); meta = json.load(open(fn + '.json'))
reps, nc = read_reps(m, CERT[m])
mirror = [tuple([w[0]] + list(w[1:])[::-1]) for w in reps]
E = gen.Enc(m, K, t)
y12 = E.Y[(1, 2)]
def check(reps, label):
    cfg = rv.layered(m, reps); sg = rv.otable(cfg)
    val, nb = rv.assign(E, cfg, sg)
    A = bytearray(meta['nv'] + 1)
    for v, b in val.items(): A[v] = 1 if b else 0
    for pas in (1, 2):
        bad = 0; idx = 0
        with open(fn) as f:
            f.readline()
            for line in f:
                idx += 1
                cl = [int(x) for x in line.split()[:-1]]
                if not any((l > 0 and A[l]) or (l < 0 and not A[-l]) for l in cl):
                    pos = [l for l in cl if l > nb]
                    if pas == 1 and len(pos) == 1: A[pos[0]] = 1
                    else: bad += 1
        assert idx == meta['ncl'], (idx, meta['ncl'])
    print('%s: layers=%d psi=%s clauses=%d nviol=%d Y(1,2)=%d' % (label, cfg['t'], [round(x, 4) for x in cfg['psi']], idx, bad, A[y12]), flush=True)
    return bad, A[y12]
b0, y0 = check(reps, 'original'); b1, y1 = check(mirror, 'mirror')
assert b0 == 0 and b1 == 0 and y0 != y1
print('OK: both satisfy the CNF; Y(1,2) differs')
