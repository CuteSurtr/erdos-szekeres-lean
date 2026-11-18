"""Per-state realizability over all pools (in-states; plus out-states and transposes as separate tallies)."""
import sys, json, glob
import fl
from fl import *
cnt_in = [0] * N; cnt_any = [0] * N; nsets = 0
for fn in sorted(glob.glob('pool_*.jsonl')) + sorted(glob.glob('sets_*.jsonl')):
    for rec in load_jsonl(fn):
        P = [tuple(p) for p in rec['P']]
        S = Set66(P)
        if not S.ok: continue
        nsets += 1
        for i in set(S.in_state): cnt_in[i] += 1; cnt_any[i] += 1; cnt_any[TR[i]] += 1
        for i in set(S.out_state): cnt_any[i] += 1; cnt_any[TR[i]] += 1
print('sets', nsets)
never = [i for i in range(N) if cnt_any[i] == 0]
print('never occupied (any symmetry image):', [''.join(map(str, STATES[i])) for i in never])
print('never occupied as in-state:', [''.join(map(str, STATES[i])) for i in range(N) if cnt_in[i] == 0])
six = [SINDEX[f] for f in [(4,1,1,1),(4,2,1,1),(4,2,2,1),(4,3,1,1),(4,3,2,1),(4,3,3,1)]]
print('the six common holes: counts', [(''.join(map(str, STATES[i])), cnt_in[i], cnt_any[i]) for i in six])
