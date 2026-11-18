"""Exact real-point controls, independent of the original encoders.
Endpoint-chain DP adapted from the prior independent real_geometry.py; only
N66 row and mirror/SB checks are retained (no residual-encoder imports).
"""
import hashlib
import itertools as it
import json
import pathlib
import random
from model import D, HERE, S, tau

def det(a,b,c):
    return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])

def geometry(points):
    p=sorted(points); n=len(p)
    assert len({q[0] for q in p})==n
    signs={q:det(*(p[i] for i in q)) for q in it.combinations(range(n),3)}
    assert all(signs.values())
    ending=[{},{}]
    for t in (0,1):
        for j in range(n):
            for i in range(j):
                ending[t][i,j]=max([2]+[ending[t][k,i]+1 for k in range(i)
                                         if (signs[k,i,j]>0)==bool(t)])
    cap=max(ending[0].values(),default=1);cup=max(ending[1].values(),default=1)
    polygon=0
    for a in range(n):
        best=[]
        for t in (0,1):
            dp={(a,j):2 for j in range(a+1,n)}
            for j in range(a+1,n):
                for i in range(a+1,j):
                    cand=[dp[k,i]+1 for k in range(a,i) if (k,i) in dp and
                          (signs[k,i,j]>0)==bool(t)]
                    if cand: dp[i,j]=max(cand)
            best.append({j:max([0]+[v for (i,k),v in dp.items() if k==j])
                         for j in range(a+1,n)})
        polygon=max([polygon]+[best[0][j]+best[1][j]-2 for j in range(a+1,n)])
    assert cap<=5 and cup<=5 and polygon<=7
    index={s:i for i,s in enumerate(S)}; owners=[]
    for j in range(n):
        labels=[(ending[0][i,j]-1,ending[1][i,j]-1) for i in range(j)]
        profile=tuple(max([0]+[b for a,b in labels if a>=column]) for column in range(1,5))
        owners.append(index[profile])
    assert len(set(owners))==n and owners[:2]==[0,1]
    return owners, {'points':n,'cap':cap,'cup':cup,'polygon':polygon}

def main():
    source=pathlib.Path('/home/jay/research/data/verify-N66-20261113/etvsets.txt')
    fixtures=[]
    for raw in source.read_text().splitlines():
        values=list(map(int,raw.split())); points=list(zip(values[1::2],values[2::2]))
        assert len(points)==values[0]; fixtures.append(points)
    rng=random.Random(566775)
    samples=fixtures+[rng.sample(p,k) for p in fixtures for k in (8,16,24)]
    rows=[(set(s),d) for s,d in json.loads((D/'used_rows.json').read_text())]
    pairs=json.loads((D/'layout.json').read_text())['sb_pairs']
    coverage=set(); rowchecks=0; tight=0; details=[]; sb_clauses_checked=0
    for points in samples:
        owners,stats=geometry(points)
        reflected,mirrorstats=geometry([(x,-y) for x,y in points])
        assert reflected==[tau[s] for s in owners]
        for occ in (set(owners),set(reflected)):
            coverage.update(occ)
            for support,d in rows:
                holes=len(support-occ)
                assert holes>=d
                tight+=holes==d;rowchecks+=1
        original=set(owners);mirror=set(reflected)
        def lex(occ):
            return next((a not in occ for a,b in pairs if (a in occ)!=(b in occ)),True)
        assert lex(original) or lex(mirror)
        chosen=original if lex(original) else mirror
        equalprefix=True
        for j,(a,b) in enumerate(pairs):
            x,y=a in chosen,b in chosen
            assert not equalprefix or not x or y;sb_clauses_checked+=1
            if j<len(pairs)-1:
                e=equalprefix and x==y
                assert not equalprefix or not x or not y or e
                assert not equalprefix or x or y or e
                sb_clauses_checked+=2;equalprefix=e
        details.append({**stats,'mirror_cap':mirrorstats['cap'],'mirror_cup':mirrorstats['cup'],
                        'chosen_original':lex(original),'holes':70-len(owners)})
    result={'label':'COMPUTED','result':'ZERO VIOLATIONS','sets_including_reflections':2*len(samples),
            'row_evaluations':rowchecks,'tight_rows':tight,'states_seen':len(coverage),
            'full_sb_clause_evaluations':sb_clauses_checked,'details':details,
            'fixture_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
            'limitation':'These real sets have at least 20 holes; the budget-13 counter is not a positive control.'}
    (HERE/'data/real.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    main()
