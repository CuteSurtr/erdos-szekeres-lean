#!/usr/bin/env python3
"""Simplify a rightmost projection, or try two infinitesimal old-blue clones.

No numerical realization claim: all accepted geometries are retested in exact
integer arithmetic by repair.cpp and require a separate verify.py run.
"""
import argparse
import itertools as it
import json
import math
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/selection/repair')

def run(cases,tag):
    inp=SCRATCH/f'{tag}.txt';out=SCRATCH/f'{tag}-results.jsonl'
    with inp.open('w') as f:
        for i,case in enumerate(cases):
            f.write(f'case{i} {case["n"]} {len(case["P"])}\n')
            for x,y in case['P']:f.write(f'{x} {y}\n')
    with inp.open() as fi,out.open('w') as fo:
        subprocess.run([str(SCRATCH/'repair')],stdin=fi,stdout=fo,check=True)
    maxcost=-1;best=None;valid=0;hist={}
    for line in out.read_text().splitlines():
        row=json.loads(line)
        if not row['valid']:continue
        valid+=1;w=row['roots'][-1];d=w['max_cost'];hist[d]=hist.get(d,0)+1
        if d>maxcost:
            maxcost=d;best=dict(cases[int(row['name'][4:])],r=w['r'],A=w['A'],best_B=w['best_B'],min_cost=d,cpp_summary=row)
    (HERE/'data'/f'{tag}-best.json').write_text(json.dumps(best,indent=2)+'\n')
    summary=dict(cases=len(cases),valid=valid,max_rightmost_cost=maxcost,hist=hist,input=str(inp),output=str(out))
    (HERE/'data'/f'{tag}.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))

def simple():
    src=json.loads((HERE/'data/reduced-n7.json').read_text());P=src['P'];cases=[]
    for a,b in sorted(it.product(range(-12,13),repeat=2),key=lambda x:abs(x[0])+abs(x[1])):
        if math.gcd(a,b)!=1:continue
        xs=[a*x+b*y for x,y in P]
        if len(set(xs))!=len(P):continue
        order=sorted(range(len(P)),key=lambda i:xs[i])
        Q=[[xs[i],-b*P[i][0]+a*P[i][1]] for i in order]
        cases.append(dict(n=7,P=Q,source_indices=order,projection=[a,b],reflection=1))
    run(cases,'simple-projections')

def clones():
    src=json.loads((HERE/'data/simple-projections-best.json').read_text());P=src['P'];T=set(src['A']+[src['r']])
    blue=[i for i in range(len(P)) if i not in T];cases=[]
    for p,q in it.combinations(blue,2):
        for u,v in it.product((-100,-10,-1,0,1,10,100),repeat=2):
            scale=1000000
            Q=[[x*scale,y*scale] for x,y in P]
            Q.extend([[P[p][0]*scale+1,P[p][1]*scale+u],[P[q][0]*scale+1,P[q][1]*scale+v]])
            Q.sort()
            cases.append(dict(n=8,P=Q,source='simple-projections-best.json',clones=[[p,u],[q,v]],scale=scale))
    run(cases,'two-clones-n8')

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=('simple','clones'));args=parser.parse_args()
    simple() if args.mode=='simple' else clones()
