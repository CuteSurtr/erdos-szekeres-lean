"""ETV internal-omission CEGAR (discovery driver).  usage: loop5.py <deadline-epoch> <pool> [tag]
State in this directory: rows_cycle.json (cycle rows), cores.jsonl, templates.jsonl, transported rows in
trows.jsonl, vectors.jsonl, loop.log.  Each round: exact CP-SAT minimum of holes over all rows -> probe
subsets of the occupied set with the coupled model -> minimise UNSAT supports -> transport -> repeat."""
import json, os, sys, time, random, itertools
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from ortools.sat.python import cp_model
import etv_common as ec
from etv_common import N
import coupled5, transport5
from cyclists import masks, find_lists, extend

DEADLINE = float(sys.argv[1]); POOL = int(sys.argv[2]); TAG = sys.argv[3] if len(sys.argv) > 3 else 'main'
P = lambda f: os.path.join(HERE, f)
LOG = open(P(f'loop_{TAG}.log'), 'a')
def log(**kw):
    kw['t'] = time.strftime('%H:%M:%S'); LOG.write(json.dumps(kw) + '\n'); LOG.flush(); print(json.dumps(kw), flush=True)

M = masks(ec.TT); RNG = random.Random(13)

def load_rows():
    rows = {}
    if os.path.exists(P('rows_cycle.json')):
        for s, d in json.load(open(P('rows_cycle.json'))): rows[tuple(sorted(s))] = max(d, rows.get(tuple(sorted(s)), 0))
    for fn in ('cores.jsonl', 'trows.jsonl'):
        if os.path.exists(P(fn)):
            for line in open(P(fn)):
                r = json.loads(line); s = tuple(sorted(r['support'])); rows[s] = max(1, rows.get(s, 0))
    return rows

def save_cycle(rows_cycle):
    json.dump([[list(k), v] for k, v in rows_cycle.items()], open(P('rows_cycle.json.tmp'), 'w'))
    os.replace(P('rows_cycle.json.tmp'), P('rows_cycle.json'))

def cpsat_min(rows, workers, seconds=900, hint=None):
    m = cp_model.CpModel(); h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    for i in ec.FIXED_OCC: m.Add(h[i] == 0)
    for s, d in rows.items(): m.Add(sum(h[i] for i in s) >= d)
    m.Minimize(sum(h))
    if hint:
        for i in range(N): m.AddHint(h[i], 1 if i in hint else 0)
    so = cp_model.CpSolver(); so.parameters.num_workers = workers; so.parameters.max_time_in_seconds = seconds
    so.parameters.random_seed = RNG.randrange(1000)
    st = so.Solve(m)
    H = [i for i in range(N) if so.Value(h[i])] if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None
    return so.StatusName(st), H, so.BestObjectiveBound()

def test(S):
    return S, coupled5.fast_solve(S, seconds=30)

def minimize(S):
    S = list(S); i = 0
    while i < len(S):
        T = S[:i] + S[i + 1:]
        if coupled5.fast_solve(T, seconds=30) == 'unsat': S = T
        else: i += 1
    return S

def transport_one(core):
    try: return transport5.run(core, transport_seconds=90)
    except Exception as e: return {'core': core, 'error': repr(e), 'supports': [core]}

def candidates(occ, limit, lo=10, hi=15):
    faces = find_lists(M, occ, 7, limit=4000, rng=RNG, per_start=200)
    fm = list({sum(1 << i for i in f) for f in faces})
    pool = {}
    for x, y in itertools.combinations(fm, 2) if len(fm) < 2500 else ((RNG.choice(fm), RNG.choice(fm)) for _ in range(3_000_000)):
        m = x | y; k = m.bit_count()
        if lo <= k <= hi and m not in pool: pool[m] = None
        if len(pool) > 20 * limit: break
    keys = list(pool); RNG.shuffle(keys)
    # prefer pairs whose union contains many faces
    def score(m): return sum(1 for f in fm[:600] if m & f == f)
    keys = sorted(keys[:6 * limit], key=lambda m: (-score(m), m.bit_count()))[:limit]
    return [[i for i in range(N) if m >> i & 1] for m in keys], len(fm)

def main():
    with Pool(POOL) as pool:
        rnd = 0
        while time.time() < DEADLINE - 60:
            rnd += 1
            rows = load_rows()
            st, H, bd = cpsat_min(rows, POOL)
            if H is None:
                log(event='cpsat_fail', status=st); time.sleep(5); continue
            occ = [i for i in range(N) if i not in H]
            # cycle separation first (cheap)
            L = find_lists(M, occ, 8, limit=60, rng=RNG)
            if L:
                rc = {tuple(k): v for k, v in (json.load(open(P('rows_cycle.json'))) if os.path.exists(P('rows_cycle.json')) else [])}
                rc = {tuple(sorted(k)): v for k, v in rc.items()}
                for l in L:
                    E = extend(ec.TT, l, RNG); rc[tuple(sorted(E))] = len(E) - 7
                save_cycle(rc)
                log(event='cycle_rows', added=len(L), status=st, holes=len(H), bound=bd)
                continue
            log(event='vector', round=rnd, status=st, holes=len(H), bound=bd, rows=len(rows), H=H)
            with open(P('vectors.jsonl'), 'a') as f: f.write(json.dumps({'status': st, 'holes': H, 'rows': len(rows)}) + '\n')
            cands, nf = candidates(occ, 1500)
            found = []; stats = {'sat': 0, 'unsat': 0, 'unknown': 0}; t0 = time.time()
            for S, r in pool.imap_unordered(test, cands, chunksize=2):
                stats[r] += 1
                if r == 'unsat': found.append(S)
                if len(found) >= 3 * POOL or time.time() - t0 > 600 or time.time() > DEADLINE - 60: break
            log(event='probe', faces=nf, cands=len(cands), stats=stats, secs=round(time.time() - t0))
            if not found:
                log(event='STUCK', H=H); 
                with open(P('stuck.jsonl'), 'a') as f: f.write(json.dumps(H) + '\n')
                cands, nf = candidates(occ, 1500, 14, 18)
                for S, r in pool.imap_unordered(test, cands, chunksize=2):
                    if r == 'unsat': found.append(S)
                    if len(found) >= POOL or time.time() > DEADLINE - 60: break
                if not found: return
            cores = pool.map(minimize, found)
            cores = [list(c) for c in {tuple(sorted(c)) for c in cores}]
            with open(P('cores.jsonl'), 'a') as f:
                for c in cores: f.write(json.dumps({'support': c, 'from_round': rnd, 'tag': TAG}) + '\n')
            log(event='cores', sizes=[len(c) for c in cores])
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
            log(event='transport', new_rows=n_new, per_core=[len(r['supports']) if r else 0 for r in trans],
                tests=[r.get('tests_min') if r else None for r in trans])

if __name__ == '__main__':
    main()
