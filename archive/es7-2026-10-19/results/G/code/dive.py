#!/usr/bin/env python3
"""Knuth-style random dives for tree-size estimation (same worker, budget and split rule as cnc2).

Each dive starts at the root cube; at every node it runs the cube job with the conflict budget.
If the cube closes (U) the dive ends at a leaf of depth d; if the budget is hit, the worker's
lookahead variable splits the node and the dive continues into a uniformly random child.
For the tree T(B) defined by "split until the cube closes within B conflicts" (same split rule),
Knuth's estimator 2^d is unbiased for the number of leaves, and sum_i 2^i * cpu_i is unbiased
for the total CPU of the tree. Dives stopped by --max-depth or --wall are censored: they only
give the lower bounds 2^d_reached (leaves) and sum_i 2^i * cpu_i (CPU).
Closed leaves are LRAT-checked when --lrat-check is given.

usage: dive.py CASE.cnf OUTDIR --dives D --seed S [--c0 C] [--max-depth M] [--wall SECONDS]
"""
import argparse
import json
import os
import random
import subprocess
import time
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cnf')
    ap.add_argument('out')
    ap.add_argument('--worker-exe', required=True)
    ap.add_argument('--lrat-check', default=None)
    ap.add_argument('--dives', type=int, default=1)
    ap.add_argument('--seed', type=int, default=1)
    ap.add_argument('--c0', type=int, default=20000)
    ap.add_argument('--grow', type=float, default=1.0)
    ap.add_argument('--cmax', type=int, default=2000000)
    ap.add_argument('--max-depth', type=int, default=200)
    ap.add_argument('--wall', type=float, default=1e18)
    ap.add_argument('--solve-every', type=int, default=1,
                    help='run the solver only at depths that are multiples of this; split by lookahead alone elsewhere')
    args = ap.parse_args()
    info = json.load(open(args.cnf + '.json'))
    nX = info['nX']
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    t_start = time.time()
    p = subprocess.Popen([args.worker_exe, args.cnf, str(nX), str(out)], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, text=True, bufsize=1)
    assert p.stdout.readline().startswith('READY')
    logf = open(out / 'dives.jsonl', 'a')
    jid = 0
    for k in range(args.dives):
        lits = []
        path = []
        status = 'censored'
        while True:
            if time.time() - t_start > args.wall:
                status = 'censored_wall'
                break
            if len(lits) > args.max_depth:
                status = 'censored_depth'
                break
            jid += 1
            if len(lits) % args.solve_every != 0:
                p.stdin.write(f'L {jid} {" ".join(map(str, lits))} 0\n')
                p.stdin.flush()
                r = p.stdout.readline().split()
                var = int(r[2])
                if var != 0:
                    node = {'depth': len(lits), 'res': 'L', 'conf': 0, 'cpu': float(r[4]), 'var': var}
                    with open(out / 'nodes.jsonl', 'a') as nf:
                        nf.write(json.dumps({'dive': k, 'seed': args.seed, **node, 't': round(time.time() - t_start, 1)}) + '\n')
                    path.append(node)
                    lits = lits + [var if rng.random() < 0.5 else -var]
                    continue
                jid += 1  # propagation refutes the cube: close it with a solver job (gives LRAT)
            check = 1 if args.lrat_check else 0
            b = int(min(args.cmax, args.c0 * (args.grow ** len(lits))))
            p.stdin.write(f'J {jid} {b} {check} {" ".join(map(str, lits))} 0\n')
            p.stdin.flush()
            r = p.stdout.readline().split()
            node = {'depth': len(lits), 'res': r[0], 'conf': int(r[2]), 'cpu': float(r[3])}
            with open(out / 'nodes.jsonl', 'a') as nf:
                nf.write(json.dumps({'dive': k, 'seed': args.seed, **node, 'var': int(r[4]) if r[0] == 'K' else None,
                                     't': round(time.time() - t_start, 1)}) + '\n')
            if r[0] == 'U':
                status = 'closed'
                if args.lrat_check:
                    proof = out / f'p{jid}.lrat'
                    cnfp = out / f'c{jid}.cnf'
                    with open(args.cnf) as src, open(cnfp, 'w') as dst:
                        for line in src:
                            if line.startswith('p cnf'):
                                _, _, nv, nc = line.split()
                                dst.write(f'p cnf {nv} {int(nc) + len(lits)}\n')
                            elif not line.startswith('c'):
                                dst.write(line)
                        for l in lits:
                            dst.write(f'{l} 0\n')
                    rr = subprocess.run([args.lrat_check, str(cnfp), str(proof)], capture_output=True, text=True)
                    node['lrat'] = 'VERIFIED' if ('c VERIFIED' in rr.stdout and 'NOT VERIFIED' not in rr.stdout) else 'FAILED'
                    node['proof_bytes'] = proof.stat().st_size
                    os.unlink(cnfp)
                    os.unlink(proof)
                path.append(node)
                break
            if r[0] == 'S':
                status = 'sat'
                node['model'] = str(out / f'model-{jid}.txt')
                path.append(node)
                break
            var = int(r[4])
            node['var'] = var
            node['look_cpu'] = float(r[6])
            path.append(node)
            lits = lits + [var if rng.random() < 0.5 else -var]
        d = len(lits)
        est_leaves_log2 = d
        est_cpu = sum((2 ** n['depth']) * n['cpu'] for n in path)
        rec = {'dive': k, 'seed': args.seed, 'status': status, 'depth': d, 'log2_leaves_est': est_leaves_log2,
               'cpu_est': est_cpu, 'path_cpu': sum(n['cpu'] for n in path), 'lits': lits, 'path': path,
               'c0': args.c0, 'grow': args.grow, 'solve_every': args.solve_every, 'case': info.get('case'), 'elapsed': round(time.time() - t_start, 1)}
        logf.write(json.dumps(rec) + '\n')
        logf.flush()
        print(json.dumps({x: rec[x] for x in ('dive', 'status', 'depth', 'cpu_est', 'path_cpu', 'elapsed')}), flush=True)
        if status.startswith('censored_wall') or status == 'sat':
            break
    p.stdin.close()
    p.wait()


if __name__ == '__main__':
    main()
