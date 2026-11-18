#!/usr/bin/env python3
"""Seeded finite subset tests of the existing real ETV42 n8 fixture."""
import json
import random
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/selection/repair')
source=HERE.parents[2]/'search/fixtures.json'
P=json.loads(source.read_text())['etv42']['P']
rng=random.Random(14072026)
cases=[]
for i in range(400):
    ids=sorted(rng.sample(range(len(P)),16))
    cases.append(dict(n=8,P=[P[k] for k in ids],source_indices=ids))
inp=SCRATCH/'samples8.txt';out=SCRATCH/'samples8-results.jsonl'
with inp.open('w') as f:
    for i,case in enumerate(cases):
        f.write(f'etv{i} 8 16\n')
        for x,y in case['P']:f.write(f'{x} {y}\n')
with inp.open() as fi,out.open('w') as fo:
    subprocess.run([str(SCRATCH/'repair')],stdin=fi,stdout=fo,check=True)
hist={};valid=0;best=None;maxcost=-1;rightmost=-1
for line in out.read_text().splitlines():
    row=json.loads(line)
    if not row['valid']:continue
    valid+=1
    w=max(row['roots'],key=lambda x:x['max_cost']);d=w['max_cost']
    rightmost=max(rightmost,row['roots'][-1]['max_cost'])
    hist[d]=hist.get(d,0)+1
    if d>maxcost:
        maxcost=d
        best=dict(cases[int(row['name'][3:])],r=w['r'],A=w['A'],best_B=w['best_B'],min_cost=d,cpp_summary=row)
(HERE/'data/sample8-best.json').write_text(json.dumps(best,indent=2)+'\n')
summary=dict(cases=len(cases),valid=valid,max_cost=maxcost,max_rightmost_cost=rightmost,hist=hist,
             seed=14072026,input=str(inp),output=str(out),scope='HEURISTIC coverage, exact finite enumeration on each sample')
(HERE/'data/sample8.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
