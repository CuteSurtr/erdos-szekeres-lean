"""Given a 33-hole vector, search subsets of its occupied set that the coupled model refutes.
Discovery only. Usage: probe_vec.py <tag> <holes-json-list> [max_minutes] [procs]"""
import itertools, json, os, random, sys, time
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import N, ROWS
import coupled

HERE = os.path.dirname(os.path.abspath(__file__))

def test(S):
    return S, coupled.fast_solve(S, seconds=30)

def minimize(S):
    S = list(S)
    i = 0
    while i < len(S):
        T = S[:i] + S[i + 1:]
        if coupled.fast_solve(T, seconds=30) == 'unsat':
            S = T
        else:
            i += 1
    return S

def candidates(holes, rows, rng, limit=3000):
    O = set(range(N)) - set(holes)
    faces = sorted({tuple(sorted(set(s) & O)) for s, d in rows
                    if len(s) - d == 7 and len(set(s) & O) == 7})
    fm = [sum(1 << i for i in f) for f in faces]
    pool = {}
    for x, y in itertools.combinations(fm, 2):
        m = x | y; k = m.bit_count()
        if 10 <= k <= 15 and m not in pool:
            pool[m] = sum(m & f == f for f in fm)
    ranked = sorted(pool, key=lambda m: (-pool[m], m.bit_count(), m))
    out = ranked[:limit // 2]
    # triple unions from top pairs
    for m in ranked[:300]:
        for f in rng.sample(fm, min(40, len(fm))):
            j = m | f
            if 14 <= j.bit_count() <= 17 and j not in pool:
                pool[j] = sum(j & g == g for g in fm)
                out.append(j)
    out = out[:limit]
    return [[i for i in range(N) if m >> i & 1] for m in out], len(faces)

if __name__ == '__main__':
    tag = sys.argv[1]; holes = json.loads(sys.argv[2])
    minutes = float(sys.argv[3]) if len(sys.argv) > 3 else 20
    procs = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    from mip import load_rows
    rows, _, _ = load_rows()
    rng = random.Random(1113)
    cands, nf = candidates(holes, rows, rng)
    print(json.dumps({'tag': tag, 'faces': nf, 'candidates': len(cands)}), flush=True)
    deadline = time.time() + 60 * minutes
    found = []
    stats = {'sat': 0, 'unsat': 0, 'unknown': 0}
    with Pool(procs) as P:
        for S, st in P.imap_unordered(test, cands, chunksize=1):
            stats[st] += 1
            if st == 'unsat':
                found.append(S)
                print(json.dumps({'event': 'unsat', 'size': len(S), 'support': S}), flush=True)
            if time.time() > deadline or len(found) >= 6:
                P.terminate(); break
    print(json.dumps({'stats': stats}), flush=True)
    cores = []
    for S in found:
        core = minimize(S)
        cores.append(core)
        print(json.dumps({'event': 'core', 'size': len(core), 'support': core}), flush=True)
    json.dump({'tag': tag, 'holes': holes, 'stats': stats, 'unsat_supports': found, 'cores': cores},
              open(os.path.join(HERE, f'probe_{tag}.json'), 'w'), indent=1)
