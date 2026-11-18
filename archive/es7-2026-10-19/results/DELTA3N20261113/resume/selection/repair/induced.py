#!/usr/bin/env python3
"""Bounded induced-ground check with the same fixed four-point free set."""
import argparse
import itertools as it
import json
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/selection/repair')
parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('tag');args=parser.parse_args()
src=json.loads(Path(args.source).read_text());P=src['P'];n=src['n'];T=sorted(src['A']+[src['r']]);other=[i for i in range(len(P)) if i not in T]
cases=[]
for size in range(max(0,n+3-len(T)),len(other)+1):
    for extra in it.combinations(other,size):cases.append(sorted(T+list(extra)))
inp=SCRATCH/f'{args.tag}-induced.txt';out=SCRATCH/f'{args.tag}-induced-results.jsonl'
with inp.open('w') as f:
    for i,ground in enumerate(cases):
        f.write(f'ground{i} {n} {len(ground)}\n')
        for j in ground:f.write(f'{P[j][0]} {P[j][1]}\n')
with inp.open() as fi,out.open('w') as fo:subprocess.run([str(SCRATCH/'repair')],stdin=fi,stdout=fo,check=True)
counts={};minimum=None;best=None
for line in out.read_text().splitlines():
    row=json.loads(line);assert row['valid']
    ground=cases[int(row['name'][6:])];w=row['roots'][-1];d=w['max_cost'];m=row['m']
    stat=counts.setdefault(m,dict(grounds=0,rightmost_obstructed=0));stat['grounds']+=1;stat['rightmost_obstructed']+=d>1
    if d>1 and minimum is None:
        minimum=m;best=dict(n=n,P=[P[j] for j in ground],r=w['r'],A=w['A'],best_B=w['best_B'],min_cost=d,source_indices=ground)
result=dict(n=n,fixed_free_set=T,counts=counts,smallest_rightmost_m=minimum,
            scope='all induced grounds containing the fixed four points, all old Deltas at rightmost root; not universal minimality',input=str(inp),output=str(out))
(HERE/'data'/f'{args.tag}-induced.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'data'/f'{args.tag}-induced-best.json').write_text(json.dumps(best,indent=2)+'\n')
print(json.dumps(result))
