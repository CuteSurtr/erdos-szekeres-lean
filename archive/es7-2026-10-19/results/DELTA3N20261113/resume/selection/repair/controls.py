#!/usr/bin/env python3
"""Frozen-witness checks only: 0-1 BFS, root-selected positives, clause controls."""
import collections
import itertools as it
import json
from pathlib import Path
from verify import geometry,ids,mask,cnf

HERE=Path(__file__).resolve().parent

def satisfies(B,path):
    for line in path.read_text().splitlines():
        if not line or line[0] in 'cp':continue
        C=list(map(int,line.split()))[:-1]
        if not any(bool(B>>(abs(v)-1)&1)==(v>0) for v in C):return False
    return True

def frozen(tag,source):
    d=json.loads((HERE/'data'/f'{tag}-audit.json').read_text())
    s=json.loads((HERE/'data'/source).read_text())
    m=d['m'];N=1<<m;allpoints=N-1;r=d['r'];T=mask(d['A']+[r])
    caps=list(map(mask,d['fourcaps']));targets=list(map(mask,d['targets']))
    free=[not any(B&K==K for K in caps) for B in range(N)]
    targetfree=[not any(B&H==H for H in targets) for B in range(N)]
    full=[B for B in range(N) if free[B] and targetfree[allpoints^B]]
    assert len(full)==d['full_deltas']
    dist=[100]*N;q=collections.deque(full)
    for B in full:dist[B]=0
    while q:
        B=q.popleft();v=dist[B]
        for i in range(m):
            C=B^(1<<i);cost=bool(B>>i&1)
            if dist[C]>v+cost:
                dist[C]=v+cost
                if cost:q.append(C)
                else:q.appendleft(C)
    total_old=0
    for row in s['cpp_summary']['roots']:
        j=row['r'];hist=collections.Counter()
        for A in range(N):
            if not A>>j&1 and free[A] and targetfree[allpoints^(A|(1<<j))]:hist[str(dist[A|(1<<j)])]+=1
        assert dict(hist)==row['hist'],(tag,j,hist,row['hist'])
        total_old+=sum(hist.values())
    rootfull=[B for B in full if B>>r&1]
    key=lambda B:((B&~T).bit_count(),B.bit_count(),B)
    ordinary=min(full,key=key);rooted=min(rootfull,key=key)
    assert (ordinary&~T).bit_count()==(rooted&~T).bit_count()==2
    for kind,B in [('ordinary',ordinary),('r_selected',rooted)]:
        assert satisfies(B,HERE/'data'/f'{tag}-two.cnf')
        assert not satisfies(B,HERE/'data'/f'{tag}-one.cnf')
        (HERE/'data'/f'{tag}-{kind}.model').write_text('v '+' '.join(str(i+1 if B>>i&1 else -(i+1)) for i in range(m))+' 0\n')
    return dict(tag=tag,full_deltas=len(full),r_selected_deltas=len(rootfull),
                ordinary=dict(B=ids(ordinary),new_old_blue=ids(ordinary&~T),cost=2),
                r_selected=dict(B=ids(rooted),new_old_blue=ids(rooted&~T),cost=2),
                bfs_all_roots_all_old_deltas='PASS',root_old_delta_pairs_checked=total_old)

out=dict(label='COMPUTED',frozen=[frozen('rightmost-n7','rotation-best.json'),frozen('rightmost-n8','two-clones-n8-best.json')],positive_one_blue=[])
old=HERE.parents[1]/'weak_theory/findings.json'
for obj in json.loads(old.read_text())['obstructions']:
    P=obj['P'];n=obj['n'];r=obj['r'];A=mask(obj['A']);T=A|(1<<r)
    caps,fives,targets,ngons=geometry(P,n);assert not fives and not ngons
    assert all(A&H for H in targets if not H>>r&1)
    # Check the previously recorded deletion-only obstruction exactly.
    local=T;zero_works=False
    while True:
        zero_works |= not any(local&K==K for K in caps) and all(local&H for H in targets)
        if local==0:break
        local=(local-1)&T
    assert not zero_works
    B=1;assert not B&T and all(B&H for H in targets)
    name=f'positive-n{n}-one.cnf';blue=[i for i in range(len(P)) if not T>>i&1]
    clauses,sha=cnf(HERE/'data'/name,len(P),caps,targets,blue,1)
    assert satisfies(B,HERE/'data'/name)
    control=dict(n=n,P=P,r=r,A=obj['A'],full_delta=[0],min_cost=1,cnf=name,sha256=sha,clauses=len(clauses))
    (HERE/'data'/f'positive-n{n}.json').write_text(json.dumps(control,indent=2)+'\n')
    (HERE/'data'/f'positive-n{n}-one.model').write_text('v '+' '.join(str(i+1 if B>>i&1 else -(i+1)) for i in range(len(P)))+' 0\n')
    out['positive_one_blue'].append({k:control[k] for k in ('n','r','A','full_delta','min_cost','cnf','sha256','clauses')})
# An intentionally invalid five-cap is detected, rather than admitted.
bad=[[-1,-20],[0,0],[1,10],[2,18],[3,24]]
assert geometry(bad,7)[1]==[31]
out['invalid_fivecap_control']='PASS: rejected by exact predicate'
(HERE/'data/controls.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
