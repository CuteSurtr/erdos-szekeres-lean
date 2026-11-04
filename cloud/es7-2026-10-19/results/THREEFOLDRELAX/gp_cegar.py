#!/usr/bin/env python3
"""gp_cegar.py m K t BASE.cnf DEADLINE_EPOCH : lazily add 3-term Grassmann-Pluecker sign clauses (sound for every
planar configuration: [abc][ade] - [abd][ace] + [abe][acd] = 0, so the three products are not all of one sign) for
relations violated by the current model; re-solve until UNSAT, a GP-consistent model, or the deadline.
Each round writes cnf/gp_<tag>_rN.cnf (base + all GP clauses so far)."""
import sys, os, itertools, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gen_relax as G
m, K, t = map(int, sys.argv[1:4]); base = sys.argv[4]; deadline = float(sys.argv[5])
CAD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'bin', 'cadical')
E = G.Enc(m, K, t)
n = m * t
hdr = open(base).readline().split(); nv, nc = int(hdr[2]), int(hdr[3])
gp = set()
def rel_clauses(a, b, c, d, e):
    L = [E.o(a, b, c), E.o(a, d, e), E.o(a, b, d), E.o(a, c, e), E.o(a, b, e), E.o(a, c, d)]
    out = []
    for bits in itertools.product([1, -1], repeat=6):
        s = [bits[0] * bits[1], -bits[2] * bits[3], bits[4] * bits[5]]
        if s[0] == s[1] == s[2]:
            out.append(tuple(sorted(-(L[i] if bits[i] > 0 else -L[i]) for i in range(6))))
    return out
tag = 'm%dK%dt%d' % (m, K, t)
rnd = 0
while True:
    rnd += 1
    fn = 'cnf/gp_%s_r%d.cnf' % (tag, rnd)
    with open(fn, 'w') as f, open(base) as g:
        f.write('p cnf %d %d\n' % (nv, nc + len(gp)))
        g.readline()
        while True:
            buf = g.read(1 << 24)
            if not buf: break
            f.write(buf)
        for cl in gp: f.write(' '.join(map(str, cl)) + ' 0\n')
    left = int(deadline - time.time())
    if left < 10: print('round', rnd, 'deadline'); break
    mf = 'logs/gp_%s_r%d.model' % (tag, rnd)
    r = subprocess.run([CAD, '-t', str(min(left, 300)), '-q', fn, '-w', mf], capture_output=True)
    print('round', rnd, 'gp_clauses', len(gp), 'exit', r.returncode, flush=True)
    if r.returncode != 10:
        break
    os.remove(fn) if rnd > 1 else None
    val = set()
    for line in open(mf):
        if line.startswith('v'): val.update(int(x) for x in line.split()[1:] if x != '0')
    chi = lambda a, b, c: 1 if E.o(a, b, c) in val else -1
    new = 0
    for S in itertools.combinations(range(n), 5):
        if S[0] % m != 0: continue   # one representative per rotation class (orbit variables are rotation-invariant)
        for a in S:
            b, c, d, e = [x for x in S if x != a]
            if chi(a, b, c) * chi(a, d, e) == -chi(a, b, d) * chi(a, c, e) == chi(a, b, e) * chi(a, c, d):
                for cl in rel_clauses(a, b, c, d, e):
                    if cl not in gp: gp.add(cl); new += 1
    print('  violated-relation clauses added', new, flush=True)
    if new == 0:
        print('GP-consistent model (all 3-term relations)'); break
