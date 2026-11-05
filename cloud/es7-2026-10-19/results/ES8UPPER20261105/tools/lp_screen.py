#!/usr/bin/env python3
"""Budget-64 LP screen of the 4,096 depth-12 balanced contexts.

For each context (missing states fixed to 1 = hole, occupied states fixed to 0) solve the LP
relaxation  min sum x  s.t.  every catalog row,  0 <= x <= 1,  with the HiGHS model built exactly
as pbb_strong.Solver builds it (1 thread, presolve off). Reports
  lp       : LP value at the context (budget-independent; > 64 means the context closes at once at 64)
  lp_prop  : LP value after fixing the states forced by the rows (a row with remaining demand equal
             to its free states forces all of them to be holes), iterated to a fixpoint
  forced   : number of states so forced; prop_closed: the propagation alone violates a row
  slack64  : 64 - lp (larger = more room for a 64-hole vector)
LP values are floating point (HiGHS); they only rank contexts.

usage: lp_screen.py OUT.jsonl [--workers N] [--limit K] [--budget 64] [--contexts contexts.jsonl]
Writes OUT.jsonl (sorted by ctx) and OUT.summary.json (distribution and the lowest-LP contexts).
"""
import argparse, json, multiprocessing as mp, os, sys, time
from pathlib import Path

for k in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[k] = '1'
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
G = {}


def init(budget):
    from run_context import load_pbb
    pbb = load_pbb()
    rows = pbb.load(None)
    G['pbb'] = pbb
    G['s'] = pbb.Solver(rows, budget)
    G['budget'] = budget


def lp(missing, occupied):
    s, pbb = G['s'], G['pbb']
    import numpy as np
    N = pbb.N
    lo = np.fromiter((float(missing >> i & 1) for i in range(N)), float, N)
    hi = np.fromiter((float(not (occupied >> i & 1)) for i in range(N)), float, N)
    s.h.changeColsBounds(N, s.idx, lo, hi)
    s.h.run()
    st = s.h.getModelStatus()
    if st != s.hs.HighsModelStatus.kOptimal and st != s.hs.HighsModelStatus.kInfeasible:
        s.h.clearSolver(); s.h.run(); st = s.h.getModelStatus()
    if st == s.hs.HighsModelStatus.kOptimal:
        return s.h.getObjectiveValue(), 'optimal'
    return None, str(st)


def propagate(missing, occupied):
    s, N = G['s'], G['pbb'].N
    full = (1 << N) - 1
    while True:
        free = full ^ missing ^ occupied
        add = 0
        for r, mask in enumerate(s.masks):
            rem = s.demands[r] - (mask & missing).bit_count()
            avail = mask & free
            if rem > avail.bit_count():
                return missing, True
            if rem > 0 and rem == avail.bit_count():
                add |= avail
        if not add:
            return missing, False
        missing |= add


def job(c):
    t0 = time.time()
    m = sum(1 << j for j in c['missing']); o = sum(1 << j for j in c['occupied'])
    v, st = lp(m, o)
    m2, closed = propagate(m, o)
    v2, st2 = (None, 'prop_closed') if closed else lp(m2, o)
    b = G['budget']
    return {'ctx': c['ctx'], 'lp': None if v is None else round(v, 6), 'status': st,
            'lp_prop': None if v2 is None else round(v2, 6), 'forced': m2.bit_count() - m.bit_count(),
            'prop_closed': closed, 'slack64': None if v is None else round(b - v, 6),
            'closes_at_root': v is None or v > b + 1e-8, 'n_missing': len(c['missing']),
            'b63_leaves': c['leaves'], 'b63_nodes': c['nodes'], 'seconds': round(time.time() - t0, 4)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('out')
    ap.add_argument('--workers', type=int, default=1)
    ap.add_argument('--limit', type=int, default=0, help='only the first K contexts (test)')
    ap.add_argument('--budget', type=int, default=64)
    ap.add_argument('--contexts', default=str(HERE / 'contexts.jsonl'))
    a = ap.parse_args()
    C = [json.loads(l) for l in open(a.contexts)]
    if a.limit:
        C = C[:a.limit]
    t0 = time.time()
    res = []
    if a.workers <= 1:
        init(a.budget)
        res = [job(c) for c in C]
    else:
        with mp.Pool(a.workers, initializer=init, initargs=(a.budget,)) as pool:
            for r in pool.imap_unordered(job, C, chunksize=8):
                res.append(r)
    res.sort(key=lambda r: r['ctx'])
    with open(a.out, 'w') as f:
        for r in res:
            f.write(json.dumps(r) + '\n')
    ok = [r for r in res if r['lp'] is not None]
    ok.sort(key=lambda r: (r['lp'], r['lp_prop'] if r['lp_prop'] is not None else 1e9, r['ctx']))
    vals = sorted(r['lp'] for r in ok)
    import highspy, importlib.metadata as md
    summ = {'contexts': len(res), 'budget': a.budget, 'workers': a.workers, 'wall_s': round(time.time() - t0, 1),
            'lp_seconds_mean': round(sum(r['seconds'] for r in res) / max(len(res), 1), 4),
            'non_optimal': len(res) - len(ok), 'closes_at_root': sum(r['closes_at_root'] for r in res),
            'prop_closed': sum(r['prop_closed'] for r in res),
            'lp_min': vals[0] if vals else None, 'lp_median': vals[len(vals) // 2] if vals else None,
            'lp_max': vals[-1] if vals else None,
            'lowest_lp': [{k: r[k] for k in ('ctx', 'lp', 'lp_prop', 'forced', 'b63_leaves')} for r in ok[:20]],
            'highspy': md.version('highspy'), 'finished': time.strftime('%F %T')}
    Path(a.out + '.summary.json').write_text(json.dumps(summ, indent=1))
    print(json.dumps({k: v for k, v in summ.items() if k != 'lowest_lp'} | {'lowest4': summ['lowest_lp'][:4]}))


if __name__ == '__main__':
    main()
