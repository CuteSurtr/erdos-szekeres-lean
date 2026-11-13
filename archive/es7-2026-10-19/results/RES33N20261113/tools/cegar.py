"""Residual budget-33 CEGAR driver (13 Nov 2026). Discovery only; UNSAT cores are candidate rows that
still need LRAT/cake_lpr (or Lean RUP) certification.

Loop: find a 33-hole vector (CP-SAT neighbourhood search around known vectors, then global search);
probe subsets of its occupied set with the coupled model; minimise UNSAT supports to cores; append to
newrows.json; repeat."""
import hashlib, itertools, json, os, random, sys, time
from multiprocessing import Pool
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from common import N, check
import coupled
from mip import load_rows
from probe_vec import candidates, test, minimize
import shrink_tests
from ortools.sat.python import cp_model

DEADLINE = float(sys.argv[1]) if len(sys.argv) > 1 else time.time() + 3600
LOG = open(os.path.join(HERE, 'cegar.log'), 'a')
def log(**kw):
    kw['t'] = time.strftime('%H:%M:%S')
    LOG.write(json.dumps(kw) + '\n'); LOG.flush()
    print(json.dumps(kw), flush=True)

def seeds():
    R = '/home/jay/research/lean/erdos-szekeres-lean/'
    out = []
    w = json.load(open(R + 'cloud/es7-2026-10-19/results/ES8SLACK/witnesses.json'))
    out += w['residual_2650_33_hole_witnesses_state0_occupied']
    r = json.load(open(R + 'experiments/omission-residual32-rank-search-2026-10-10/rows-and-countermodels.json'))
    out += [x['strict_countermodel_holes'] for x in r['rows']]
    out.append([12, 17, 25, 27, 33, 34, 35, 36, 44, 45, 57, 58, 60, 62, 72, 81, 85, 88, 92, 96, 98, 100,
                101, 107, 109, 111, 116, 117, 119, 124, 126, 127, 138])
    p = os.path.join(HERE, 'vectors.json')
    if os.path.exists(p):
        out += json.load(open(p))
    return out

def cpsat(rows, center=None, radius=None, seconds=60, workers=4, seed=0):
    m = cp_model.CpModel()
    h = [m.NewBoolVar(f'h{i}') for i in range(N)]
    m.Add(h[0] == 0)
    for s, d in rows:
        m.Add(sum(h[i] for i in s) >= d)
    m.Add(sum(h) <= 33)
    if center is not None:
        C = set(center)
        # |H \ C| <= radius  (number of new holes); with |H| <= 33 this bounds the distance
        m.Add(sum(h[i] for i in range(N) if i not in C) <= radius)
        for i in range(N):
            m.AddHint(h[i], 1 if i in C else 0)
    sol = cp_model.CpSolver()
    sol.parameters.max_time_in_seconds = seconds
    sol.parameters.num_workers = workers
    sol.parameters.random_seed = seed
    st = sol.Solve(m)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        H = [i for i in range(N) if sol.Value(h[i])]
        assert not check(H, rows) and 0 not in H and len(H) <= 33
        return 'found', H
    return sol.StatusName(st), None

def probe(holes, pool, rows, max_cands=1500, want=8):
    rng = random.Random(len(holes) * 7919 + sum(holes))
    cands, nf = candidates(holes, rows, rng, limit=max_cands)
    found = []; stats = {'sat': 0, 'unsat': 0, 'unknown': 0}
    it = pool.imap_unordered(test, cands, chunksize=1)
    t0 = time.time()
    for S, st in it:
        stats[st] += 1
        if st == 'unsat':
            found.append(S)
        if len(found) >= want or time.time() > DEADLINE or time.time() - t0 > 600:
            break
    cores = pool.map(minimize, found) if found else []
    # dedupe cores
    cores = [list(c) for c in {tuple(sorted(c)) for c in cores}]
    trans = pool.map(transport_one, cores) if cores else []
    return cores, trans, stats, nf, len(cands)

def transport_one(core):
    try:
        r = shrink_tests.run(core, transport_seconds=60)
        return r
    except Exception as e:
        return {'core': core, 'error': repr(e), 'supports': [core]}

FAILED = set()

def main():
    newp = os.path.join(HERE, 'newrows.json')
    newrows = json.load(open(newp)) if os.path.exists(newp) else []
    vecp = os.path.join(HERE, 'vectors.json')
    vectors = json.load(open(vecp)) if os.path.exists(vecp) else []
    with Pool(4) as pool:
        while time.time() < DEADLINE - 120:
            rows, ntpl, nnew = load_rows()
            target = None
            # 1) neighbourhood search around known vectors, most recent first
            pool_vecs = seeds()[::-1]
            for radius in (4, 8, 12):
                for c in pool_vecs:
                    if time.time() > DEADLINE - 120: break
                    key = (tuple(sorted(c)), radius, len(rows))
                    if key in FAILED: continue
                    st, H = cpsat(rows, center=c, radius=radius, seconds=20)
                    if H:
                        target = H; break
                    if st == 'INFEASIBLE': FAILED.add(key)
                if target: break
            how = 'neighbourhood'
            if not target:
                how = 'global'
                st, H = cpsat(rows, seconds=900, workers=4, seed=int(time.time()) % 100000)
                log(event='global', status=st, rows=len(rows), newrows=len(newrows))
                if not H:
                    if st == 'INFEASIBLE':
                        log(event='INFEASIBLE', rows=len(rows), note='no 33-hole vector over extended rows (CP-SAT, uncertified)')
                        return
                    continue
                target = H
            log(event='vector', how=how, holes=target, rows=len(rows), newrows=len(newrows))
            vectors.append(target); json.dump(vectors, open(vecp, 'w'))
            cores, trans, stats, nf, nc = probe(target, pool, rows)
            log(event='probe', stats=stats, faces=nf, cands=nc, cores=[len(c) for c in cores],
                transported=[len(r['supports']) if r else 0 for r in trans])
            if not cores:
                log(event='STUCK', holes=target, note='no refuted subset among candidates')
                # keep it: try broader candidates next round by recording
                json.dump(newrows, open(newp + '.tmp', 'w'), separators=(',', ':')); os.replace(newp + '.tmp', newp)
                return
            have = {tuple(r['support']) for r in newrows}
            for c in cores:
                if tuple(sorted(c)) not in have:
                    have.add(tuple(sorted(c)))
                    newrows.append({'support': sorted(c), 'from_vector': len(vectors) - 1, 'kind': 'core'})
            tpath = os.path.join(HERE, 'newtemplates.jsonl')
            for r in trans:
                if not r: continue
                tid = hashlib.sha256(json.dumps([r['core'], r.get('tests')]).encode()).hexdigest()[:16]
                with open(tpath, 'a') as tf:
                    tf.write(json.dumps({'id': tid, 'core': r['core'], 'tests': r.get('tests'),
                                         'search': r.get('search'), 'n_supports': len(r['supports'])}) + '\n')
                for s in r['supports']:
                    if tuple(sorted(s)) not in have:
                        have.add(tuple(sorted(s)))
                        newrows.append({'support': sorted(s), 'from_vector': len(vectors) - 1, 'kind': 'transport',
                                        'template': tid})
            json.dump(newrows, open(newp + '.tmp', 'w'), separators=(',', ':')); os.replace(newp + '.tmp', newp)

if __name__ == '__main__':
    main()
