#!/usr/bin/env python3
"""Bounded batched subset-pool discovery; no solver result is CERTIFIED here.

Uses the previously audited universal encoder's clauses verbatim. Only the
last 2**m subset-failure clauses are selected lazily. The exported formula
is a weakening of that universal formula, so certified UNSAT suffices.
"""
import os
os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
import argparse
import hashlib
import itertools as it
import json
import math
from pathlib import Path
import random
import resource
import signal
import time
import numpy as np
from pysat.solvers import Cadical195


def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20), b''): h.update(b)
    return h.hexdigest()


class Geometry:
    """Boolean sign semantics, all four-subsets, and full subset transforms."""
    def __init__(self,m,n):
        self.m,self.n=m,n
        self.triples=list(it.combinations(range(m),3))
        t={q:i for i,q in enumerate(self.triples)}
        quads=list(it.combinations(range(m),4))
        qi={q:i for i,q in enumerate(quads)}
        self.qt=np.array([[t[q] for q in it.combinations(s,3)] for s in quads],dtype=np.int32)
        self.cap4mask=np.array([sum(1<<i for i in s) for s in quads],dtype=np.int32)
        self.cap5=np.array([[t[q] for q in it.combinations(s,3)] for s in it.combinations(range(m),5)],dtype=np.int32).reshape(-1,10)
        self.gons={}
        for k in (n-1,n):
            sets=list(it.combinations(range(m),k))
            self.gons[k]=(np.array([sum(1<<i for i in s) for s in sets],dtype=np.int32),
                          np.array([[qi[q] for q in it.combinations(s,4)] for s in sets],dtype=np.int32).reshape(len(sets),math.comb(k,4)))

    def upward(self,seeds):
        a=np.zeros(1<<self.m,dtype=np.uint8);a[seeds]=1
        for k in range(self.m):
            b=a.reshape(-1,2,1<<k)
            b[:,1,:]|=b[:,0,:]
        return a

    def analyze(self,signs):
        o=np.array([c=='+' for c in signs],dtype=np.bool_)
        assert len(o)==len(self.triples)
        q=o[self.qt]
        assert np.all(np.sum(q[:,1:]!=q[:,:-1],axis=1)<=1), 'bad signotope'
        assert not np.any(np.all(~o[self.cap5],axis=1)), 'five-cap'
        convex=(q[:,0]==q[:,1]) & (q[:,2]==q[:,3])
        assert not np.any(np.all(convex[self.gons[self.n][1]],axis=1)), 'n-gon'
        caps=self.cap4mask[np.all(~q,axis=1)]
        gmask,sub=self.gons[self.n-1]
        targets=gmask[np.all(convex[sub],axis=1)]
        badred=self.upward(caps);badblue=self.upward(targets)
        working=np.flatnonzero((badred==0)&(badblue[::-1]==0))
        return working,dict(fourcaps=len(caps),targets=len(targets),working_deltas=len(working))


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source',type=Path,required=True,help='prior encoder result.json')
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--seconds',type=int,default=600)
    ap.add_argument('--batch',type=int,default=128)
    ap.add_argument('--seed',type=int,default=1)
    ap.add_argument('--as-mib',type=int,default=700)
    a=ap.parse_args()
    if a.batch<=0 or a.seconds<=0 or a.as_mib<200:
        ap.error('require batch>0, seconds>0 and as-mib>=200')
    startup_source=Path(__file__).read_bytes()
    startup_hash=hashlib.sha256(startup_source).hexdigest()
    resource.setrlimit(resource.RLIMIT_AS,(a.as_mib<<20,a.as_mib<<20))
    a.out.mkdir(parents=True,exist_ok=False)
    (a.out/'script_snapshot.py').write_bytes(startup_source)
    start=time.monotonic();end=start+a.seconds;rng=random.Random(a.seed)
    source=json.loads(a.source.read_text());p=source['parameters'];e=source['encoding']
    assert p['mode']=='weak' and p['sym']=='none' and not p['cube'] and not p['fix_signs']
    m,n=p['m'],p['n'];count=1<<m
    assert e['phases']['forall_delta']['clauses']==count
    original=a.source.parent/'case.cnf'
    assert sha(original)==source['hashes']['case.cnf']
    total=e['clauses'];base_count=total-count
    pool_clauses=[];used=set();pool=[]
    g=Geometry(m,n)
    result=dict(label='COMPUTED',status='STARTED',m=m,n=n,batch=a.batch,seed=a.seed,
                source=str(a.source),source_cnf_sha256=sha(original),
                source_result_sha256=sha(a.source),variables=e['variables'],base_clauses=base_count,
                source_script_sha256=startup_hash,
                seconds_limit=a.seconds,as_mib=a.as_mib,solver='PySAT CaDiCaL 1.9.5 (finder only)')
    stopping=False
    def stop(*_):
        nonlocal stopping
        stopping=True
    signal.signal(signal.SIGTERM,stop)
    def save():
        result.update(pool_size=len(pool),elapsed_seconds=round(time.monotonic()-start,3))
        (a.out/'result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
        (a.out/'pool.json').write_text(json.dumps(dict(m=m,n=n,masks=pool))+'\n')
    save()
    with Cadical195() as solver, original.open() as inp, (a.out/'base.cnf').open('w') as out:
        header=inp.readline().split();assert header[:2]==['p','cnf']
        assert int(header[2])==e['variables'] and int(header[3])==total
        out.write(f'p cnf {e["variables"]} {base_count}\n')
        actual=0
        for line in inp:
            cl=list(map(int,line.split()));assert cl and cl[-1]==0
            assert all(0<abs(x)<=e['variables'] for x in cl[:-1])
            if actual<base_count:
                solver.add_clause(cl[:-1]);out.write(line)
            else:pool_clauses.append(cl[:-1])
            actual+=1
        assert actual==total and len(pool_clauses)==count
        out.flush()
        calls=iterations=0;lastsave=0
        result['status']='SEARCHING';save()
        with (a.out/'events.jsonl').open('w',buffering=1) as events:
            while time.monotonic()<end and not stopping:
                solver.conf_budget(5000)
                answer=solver.solve_limited();calls+=1
                if answer is False:
                    result['status']='UNSAT_UNCERTIFIED';break
                if answer is None:
                    if time.monotonic()-lastsave>10:
                        result.update(calls=calls,iterations=iterations);save();lastsave=time.monotonic()
                    continue
                iterations+=1
                mod=solver.get_model();values={abs(v):v>0 for v in mod}
                signs=''.join('+' if values[i+1] else '-' for i in range(len(g.triples)))
                working,stats=g.analyze(signs)
                assert all(int(d) not in used for d in working), 'pooled Delta still works'
                if not len(working):
                    result['status']='ABSTRACT_CANDIDATE';result['signs']=signs
                    result['candidate_counts']=stats;break
                if len(working)<=a.batch:chosen=list(map(int,working))
                else:chosen=rng.sample(list(map(int,working)),a.batch)
                # Every chosen mask is a real working Delta of this abstract model.
                # Reversal adds legitimate extra subset clauses, without symmetry assumptions.
                add=[]
                for d in chosen:
                    rev=int(f'{d:0{m}b}'[::-1],2)
                    for v in (d,rev):
                        if v not in used:
                            used.add(v);pool.append(v);add.append(v);solver.add_clause(pool_clauses[v])
                events.write(json.dumps(dict(iteration=iterations,seconds=round(time.monotonic()-start,3),
                                            pool_size=len(pool),added=len(add),signs_sha256=hashlib.sha256(signs.encode()).hexdigest(),**stats))+'\n')
                if time.monotonic()-lastsave>10:
                    result.update(calls=calls,iterations=iterations);save();lastsave=time.monotonic()
            else:result['status']='UNKNOWN'
        result.update(calls=calls,iterations=iterations)
    # Preserve a plain, independently certifiable weakening of the original CNF.
    with (a.out/'final.cnf').open('w') as out,(a.out/'base.cnf').open() as inp:
        next(inp);out.write(f'p cnf {e["variables"]} {base_count+len(pool)}\n')
        for line in inp:out.write(line)
        for d in pool:out.write(' '.join(map(str,pool_clauses[d]))+' 0\n')
    result['final_cnf_sha256']=sha(a.out/'final.cnf')
    save();print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
