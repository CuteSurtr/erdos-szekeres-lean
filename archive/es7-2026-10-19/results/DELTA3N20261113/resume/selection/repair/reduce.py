#!/usr/bin/env python3
"""Exhaust all induced grounds containing a fixed failing four-point free set.

Uses the C++ min-plus transform once per ground, never all pairs (A,B).
Output is finite-fixture minimality only, not universal order-type minimality.
"""
import itertools
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/selection/repair')
records=json.loads((HERE/'data/fixtures.json').read_text())
src=next(x for x in records if x['name']=='minimum16-n7')
P=src['P']
T=[1,5,6,7]
rest=[i for i in range(len(P)) if i not in T]
cases=[]
for size in range(5,len(rest)+1):
    for extra in itertools.combinations(rest,size):
        ids=sorted(T+list(extra))
        cases.append(ids)
inputpath=SCRATCH/'induced-T.txt'
with inputpath.open('w') as f:
    for idx,ids in enumerate(cases):
        f.write(f'sub{idx} 7 {len(ids)}\n')
        for i in ids: f.write(f'{P[i][0]} {P[i][1]}\n')
outpath=SCRATCH/'induced-T-results.jsonl'
with inputpath.open() as fi, outpath.open('w') as fo:
    subprocess.run([str(SCRATCH/'repair')],stdin=fi,stdout=fo,check=True)
best=None
counts={}
for line in outpath.read_text().splitlines():
    row=json.loads(line)
    idx=int(row['name'][3:]); ids=cases[idx]
    obs=[x for x in row['roots'] if x['max_cost']>=2]
    stats=counts.setdefault(len(ids),{'grounds':0,'obstructed_grounds':0})
    stats['grounds']+=1; stats['obstructed_grounds']+=bool(obs)
    if obs and best is None:
        w=min(obs,key=lambda x:(len(x['A']),x['r']))
        best=dict(n=7,P=[P[i] for i in ids],source=src,source_indices=ids,
                  r=w['r'],A=w['A'],min_cost=w['max_cost'],best_B=w['best_B'],
                  cpp_summary=row)
assert best is not None
(HERE/'data/reduced-n7.json').write_text(json.dumps(best,indent=2)+'\n')
summary=dict(fixed_free_indices=T,counts=counts,smallest_m=len(best['P']),
             input=str(inputpath),output=str(outpath),minimum_scope='induced subsets containing fixed T only')
(HERE/'data/reduction.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
print(json.dumps({k:best[k] for k in ('n','P','source_indices','r','A','min_cost','best_B')}))
