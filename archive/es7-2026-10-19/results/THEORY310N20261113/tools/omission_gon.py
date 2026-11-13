#!/usr/bin/env python3
"""Internal omission IP v2: lazy cycle rows with maximal-list extension.
Env CAPA (cap coords 1..A), CUPB (cup coords 1..B).  Valid lower bound on
holes = MIP dual bound with the generated (all valid) rows."""
import os, sys, time, json, itertools, random
os.environ.setdefault('CAPA', '4'); os.environ.setdefault('CUPB', '5')
import omission_gen as og
import numpy as np, highspy
N, T, ST = og.N, og.T, og.ST
GON = int(os.environ.get("GON", 8))
rng = random.Random(1)

def valid_insert(lst, x, p):
    new = lst[:p] + [x] + lst[p:]
    k = len(new); i = p
    for a in range(k):
        for b in range(a + 1, k):
            if i in (a, b):
                continue
            tri = sorted([a, b, i])
            if not T[new[tri[0]], new[tri[1]], new[tri[2]]]:
                return None
    return new

def extend(lst):
    lst = list(lst); changed = True
    cand = list(range(N)); rng.shuffle(cand)
    while changed:
        changed = False
        for x in cand:
            if x in lst:
                continue
            for p in range(len(lst) + 1):
                new = valid_insert(lst, x, p)
                if new is not None:
                    lst = new; changed = True; break
    return lst

def find_lists(occ, limit):
    occ = sorted(occ); res = []; seen = set()
    def dfs(seq):
        if len(seq) == GON:
            key = frozenset(seq)
            if key not in seen:
                seen.add(key); res.append(tuple(seq))
            return len(res) >= limit
        for x in occ:
            if x in seq or x < seq[0]:
                continue
            if all(T[seq[i], seq[j], x] for i in range(len(seq)) for j in range(i + 1, len(seq))):
                if dfs(seq + [x]):
                    return True
        return False
    starts = occ[:]; rng.shuffle(starts)
    for s in starts:
        before = len(res)
        def dfs_s(seq):
            if len(seq) == GON:
                key = frozenset(seq)
                if key not in seen:
                    seen.add(key); res.append(tuple(seq))
                return len(res) - before >= 3
            for x in occ:
                if x in seq or x < seq[0]:
                    continue
                if all(T[seq[i], seq[j], x] for i in range(len(seq)) for j in range(i + 1, len(seq))):
                    if dfs_s(seq + [x]):
                        return True
            return False
        dfs_s([s])
        if len(res) >= limit:
            break
    return res

def solve(rows, fixed, tl):
    h = highspy.Highs(); h.silent(); h.setOptionValue('threads', 1); h.setOptionValue('time_limit', float(tl))
    inf = highspy.kHighsInf
    for i in range(N):
        h.addVar(0.0, 0.0 if i in fixed else 1.0); h.changeColCost(i, 1.0)
        h.changeColIntegrality(i, highspy.HighsVarType.kInteger)
    for sup, d in rows:
        h.addRow(float(d), inf, len(sup), np.array(sorted(sup), dtype=np.int32), np.ones(len(sup)))
    h.run(); sol = h.getSolution().col_value; info = h.getInfo()
    return [i for i in range(N) if sol[i] > 0.5], info.mip_dual_bound, str(h.getModelStatus())

if __name__ == '__main__':
    budget = float(sys.argv[1]); per = int(sys.argv[2]); t0 = time.time()
    rows = {}; fixed = {0, ST.index(tuple([1] + [0] * (og.A - 1)))}
    best = 0; it = 0
    while time.time() - t0 < budget:
        it += 1
        holes, bound, status = solve([(s, d) for s, d in rows.items()], fixed, 120)
        best = max(best, bound)
        occ = [i for i in range(N) if i not in holes]
        lists = find_lists(occ, per)
        added = 0
        for L in lists:
            E = extend(L); key = frozenset(E)
            if key not in rows:
                rows[key] = len(E) - (GON - 1); added += 1
        print(f'it {it} rows {len(rows)} incumbent {len(holes)} dual {bound:.2f} best {best:.2f} {status} added {added} maxlen {max([len(r) for r in rows] or [0])} t={time.time()-t0:.0f}s', flush=True)
        if not lists:
            break
    json.dump({'A': og.A, 'B': og.B, 'best_dual': best, 'rows': [[sorted(k), v] for k, v in rows.items()]},
              open(f'omission2_A{og.A}_B{og.B}_gon{GON}.json', 'w'))
    print('final best dual bound', best, 'capacity <=', N - int(np.ceil(best - 1e-6)))
