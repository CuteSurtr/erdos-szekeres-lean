#!/usr/bin/env python3
"""Bounded fixed-x numerical finder; ONLY exact integer signs count."""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
import hashlib
from fractions import Fraction
from itertools import combinations
import json
from math import lcm
from pathlib import Path
import random
import resource
import time
import traceback
import warnings

resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
resource.setrlimit(resource.RLIMIT_CPU,(18,18))
HERE=Path(__file__).resolve().parent
DATA=HERE/'data'
SOURCE=Path('/home/jay/research/data/delta3-codex-20261113/extension/small-delta/n7m11k2/solve/cadical.log')


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    start=time.monotonic();attempts=[]
    out={'status':'UNRESOLVED_REALIZABILITY','label':'HEURISTIC until exact coordinates checked',
         'source':str(SOURCE),'source_sha256':sha(SOURCE),'script_sha256':sha(Path(__file__))}
    try:
        import numpy as np
        from scipy.optimize import linprog, OptimizeWarning
        model={}
        for line in SOURCE.read_text().splitlines():
            if line.startswith('v '):
                model.update((abs(z),z>0) for z in map(int,line.split()[1:]) if z)
        triples=list(combinations(range(11),3));signs=[1 if model[i+1] else -1 for i in range(len(triples))]
        rng=random.Random(20261114)
        x_cases=[list(range(11)),[i*i for i in range(11)],[(1<<i)-1 for i in range(11)]]
        for trial in range(80):
            x=[0]
            for i in range(10):x.append(x[-1]+rng.randint(1,2**(trial%6+1)))
            x_cases.append(x)
        for trial,x in enumerate(x_cases):
            if time.monotonic()-start>12:break
            mat=[]
            for (a,b,c),s in zip(triples,signs):
                row=[0]*11
                row[a]=-s*(x[c]-x[b]);row[b]=s*(x[c]-x[a]);row[c]=-s*(x[b]-x[a])
                mat.append(row)
            with warnings.catch_warnings():
                warnings.simplefilter('ignore',OptimizeWarning)
                r=linprog(np.zeros(11),A_ub=np.array(mat,dtype=float),b_ub=-np.ones(len(mat)),
                          bounds=[(0,0)]+[(None,None)]*9+[(0,0)],method='highs',
                          options={'threads':1,'time_limit':0.25})
            attempt={'trial':trial,'x':x,'numeric_status':int(r.status),'candidate_available':r.x is not None}
            attempts.append(attempt)
            if r.x is None:continue
            for bound in (100,10000,1000000):
                qs=[Fraction(float(y)).limit_denominator(bound) for y in r.x]
                den=lcm(*(q.denominator for q in qs))
                P=[[u,int(q*den)] for u,q in zip(x,qs)]
                ds=[(P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
                    for a,b,c in triples]
                if all(d*s>0 for d,s in zip(ds,signs)):
                    candidate={'P':P,'n':7,'m':11,'terminal_delta':[0,1,3],
                               'source':str(SOURCE),'source_sha256':sha(SOURCE),
                               'signs':''.join('+' if s>0 else '-' for s in signs),
                               'finder':'fixed-x LP proposal followed by exact integer determinant acceptance',
                               'trial':trial,'rational_denominator_bound':bound,'minimum_absolute_determinant':min(map(abs,ds))}
                    with (DATA/'sat11.candidate.json').open('x') as f:
                        json.dump(candidate,f,indent=2);f.write('\n')
                    out.update(status='EXACT_INTEGER_REALIZATION',label='COMPUTED exact signs',trial=trial)
                    return
            attempt['exact_rounding']='FAILED'
    except BaseException:
        out.update(status='FAILED',error=traceback.format_exc());raise
    finally:
        out.update(attempts=attempts,seconds=time.monotonic()-start,
                   max_rss_KiB=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
        with (DATA/'realize.json').open('x') as f:
            json.dump(out,f,indent=2);f.write('\n')
        print(json.dumps({k:v for k,v in out.items() if k!='attempts'}))


if __name__=='__main__':main()
