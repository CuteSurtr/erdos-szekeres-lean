#!/usr/bin/env python3
"""Small exhaustive checks against the old encoder and direct 4-subset semantics.
Run with the specified Python, -B, OMP/BLAS threads=1, and timeout 18s.
Does not run a frontier solve. Writes only to the assigned scratch encoder/.
"""
import itertools as it
import json
import os
from pathlib import Path
import subprocess
import sys
import time

for key in ('OMP_NUM_THREADS', 'OPENBLAS_NUM_THREADS', 'MKL_NUM_THREADS'):
    os.environ[key] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from pysat.solvers import Glucose4

HERE = Path(__file__).resolve().parent
OLD = HERE.parents[1] / 'DELTA2N20261113' / 'tools'
WORK = Path('/home/jay/research/data/delta3-codex-20261113/encoder')
sys.path.insert(0, str(OLD))
import upper_exact
from eager_cert import Enc


def configurations(m):
    ts = list(it.combinations(range(m),3))
    ids = {t:i+1 for i,t in enumerate(ts)}
    clauses = []
    for q in it.combinations(range(m),4):
        v = [ids[t] for t in it.combinations(q,3)]
        for a,b,c in it.combinations(v,3):
            clauses += [[-a,b,-c], [a,-b,c]]
    with Glucose4(bootstrap_with=clauses) as solver:
        answer = []
        while solver.solve():
            val = {abs(x):x>0 for x in solver.get_model()}
            signs = [i if val[i] else -i for i in range(1,len(ts)+1)]
            answer.append((signs, {t:val[i] for t,i in ids.items()}))
            solver.add_clause([-x for x in signs])
    assert len(answer) == {4:8,5:62,6:908}[m]
    return answer


def direct(t,m,n,mode):
    full=(1<<m)-1
    def cap(s):
        return all(not t[q] for q in it.combinations(s,3))
    def convex(s):
        return all(t[a,b,c]==t[a,b,d] and t[a,c,d]==t[b,c,d]
                   for a,b,c,d in it.combinations(s,4))
    mask=lambda s:sum(1<<x for x in s)
    valid = (not any(cap(s) for s in it.combinations(range(m),5)) and
             not any(convex(s) for s in it.combinations(range(m),n)))
    caps=[mask(s) for s in it.combinations(range(m),4) if cap(s)]
    targets=[]
    for s in it.combinations(range(m),n-1):
        if not convex(s):continue
        u,v=s[0],s[-1]
        if mode=='weak':key=s
        else:key=[u,v]+[p for p in s[1:-1] if t[u,p,v]==(mode=='cup')]
        targets.append(mask(key))
    fail=[any(k&d==k for k in caps) or any(h&d==0 for h in targets) for d in range(full+1)]
    return valid,fail


def new_formula(m,n,mode,pool):
    path=WORK/f'semantic-{m}-{n}-{mode}-{pool}.cnf'
    p=subprocess.run([str(WORK/'delta_cnf'),'--m',str(m),'--n',str(n),'--mode',mode,
                      '--pool',pool,'--out',str(path)],capture_output=True,text=True,check=True)
    stats=json.loads(p.stdout)
    clauses=[]
    for line in path.read_text().splitlines():
        if line[0] in 'pc':continue
        c=list(map(int,line.split())); assert c[-1]==0
        clauses.append(c[:-1])
    assert len(clauses)==stats['clauses']
    # With sym=none and no fixed signs/cube, the final 2^m clauses are the pool.
    return stats['variables'],clauses[:-(1<<m)],clauses[-(1<<m):]


def old_formula(m,n,mode):
    if mode=='weak':
        e=Enc(5,n,m,False)
        defs=list(e.base)+list(e.wit)
        pool=[e.pool_clause([p for p in range(m) if d>>p&1]) for d in range(1<<m)]
        return e.nv,defs,pool
    _,nv,clauses=upper_exact.build(5,n,m,mode=='cup',False)
    oldpool=clauses[-(1<<m):]
    order=[sum(1<<p for p in s) for k in range(m+1) for s in it.combinations(range(m),k)]
    pool=[None]*(1<<m)
    for d,c in zip(order,oldpool):pool[d]=c
    return nv,clauses[:-(1<<m)],pool


def main():
    started=time.monotonic(); rows=[]
    configurations_by_m={m:configurations(m) for m in (4,5,6)}
    cases=[(4,5,'cup'),(5,5,'weak'),(5,5,'cup'),(5,5,'cap'),
           (5,8,'cup'),(6,6,'cup'),(6,6,'cap'),(6,6,'weak')]
    for m,n,mode in cases:
        configurations_=configurations_by_m[m]
        solvers=[]
        try:
            for name in ('lattice','flat','record'):
                nv,defs,pool=(old_formula(m,n,mode) if name=='record'
                              else new_formula(m,n,mode,name))
                solver=Glucose4(bootstrap_with=defs)
                selectors=list(range(nv+1,nv+1+(1<<m)))
                for s,c in zip(selectors,pool):solver.add_clause([-s]+c)
                solvers.append((name,solver,selectors))
            valid_count=queries=0
            for signs,t in configurations_:
                valid,fail=direct(t,m,n,mode)
                valid_count+=valid
                for name,solver,selectors in solvers:
                    assert solver.solve(assumptions=signs)==valid, (m,n,mode,name,'base')
                    if not valid:continue
                    for d,s in enumerate(selectors):
                        got=solver.solve(assumptions=signs+[s]);queries+=1
                        assert got==fail[d], (m,n,mode,name,d,signs,got,fail[d])
            row=dict(m=m,n=n,mode=mode,signotopes=len(configurations_),valid=valid_count,
                     comparisons=queries,mismatches=0)
            rows.append(row); print(json.dumps(row),flush=True)
        finally:
            for _,solver,_ in solvers:solver.delete()
    result=dict(label='COMPUTED',cases=rows,comparisons=sum(x['comparisons'] for x in rows),
                wall_seconds=round(time.monotonic()-started,3))
    (WORK/'semantic-controls.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'total_comparisons':result['comparisons'],'wall_seconds':result['wall_seconds']}))


if __name__=='__main__':
    main()
