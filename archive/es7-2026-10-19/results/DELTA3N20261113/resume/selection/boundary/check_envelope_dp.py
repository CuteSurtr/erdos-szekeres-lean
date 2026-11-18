#!/usr/bin/env python3
"""Cross-check endpoint chains against exhaustive subsets and integer hulls."""
from itertools import combinations as C
import hashlib,json,random,resource
from pathlib import Path
from check_envelope import maxima,det,HERE
from check_models import hull
resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
resource.setrlimit(resource.RLIMIT_CPU,(18,18))
rng=random.Random(20261114);counts={}
for m in range(2,9):
 for trial in range(40):
  while True:
   P=[(i,rng.randrange(-1000,1001)) for i in range(m)]
   if all(det(P,*t) for t in C(range(m),3)):break
  expected=[2,2,2]
  for k in range(3,m+1):
   for S in C(range(m),k):
    ds=[det(P,*t) for t in C(S,3)]
    if all(x<0 for x in ds):expected[0]=k
    if all(x>0 for x in ds):expected[1]=k
    if len(hull(P,S))==k:expected[2]=k
  assert tuple(expected)==maxima(P,range(m)),(P,expected,maxima(P,range(m)))
 counts[m]=40
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
record={'label':'COMPUTED exact cross-check','status':'PASS','seed':20261114,
        'cases_by_size':counts,'cases':sum(counts.values()),
        'sources':{str(p.relative_to(HERE)):sha(p) for p in [Path(__file__),HERE/'check_envelope.py',HERE/'check_models.py']}}
(HERE/'data/envelope_dp_controls.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS','cases':record['cases']}))
