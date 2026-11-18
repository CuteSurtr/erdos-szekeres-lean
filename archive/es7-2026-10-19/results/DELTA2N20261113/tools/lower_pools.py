"""Lower-chain form on further real pools of ETVTHY20261113 (general a): usage lower_pools.py a n poolfile.jsonl"""
import sys, json, time
from lower_lib import lower_delta, Analysis
import pyexact_etvthy as px
a, n, fn = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
cnt = ok = skipped = 0; t0 = time.time(); sizes = []
for line in open(fn):
    P = sorted(tuple(p) for p in json.loads(line)['P']); A = Analysis(P)
    if max(A.cap_end) > a - 1 or A.gon() > n - 1: skipped += 1; continue
    st, D, rounds = lower_delta(P, n, a - 1, A); cnt += 1; sizes.append(len(P))
    if st == 'OK':
        sub = [P[i] for i in D]
        if len(sub) >= 2:
            _, _, cb, _ = px.chains(sub); assert max(cb.values()) <= a - 2
        ok += 1
    else: print('FAIL', st, fn.split('/')[-1], cnt, len(P), 'points', flush=True)
print('%s (a=%d, n=%d): %d valid sets with %d-%d points (%d skipped as not valid for these parameters), lower-chain Delta exists in %d; %.0fs' % (fn.split('/')[-1], a, n, cnt, min(sizes or [0]), max(sizes or [0]), skipped, ok, time.time() - t0), flush=True)
