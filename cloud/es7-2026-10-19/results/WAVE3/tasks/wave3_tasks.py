#!/usr/bin/env python3
"""Write results/WAVE3/tasks/G*.json from a gfrontier JSON. usage: wave3_tasks.py GF.json S_LISTS.json OUTDIR
Cases handled elsewhere (U3_L, U_L8, U4_L by F1-F7; S-list cases by S1-S5) are excluded. A case split over
several agents is split by position (p mod k) in the sorted open list. Prints the plan with a cost estimate."""
import json, sys, os
gf = json.load(open(sys.argv[1])); S = json.load(open(sys.argv[2])); out = sys.argv[3]
skip = {'U3_L', 'U_L8', 'U4_L', 'U7_L'} | set(sum(S.values(), []))
openc = {c: v['open'] for c, v in gf.items() if v['open'] and c not in skip}
def cost(cubes):  # core-seconds, rough: depth-7 top 150 s, deeper 20 s, whole case 3600 s
    return sum(3600 if len(c) == 0 else 150 if len(c) <= 7 else 20 for c in cubes)
# big cases: own agent(s); the rest packed greedily
plan = {}
big = sorted(openc, key=lambda c: -cost(openc[c]))
agents = []
for c in big:
    import math
    k = min(3, max(1, math.ceil(cost(openc[c]) / (1.0 * 3600 * 4))))   # ~1 h estimated per agent: splits usually double or triple the work
    if cost(openc[c]) >= 0.6 * 3600 * 4:
        for i in range(k):
            agents.append({c: openc[c][i::k]})
        del openc[c]
rest = sorted(openc, key=lambda c: -cost(openc[c]))
bins = []
for c in rest:
    for b in bins:
        if sum(cost(v) for v in b.values()) + cost(openc[c]) <= 1.5 * 3600 * 4:
            b[c] = openc[c]; break
    else:
        bins.append({c: openc[c]})
agents += bins
os.makedirs(out, exist_ok=True)
for i, a in enumerate(agents, 1):
    name = f'G{i}'
    json.dump(a, open(os.path.join(out, f'{name}.json'), 'w'))
    summ = '; '.join(f"{c}: {len(v)} cube{'s' if len(v) != 1 else ''}" + (' (whole case)' if v == [[]] else '') for c, v in a.items())
    plan[name] = summ
    print(name, f"est {sum(cost(v) for v in a.values())/14400:.2f} VM-h |", summ)
json.dump(plan, open(os.path.join(out, 'plan.json'), 'w'), indent=1)
