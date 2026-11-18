#!/usr/bin/env python3
"""Exact rational projection representatives; keep every outcome."""
import itertools
import json
import math
import subprocess
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/selection/repair')
src=json.loads((HERE/'data/reduced-n7.json').read_text())
P=src['P']
# Rational test directions on both sides of each pair-tie direction.
# Adding epsilon*(dx,dy) moves across the tie without float arithmetic.
# Epsilon denominator exceeds every determinant scale, so no other tie
# direction is crossed unless it coincides. Duplicate orders are collapsed.
scale=10**10
directions={(1,0),(0,1),(-1,0),(0,-1)}
for p,q in itertools.combinations(P,2):
    dx,dy=q[0]-p[0],q[1]-p[1]
    g=math.gcd(dx,dy); dx//=g;dy//=g
    # Moderately sized integer perturbations suffice for search; no claim
    # that every angular cell is represented unless independently checked.
    for sign in (-1,1):
        for side in (-1,1): directions.add((sign*(-dy*1000+side*dx),sign*(dx*1000+side*dy)))
cases=[]; seen=set()
for a,b in sorted(directions):
    projection=[a*x+b*y for x,y in P]
    if len(set(projection))<len(P): continue
    order=sorted(range(len(P)),key=lambda i:projection[i])
    for reflection in (-1,1):
        sig=(tuple(order),reflection)
        if sig in seen: continue
        seen.add(sig)
        Q=[[projection[i],reflection*(-b*P[i][0]+a*P[i][1])] for i in order]
        if max(abs(v) for p in Q for v in p)>10**15: continue
        cases.append(dict(n=7,P=Q,source_indices=order,projection=[a,b],reflection=reflection))
inp=SCRATCH/'rotations.txt'; out=SCRATCH/'rotations-results.jsonl'
with inp.open('w') as f:
    for i,case in enumerate(cases):
        f.write(f'rot{i} 7 {len(P)}\n')
        for x,y in case['P']: f.write(f'{x} {y}\n')
with inp.open() as fi,out.open('w') as fo:
    subprocess.run([str(SCRATCH/'repair')],stdin=fi,stdout=fo,check=True)
valid=0; maximum=-1; best=None
for line in out.read_text().splitlines():
    row=json.loads(line)
    if not row['valid']:continue
    valid+=1
    w=row['roots'][-1]
    if w['max_cost']>maximum:
        maximum=w['max_cost']
        best=dict(cases[int(row['name'][3:])],r=w['r'],A=w['A'],best_B=w['best_B'],min_cost=w['max_cost'],cpp_summary=row)
(HERE/'data/rotation-best.json').write_text(json.dumps(best,indent=2)+'\n')
summary=dict(cases=len(cases),valid=valid,max_rightmost_cost=maximum,input=str(inp),output=str(out),
             projection_scope='finite rational direction sample; no exhaustive direction claim')
(HERE/'data/rotations.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
