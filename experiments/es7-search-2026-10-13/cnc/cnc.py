#!/usr/bin/env python3
"""Adaptive cube-and-conquer over a CNF with persistent CaDiCaL workers.

Cubes form a binary partition: the root cube is empty; a cube that exhausts its
conflict budget is split on the worker's lookahead literal into cube+[l] and
cube+[-l]. Every cube is therefore closed (UNSAT), satisfiable (stop), or still
open; the open cubes always cover exactly the not-yet-refuted part of the search.
Progress weight of a cube = 2^-len(cube). State is checkpointed atomically.
UNSAT answers here are solver claims without proof logs (search, not proof).
"""
import heapq, json, os, subprocess, sys, threading, time, queue
from pathlib import Path
cnf, outdir, nworkers = sys.argv[1], Path(sys.argv[2]), int(sys.argv[3])
base_limit = int(os.environ.get('BASE_LIMIT', '20000')); grow = float(os.environ.get('GROW', '1.6'))
outdir.mkdir(parents=True, exist_ok=True)
state_path = outdir / 'state.json'
if state_path.exists():
    st = json.loads(state_path.read_text())
else:
    st = {'cnf': cnf, 'open': [[[], base_limit]], 'closed_weight': 0.0, 'closed': 0, 'splits': 0,
          'sat': None, 'started': time.time(), 'cpu_jobs': 0}
lock = threading.Lock(); stop = threading.Event()
deques = [[] for _ in range(nworkers)]  # per-worker lineage queues (learned-clause locality)
open_set = {}
next_id = [0]
def enqueue(cube, limit, w=None):
    i = next_id[0]; next_id[0] += 1; open_set[i] = (cube, limit)
    if w is None: w = min(range(nworkers), key=lambda k: len(deques[k]))
    deques[w].append(i)
for cube, limit in st['open']: enqueue(cube, limit)
def take(w):
    with lock:
        if deques[w]: return deques[w].pop()
        victim = max(range(nworkers), key=lambda k: len(deques[k]))
        if deques[victim]: return deques[victim].pop(0)
        return None
def save():
    st['open'] = [list(v) for v in open_set.values()]
    tmp = state_path.with_suffix('.tmp'); tmp.write_text(json.dumps(st)); tmp.replace(state_path)
log = open(outdir / 'cnc.log', 'a')
def worker(w):
    p = subprocess.Popen([str(Path(__file__).with_name('worker')), cnf, str(outdir)], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, text=True, bufsize=1)
    assert p.stdout.readline().startswith('READY')
    while not stop.is_set():
        i = take(w)
        if i is None:
            with lock:
                if not open_set: return
            time.sleep(1); continue
        cube, limit = open_set[i]
        p.stdin.write(f"{i} {limit} {' '.join(map(str, cube))} 0\n"); p.stdin.flush()
        r = p.stdout.readline().split()
        with lock:
            st['cpu_jobs'] += 1
            del open_set[i]
            if r[0] == 'U':
                st['closed'] += 1; st['closed_weight'] += 2.0 ** -len(cube)
            elif r[0] == 'S':
                st['sat'] = {'cube': cube, 'model': f'model-{i}.txt', 'time': time.time()}
                log.write(json.dumps({'event': 'SAT', 'cube': cube, 'model': f'model-{i}.txt'}) + '\n'); log.flush()
                stop.set()
            else:
                lit = int(r[2]); st['splits'] += 1
                if lit == 0:  # no split literal: retry the cube with a larger budget
                    enqueue(cube, int(limit * grow), w)
                else:
                    nl = int(limit * grow)
                    enqueue(cube + [-lit], nl, w); enqueue(cube + [lit], nl, w)
    p.kill()
threads = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(nworkers)]
for t in threads: t.start()
last = 0
while any(t.is_alive() for t in threads):
    time.sleep(5)
    if time.time() - last > 60:
        with lock:
            save()
            d = max((len(c) for c, _ in open_set.values()), default=0)
            log.write(json.dumps({'t': round(time.time() - st['started']), 'closed': st['closed'], 'closed_weight': st['closed_weight'],
                                  'open': len(open_set), 'max_depth': d, 'splits': st['splits'], 'jobs': st['cpu_jobs'], 'sat': bool(st['sat'])}) + '\n'); log.flush()
        last = time.time()
with lock: save()
print(json.dumps({'sat': st['sat'], 'closed': st['closed'], 'closed_weight': st['closed_weight'], 'open': len(open_set)}))
