#!/usr/bin/env python3
"""Exact minimization of the red part of a witnessed real cap star."""
import itertools as it,json
from pathlib import Path
W=Path('/home/jay/research/data/delta3-codex-20261113/resume/pool/maximal')
records=[json.loads(s) for s in (W/'real-search.jsonl').read_text().splitlines()]
o=next(x for x in records if x['status']=='COORDINATE_CANDIDATE')
P=o['P'];R=o['red'];B=[i for i in range(len(P)) if i not in R]
def det(a,b,c):
 return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
def cap(s):return all(det(*q)<0 for q in it.combinations(sorted(s),3))
def convex(s):
 h=[]
 for i in s:
  while len(h)>1 and det(h[-2],h[-1],i)<0:h.pop()
  h.append(i)
 u=[]
 for i in s[::-1]:
  while len(u)>1 and det(u[-2],u[-1],i)<0:u.pop()
  u.append(i)
 return len(h)+len(u)-2==len(s)
assert not any(cap(q) for q in it.combinations(R,4))
targets=[h for h in it.combinations(B,6) if convex(h)]
block={}
for p in B:
 a=bytearray(1<<len(R))
 for q in it.combinations(range(len(R)),3):
  if cap([R[i] for i in q]+[p]):a[sum(1<<i for i in q)]=1
 for s in range(len(a)):
  if a[s]:
   for i in range(len(R)):
    if not s>>i&1:a[s|(1<<i)]=1
 block[p]=a
answer=None
for s in sorted(range(1<<len(R)),key=int.bit_count):
 H=next((h for h in targets if all(block[p][s] for p in h)),None)
 if H is not None:
  Q=[R[i] for i in range(len(R)) if s>>i&1];answer=Q,list(H);break
assert answer
Q,H=answer;S=sorted(Q+H);idx={p:i for i,p in enumerate(S)}
out=dict(label='COMPUTED',kind='real coherent cap-star; not a Delta counterexample',
         m=len(S),n=7,P=[P[i] for i in S],red=[idx[p] for p in Q],
         blue_target=[idx[p] for p in H],source_indices=S,
         source_pool_index=o['pool_index'],
         blockers={str(idx[p]):[idx[x] for x in next(sorted(list(A)+[p]) for A in it.combinations(Q,3) if cap(list(A)+[p]))] for p in H})
(W/'real-star.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
