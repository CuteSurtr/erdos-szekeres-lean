"""Certified version of the negative answers of upper_real.py: for every certificate set of ETVTHY20261113 listed in
upper_real.log as having NO 4-cap-free Delta meeting every upper chain, write the small CNF
    variables x_p (p in Delta);  for every 4-cap K: not all of K;  for every upper chain U: some point of U
(caps and chains from exact integer orientations, pyexact), run CaDiCaL 2.1.3 with LRAT and check with cake_lpr.
usage: upper_real_cert.py upper_real.log outdir"""
import sys, os, json, re, subprocess, hashlib
import pyexact_etvthy as px
from upper_lib import upper_chains, caps4
W = '/home/jay/research/data/etvthy-20261113/'
CAD = '/usr/bin/cadical'; CAKE = os.path.expanduser('~/.local/bin/cake_lpr')
out = sys.argv[2]; os.makedirs(out, exist_ok=True); cache = {}; nok = 0; tot = 0
kfile = {'pool_main.jsonl': 8, 'maxpiece.jsonl': 8, 'maxpiece_dr.jsonl': 8, 'maxpiece_r7.jsonl': 8, 'pool_hept.jsonl': 7}
for line in open(sys.argv[1]):
    mm = re.match(r'NO upper-chain transversal: (\S+) (\d+) (\d+) points', line)
    if not mm: continue
    fn, idx, m = mm.group(1), int(mm.group(2)), int(mm.group(3)); n = kfile[fn]; tot += 1
    if fn not in cache: cache[fn] = [json.loads(l)['P'] for l in open(W + fn)]
    P = sorted(tuple(p) for p in cache[fn][idx]); assert len(P) == m
    O = px.otable(P); capE, cupE, capB, cupB = px.chains(P, O)
    assert max(capB.values()) <= 4 and max(capB[k] + cupB[k] - 2 for k in capB) <= n - 1
    cl = [[-(i + 1) for i in K] for K in caps4(P, O)] + [[i + 1 for i in U] for U in upper_chains(P, O, capB, cupB, n)]
    tag = '%s_%d' % (fn.split('.')[0], idx); cnf = os.path.join(out, tag + '.cnf'); lrat = os.path.join(out, tag + '.lrat')
    with open(cnf, 'w') as f:
        f.write('p cnf %d %d\n' % (m, len(cl)))
        for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
    r = subprocess.run([CAD, '-q', '--lrat=true', '--binary=false', cnf, lrat], capture_output=True, text=True)
    ver = ''
    if r.returncode == 20:
        c = subprocess.run([CAKE, '--CML_HEAP_SIZE=300', '--CML_STACK_SIZE=50', cnf, lrat], capture_output=True, text=True)
        ver = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in c.stdout else 'cake FAILED'
        nok += ver == 's VERIFIED UNSAT'
    h = hashlib.sha256(open(cnf, 'rb').read()).hexdigest()
    if os.path.exists(lrat): os.remove(lrat)
    print('%s index %d (n=%d, %d points): %d clauses, cadical exit %d, %s, cnf sha256 %s' % (fn, idx, n, m, len(cl), r.returncode, ver, h), flush=True)
print('%d of %d negative answers CERTIFIED (cake_lpr)' % (nok, tot), flush=True)
