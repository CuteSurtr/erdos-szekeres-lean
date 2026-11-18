"""Scan k-subsets of the 70 states of the (6,6;8) catalog for abstract realizability on at most n points.
Incremental CaDiCaL (pysat) with assumptions occ(s); numpy coverage test against the realizable sets found.
usage: scan4.py <n> <k> <out.jsonl> [must_contain_state_index or -1] [batch]"""
import sys, json, time, itertools, os
import numpy as np
os.environ["ETV_A"] = "4"; os.environ["ETV_B"] = "4"
import etv_common as ec
import witg
n, k, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
must = int(sys.argv[4]) if len(sys.argv) > 4 else -1
BATCH = int(sys.argv[5]) if len(sys.argv) > 5 else 20000
w = witg.WitG(6, 6, n); so = w.solver(); NS = len(w.S)
assert [tuple(s) for s in w.S] == [tuple(s) for s in ec.STATES]
K = np.zeros((0, NS), dtype=bool); Kl = []
t0 = time.time(); nq = nsat = ncand = done = 0
def gen():
    if must < 0:
        yield from itertools.combinations(range(NS), k)
    else:
        rest = [s for s in range(NS) if s != must]
        for T in itertools.combinations(rest, k - 1): yield tuple(sorted(T + (must,)))
def flush(batch):
    global K, Kl, nq, nsat, ncand
    B = np.array(batch, dtype=np.int64)
    cov = np.zeros(len(batch), dtype=bool)
    if len(Kl):
        K = np.array(Kl, dtype=bool)
        for c0 in range(0, len(Kl), 512):
            Kc = K[c0:c0 + 512]
            m = np.ones((Kc.shape[0], len(batch)), dtype=bool)
            for j in range(k): m &= Kc[:, B[:, j]]
            cov |= m.any(axis=0)
    for idx in np.nonzero(~cov)[0]:
        T = batch[idx]
        if any(all(row[s] for s in T) for row in Kl[-50:]): continue
        nq += 1
        if so.solve(assumptions=[w.occ[s] for s in T]):
            m_, st, sig = w.decode_states(so.get_model()); row = [False] * NS
            for s in st: row[s] = True
            assert all(row[s] for s in T)
            Kl.append(row); nsat += 1
        else:
            ncand += 1
            with open(out, 'a') as f: f.write(json.dumps({'T': list(T), 'n': n, 'status': 'UNSAT_at_n'}) + '\n')
batch = []
for T in gen():
    batch.append(T); done += 1
    if len(batch) >= BATCH:
        flush(batch); batch = []
        print(f'{done} subsets, {nq} queries, {nsat} sat, {ncand} unsat-at-n, known {len(Kl)}, {time.time()-t0:.0f}s', flush=True)
if batch: flush(batch)
print(f'DONE {done} subsets, {nq} queries, {nsat} sat, {ncand} unsat-at-n={n}, {time.time()-t0:.0f}s', flush=True)
