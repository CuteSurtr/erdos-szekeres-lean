#!/usr/bin/env python3
"""Heuristic coordinate simplifier; accepts only exact orientation matches."""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
import argparse,hashlib,itertools,json,math,random,resource,time,warnings
from pathlib import Path
def det(P,a,b,c):return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(2048<<20,2048<<20));a.out.mkdir(parents=True,exist_ok=False)
 import numpy as np
 from scipy.optimize import linprog
 src=json.loads(a.input.read_text());P=src['P'];m=len(P);triples=list(itertools.combinations(range(m),3));signs=[1 if det(P,*t)>0 else -1 for t in triples];assert all(det(P,*t) for t in triples)
 start=time.monotonic();attempts=0;accepted=0;rng=random.Random(202611140535)
 def try_x(X):
  nonlocal attempts
  rows=[]
  for (u,v,w),sg in zip(triples,signs):
   row=np.zeros(m+1);coeff=[X[w]-X[v],-(X[w]-X[u]),X[v]-X[u]];scale=max(map(abs,coeff))
   for i,c in zip((u,v,w),coeff):row[i]=-sg*c/scale
   rows.append(row)
  rhs=[-1.]*len(rows)
  for i in range(m):
   for sg in [-1,1]:
    row=np.zeros(m+1);row[i]=sg;row[-1]=-1;rows.append(row);rhs.append(0.)
  bounds=[(None,None)]*m+[(0,None)];bounds[0]=bounds[m-1]=(0,0);obj=np.zeros(m+1);obj[-1]=1
  with warnings.catch_warnings():
   warnings.simplefilter('ignore');res=linprog(obj,A_ub=np.array(rows),b_ub=np.array(rhs),bounds=bounds,method='highs-ds',options={'threads':1,'parallel':False,'time_limit':2.0})
  found=None
  if res.x is not None and all(math.isfinite(float(v)) for v in res.x):
   for scale in [1,2,4,8,16,32,64,128,256,1024,1000000]:
    Q=[[int(x),int(round(float(y)*scale))] for x,y in zip(X,res.x[:m])]
    if all(sg*det(Q,*t)>0 for t,sg in zip(triples,signs)):
     gy=math.gcd(*(q[1] for q in Q));gx=math.gcd(*(q[0] for q in Q));found=[[x//max(gx,1),y//max(gy,1)] for x,y in Q];break
  attempts+=1
  with (a.out/'attempts.jsonl').open('a') as f:f.write(json.dumps({'attempt':attempts,'X':X,'finder_status':int(res.status),'exact_orientation_match':found is not None})+'\n')
  return found
 Q=try_x([x for x,y in P]);P=Q if Q else P
 for sweep in range(20):
  changed=False;indices=list(range(m-1));rng.shuffle(indices)
  for i in indices:
   if time.monotonic()-start>500:break
   gaps=[P[j+1][0]-P[j][0] for j in range(m-1)];old=gaps[i]
   choices=sorted({1,2,3,4,5,8,16,32,64,old//4,old//2,3*old//4,old-1})
   for value in choices:
    if value<=0 or value>=old:continue
    trial=gaps.copy();trial[i]=value;X=[0]+list(itertools.accumulate(trial));Q=try_x(X)
    if Q is not None:
     P=Q;changed=True;accepted+=1
     with (a.out/'accepted.jsonl').open('a') as f:f.write(json.dumps({'sweep':sweep,'gap':i,'new_gap':value,'P':P})+'\n')
     break
  if not changed or time.monotonic()-start>500:break
 assert all(sg*det(P,*t)>0 for t,sg in zip(triples,signs))
 out={'label':'COMPUTED exact integer realization; heuristic simplification, no minimality claim','P':P,'m':m,'n':7,'orientation_signs':''.join('+' if x>0 else '-' for x in signs),'attempts':attempts,'accepted_gap_reductions':accepted,'seconds':round(time.monotonic()-start,3),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'minimum_absolute_determinant':min(abs(det(P,*t)) for t in triples),'source_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'scope':'Every accepted realization has all original triple orientations. No assertion relies on an LP infeasibility status.'}
 (a.out/'witness.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'witness.points').write_text(f'{m} 7\n'+''.join(f'{x} {y}\n' for x,y in P));print(json.dumps({k:out[k] for k in ['P','attempts','accepted_gap_reductions','seconds','peak_rss_kib']}),flush=True)
if __name__=='__main__':main()
