#!/usr/bin/env python3
"""Independent exact Python geometry, full-subset audit and coloring CNFs.

Does not import the finder or use its min-plus transform. Polygon tests use
supporting edges; caps require every triple to be negative. For the one
specified old Delta, all B are scanned once. No SAT solver is invoked.
"""
import argparse
import hashlib
import itertools as it
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent

def det(P,a,b,c):
    x,y=P[a];u,v=P[b];s,t=P[c]
    return (u-x)*(t-y)-(v-y)*(s-x)

def mask(xs):return sum(1<<x for x in xs)
def ids(x):return [i for i in range(x.bit_length()) if x>>i&1]

def geometry(P,n):
    m=len(P)
    assert all(isinstance(x,int) for p in P for x in p)
    assert all(P[i][0]<P[i+1][0] for i in range(m-1))
    signs={C:(1 if det(P,*C)>0 else -1 if det(P,*C)<0 else 0) for C in it.combinations(range(m),3)}
    assert all(signs.values()), 'collinear triple'
    def sgn(a,b,c):
        C=(a,b,c); parity=sum(C[i]>C[j] for i in range(3) for j in range(i+1,3))
        return signs[tuple(sorted(C))]*(-1 if parity%2 else 1)
    def cap(C):return all(signs[T]<0 for T in it.combinations(C,3))
    def convex(C):
        # A point is a hull vertex iff it belongs to a supporting edge.
        # General position makes both implications exact (no edge interiors).
        exposed=set()
        for a,b in it.combinations(C,2):
            sides={sgn(a,b,c) for c in C if c!=a and c!=b}
            if len(sides)==1:exposed.update((a,b))
        return len(exposed)==len(C)
    caps=[mask(C) for C in it.combinations(range(m),4) if cap(C)]
    fives=[mask(C) for C in it.combinations(range(m),5) if cap(C)]
    targets=[mask(C) for C in it.combinations(range(m),n-1) if convex(C)]
    ngons=[mask(C) for C in it.combinations(range(m),n) if convex(C)]
    return caps,fives,targets,ngons

def cnf(path,m,caps,targets,blue,budget):
    clauses=[[-(i+1) for i in ids(K)] for K in caps]
    clauses.extend([[i+1 for i in ids(H)] for H in targets])
    clauses.extend([[-(i+1) for i in C] for C in it.combinations(blue,budget+1)])
    with path.open('w') as f:
        f.write('c v_i selects zero-based point i-1; both colors of r allowed\n')
        f.write(f'c old-blue addition budget {budget}\n')
        f.write(f'p cnf {m} {len(clauses)}\n')
        for C in clauses:f.write(' '.join(map(str,C))+' 0\n')
    return clauses,hashlib.sha256(path.read_bytes()).hexdigest()

def audit(w,name):
    P=w['P'];n=w['n'];m=len(P);r=w['r'];A=mask(w['A']);T=A|(1<<r)
    assert not A>>r&1
    caps,fives,targets,ngons=geometry(P,n)
    assert not fives and not ngons
    assert not any(A&K==K for K in caps)
    oldtargets=[H for H in targets if not H>>r&1]
    assert all(A&H for H in oldtargets)
    costs={};best=None;full=[]
    for B in range(1<<m):
        if any(B&K==K for K in caps) or any(not B&H for H in targets):continue
        full.append(B);d=(B&~T).bit_count();costs[d]=costs.get(d,0)+1
        if best is None or (d,B.bit_count(),B)<((best&~T).bit_count(),best.bit_count(),best):best=B
    assert best is not None
    minimum=min(costs)
    if 'min_cost' in w:assert minimum==w['min_cost']
    blue=[i for i in range(m) if not T>>i&1]
    clauses,sha=cnf(HERE/'data'/f'{name}-one.cnf',m,caps,targets,blue,1)
    control,controlsha=cnf(HERE/'data'/f'{name}-two.cnf',m,caps,targets,blue,2)
    def satisfies(B,Cs):return all(any(bool(B>>(abs(v)-1)&1)==(v>0) for v in C) for C in Cs)
    assert satisfies(best,control)
    assert sum(satisfies(B,clauses) for B in full)==sum(v for k,v in costs.items() if k<=1)
    branches=[]
    for q in [None]+blue:
        allowed=T|(0 if q is None else 1<<q)
        local=[]
        B=allowed
        while True:
            if not any(B&K==K for K in caps):local.append(B)
            if B==0:break
            B=(B-1)&allowed
        maximal=[B for B in local if not any(B!=C and B&C==B for C in local)]
        cert=[]
        for B in maximal:
            missed=next((H for H in targets if not H&B),None)
            if minimum>1:assert missed is not None
            cert.append(dict(B=ids(B),missed=ids(missed) if missed else None))
        traces=sorted({H&allowed for H in targets},key=lambda v:(v.bit_count(),v))
        minimal=[]
        for H in traces:
            if not any(G&H==G for G in minimal):minimal.append(H)
        branches.append(dict(new_old_blue=q,maximal_capfree=cert,minimal_target_traces=[ids(H) for H in minimal]))
    data=dict(label='COMPUTED',n=n,m=m,P=P,r=r,rightmost=(r==m-1),A=ids(A),
              min_cost=minimum,best_B=ids(best),new_old_blue=ids(best&~T),
              full_delta_cost_histogram=costs,full_deltas=len(full),
              fourcaps=[ids(K) for K in caps],fivecaps=[],targets=[ids(H) for H in targets],ngons=[],
              old_targets=len(oldtargets),old_delta=True,branches=branches,
              cnf=dict(file=f'{name}-one.cnf',variables=m,clauses=len(clauses),sha256=sha,
                       state='UNSOLVED; exact enumeration has no model if min_cost>1; parent certification requested'),
              two_control=dict(file=f'{name}-two.cnf',variables=m,clauses=len(control),sha256=controlsha,model=ids(best)))
    target=HERE/'data'/f'{name}-audit.json';target.write_text(json.dumps(data,indent=2)+'\n')
    (HERE/'data'/f'{name}-two.model').write_text('v '+' '.join(str(i+1 if best>>i&1 else -(i+1)) for i in range(m))+' 0\n')
    print(json.dumps({k:data[k] for k in ('label','n','m','r','rightmost','A','min_cost','best_B','new_old_blue','full_deltas','old_targets','cnf')}))
    return data

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('source');parser.add_argument('name');args=parser.parse_args()
    audit(json.loads(Path(args.source).read_text()),args.name)
