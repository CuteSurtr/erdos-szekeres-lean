#!/usr/bin/env python3
"""Adaptive cube-and-conquer for the PRIMEFOLD Theorem E relaxation (clsat2.py 9 29 1) under the symmetry-breaking unit
A = -G[8,5] (justified by sigma-invariance, see README).  Single thread.
Each open cube: CaDiCaL without proof for TL s.  UNSAT -> re-solve with text LRAT (limit PL s) -> cake_lpr -> record
(hashes; proof zstd-compressed only after 's VERIFIED UNSAT').  SAT -> record model.  Unknown -> split on the
lookahead-best variable (pysat minisat22 propagation, product of implied-literal counts) into two children.
State in OUT/: tree.tsv (node id, parent, cube, status), nodes/<id>/.  Order: DFS (deepest first) unless BFS=1."""
import os, sys, time, json, subprocess, hashlib
from pysat.formula import CNF
from pysat.solvers import Solver
M9 = '/home/jay/research/data/satopen-20261113/m9'
CNFF = os.environ.get('CNFF', M9 + '/m9_n29_s1.cnf')
OUT = os.environ.get('OUT', M9 + '/cc1')
TL = int(os.environ.get('TL', 30)); PL = int(os.environ.get('PL', 600))
ROOT = json.loads(os.environ.get('ROOT', '[-11834]'))      # G[8,5] = 11834
BFS = os.environ.get('BFS', '0') == '1'
HARD = os.environ.get('HARD', '05:36')
os.makedirs(OUT + '/nodes', exist_ok=True)
F = CNF(from_file=CNFF); NV = F.nv; HDR = open(CNFF).readline().split(); NCL = int(HDR[3])
BODY = open(CNFF).read().split('\n', 1)[1]
S = Solver(name='m22', bootstrap_with=F.clauses)
def log(msg):
    with open(OUT + '/log.txt', 'a') as f: f.write(time.strftime('%F %T ') + msg + '\n')
def write_cnf(path, cube):
    with open(path, 'w') as f:
        f.write('p cnf %d %d\n' % (NV, NCL + len(cube))); f.write(BODY)
        if not BODY.endswith('\n'): f.write('\n')
        for l in cube: f.write('%d 0\n' % l)
def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 22), b''): h.update(b)
    return h.hexdigest()
def lookahead(cube):
    st, imp = S.propagate(assumptions=cube)
    if not st: return None
    base = len(imp); fixed = set(abs(l) for l in imp) | set(abs(l) for l in cube)
    best = None
    for v in range(1, NV + 1):
        if v in fixed: continue
        a = S.propagate(assumptions=cube + [v]); b = S.propagate(assumptions=cube + [-v])
        if not a[0] or not b[0]: continue      # failed literal: not used as a split variable
        sc = (len(a[1]) - base) * (len(b[1]) - base) + len(a[1]) + len(b[1])
        if best is None or sc > best[0]: best = (sc, v)
    return best
nodes = {}   # id -> dict
tree = OUT + '/tree.tsv'
if os.path.exists(tree):
    for line in open(tree):
        i, par, cube, stt = line.rstrip('\n').split('\t'); nodes[i] = dict(par=par, cube=json.loads(cube), st=stt)
else:
    nodes['r'] = dict(par='-', cube=ROOT, st='open')
def save():
    with open(tree + '.tmp', 'w') as f:
        for i, d in nodes.items(): f.write('%s\t%s\t%s\t%s\n' % (i, d['par'], json.dumps(d['cube']), d['st']))
    os.replace(tree + '.tmp', tree)
save(); log('start TL=%d PL=%d ROOT=%s BFS=%s' % (TL, PL, ROOT, BFS))
while True:
    if time.strftime('%H:%M') >= HARD and time.strftime('%H:%M') < '12:00': log('hard deadline'); break
    op = [i for i, d in nodes.items() if d['st'] == 'open']
    if not op: log('no open cubes: done'); break
    i = (min if BFS else max)(op, key=lambda k: (len(nodes[k]['cube']), k))
    d = nodes[i]; nd = OUT + '/nodes/' + i; os.makedirs(nd, exist_ok=True)
    cnf = nd + '/cube.cnf'; write_cnf(cnf, d['cube'])
    t0 = time.time()
    r = subprocess.run(['cadical', '-q', '-t', str(TL), cnf], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode
    t1 = time.time() - t0
    if r == 20:
        t0 = time.time()
        r2 = subprocess.run(['cadical', '-t', str(PL), '--lrat', '--binary=false', cnf, nd + '/proof.lrat'],
                            stdout=open(nd + '/cadical.out', 'w'), stderr=subprocess.STDOUT).returncode
        t2 = time.time() - t0
        if r2 != 20:
            d['st'] = 'unsat-noproof'; log('%s UNSAT in %.1fs but proof run rc=%d' % (i, t1, r2)); save(); continue
        hc, hp = sha(cnf), sha(nd + '/proof.lrat'); sz = os.path.getsize(nd + '/proof.lrat')
        t0 = time.time()
        ck = subprocess.run([os.path.expanduser('~/.local/bin/cake_lpr'), '--CML_HEAP_SIZE=%s' % os.environ.get('CAKEHEAP', '1500'), '--CML_STACK_SIZE=300', cnf, nd + '/proof.lrat'],
                            capture_output=True, text=True)
        t3 = time.time() - t0
        ok = any(l.strip() == 's VERIFIED UNSAT' for l in ck.stdout.splitlines())
        with open(nd + '/result.txt', 'w') as f:
            f.write('cube %s %s\ncnf_sha256 %s\nproof_sha256 %s\nproof_bytes %d\nsolve_noproof %.1fs proof_run %.1fs cake %.1fs\ncake_stdout %s\ncake_stderr %s\nVERIFIED %s\n'
                    % (i, json.dumps(d['cube']), hc, hp, sz, t1, t2, t3, ck.stdout.strip()[:200].replace('\n', ' | '), ck.stderr.strip()[:200].replace('\n', ' | '), ok))
        if ok:
            subprocess.run(['zstd', '-q', '-3', '-T1', '--rm', nd + '/proof.lrat', '-o', nd + '/proof.lrat.zst'])
            os.remove(cnf); d['st'] = 'verified'
        else: d['st'] = 'unsat-unverified'
        log('%s depth %d UNSAT %.1fs, proof %.1fs %dB, cake %.1fs %s' % (i, len(d['cube']), t1, t2, sz, t3, 'VERIFIED' if ok else 'NOT VERIFIED'))
    elif r == 10:
        d['st'] = 'SAT'; os.rename(cnf, nd + '/sat_cube.cnf'); log('%s SAT (!) in %.1fs' % (i, t1))
    else:
        os.remove(cnf)
        t0 = time.time(); b = lookahead(d['cube']); tl = time.time() - t0
        if b is None: d['st'] = 'propfail'; log('%s: cube fails by propagation (rc=%d)' % (i, r)); save(); continue
        v = b[1]; d['st'] = 'split:%d' % v
        nodes[i + '0'] = dict(par=i, cube=d['cube'] + [v], st='open'); nodes[i + '1'] = dict(par=i, cube=d['cube'] + [-v], st='open')
        log('%s depth %d unknown after %.1fs; split on %d (score %d, lookahead %.1fs)' % (i, len(d['cube']), t1, v, b[0], tl))
    save()
S.delete()
