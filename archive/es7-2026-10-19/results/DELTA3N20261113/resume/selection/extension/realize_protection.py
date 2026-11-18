#!/usr/bin/env python3
"""Heuristic LP finder; only exact integer determinant checks accept a witness.

HiGHS statuses are never mathematical evidence. A failed LP attempt means
only that this invocation supplied no independently checked realization.
"""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
import argparse,hashlib,itertools,json,math,random,resource,time,warnings
from pathlib import Path
def det(P,a,b,c):return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--signs',type=Path,required=True);ap.add_argument('--m',type=int,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--attempts',type=int,default=1000);ap.add_argument('--seconds',type=int,default=900);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(600<<20,600<<20));a.out.mkdir(parents=True,exist_ok=False)
 import numpy as np
 from scipy.optimize import linprog
 import scipy
 signs=a.signs.read_text().strip();triples=list(itertools.combinations(range(a.m),3));assert len(signs)==len(triples) and set(signs)<={'+','-'}
 rng=random.Random(202611140521);start=time.monotonic();witness=None;attempts=0
 for k in range(a.attempts):
  if time.monotonic()-start>a.seconds:break
  gaps=[1]*(a.m-1) if k==0 else [rng.randint(1,10**rng.randrange(1,7)) for _ in range(a.m-1)]
  X=[0]+list(itertools.accumulate(gaps));rows=[]
  for (u,v,w),s in zip(triples,signs):
   row=np.zeros(a.m);sg=1 if s=='+' else -1;coef=[X[w]-X[v],-(X[w]-X[u]),X[v]-X[u]];scale=max(map(abs,coef))
   for i,c in zip((u,v,w),coef):row[i]=-sg*c/scale
   rows.append(row)
  bounds=[(None,None)]*a.m;bounds[0]=bounds[-1]=(0,0);t=time.monotonic()
  with warnings.catch_warnings(record=True) as ws:
   ans=linprog(np.zeros(a.m),A_ub=np.array(rows),b_ub=-np.ones(len(rows)),bounds=bounds,method='highs-ds',options={'threads':1,'parallel':False,'time_limit':5.0})
  rec={'attempt':k,'X':X,'finder_status':int(ans.status),'finder_message':str(ans.message),'finder_success':bool(ans.success),'seconds':round(time.monotonic()-t,4),'warnings':[str(w.message) for w in ws],'exact_witness':False}
  if ans.x is not None and all(math.isfinite(float(z)) for z in ans.x):
   for scale in [1000,1000000,1000000000,1000000000000]:
    P=[[int(x),int(round(float(y)*scale))] for x,y in zip(X,ans.x)]
    vals=[det(P,*t) for t in triples]
    if all(v!=0 and (v>0)==(s=='+') for v,s in zip(vals,signs)):
     gy=math.gcd(*(p[1] for p in P));gx=math.gcd(*(p[0] for p in P));P=[[x//max(1,gx),y//max(1,gy)] for x,y in P]
     assert all((det(P,*t)>0)==(s=='+') and det(P,*t)!=0 for t,s in zip(triples,signs))
     rec['exact_witness']=True;witness={'label':'COMPUTED exact integer realization','P':P,'m':a.m,'orientation_signs':signs,'minimum_absolute_determinant':min(abs(det(P,*t)) for t in triples),'attempt':k,'scope':'All orientation signs match the SAT orientation model. Other semantic claims require the separate model audit.','signs_sha256':hashlib.sha256(a.signs.read_bytes()).hexdigest(),'finder_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()};break
  attempts+=1
  with (a.out/'attempts.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n')
  if witness is not None:
   (a.out/'witness.json').write_text(json.dumps(witness,indent=2)+'\n');break
  if not k%100:(a.out/'status.json').write_text(json.dumps({'attempts':attempts,'seconds':round(time.monotonic()-start,3)})+'\n')
 out={'label':'COMPUTED' if witness else 'HEURISTIC','status':'EXACT_INTEGER_REALIZATION' if witness else 'NO_VERIFIED_WITNESS','attempts':attempts,'seconds':round(time.monotonic()-start,3),'scipy_version':scipy.__version__,'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'No infeasibility or nonrealizability conclusion is drawn from LP statuses.'}
 (a.out/'DONE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
