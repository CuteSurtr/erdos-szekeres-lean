#!/usr/bin/env python3
"""Cube-and-conquer driver (cnc2) fixing the known cnc.py bugs.

* Shallowest-first: one global priority queue keyed by (depth, creation order); no per-worker
  stacks, no newest-first popping.
* Exact weights: a cube at depth d has weight 2^-d, accumulated as fractions.Fraction; the
  closed weight is exactly 1 iff every leaf is closed.
* Orientation-variable splitting: the worker's lookahead only considers variables 1..nX
  (the X(i,j,k) orientation variables); auxiliary cap/cup/hull/counter variables are never split.
* Every cube job runs a fresh CaDiCaL on (case CNF + cube units) with ASCII LRAT tracing; a
  closed cube's proof is checked by lrat-check against (case CNF + cube units) when selected
  (all cubes at depth <= --check-depth, plus a --check-frac random sample), otherwise deleted.
* The cube tree is logged (tree.jsonl): each split records its variable, each leaf its result,
  so the partition can be audited offline.

usage: cnc2.py CASE.cnf OUTDIR --workers W [--c0 C] [--grow G] [--cmax C] [--check-frac P]
               [--check-depth D] [--check-threads T] [--wall S] [--snapshot S]
"""
import argparse
import heapq
import json
import os
import random
import subprocess
import threading
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent


def frac_str(x):
    return f'{x.numerator}/{x.denominator}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cnf')
    ap.add_argument('out')
    ap.add_argument('--workers', type=int, default=4)
    ap.add_argument('--worker-exe', default=None)
    ap.add_argument('--lrat-check', default=None)
    ap.add_argument('--verify-sig', default=None)
    ap.add_argument('--c0', type=int, default=20000, help='conflict budget at depth 0')
    ap.add_argument('--grow', type=float, default=1.0, help='budget factor per depth level')
    ap.add_argument('--cmax', type=int, default=2000000)
    ap.add_argument('--check-frac', type=float, default=1.0)
    ap.add_argument('--check-depth', type=int, default=3)
    ap.add_argument('--check-threads', type=int, default=1)
    ap.add_argument('--wall', type=float, default=1e18, help='stop launching jobs after this many seconds')
    ap.add_argument('--snapshot', type=float, default=1800)
    ap.add_argument('--status', type=float, default=60)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--stop-on-sat', action='store_true', default=True)
    ap.add_argument('--resume', action='store_true', help='continue from OUTDIR/tree.jsonl')
    args = ap.parse_args()

    info = json.load(open(args.cnf + '.json'))
    N, K, nX = info['N'], info['K'], info['nX']
    out = Path(args.out)
    (out / 'proofs').mkdir(parents=True, exist_ok=True)
    wexe = args.worker_exe or str(HERE / 'cnc_worker')
    lc = args.lrat_check
    rng = random.Random(args.seed)

    # header of the CNF, for building (CNF + cube units) files for lrat-check
    with open(args.cnf) as f:
        hdr_lines = []
        body_offset = 0
        for line in f:
            body_offset += len(line.encode())
            if line.startswith('p cnf'):
                _, _, nv, nc = line.split()
                nv, nc = int(nv), int(nc)
                break

    lock = threading.Lock()
    cv = threading.Condition(lock)
    heap = []
    cubes = {}
    seq = [0]
    st = {'closed_weight': Fraction(0), 'closed': 0, 'split': 0, 'sat': None, 'jobs': 0,
          'solve_cpu': 0.0, 'look_cpu': 0.0, 'inflight': 0, 'started': time.time(),
          'checked': 0, 'check_ok': 0, 'check_fail': 0, 'check_cpu': 0.0, 'proof_bytes_closed': 0,
          'unchecked_deleted': 0, 'failed_lit_splits': 0}
    per_depth = {}  # depth -> Counter(created, closed, split)
    tree = open(out / 'tree.jsonl', 'a')
    log = open(out / 'cnc2.log', 'a')
    stop = threading.Event()
    check_q = []
    check_cv = threading.Condition()

    def depth_stat(d):
        return per_depth.setdefault(d, Counter())

    def push(lits, depth, parent):
        i = seq[0]
        seq[0] += 1
        cubes[i] = {'lits': lits, 'depth': depth, 'parent': parent}
        heapq.heappush(heap, (depth, i))
        depth_stat(depth)['created'] += 1
        return i

    tree_path = out / 'tree.jsonl'
    if args.resume and tree_path.exists() and tree_path.stat().st_size > 0:
        # replay the tree log: rebuild open cubes, closed weight and per-depth counters
        lits_of = {}
        resolved = set()
        for line in open(tree_path):
            r = json.loads(line)
            if 'lits' in r and r.get('parent') is None and 'res' not in r:
                lits_of[r['id']] = r['lits']
                depth_stat(0)['created'] += 1
            elif r.get('res') == 'K':
                a, b = r['children']
                base = lits_of[r['id']]
                lits_of[a] = base + [r['var']]
                lits_of[b] = base + [-r['var']]
                d = len(base)
                depth_stat(d)['split'] += 1
                depth_stat(d + 1)['created'] += 2
                st['split'] += 1
                resolved.add(r['id'])
            elif r.get('res') == 'U':
                d = len(lits_of[r['id']])
                st['closed'] += 1
                st['closed_weight'] += Fraction(1, 2 ** d)
                depth_stat(d)['closed'] += 1
                resolved.add(r['id'])
            elif r.get('res') == 'S':
                raise SystemExit('tree log contains a SAT leaf; not resuming')
            if 'res' in r:
                st['jobs'] += 1
                st['solve_cpu'] += r.get('cpu', 0.0)
        for i, l in lits_of.items():
            if i not in resolved:
                cubes[i] = {'lits': l, 'depth': len(l), 'parent': None}
                heapq.heappush(heap, (len(l), i))
        seq[0] = max(lits_of) + 1
        tree.write(json.dumps({'resume': time.strftime('%Y-%m-%d %H:%M:%S'), 'open': len(cubes),
                               'closed_weight': frac_str(st['closed_weight'])}) + '\n')
    else:
        root = push([], 0, None)
        tree.write(json.dumps({'id': root, 'parent': None, 'depth': 0, 'lits': []}) + '\n')

    def budget(d):
        return int(min(args.cmax, args.c0 * (args.grow ** d)))

    def run_check(cid, lits, proof):
        cnfp = out / 'proofs' / f'c{cid}.cnf'
        with open(args.cnf, 'rb') as src, open(cnfp, 'wb') as dst:
            src.seek(body_offset)
            dst.write(f'p cnf {nv} {nc + len(lits)}\n'.encode())
            while True:
                b = src.read(1 << 20)
                if not b:
                    break
                dst.write(b)
            for l in lits:
                dst.write(f'{l} 0\n'.encode())
        t0 = time.time()
        r = subprocess.run([lc, str(cnfp), str(proof)], capture_output=True, text=True)
        dt = time.time() - t0
        ok = ('c VERIFIED' in r.stdout) and ('NOT VERIFIED' not in r.stdout)
        os.unlink(cnfp)
        os.unlink(proof)
        return ok, dt

    def checker():
        while True:
            with check_cv:
                while not check_q:
                    if stop.is_set() and st['inflight'] == 0:
                        return
                    check_cv.wait(1)
                cid, lits, proof = check_q.pop(0)
            ok, dt = run_check(cid, lits, proof)
            with lock:
                st['checked'] += 1
                st['check_ok'] += ok
                st['check_fail'] += (not ok)
                st['check_cpu'] += dt
                tree.write(json.dumps({'id': cid, 'lrat_check': 'VERIFIED' if ok else 'FAILED', 'secs': round(dt, 3)}) + '\n')
                tree.flush()

    def worker(w):
        p = subprocess.Popen([wexe, args.cnf, str(nX), str(out / 'proofs')], stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, text=True, bufsize=1)
        line = p.stdout.readline()
        assert line.startswith('READY'), line
        while True:
            with cv:
                while not heap and st['inflight'] > 0 and not stop.is_set():
                    cv.wait(1)
                if stop.is_set() or not heap or time.time() - st['started'] > args.wall:
                    if not heap and st['inflight'] == 0:
                        stop.set()
                    if time.time() - st['started'] > args.wall:
                        stop.set()
                    cv.notify_all()
                    break
                d, cid = heapq.heappop(heap)
                c = cubes[cid]
                st['inflight'] += 1
            lits = c['lits']
            b = budget(d)
            p.stdin.write(f'J {cid} {b} 1 {" ".join(map(str, lits))} 0\n')
            p.stdin.flush()
            r = p.stdout.readline().split()
            with cv:
                st['inflight'] -= 1
                st['jobs'] += 1
                kind = r[0]
                conf, cpu = int(r[2]), float(r[3])
                rec = {'id': cid, 'res': kind, 'conf': conf, 'cpu': cpu, 'budget': b}
                proof = out / 'proofs' / f'p{cid}.lrat'
                if kind == 'U':
                    st['solve_cpu'] += cpu
                    st['closed'] += 1
                    st['closed_weight'] += Fraction(1, 2 ** d)
                    depth_stat(d)['closed'] += 1
                    size = proof.stat().st_size if proof.exists() else -1
                    st['proof_bytes_closed'] += max(size, 0)
                    rec['proof_bytes'] = size
                    if lc and (d <= args.check_depth or rng.random() < args.check_frac):
                        with check_cv:
                            check_q.append((cid, lits, proof))
                            check_cv.notify()
                        rec['check'] = 'queued'
                    else:
                        if proof.exists():
                            os.unlink(proof)
                        st['unchecked_deleted'] += 1
                    del cubes[cid]
                elif kind == 'S':
                    st['solve_cpu'] += cpu
                    st['sat'] = {'cube': cid, 'model': str(out / 'proofs' / f'model-{cid}.txt')}
                    depth_stat(d)['sat'] += 1
                    if args.verify_sig:
                        vr = subprocess.run([args.verify_sig, str(N), str(K), st['sat']['model']], capture_output=True, text=True).stdout
                        st['sat']['verify'] = json.loads(vr)
                        rec['verify'] = st['sat']['verify']
                    if args.stop_on_sat:
                        stop.set()
                elif kind == 'K':
                    var, score, lcpu = int(r[4]), float(r[5]), float(r[6])
                    st['solve_cpu'] += cpu - lcpu
                    st['look_cpu'] += lcpu
                    st['split'] += 1
                    if score >= 1e17:
                        st['failed_lit_splits'] += 1
                    depth_stat(d)['split'] += 1
                    a = push(lits + [var], d + 1, cid)
                    bb = push(lits + [-var], d + 1, cid)
                    rec.update({'var': var, 'score': score, 'children': [a, bb]})
                    del cubes[cid]
                else:  # 'F': propagation refutes the cube but the solver did not close it; retry with larger budget
                    raise RuntimeError(f'unexpected worker reply {r}')
                tree.write(json.dumps(rec) + '\n')
                tree.flush()
                cv.notify_all()
        p.stdin.close()
        p.wait()

    def snapshot(kind):
        with lock:
            openc = [cubes[i]['depth'] for i in cubes]
            hist = Counter(openc)
            cw = st['closed_weight']
            open_w = sum((Fraction(1, 2 ** d) for d in openc), Fraction(0))
            s = {'kind': kind, 't': round(time.time() - st['started'], 1), 'closed': st['closed'], 'split': st['split'],
                 'open': len(openc), 'inflight': st['inflight'], 'jobs': st['jobs'],
                 'closed_weight': frac_str(cw), 'closed_weight_float': float(cw),
                 'open_weight': frac_str(open_w), 'weight_sum_is_1': cw + open_w == 1,
                 'open_depth_hist': {str(k): hist[k] for k in sorted(hist)},
                 'min_open_depth': min(openc) if openc else None, 'max_open_depth': max(openc) if openc else None,
                 'per_depth': {str(k): dict(per_depth[k]) for k in sorted(per_depth)},
                 'solve_cpu': round(st['solve_cpu'], 1), 'look_cpu': round(st['look_cpu'], 1),
                 'checked': st['checked'], 'check_ok': st['check_ok'], 'check_fail': st['check_fail'],
                 'check_secs': round(st['check_cpu'], 1), 'proof_bytes_closed': st['proof_bytes_closed'],
                 'unchecked_deleted': st['unchecked_deleted'], 'failed_lit_splits': st['failed_lit_splits'],
                 'sat': st['sat']}
        log.write(json.dumps(s) + '\n')
        log.flush()
        return s

    log.write(json.dumps({'start': time.strftime('%Y-%m-%d %H:%M:%S'), 'cnf': args.cnf, 'N': N, 'K': K, 'nX': nX,
                          'case': info.get('case'), 'args': vars(args)}) + '\n')
    log.flush()
    checkers = [threading.Thread(target=checker, daemon=True) for _ in range(args.check_threads if lc else 0)]
    for t in checkers:
        t.start()
    threads = [threading.Thread(target=worker, args=(w,), daemon=True) for w in range(args.workers)]
    for t in threads:
        t.start()
    last_status = last_snap = time.time()
    while any(t.is_alive() for t in threads):
        time.sleep(1)
        now = time.time()
        if now - last_snap >= args.snapshot:
            snapshot('frontier')
            last_snap = now
            last_status = now
        elif now - last_status >= args.status:
            snapshot('status')
            last_status = now
    stop.set()
    for t in checkers:
        t.join()
    final = snapshot('final')
    final['result'] = ('SAT' if st['sat'] else ('UNSAT' if final['open'] == 0 and final['closed_weight'] == '1/1' else 'OPEN'))
    log.write(json.dumps({'result': final['result']}) + '\n')
    log.flush()
    with open(out / 'final.json', 'w') as f:
        json.dump(final, f, indent=1)
    print(json.dumps({k: final[k] for k in ('result', 'closed', 'split', 'open', 'closed_weight', 'closed_weight_float',
                                             'max_open_depth', 'jobs', 'solve_cpu', 'look_cpu', 'checked', 'check_ok', 'check_fail')}))


if __name__ == '__main__':
    main()
