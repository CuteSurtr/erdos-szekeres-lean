#!/usr/bin/env python3
"""Parallel exact LP branch-and-bound for the <= BUDGET-hole residual question.

Leaves use the omission-tree certificate format of
experiments/omission-residual32-resume-2026-10-10/search.py: a numerical LP only
suggests integer row weights; a leaf is kept only if its exact integer margin is
positive. Every context subtree is written separately and can be assembled into a
single tree for scripts/omission_tree.check_tree.
"""
import gzip, json, math, multiprocessing as mp, os, sys, time
for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[k] = '1'
from pathlib import Path
import numpy as np

SRC = os.environ.get('SRC', 'experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz')
_D0 = json.load(gzip.open(SRC) if SRC.endswith('.gz') else open(SRC))
N = len(_D0['states'])
ROOT_OCC = [int(x) for x in os.environ.get('ROOT_OCC', '0').split(',') if x != '']


def load(extra):
    d = json.load(gzip.open(SRC) if SRC.endswith('.gz') else open(SRC))
    rows = [(r['support'], r['rhs']) for r in d['constraints']]
    if extra:
        rows += [(r['support'], r['rhs']) for r in json.load(open(extra))]
    return rows


def margin(rows, masks, demands, budget, missing, occupied, node):
    lower = 0
    loads = [0] * N
    cap = node['capacity']
    free = ((1 << N) - 1) ^ missing ^ occupied
    for r, w in node['weights']:
        lower += w * max(0, demands[r] - (masks[r] & missing).bit_count())
        for i in rows[r][0]:
            loads[i] += w
    excess = sum(max(0, loads[i] - cap) for i in range(N) if free >> i & 1)
    return lower - cap * (budget - missing.bit_count()) - excess


class Solver:
    def __init__(self, rows, budget):
        import highspy
        self.hs = highspy
        self.rows, self.budget = rows, budget
        self.masks = [sum(1 << i for i in s) for s, _ in rows]
        self.demands = [d for _, d in rows]
        h = highspy.Highs()
        h.setOptionValue('output_flag', False)
        h.setOptionValue('threads', 1)
        h.setOptionValue('presolve', 'off')
        v = [h.addVariable(lb=0, ub=1, obj=1) for _ in range(N)]
        for s, d in rows:
            h.addConstr(h.qsum(v[i] for i in s) >= d)
        self.h = h
        self.idx = np.arange(N, dtype=np.int32)

    def expand(self, missing, occupied):
        """Return ('leaf', node) or ('branch', var) or ('witness', holes)."""
        hs, h, budget = self.hs, self.h, self.budget
        if missing.bit_count() > budget:
            return 'leaf', {'type': 'over_budget'}
        free = ((1 << N) - 1) ^ missing ^ occupied
        force = None
        for r, mask in enumerate(self.masks):
            rem = self.demands[r] - (mask & missing).bit_count()
            avail = mask & free
            if rem > avail.bit_count():
                leaf = {'type': 'weighted', 'capacity': 0, 'weights': [[r, 1]]}
                assert margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0
                return 'leaf', leaf
            if rem and rem == avail.bit_count() and force is None:
                force = (avail & -avail).bit_length() - 1
        if force is not None:
            return 'branch', force
        lo = np.fromiter((float(missing >> i & 1) for i in range(N)), float, N)
        hi = np.fromiter((float(not (occupied >> i & 1)) for i in range(N)), float, N)
        h.changeColsBounds(N, self.idx, lo, hi)
        h.run()
        st = h.getModelStatus()
        if st != hs.HighsModelStatus.kOptimal and st != hs.HighsModelStatus.kInfeasible:
            h.clearSolver()
            h.run()
            st = h.getModelStatus()
        if st == hs.HighsModelStatus.kOptimal:
            sol = h.getSolution()
            obj = h.getObjectiveValue()
            if obj > budget + 1e-8:
                for scale in (10, 32, 100, 256, 1000, 10000, 100000):
                    ws = [[r, max(0, round(scale * x))] for r, x in enumerate(sol.row_dual) if x > 0.5 / scale]
                    leaf = {'type': 'weighted', 'capacity': scale, 'weights': [[r, w] for r, w in ws if w]}
                    if margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0:
                        return 'leaf', leaf
            x = sol.col_value
            fr = [i for i in range(N) if free >> i & 1 and 1e-7 < x[i] < 1 - 1e-7]
            if not fr:
                holes = [i for i in range(N) if x[i] > 0.5]
                if len(holes) <= budget and all(
                        len(set(holes) & set(s)) >= d for s, d in self.rows) and 0 not in holes:
                    return 'witness', holes
                return 'branch', min(i for i in range(N) if free >> i & 1)
            K = STRONG.get('k', 0) if (missing | occupied).bit_count() < STRONG.get('depth', 99) else STRONG.get('k_low', 0)
            if K:
                cand = sorted(fr, key=lambda i: (abs(x[i] - 0.5), i))[:K]
                best = None
                for c in cand:
                    gains = []
                    for b in (0, 1):
                        l2, h2 = lo.copy(), hi.copy()
                        l2[c] = b; h2[c] = b
                        h.changeColsBounds(N, self.idx, l2, h2); h.run()
                        st2 = h.getModelStatus()
                        o2 = h.getObjectiveValue() if st2 == hs.HighsModelStatus.kOptimal else budget + 1
                        gains.append(max(min(o2, budget + 1) - obj, 1e-3))
                    key = gains[0] * gains[1]
                    if best is None or key > best[0]:
                        best = (key, c)
                h.changeColsBounds(N, self.idx, lo, hi)
                return 'branch', best[1]
            return 'branch', min(fr, key=lambda i: (abs(x[i] - 0.5), i))
        if st == hs.HighsModelStatus.kInfeasible:
            _, exists, ray = h.getDualRay()
            if exists:
                for scale in (1000, 1000000, 1000000000):
                    leaf = {'type': 'weighted', 'capacity': 0,
                            'weights': [[r, max(0, round(scale * y))] for r, y in enumerate(ray) if y > 0.5 / scale]}
                    if margin(self.rows, self.masks, self.demands, budget, missing, occupied, leaf) > 0:
                        return 'leaf', leaf
        free_list = [i for i in range(N) if free >> i & 1]
        return 'branch', max(free_list, key=lambda i: sum(1 for m in self.masks if m >> i & 1))


G = {}
STRONG = {}


def init(extra, budget):
    STRONG.update(k=int(os.environ.get('K_TOP', '40')), depth=int(os.environ.get('D_TOP', '12')), k_low=int(os.environ.get('K_LOW', '12')))
    G['s'] = Solver(load(extra), budget)


def run_context(job):
    cid, missing, occupied, outdir = job
    s = G['s']
    t0 = time.time()
    nodes = [{'type': 'pending'}]
    stack = [(0, missing, occupied)]
    count = 0
    while stack:
        i, m, o = stack.pop()
        kind, val = s.expand(m, o)
        count += 1
        if kind == 'leaf':
            nodes[i] = val
        elif kind == 'witness':
            return cid, 'witness', val, count, time.time() - t0
        else:
            z, one = len(nodes), len(nodes) + 1
            nodes += [{'type': 'pending'}, {'type': 'pending'}]
            nodes[i] = {'type': 'branch', 'vertex': val, 'zero': z, 'one': one}
            stack.append((z, m, o | (1 << val)))
            stack.append((one, m | (1 << val), o))
    rec = {'context': cid, 'missing': [j for j in range(N) if missing >> j & 1],
           'occupied': [j for j in range(N) if occupied >> j & 1], 'root': 0, 'nodes': nodes}
    with gzip.open(Path(outdir) / f'ctx-{cid}.json.gz', 'wt', compresslevel=6) as f:
        json.dump(rec, f, separators=(',', ':'))
    return cid, 'closed', len(nodes), count, time.time() - t0


def main():
    budget, procs, depth, outdir = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
    extra = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] else None
    Path(outdir).mkdir(parents=True, exist_ok=True)
    init(extra, budget)
    s = G['s']
    # Master: expand the tree breadth-first to the requested number of open contexts,
    # or reload a saved master tree so that a restart does not repeat this phase.
    nodes = [{'type': 'pending'}]
    frontier = [(0, 0, sum(1 << i for i in ROOT_OCC))]  # (index, missing, occupied) at the root
    master_leaves = 0
    saved = Path(outdir) / 'master.json'
    if saved.exists():
        m = json.loads(saved.read_text())
        if m.get('budget') == budget and m.get('source') == SRC and m.get('root_occupied', [0]) == ROOT_OCC:
            nodes = m['nodes']; master_leaves = m.get('master_leaves', 0); ctx = {}
            stack = [(0, 0, sum(1 << i for i in ROOT_OCC))]
            while stack:
                i, mm, oo = stack.pop(); nd = nodes[i]
                if nd['type'] == 'branch':
                    stack.append((nd['zero'], mm, oo | (1 << nd['vertex']))); stack.append((nd['one'], mm | (1 << nd['vertex']), oo))
                elif nd['type'] == 'context':
                    ctx[nd['context']] = (i, mm, oo)
            frontier = [ctx[c] for c in sorted(ctx)]
            print(json.dumps({'event': 'reloaded_master', 'contexts': len(frontier)}), flush=True)
            depth = 0  # skip expansion
    while frontier and len(frontier) < depth:
        nxt = []
        for i, m, o in frontier:
            kind, val = s.expand(m, o)
            if kind == 'leaf':
                nodes[i] = val
                master_leaves += 1
            elif kind == 'witness':
                print(json.dumps({'event': 'WITNESS', 'holes': val}), flush=True)
                return
            else:
                z, one = len(nodes), len(nodes) + 1
                nodes += [{'type': 'pending'}, {'type': 'pending'}]
                nodes[i] = {'type': 'branch', 'vertex': val, 'zero': z, 'one': one}
                nxt += [(z, m, o | (1 << val)), (one, m | (1 << val), o)]
        frontier = nxt
    jobs = []
    for cid, (i, m, o) in enumerate(frontier):
        if nodes[i].get('type') != 'context':
            nodes[i] = {'type': 'context', 'context': cid}
        if not (Path(outdir) / f'ctx-{cid}.json.gz').exists():
            jobs.append((cid, m, o, outdir))
    (Path(outdir) / 'master.json').write_text(json.dumps(
        {'source': SRC, 'root_occupied': ROOT_OCC, 'extra': extra, 'budget': budget, 'root': 0, 'nodes': nodes,
         'contexts': len(frontier), 'master_leaves': master_leaves}))
    print(json.dumps({'event': 'start', 'contexts': len(frontier), 'todo': len(jobs),
                      'master_leaves': master_leaves}), flush=True)
    t0 = time.time()
    done = total_nodes = 0
    with mp.Pool(procs, initializer=init, initargs=(extra, budget)) as pool:
        for cid, status, size, count, secs in pool.imap_unordered(run_context, jobs):
            if status == 'witness':
                print(json.dumps({'event': 'WITNESS', 'context': cid, 'holes': size}), flush=True)
                Path(outdir, 'WITNESS.json').write_text(json.dumps({'holes': size, 'context': cid}))
                pool.terminate()
                return
            done += 1
            total_nodes += count
            print(json.dumps({'event': 'closed', 'context': cid, 'nodes': count, 'seconds': round(secs, 1),
                              'done': done, 'todo': len(jobs), 'total_nodes': total_nodes,
                              'elapsed': round(time.time() - t0)}), flush=True)
    print(json.dumps({'event': 'DONE', 'contexts': len(frontier), 'total_nodes': total_nodes}), flush=True)


if __name__ == '__main__':
    main()
