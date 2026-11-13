"""Lazy row-subset extraction: start from the cycle and block rows, repeatedly compute an exact optimum (RC2)
over the subset and add rows of the full set violated by the optimum, until the subset optimum reaches the
target.  The subset then suffices for "holes >= target" (as far as RC2 is exact: COMPUTED).
usage: lazy_subset.py <full_rows.json> <target> <out_subset.json> [per_iter]"""
import json, sys, time, random
from pysat.formula import WCNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.examples.rc2 import RC2
import etv_common as ec
from etv_common import N
full = [(tuple(s), d) for s, d in json.load(open(sys.argv[1]))]
target = int(sys.argv[2]); out = sys.argv[3]; per = int(sys.argv[4]) if len(sys.argv) > 4 else 60
def rc2_opt(rows):
    pool = IDPool(start_from=N + 1); w = WCNF(); var = lambda i: i + 1
    for i in ec.FIXED_OCC: w.append([-var(i)])
    for s, d in rows:
        L = [var(i) for i in s if i not in ec.FIXED_OCC]
        if d == 1: w.append(L)
        else:
            for c in CardEnc.atleast(lits=L, bound=d, vpool=pool, encoding=EncType.seqcounter).clauses: w.append(c)
    for i in range(N):
        if i not in ec.FIXED_OCC: w.append([-var(i)], weight=1)
    with RC2(w, solver='g4', adapt=True, exhaust=True, minz=True, trim=5) as r:
        m = r.compute(); return r.cost, [i for i in range(N) if m[i] > 0]
masks = [sum(1 << i for i in s) for s, d in full]
sub = [k for k, (s, d) in enumerate(full) if d >= 2 or len(s) <= 9]   # start: all cycle/block-like rows
subset = set(sub); rng = random.Random(1); t0 = time.time(); it = 0
while True:
    it += 1
    cost, H = rc2_opt([full[k] for k in sorted(subset)])
    hm = sum(1 << i for i in H)
    viol = [k for k, (s, d) in enumerate(full) if (masks[k] & hm).bit_count() < d]
    print(json.dumps({'it': it, 'subset': len(subset), 'opt': cost, 'violated_in_full': len(viol), 't': round(time.time() - t0, 1)}), flush=True)
    if cost >= target: break
    if not viol:
        print(json.dumps({'event': 'FULL_OPTIMUM_BELOW_TARGET', 'holes': H})); sys.exit(1)
    rng.shuffle(viol); viol.sort(key=lambda k: len(full[k][0]))
    subset.update(viol[:per])
res = [[list(full[k][0]), full[k][1]] for k in sorted(subset)]
json.dump(res, open(out, 'w'))
print(json.dumps({'event': 'DONE', 'subset': len(res), 'target': target, 'seconds': round(time.time() - t0, 1)}))
