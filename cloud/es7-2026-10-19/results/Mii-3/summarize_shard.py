#!/usr/bin/env python3
"""Summarize leaves.jsonl of the Mii-3 shard.  usage: summarize_shard.py <leaves.jsonl> <cubes.icnf>
Closed weight uses 2^-len(cube) (cubes form a binary partition: checked for the top-level file
and for every split by shard_driver.check_partition); shard weight is 16/128 of the instance."""
import sys, json, collections
from fractions import Fraction as F
recs = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
top = [[int(x) for x in l.split()[1:-1]] for i, l in enumerate(open(sys.argv[2])) if i % 8 == 3]
done = {tuple(r['cube']): r for r in recs}
pend = {tuple(c) for c in top}
for r in recs:
    if r['status'] == 'SPLIT': pend |= {tuple(c) for c in r['children'] + r['gap_children']}
openc = sorted(pend - set(done))
st = collections.Counter(r['status'] for r in recs)
uns = [r for r in recs if r['status'] == 'UNSAT']
cw = sum((F(1, 2 ** len(r['cube'])) for r in uns), F(0))
ow = sum((F(1, 2 ** len(c)) for c in openc), F(0))
shard_w = F(16, 128)
gaps = sum(len(r['gap_children']) for r in recs if r['status'] == 'SPLIT')
print(json.dumps({"records": len(recs), "status": dict(st), "unsat_lrat_verified": sum(r['lrat'] == 'VERIFIED' for r in uns),
  "unsat_lrat_other": sum(r['lrat'] != 'VERIFIED' for r in uns), "sat": st.get('SAT', 0), "open_leaves": len(openc),
  "open_by_depth": dict(collections.Counter(len(c) for c in openc)), "split_gap_children_total": gaps,
  "closed_weight_of_shard": float(cw / shard_w), "open_weight_of_shard": float(ow / shard_w),
  "closed_plus_open_equals_shard": cw + ow == shard_w,
  "unsat_solve_s_total": round(sum(r['solve_s'] for r in uns), 1),
  "unsat_solve_s_max": max((r['solve_s'] for r in uns), default=0),
  "lrat_check_s_total": round(sum(r['lrat_check_s'] for r in uns), 1),
  "top_cubes_closed": sum(1 for c in top if tuple(c) in done and done[tuple(c)]['status'] == 'UNSAT')}, indent=1))
