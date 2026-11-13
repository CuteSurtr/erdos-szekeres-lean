#!/usr/bin/env python3
"""Solve one shard of a march_cu cube file, with LRAT checking and recursive splitting.

usage: shard.py <cnf> <cubes.icnf> <shard> <nshards> <bindir> <workdir> <resultdir> [workers=4] [tlim=300] [split_depth=6]

Shard = cubes whose 0-based line index i satisfies i % nshards == shard.
Each job is CNF + cube literals as unit clauses, solved by `cadical --lrat --binary=false -t tlim`;
the proof is streamed through a FIFO into drat-trim's `lrat-check` against that same CNF, so no
proof file is stored.  A cube is UNSAT-certified only if cadical says UNSAT and lrat-check prints
"c VERIFIED".  A cube that hits the time limit is split with `march_cu -d split_depth` on
CNF + cube; the children are march_cu's leaves (it also writes the leaves it refuted by look-ahead), checked
to form a complete binary decision tree (any missing sibling branch would be added), so every
child is again solved with LRAT and the children partition the parent.  If march_cu refutes the
whole sub-problem ("a 0"), the cube is re-solved once with 8x the time limit instead.

Outputs in <resultdir>: leaves.jsonl (one line per finished leaf), splits.jsonl (one line per
split node, with its children), sat/ (models of SAT leaves).  Restart-safe: finished leaves and
recorded splits are not redone.
"""
import sys, os, json, subprocess, time, threading, queue, hashlib

cnf, cubef, shard, nsh, bindir, wd, rd = sys.argv[1:8]
shard, nsh = int(shard), int(nsh)
workers = int(sys.argv[8]) if len(sys.argv) > 8 else 4
tlim = int(sys.argv[9]) if len(sys.argv) > 9 else 300
sdepth = int(sys.argv[10]) if len(sys.argv) > 10 else 6
FORCE = int(os.environ.get('SHARD_TEST_FORCE_SPLIT_BELOW', '0'))   # testing only; 0 in real runs
os.makedirs(wd, exist_ok=True); os.makedirs(os.path.join(rd, 'sat'), exist_ok=True)
LEAVES, SPLITS = os.path.join(rd, 'leaves.jsonl'), os.path.join(rd, 'splits.jsonl')

head, body = None, []
with open(cnf) as f:
    for line in f:
        if line.startswith('p'): head = line.split(); continue
        if line.startswith('c'): continue
        body.append(line)
NV, NC = int(head[2]), int(head[3])
BODY = ''.join(body); del body

def read_cubes(path):
    out = []
    for line in open(path):
        t = line.split()
        if t and t[0] == 'a': out.append([int(x) for x in t[1:-1]])
    return out

def complete_children(cubes):
    """Given march_cu leaf cubes (decision sequences), return them plus the missing (refuted)
    sibling branches so that the result is a complete binary partition. Raises if the cubes do
    not form a binary decision tree."""
    out = []
    def rec(cs, pre):
        if any(len(c) == len(pre) for c in cs):
            if len(cs) != 1: raise ValueError('leaf with descendants at %r' % (pre,))
            out.append(list(pre)); return
        vs = set(abs(c[len(pre)]) for c in cs)
        if len(vs) != 1: raise ValueError('two decision variables at %r' % (pre,))
        v = vs.pop()
        for lit in (v, -v):
            sub = [c for c in cs if c[len(pre)] == lit]
            if sub: rec(sub, pre + [lit])
            else: out.append(pre + [lit])          # refuted by march_cu: solve it anyway
    if cubes: rec(cubes, [])
    return out

lock = threading.Lock()
def append(path, obj):
    with lock:
        with open(path, 'a') as f: f.write(json.dumps(obj) + '\n'); f.flush(); os.fsync(f.fileno())

def write_cnf(path, cube):
    with open(path, 'w') as f:
        f.write('p cnf %d %d\n' % (NV, NC + len(cube))); f.write(BODY)
        for l in cube: f.write('%d 0\n' % l)

def solve(cube, tag, lim):
    d = os.path.join(wd, tag); os.makedirs(d, exist_ok=True)
    c = os.path.join(d, 'f.cnf'); p = os.path.join(d, 'p'); write_cnf(c, cube)
    if os.path.exists(p): os.remove(p)
    os.mkfifo(p)
    chk = subprocess.Popen([os.path.join(bindir, 'lrat-check'), c, p],
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    t0 = time.time()
    r = subprocess.run([os.path.join(bindir, 'cadical'), '--lrat', '--binary=false', '-t', str(lim), c, p],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0
    out = chk.communicate()[0]
    st = [l for l in r.stdout.splitlines() if l.startswith('s ')]
    st = st[0][2:] if st else 'UNKNOWN'
    model = [l for l in r.stdout.splitlines() if l.startswith('v ')]
    lines = out.splitlines()
    ver = 'VERIFIED' if 'c VERIFIED' in lines else ('NOT VERIFIED' if 'c NOT VERIFIED' in lines else 'NO RESULT')
    return st, dt, ver, model, c, d

def march_split(cube, tag):
    d = os.path.join(wd, tag); os.makedirs(d, exist_ok=True)
    c = os.path.join(d, 'f.cnf'); write_cnf(c, cube); o = os.path.join(d, 'sub.icnf')
    t0 = time.time()
    r = subprocess.run([os.path.join(bindir, 'march_cu'), c, '-d', str(sdepth), '-o', o],
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    dt = time.time() - t0
    sat = any(l.startswith('s SATISFIABLE') for l in r.stdout.splitlines())
    subs = read_cubes(o) if os.path.exists(o) else []
    refl = [l for l in r.stdout.splitlines() if 'refuted' in l.lower()]
    return subs, dt, sat, refl, r.stdout[-2000:]

def key(c): return ' '.join(map(str, c))

# ---- restart state
done, splits = {}, {}
if os.path.exists(LEAVES):
    for line in open(LEAVES):
        o = json.loads(line); done[key(o['cube'])] = o
if os.path.exists(SPLITS):
    for line in open(SPLITS):
        o = json.loads(line)
        if 'children' in o: splits[key(o['cube'])] = o

allc = read_cubes(cubef)
mine = [(i, c) for i, c in enumerate(allc) if i % nsh == shard]
print('shard %d/%d: %d of %d cubes' % (shard, nsh, len(mine), len(allc)), flush=True)

Q = queue.Queue()
def enqueue(root, cube):
    k = key(cube)
    if k in done: return
    if k in splits:
        for ch in splits[k]['children']: enqueue(root, ch)
        return
    Q.put((root, cube))
for i, c in mine: enqueue(i, c)

def worker(w):
    while True:
        try: item = Q.get(timeout=5)
        except queue.Empty:
            if busy[0] == 0 and Q.empty(): return
            continue
        with lock: busy[0] += 1
        try:
            root, cube = item[0], item[1]; lim = item[2] if len(item) > 2 else tlim
            tag = 'w%d' % w
            if len(cube) < FORCE: st, dt, ver, model = 'UNKNOWN', 0.0, '', []   # testing only
            else: st, dt, ver, model, cpath, d = solve(cube, tag, lim)
            if st == 'UNSATISFIABLE':
                rec = {'root': root, 'cube': cube, 'depth': len(cube), 'status': 'UNSAT', 'time_s': round(dt, 2), 'lrat': ver}
                append(LEAVES, rec); print(json.dumps(rec), flush=True)
            elif st == 'SATISFIABLE':
                h = hashlib.sha256(key(cube).encode()).hexdigest()[:16]
                mp = os.path.join(rd, 'sat', 'model_%s.txt' % h)
                with open(mp, 'w') as f: f.write('c cube ' + key(cube) + '\n' + '\n'.join(model) + '\n')
                rec = {'root': root, 'cube': cube, 'depth': len(cube), 'status': 'SAT', 'time_s': round(dt, 2), 'lrat': 'n/a', 'model': os.path.basename(mp)}
                append(LEAVES, rec); print('SAT ' + json.dumps(rec), flush=True)
                open(os.path.join(rd, 'SAT_FOUND'), 'a').write(mp + '\n')
            elif lim > tlim:
                rec = {'root': root, 'cube': cube, 'depth': len(cube), 'status': 'OPEN', 'time_s': round(dt, 2), 'lrat': 'n/a'}
                append(SPLITS, rec); print('OPEN ' + json.dumps(rec), flush=True)
            else:
                subs, mdt, msat, refl, mout = march_split(cube, tag)
                if msat:
                    append(SPLITS, {'root': root, 'cube': cube, 'note': 'march_cu reported SAT', 'out': mout})
                    open(os.path.join(rd, 'SAT_FOUND'), 'a').write('march_cu SAT on ' + key(cube) + '\n')
                    continue
                rel = complete_children(subs)
                if rel == [[]] or not rel:
                    # march_cu refuted CNF + cube by look-ahead alone; that is not LRAT-checked, so
                    # re-solve this cube once more with a long time limit instead of splitting.
                    rec = {'root': root, 'cube': cube, 'note': 'march_cu refuted whole cube; long re-solve', 'out': mout[-300:]}
                    append(SPLITS, rec); Q.put((root, cube, tlim * 8))
                    continue
                children = [cube + r for r in rel]
                rec = {'root': root, 'cube': cube, 'depth': len(cube), 'timeout_s': round(dt, 2), 'cadical_status': st,
                       'march_time_s': round(mdt, 2), 'march_cubes': len(subs), 'march_refuted_info': refl[-3:],
                       'children': children, 'n_children': len(children)}
                append(SPLITS, rec); splits[key(cube)] = rec
                print('SPLIT root %d depth %d -> %d children (%d march cubes)' % (root, len(cube), len(children), len(subs)), flush=True)
                for ch in children: Q.put((root, ch))
        finally:
            with lock: busy[0] -= 1

busy = [0]
ts = [threading.Thread(target=worker, args=(w,)) for w in range(workers)]
for t in ts: t.start()
for t in ts: t.join()
print('queue empty; finished', flush=True)
