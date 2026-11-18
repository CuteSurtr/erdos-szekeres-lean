#!/usr/bin/env python3
"""Extract a small coherent cap-star from a fixed abstract SAT witness."""
import itertools as it,json
from pathlib import Path
W=Path('/home/jay/research/data/delta3-codex-20261113/resume/pool/maximal')
o=json.loads((W/'n7m16.geometry.json').read_text());m=o['m'];n=o['n']
t=dict(zip(it.combinations(range(m),3),(s=='+' for s in o['signs'])))
values={}
for line in (W/'n7m16.solver.out').read_text().splitlines():
 if line.startswith('v '):
  for x in map(int,line.split()[1:]):
   if x:values[abs(x)]=x>0
R=[i for i in range(m) if values[len(t)+1+i]]
def cap(s):return all(not t[q] for q in it.combinations(s,3))
def convex(s):return all(t[a,b,c]==t[a,b,d] and t[a,c,d]==t[b,c,d] for a,b,c,d in it.combinations(s,4))
assert not any(cap(s) for s in it.combinations(R,4))
assert all(any(cap(tuple(sorted(s+(p,)))) for s in it.combinations(R,3)) for p in range(m) if p not in R)
best=None
for H in it.combinations([i for i in range(m) if i not in R],n-1):
 if not convex(H):continue
 for k in range(3,len(R)+1):
  if best is not None and k>=len(best[0]):break
  found=False
  for Q in it.combinations(R,k):
   if all(any(cap(tuple(sorted(A+(p,)))) for A in it.combinations(Q,3)) for p in H):
    best=(Q,H);found=True;break
  if found:break
assert best is not None
Q,H=best;S=sorted(Q+H);idx={p:i for i,p in enumerate(S)}
result=dict(label='COMPUTED',kind='coherent cap-star, not a Delta counterexample',m=len(S),n=n,
            signs=''.join('+' if t[tuple(S[i] for i in q)] else '-' for q in it.combinations(range(len(S)),3)),
            red=[idx[p] for p in Q],blue_target=[idx[p] for p in H],source_indices=S,
            source_red=R,blockers={str(idx[p]):[idx[x] for x in next(tuple(sorted(A+(p,))) for A in it.combinations(Q,3) if cap(tuple(sorted(A+(p,)))))] for p in H})
(W/'star.geometry.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
