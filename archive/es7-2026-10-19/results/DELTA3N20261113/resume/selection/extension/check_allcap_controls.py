#!/usr/bin/env python3
"""Parent exact replay using only coordinates and proposed selections."""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import resource
import time

resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20))
E=Path(__file__).resolve().parent
source=E/'low_split/consequences/data/all_cap_controls.json'
data=json.loads(source.read_text())
results=[]
start=time.monotonic()
for name,case in data['cases'].items():
    pts=case['points'];m=len(pts);n=case['n'];cut=case['cut']
    def det(i,j,k):
        a,b,c=pts[i],pts[j],pts[k]
        return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    signs={t:det(*t) for t in combinations(range(m),3)}
    assert all(signs.values())
    assert all(pts[i][0]<pts[i+1][0] for i in range(m-1))
    assert all(v<0 for (a,b,c),v in signs.items() if a<cut<=c)
    def cap(q):return all(signs[t]<0 for t in combinations(q,3))
    def convex(q):
        if len(q)<3:return True
        chains=[]
        for seq in [q,tuple(reversed(q))]:
            h=[]
            for i in seq:
                while len(h)>1 and det(h[-2],h[-1],i)<=0:h.pop()
                h.append(i)
            chains.append(h)
        return len(chains[0])+len(chains[1])-2==len(q)
    four=[q for q in combinations(range(m),4) if cap(q)]
    assert len(four)==case['caps4']
    assert not any(cap(q) for q in combinations(range(m),5))
    assert not any(convex(q) for q in combinations(range(m),n))
    targets=[q for q in combinations(range(m),n-1) if convex(q)]
    assert len(targets)==case['targets']
    ends={q[-2:] for q in four}
    counts=[]
    for sel in case['selections']:
        A=tuple(sel['A']);assert list(A)==sorted(set(A)) and all(0<=i<m for i in A)
        assert not any(set(q)<=set(A) for q in four)
        assert all(set(q)&set(A) for q in targets)
        triples=[q for q in combinations(A,3) if cap(q)]
        assert all(q[-2:] in ends for q in triples)
        assert len(triples)==sel['selected_cap_triples']
        if cut>=2 and m-cut>=2:
            assert set(range(cut,m))<=set(A) and len(set(A)&set(range(cut)))==1
        counts.append({'A':A,'selected_cap_triples':len(triples)})
    results.append({'case':name,'m':m,'n':n,'cut':cut,'caps4':len(four),
                    'targets':len(targets),'selections':counts})
out={'label':'COMPUTED exact parent control replay','status':'PASS','cases':results,
     'total_selections':sum(len(r['selections']) for r in results),
     'seconds':time.monotonic()-start,
     'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
     'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
     'scope':'These24 coordinate controls only; the general all-cap lemma has a separate written proof.'}
(E/'data/all-cap-parent-controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','total_selections','seconds','input_sha256']}))
