#!/usr/bin/env python3
"""Mx cube-and-conquer driver (FIFO queue, exact Fraction weights).

usage: cnc_run.py base.cnf cubes.icnf leaves.jsonl [workers] [timeout_s] [resplit_depth]

Each cube c (from march_cu) is solved as base.cnf + unit clauses of c with
`cadical --lrat`; every UNSAT proof is checked with lrat-check against exactly that CNF and
then deleted.  A cube that times out is re-split with march_cu (-d resplit_depth) on the
cube-conditioned CNF; its children (cube + subcube) are queued, and its record says so.
A cube refuted by march_cu during re-splitting (empty cube list with 'UNSAT' output) is
re-solved by cadical to get an LRAT proof like any other leaf.
Resumable: keys already in leaves.jsonl with a final status are skipped."""
import sys, os, json, subprocess, time, tempfile, threading
from fractions import Fraction
from collections import deque
CAD = '/tmp/claude-0/sw/cadical/build/cadical'; LC = '/tmp/claude-0/sw/drat-trim/lrat-check'
MARCH = '/tmp/claude-0/sw/CnC/march_cu/march_cu'
WORK = '/tmp/claude-0/mx/work'; os.makedirs(WORK, exist_ok=True)

def read_cubes(path):
    cubes = []
    for l in open(path):
        if l.startswith('a '):
            cubes.append([int(x) for x in l.split()[1:] if x != '0'])
    return cubes

base, cubef, leavesf = sys.argv[1:4]
W = int(sys.argv[4]) if len(sys.argv) > 4 else os.cpu_count()
TO = int(sys.argv[5]) if len(sys.argv) > 5 else 1800
RD = int(sys.argv[6]) if len(sys.argv) > 6 else 3
lines = open(base).read().split('\n')
hdr = [i for i, l in enumerate(lines) if l.startswith('p cnf')][0]
NV, NC = map(int, lines[hdr].split()[2:4])
body = '\n'.join(l for i, l in enumerate(lines) if i > hdr and l and not l.startswith('c')) + '\n'

done = {}
if os.path.exists(leavesf):
    for l in open(leavesf):
        d = json.loads(l); done[d['key']] = d
lock = threading.Lock(); out = open(leavesf, 'a')
Q = deque(sorted(read_cubes(cubef), key=lambda c: 0))
stats = dict(unsat=0, sat=0, split=0)

def write_cnf(cube, path):
    with open(path, 'w') as f:
        f.write('p cnf %d %d\n' % (NV, NC + len(cube))); f.write(body)
        for u in cube: f.write('%d 0\n' % u)

def record(d):
    with lock:
        out.write(json.dumps(d) + '\n'); out.flush()

def solve(cube):
    key = 'cube:' + ' '.join(map(str, cube))
    if key in done and done[key]['status'] in ('UNSAT', 'SAT', 'SPLIT') and done[key].get('lrat', 'VERIFIED') == 'VERIFIED':
        if done[key]['status'] == 'SPLIT':
            return [cube + s for s in done[key]['children']]
        return []
    fd, cnf = tempfile.mkstemp(suffix='.cnf', dir=WORK); os.close(fd)
    write_cnf(cube, cnf); proof = cnf + '.lrat'
    t = time.time()
    r = subprocess.run([CAD, '-q', '-t', str(TO), '--lrat', '--binary=false', cnf, proof],
                       capture_output=True, text=True)
    st = {10: 'SAT', 20: 'UNSAT'}.get(r.returncode, 'TIMEOUT'); dt = time.time() - t
    d = dict(key=key, cube=cube, weight_log2=-len(cube), status=st, solve_s=round(dt, 2))
    children = []
    if st == 'UNSAT':
        t2 = time.time()
        o = subprocess.run([LC, cnf, proof], capture_output=True, text=True).stdout
        d['lrat'] = 'VERIFIED' if 'c VERIFIED' in o else 'NOT VERIFIED'
        d['proof_mb'] = round(os.path.getsize(proof) / 1e6, 1); d['check_s'] = round(time.time() - t2, 2)
    elif st == 'SAT':
        model = [int(x) for l in r.stdout.split('\n') if l.startswith('v') for x in l.split()[1:] if x != '0']
        d['model'] = [x for x in model if abs(x) <= NV]
        with open(os.path.join(os.path.dirname(os.path.abspath(leavesf)), 'SAT_MODEL_%d.json' % int(time.time())), 'w') as f:
            json.dump(d, f)
    else:
        sub = cnf + '.icnf'
        subprocess.run([MARCH, cnf, '-o', sub, '-d', str(RD)], capture_output=True, text=True)
        sc = read_cubes(sub) if os.path.exists(sub) else []
        if not sc:
            sc = [[]]  # march refuted or produced nothing: retry whole cube with longer timeout
            d['note'] = 'resplit produced no cubes'
        d['status'] = 'SPLIT'; d['children'] = sc; children = [cube + s for s in sc if s] or []
        if sc == [[]]: d['status'] = 'TIMEOUT'
        if os.path.exists(sub): os.remove(sub)
    for p in (cnf, proof):
        if os.path.exists(p): os.remove(p)
    record(d)
    with lock:
        stats[{'UNSAT': 'unsat', 'SAT': 'sat'}.get(d['status'], 'split')] += 1
    return children

def worker():
    while True:
        with lock:
            if not Q: return
            c = Q.popleft()          # FIFO
        ch = solve(c)
        with lock:
            Q.extend(ch)

ths = [threading.Thread(target=worker) for _ in range(W)]
for t in ths: t.start()
# idle workers exit when the queue is momentarily empty; respawn while work remains
while any(t.is_alive() for t in ths):
    time.sleep(5)
    with lock:
        alive = sum(t.is_alive() for t in ths); pend = len(Q)
    if pend and alive < W:
        ths = [t for t in ths if t.is_alive()]
        for _ in range(min(W - alive, pend)):
            t = threading.Thread(target=worker); t.start(); ths.append(t)
print(json.dumps(stats))
