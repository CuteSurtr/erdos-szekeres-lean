"""Scan all k-subsets of the 70 states of the (6,6;8) catalog for abstract realizability on at most n points
(incremental CaDiCaL via pysat, assumptions occ(s)).  SAT = realizable (model re-checked by independent DP).
UNSAT at this n is only a candidate (needs wit.py at nmax(T)).
usage: scan3.py <n> <k> <out.jsonl> [start_index]"""
import sys, json, time, itertools, os
import witg
n, k, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
w = witg.WitG(6, 6, n); so = w.solver(); NS = len(w.S)
os.environ["ETV_A"] = "4"; os.environ["ETV_B"] = "4"
import etv_common as ec
assert [tuple(s) for s in w.S] == [tuple(s) for s in ec.STATES]
known = []      # realizable occupancy masks seen so far (to skip queries)
t0 = time.time(); nq = 0; nsat = 0; cands = []
done = 0
for T in itertools.combinations(range(NS), k):
    done += 1
    mask = sum(1 << s for s in T)
    if any(mask & ~M == 0 for M in known): continue
    nq += 1
    if so.solve(assumptions=[w.occ[s] for s in T]):
        m, st, sig = w.decode_states(so.get_model()); M = sum(1 << s for s in set(st))
        assert mask & ~M == 0
        known.append(M); nsat += 1
        if len(known) > 4000: known = sorted(known, key=lambda x: -bin(x).count('1'))[:2000]
    else:
        cands.append(T)
        with open(out, 'a') as f: f.write(json.dumps({'T': list(T), 'n': n, 'status': 'UNSAT_at_n'}) + '\n')
    if nq % 500 == 0:
        print(f'{done} subsets, {nq} queries, {nsat} sat, {len(cands)} unsat-at-n, {time.time()-t0:.0f}s', flush=True)
print(f'DONE {done} subsets, {nq} queries, {nsat} sat, {len(cands)} unsat-at-n={n}, {time.time()-t0:.0f}s', flush=True)
