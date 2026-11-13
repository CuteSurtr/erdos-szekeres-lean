#!/usr/bin/env python3
"""Exact LP branch-and-bound for "at most BUDGET holes" over a row file (adapted from the repo's
experiments/omission-final313-2026-10-11/search/pbb_strong.py; N = 84 or 126, rows from JSON).
Leaves are weighted-capacity certificates whose integer margin is recomputed exactly (scripts/omission_tree.py
format); the LP only suggests weights.  Root: branch on the two fixed states (first two points); their 'one'
children are 'pending' and are discharged by the fixed-state lemma (README §2).
usage: pbb5.py <rows.json [[support,demand],...]> <budget> <procs> <contexts> <outdir>"""
import gzip, json, math, multiprocessing as mp, os, sys, time
for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[k] = '1'
from pathlib import Path
import numpy as np
import etv_common as ec
N = ec.N

def margin(rows, masks, demands, budget, missing, occupied, node):
    lower = 0; loads = [0] * N; cap = node['capacity']
    free = ((1 << N) - 1) ^ missing ^ occupied
    for r, w in node['weights']:
        lower += w * max(0, demands[r] - (masks[r] & missing).bit_count())
        for i in rows[r][0]: loads[i] += w
    excess = sum(max(0, loads[i] - cap) for i in range(N) if free >> i & 1)
    return lower - cap * (budget - missing.bit_count()) - excess

class Solver:
    def __init__(self, rows, budget):
        import highspy
        self.hs = highspy; self.rows, self.budget = rows, budget
        self.masks = [sum(1 << i for i in s) for s, _ in rows]; self.demands = [d for _, d in rows]
        h = highspy.Highs(); h.setOptionValue('output_flag', False); h.setOptionValue('threads', 1)
        h.setOptionValue('presolve', 'off')
        v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
        for s, d in rows: h.addConstr(h.qsum(v[i] for i in s) >= d)
        self.h = h; self.idx = np.arange(N, dtype=np.int32)
    def expand(self, missing, occupied):
        hs, h, budget = self.hs, self.h, self.budget
        if missing.bit_count() > budget: return 'leaf', {'type': 'over_budget'}
        free = ((1 << N) - 1) ^ missing ^ occupied
        force = None
        for r, mask in enumerate(self.masks):
            rem = self.demands[r] - (mask & missing).bit_count(); avail = mask & free
            if rem > avail.bit_count():
                leaf = {'type': 'weighted', 'capacity': 0, 'weights': [[r, 1]]}
                assert margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0
                return 'leaf', leaf
            if rem > 0 and rem == avail.bit_count() and force is None:
                force = (avail & -avail).bit_length() - 1
        if force is not None: return 'branch', force
        lo = np.fromiter((float(missing >> i & 1) for i in range(N)), float, N)
        hi = np.fromiter((float(not (occupied >> i & 1)) for i in range(N)), float, N)
        h.changeColsBounds(N, self.idx, lo, hi); h.run(); st = h.getModelStatus()
        if st != hs.HighsModelStatus.kOptimal and st != hs.HighsModelStatus.kInfeasible:
            h.clearSolver(); h.run(); st = h.getModelStatus()
        if st == hs.HighsModelStatus.kOptimal:
            sol = h.getSolution(); obj = h.getObjectiveValue()
            if obj > budget + 1e-8:
                for scale in (6, 10, 12, 30, 32, 60, 100, 256, 1000, 10000, 100000):
                    ws = [[r, max(0, round(scale * x))] for r, x in enumerate(sol.row_dual) if x > 0.5 / scale]
                    leaf = {'type': 'weighted', 'capacity': scale, 'weights': [[r, w] for r, w in ws if w]}
                    if margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0: return 'leaf', leaf
            x = sol.col_value
            fr = [i for i in range(N) if free >> i & 1 and 1e-7 < x[i] < 1 - 1e-7]
            if not fr:
                holes = [i for i in range(N) if x[i] > 0.5]
                if len(holes) <= budget and all(len(set(holes) & set(s)) >= d for s, d in self.rows) and not (set(holes) & set(ec.FIXED_OCC)):
                    return 'witness', holes
                return 'branch', min(i for i in range(N) if free >> i & 1)
            K = STRONG['k'] if (missing | occupied).bit_count() < STRONG['depth'] else STRONG['k_low']
            if K:
                cand = sorted(fr, key=lambda i: (abs(x[i] - 0.5), i))[:K]; best = None
                for c in cand:
                    gains = []
                    for b in (0, 1):
                        l2, h2 = lo.copy(), hi.copy(); l2[c] = b; h2[c] = b
                        h.changeColsBounds(N, self.idx, l2, h2); h.run(); st2 = h.getModelStatus()
                        o2 = h.getObjectiveValue() if st2 == hs.HighsModelStatus.kOptimal else budget + 1
                        gains.append(max(min(o2, budget + 1) - obj, 1e-3))
                    key = gains[0] * gains[1]
                    if best is None or key > best[0]: best = (key, c)
                h.changeColsBounds(N, self.idx, lo, hi)
                return 'branch', best[1]
            return 'branch', min(fr, key=lambda i: (abs(x[i] - 0.5), i))
        if st == hs.HighsModelStatus.kInfeasible:
            _, exists, ray = h.getDualRay()
            if exists:
                for scale in (1000, 1000000, 1000000000):
                    leaf = {'type': 'weighted', 'capacity': 0, 'weights': [[r, max(0, round(scale * y))] for r, y in enumerate(ray) if y > 0.5 / scale]}
                    if margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0: return 'leaf', leaf
        free_list = [i for i in range(N) if free >> i & 1]
        return 'branch', max(free_list, key=lambda i: sum(1 for m in self.masks if m >> i & 1))

G = {}; STRONG = {}
def init(rowsfile, budget):
    STRONG.update(k=int(os.environ.get('K_TOP', '16')), depth=int(os.environ.get('D_TOP', '8')), k_low=int(os.environ.get('K_LOW', '4')))
    G['s'] = Solver([(s, d) for s, d in json.load(open(rowsfile))], budget)

def run_context(job):
    cid, missing, occupied, outdir = job
    s = G['s']; t0 = time.time(); nodes = [{'type': 'pending'}]; stack = [(0, missing, occupied)]; count = 0
    while stack:
        i, m, o = stack.pop(); kind, val = s.expand(m, o); count += 1
        if kind == 'leaf': nodes[i] = val
        elif kind == 'witness': return cid, 'witness', val, count, time.time() - t0
        else:
            z, one = len(nodes), len(nodes) + 1
            nodes += [{'type': 'pending'}, {'type': 'pending'}]
            nodes[i] = {'type': 'branch', 'vertex': val, 'zero': z, 'one': one}
            stack.append((z, m, o | (1 << val))); stack.append((one, m | (1 << val), o))
    rec = {'context': cid, 'missing': [j for j in range(N) if missing >> j & 1], 'occupied': [j for j in range(N) if occupied >> j & 1], 'root': 0, 'nodes': nodes}
    with gzip.open(Path(outdir) / f'ctx-{cid}.json.gz', 'wt', compresslevel=6) as f: json.dump(rec, f, separators=(',', ':'))
    return cid, 'closed', len(nodes), count, time.time() - t0

def main():
    rowsfile, budget, procs, depth, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    Path(outdir).mkdir(parents=True, exist_ok=True)
    init(rowsfile, budget); s = G['s']
    f0, f1 = ec.FIXED_OCC
    # root: branch on f0 (one-child pending), then f1 (one-child pending)
    nodes = [{'type': 'branch', 'vertex': f0, 'zero': 1, 'one': 2}, {'type': 'branch', 'vertex': f1, 'zero': 3, 'one': 4},
             {'type': 'pending', 'note': 'fixed state 0 missing'}, {'type': 'pending'}, {'type': 'pending', 'note': 'fixed state 1 missing'}]
    frontier = [(3, 0, (1 << f0) | (1 << f1))]; master_leaves = 0
    while frontier and len(frontier) < depth:
        nxt = []
        for i, m, o in frontier:
            kind, val = s.expand(m, o)
            if kind == 'leaf': nodes[i] = val; master_leaves += 1
            elif kind == 'witness':
                print(json.dumps({'event': 'WITNESS', 'holes': val}), flush=True); Path(outdir, 'WITNESS.json').write_text(json.dumps({'holes': val})); return
            else:
                z, one = len(nodes), len(nodes) + 1
                nodes += [{'type': 'pending'}, {'type': 'pending'}]
                nodes[i] = {'type': 'branch', 'vertex': val, 'zero': z, 'one': one}
                nxt += [(z, m, o | (1 << val)), (one, m | (1 << val), o)]
        frontier = nxt
    jobs = []
    for cid, (i, m, o) in enumerate(frontier):
        nodes[i] = {'type': 'context', 'context': cid}
        if not (Path(outdir) / f'ctx-{cid}.json.gz').exists(): jobs.append((cid, m, o, outdir))
    (Path(outdir) / 'master.json').write_text(json.dumps({'rows': rowsfile, 'budget': budget, 'root': 0, 'nodes': nodes, 'contexts': len(frontier), 'master_leaves': master_leaves}))
    print(json.dumps({'event': 'start', 'contexts': len(frontier), 'todo': len(jobs), 'master_leaves': master_leaves}), flush=True)
    t0 = time.time(); done = total = 0
    with mp.Pool(procs, initializer=init, initargs=(rowsfile, budget)) as pool:
        for cid, status, size, count, secs in pool.imap_unordered(run_context, jobs):
            if status == 'witness':
                print(json.dumps({'event': 'WITNESS', 'context': cid, 'holes': size}), flush=True)
                Path(outdir, 'WITNESS.json').write_text(json.dumps({'holes': size, 'context': cid})); pool.terminate(); return
            done += 1; total += count
            print(json.dumps({'event': 'closed', 'context': cid, 'nodes': count, 'seconds': round(secs, 1), 'done': done, 'todo': len(jobs), 'total_nodes': total, 'elapsed': round(time.time() - t0)}), flush=True)
    print(json.dumps({'event': 'DONE', 'contexts': len(frontier), 'total_nodes': total}), flush=True)

if __name__ == '__main__':
    main()
