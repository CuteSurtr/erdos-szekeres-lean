"""ETV internal-omission CEGAR, v2 (in-process minimisation/shrinking).  usage: loop6.py <deadline> <pool> [tag]
Same files as loop5.py.  Discovery only: rows are certified separately (certify5.py)."""
import json, os, sys, time, random, itertools
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from ortools.sat.python import cp_model
import etv_common as ec
from etv_common import N
import coupled5, transport5, engine
from cyclists import masks, find_lists, extend

DEADLINE = float(sys.argv[1]); POOL = int(sys.argv[2]); TAG = sys.argv[3] if len(sys.argv) > 3 else 'v2'
P = lambda f: os.path.join(HERE, f)
LOG = open(P(f'loop_{TAG}.log'), 'a')
def log(**kw):
    kw['t'] = time.strftime('%H:%M:%S'); LOG.write(json.dumps(kw) + '\n'); LOG.flush(); print(json.dumps(kw), flush=True)
M = masks(ec.TT); RNG = random.Random(int(time.time()))

def load_rows():
    rows = {}
    for s, d in json.load(open(P('rows_cycle.json'))): rows[tuple(sorted(s))] = max(d, rows.get(tuple(sorted(s)), 0))
    for fn in ('cores.jsonl', 'trows.jsonl'):
        if os.path.exists(P(fn)):
            for line in open(P(fn)):
                s = tuple(sorted(json.loads(line)['support'])); rows[s] = max(1, rows.get(s, 0))
    return rows

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

def probe_vector(pool, H, want):
    occ = [i for i in range(N) if i not in H]
    found = []; stats = {'sat': 0, 'unsat': 0, 'unknown': 0}
    for lo, hi in ((10, 15), (14, 18)):
        cands, nf = candidates(occ, 1500, lo, hi)
        for S, r in pool.imap_unordered(test, cands, chunksize=4):
            stats[r] += 1
            if r == 'unsat': found.append(S)
            if len(found) >= want: break
        if found: break
    return found, stats, nf

def main():
    with Pool(POOL) as pool:
        rnd = 0
        while time.time() < DEADLINE - 30:
            rnd += 1; t0 = time.time()
            rows = load_rows()
            st, H, bd = cpsat_min(rows, POOL)
            if H is None: log(event='cpsat_fail', status=st); time.sleep(5); continue
            occ = [i for i in range(N) if i not in H]
            L = find_lists(M, occ, 8, limit=60, rng=RNG)
            if L:
                rc = {tuple(sorted(k)): v for k, v in json.load(open(P('rows_cycle.json')))}
                for l in L:
                    E = extend(ec.TT, l, RNG); rc[tuple(sorted(E))] = len(E) - 7
                json.dump([[list(k), v] for k, v in rc.items()], open(P('rows_cycle.json.tmp'), 'w')); os.replace(P('rows_cycle.json.tmp'), P('rows_cycle.json'))
                log(event='cycle_rows', added=len(L), status=st, holes=len(H)); continue
            vecs = [H]
            st2, H2, _ = cpsat_min(rows, POOL, nogoods=[H], seconds=60)
            if H2 is not None and len(H2) == len(H) and not find_lists(M, [i for i in range(N) if i not in H2], 8, limit=1):
                vecs.append(H2)
            log(event='vector', round=rnd, status=st, holes=len(H), bound=bd, rows=len(rows), H=H, second=H2 if len(vecs) > 1 else None)
            with open(P('vectors.jsonl'), 'a') as f:
                for V in vecs: f.write(json.dumps({'status': st, 'holes': V, 'rows': len(rows), 't': time.strftime('%H:%M:%S')}) + '\n')
            found = []
            for V in vecs:
                fv, stats, nf = probe_vector(pool, V, 2 * POOL)
                log(event='probe', faces=nf, stats=stats, found=len(fv))
                if not fv:
                    log(event='STUCK', H=V)
                    with open(P('stuck.jsonl'), 'a') as f: f.write(json.dumps(V) + '\n')
                found += fv
            if not found: return
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

if __name__ == '__main__':
    main()
