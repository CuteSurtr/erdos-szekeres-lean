"""ETV internal-omission CEGAR, v3 (feasibility at a level).  usage: loop7.py <deadline> <pool> <level> [tag]
level = current proven minimum; each round asks CP-SAT for a vector with at most `level` holes.
INFEASIBLE => the minimum over the current rows is >= level+1 (COMPUTED), level is raised.
Same files as loop5.py.  Discovery only: rows are certified separately (certify5.py)."""
import json, os, sys, time, random, itertools
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ortools.sat.python import cp_model
import etv_common as ec
from etv_common import N
import coupled5, transport5, engine
from cyclists import masks, find_lists, extend

DEADLINE = float(sys.argv[1]); POOL = int(sys.argv[2]); LEVEL = int(sys.argv[3]); TAG = sys.argv[4] if len(sys.argv) > 4 else 'v3'
P = lambda f: os.path.join(HERE, f)
LOG = open(P(f'loop_{TAG}.log'), 'a')
def log(**kw):
    kw['t'] = time.strftime('%H:%M:%S'); LOG.write(json.dumps(kw) + '\n'); LOG.flush(); print(json.dumps(kw), flush=True)
M = masks(ec.TT); RNG = random.Random(int(time.time()))

import rowsio, blocks5
BG = blocks5.graphs()
def load_rows():
    return {s: d for s, (d, k) in rowsio.load_all(HERE).items()}

def block_separate(occ):
    om = 0
    for i in occ: om |= 1 << i
    new = []
    for K, adj in BG.items():
        C = blocks5.max_clique(adj, om)
        if len(C) >= 23:
            new.append(blocks5.extend(adj, C))
    return new

def cpsat_feas(rows, workers, level, nogoods=(), seconds=150):
    m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    for i in ec.FIXED_OCC: m.Add(h[i] == 0)
    for s, d in rows.items(): m.Add(sum(h[i] for i in s) >= d)
    for H in nogoods:
        Hs = set(H); m.Add(sum(h[i] for i in Hs) - sum(h[i] for i in range(N) if i not in Hs) <= len(Hs) - 1)
    m.Add(sum(h) <= level)
    so = cp_model.CpSolver(); so.parameters.num_workers = workers; so.parameters.max_time_in_seconds = seconds
    so.parameters.random_seed = RNG.randrange(10**6)
    st = so.Solve(m)
    H = [i for i in range(N) if so.Value(h[i])] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return so.StatusName(st), H

def cadical_feas(rows, workers, level, nogoods=(), seconds=150):
    """Same contract as cpsat_feas, with CaDiCaL on the PB CNF (pbcnf5.build); nogoods are search-only clauses."""
    import subprocess
    from pbcnf5 import build
    top, cls = build([(list(s), d) for s, d in rows.items()], level, N, ec.FIXED_OCC)
    for H in nogoods:
        Hs = set(H); cls = cls + [[-(i + 1) for i in Hs] + [(i + 1) for i in range(N) if i not in Hs]]
    path = P(f'fcnf/feas_{os.getpid()}.cnf'); os.makedirs(P('fcnf'), exist_ok=True)
    with open(path, 'w') as f:
        f.write(f'p cnf {top} {len(cls)}\n')
        for c in cls: f.write(' '.join(map(str, c)) + ' 0\n')
    r = subprocess.run(['cadical', '-q', '-t', str(int(seconds)), '--seed=%d' % RNG.randrange(10**6), path], capture_output=True, text=True)
    os.remove(path)
    if r.returncode == 20: return 'INFEASIBLE', None
    if r.returncode != 10: return 'UNKNOWN', None
    vals = set(int(x) for line in r.stdout.splitlines() if line.startswith('v') for x in line.split()[1:])
    return 'FEASIBLE', [i for i in range(N) if (i + 1) in vals]

if os.environ.get('FINDER') == 'cadical':
    cpsat_feas = cadical_feas

def cpsat_min(rows, workers, nogoods=(), seconds=600):
    m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    for i in ec.FIXED_OCC: m.Add(h[i] == 0)
    for s, d in rows.items(): m.Add(sum(h[i] for i in s) >= d)
    for H in nogoods:   # search diversity only (never part of a bound)
        Hs = set(H); m.Add(sum(h[i] for i in Hs) - sum(h[i] for i in range(N) if i not in Hs) <= len(Hs) - 1)
    m.Minimize(sum(h))
    so = cp_model.CpSolver(); so.parameters.num_workers = workers; so.parameters.max_time_in_seconds = seconds
    so.parameters.random_seed = RNG.randrange(10**6)
    st = so.Solve(m)
    H = [i for i in range(N) if so.Value(h[i])] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return so.StatusName(st), H, so.BestObjectiveBound()

def test(S): return S, coupled5.fast_solve(S, seconds=30)
def minimize(S):
    try: return engine.minimize_fast(S)
    except Exception as e: return None
def transport_one(core):
    try:
        tests, info = transport5.used_tests(core)
        if tests is None: return None
        small = engine.shrink_fast(core, tests)
        sups, sinfo = transport5.search(core, small, limit=40)
        return {'core': core, 'tests_used': len(tests), 'tests_min': len(small), 'tests': small, 'supports': sups, 'search': sinfo}
    except Exception as e:
        return {'core': core, 'error': repr(e), 'supports': [core]}

def candidates(occ, limit, lo=10, hi=15):
    faces = find_lists(M, occ, 7, limit=5000, rng=RNG, per_start=300)
    fm = list({sum(1 << i for i in f) for f in faces})
    pool = set()
    it = itertools.combinations(fm, 2) if len(fm) < 2500 else ((RNG.choice(fm), RNG.choice(fm)) for _ in range(2_000_000))
    for x, y in it:
        m = x | y
        if lo <= m.bit_count() <= hi: pool.add(m)
        if len(pool) > 30 * limit: break
    keys = list(pool); RNG.shuffle(keys)
    fs = fm[:800]
    keys = sorted(keys[:8 * limit], key=lambda m: (-sum(1 for f in fs if m & f == f), m.bit_count()))[:limit]
    return [[i for i in range(N) if m >> i & 1] for m in keys], len(fm)

FORCED = (ec.TT | ec.TT.transpose(0, 2, 1))
def dense_candidates(occ, ncand, lo, hi):
    faces = find_lists(M, occ, 7, limit=3000, rng=RNG, per_start=200)
    if not faces: return []
    def grow(seed, size):
        S = list(seed)
        while len(S) < size:
            sc = sorted(((sum(1 for a, b in itertools.combinations(S, 2) if FORCED[a, b, x]) + RNG.random() * 3, x) for x in occ if x not in S), reverse=True)
            S.append(sc[RNG.randrange(min(3, len(sc)))][1])
        return tuple(sorted(S))
    out = set(); tries = 0
    while len(out) < ncand and tries < 5 * ncand:
        tries += 1
        seed = sorted(set(RNG.choice(faces)) | set(RNG.choice(faces))); size = RNG.randrange(lo, hi + 1)
        if len(seed) > size: seed = RNG.sample(seed, size)
        out.add(grow(seed, size))
    return [list(c) for c in out]

def test60(S): return S, coupled5.fast_solve(S, seconds=60)

def probe_vector(pool, H, want, big=False):
    occ = [i for i in range(N) if i not in H]
    found = []; stats = {'sat': 0, 'unsat': 0, 'unknown': 0}; nf = 0
    stages = [('faces', 10, 15), ('faces', 14, 18), ('dense', 15, 17)] + ([('dense', 17, 19)] if big else [])
    for kind, lo, hi in stages:
        if kind == 'faces': cands, nf = candidates(occ, 1500, lo, hi); fn = test
        else: cands = dense_candidates(occ, 800 if big else 400, lo, hi); fn = test60
        for S, r in pool.imap_unordered(fn, cands, chunksize=2):
            stats[r] += 1
            if r == 'unsat': found.append(S)
            if len(found) >= want: break
        if len(found) >= max(2, want // 2): break
    return found, stats, nf

STUCKV = []
def process_found(pool, found, rnd, rows, t0):
    cores = [c for c in pool.map(minimize, found) if c]
    cores = [list(c) for c in {tuple(sorted(c)) for c in cores}]
    with open(P('cores.jsonl'), 'a') as f:
        for c in cores: f.write(json.dumps({'support': c, 'from_round': rnd, 'tag': TAG}) + '\n')
    trans = pool.map(transport_one, cores)
    n_new = 0
    with open(P('templates.jsonl'), 'a') as tf, open(P('trows.jsonl'), 'a') as rf:
        for r in trans:
            if not r: continue
            tf.write(json.dumps({k: v for k, v in r.items() if k != 'supports'}) + '\n')
            for s in r['supports']:
                if tuple(sorted(s)) not in rows:
                    rows[tuple(sorted(s))] = 1; n_new += 1
                    rf.write(json.dumps({'support': sorted(s), 'core': r['core']}) + '\n')
    log(event='transport', cores=[len(c) for c in cores], new_rows=n_new,
        per_core=[len(r['supports']) if r else 0 for r in trans], secs=round(time.time() - t0))

def main():
    global LEVEL
    with Pool(POOL) as pool:
        rnd = 0
        while time.time() < DEADLINE - 30:
            rnd += 1; t0 = time.time()
            rows = load_rows()
            st, H = cpsat_feas(rows, POOL, LEVEL, nogoods=STUCKV, seconds=60)
            if st == 'INFEASIBLE':
                if STUCKV:
                    log(event='level_exhausted_except_stuck', level=LEVEL, stuck=len(STUCKV))
                    found = []; keep = []
                    for V in STUCKV:
                        fv, stats, nf = probe_vector(pool, V, 2 * POOL, big=True)
                        log(event='stuck_retry', found=len(fv), stats=stats)
                        if fv: found += fv
                        else: keep.append(V)
                    STUCKV[:] = keep
                    if found: process_found(pool, found, rnd, rows, t0); continue
                    LEVEL += 1; log(event='explore_next_level', level=LEVEL, stuck=len(STUCKV)); continue
                LEVEL += 1; log(event='level_up', level=LEVEL, rows=len(rows), note='CP-SAT INFEASIBLE at previous level (no nogoods)')
                json.dump({'level': LEVEL, 'rows': len(rows), 't': time.strftime('%H:%M:%S')}, open(P('level.json'), 'w'))
                continue
            if H is None:
                log(event='cpsat_unknown', status=st, level=LEVEL)
                st, H = cpsat_feas(rows, POOL, LEVEL + 1, nogoods=STUCKV, seconds=60)
                if H is None: log(event='cpsat_unknown', status=st, level=LEVEL + 1); continue
            occ = [i for i in range(N) if i not in H]
            L = find_lists(M, occ, 8, limit=60, rng=RNG)
            if L:
                rc = {tuple(sorted(k)): v for k, v in json.load(open(P('rows_cycle.json')))}
                for l in L:
                    E = extend(ec.TT, l, RNG); rc[tuple(sorted(E))] = len(E) - 7
                json.dump([[list(k), v] for k, v in rc.items()], open(P('rows_cycle.json.tmp'), 'w')); os.replace(P('rows_cycle.json.tmp'), P('rows_cycle.json'))
                log(event='cycle_rows', added=len(L), status=st, holes=len(H)); continue
            B = block_separate(occ)
            if B:
                p = P('rows_block.json'); rb = {tuple(sorted(s)): d for s, d in (json.load(open(p)) if os.path.exists(p) else [])}
                for C in B: rb[tuple(sorted(C))] = len(C) - 22
                json.dump([[list(k), v] for k, v in rb.items()], open(p + '.tmp', 'w')); os.replace(p + '.tmp', p)
                log(event='block_rows', added=len(B), sizes=[len(C) for C in B], holes=len(H)); continue
            vecs = [H]
            st2, H2 = cpsat_feas(rows, POOL, len(H), nogoods=STUCKV + [H], seconds=30)
            if H2 is not None and not find_lists(M, [i for i in range(N) if i not in H2], 8, limit=1):
                vecs.append(H2)
            log(event='vector', round=rnd, status=st, holes=len(H), level=LEVEL, rows=len(rows), H=H, second=H2 if len(vecs) > 1 else None)
            with open(P('vectors.jsonl'), 'a') as f:
                for V in vecs: f.write(json.dumps({'status': st, 'holes': V, 'rows': len(rows), 't': time.strftime('%H:%M:%S')}) + '\n')
            found = []
            for V in vecs:
                fv, stats, nf = probe_vector(pool, V, 2 * POOL)
                log(event='probe', faces=nf, stats=stats, found=len(fv))
                if not fv:
                    log(event='STUCK', H=V); STUCKV.append(V)
                    with open(P('stuck.jsonl'), 'a') as f: f.write(json.dumps(V) + '\n')
                found += fv
            if found: process_found(pool, found, rnd, rows, t0)

if __name__ == '__main__':
    main()
