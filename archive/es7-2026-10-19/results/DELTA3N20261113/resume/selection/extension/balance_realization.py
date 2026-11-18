#!/usr/bin/env python3
"""Numerical coordinate search, accepted only by integer determinant replay."""
import os
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',NUMEXPR_NUM_THREADS='1')
import argparse,hashlib,itertools,json,math,random,resource,time
from pathlib import Path
def det(P,a,b,c):return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
class Deadline(Exception):pass
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seconds',type=int,default=500);a=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(2048<<20,2048<<20));a.out.mkdir(parents=True,exist_ok=False)
 import numpy as np
 from scipy.optimize import minimize
 src=json.loads(a.input.read_text());original=src['P'];m=len(original);triples=list(itertools.combinations(range(m),3));sign=np.array([1 if det(original,*t)>0 else -1 for t in triples]);assert all(det(original,*t) for t in triples)
 ids=np.array(triples);ia,ib,ic=ids.T;row=np.arange(len(ids));start=time.monotonic();best=original;best_score=(max(abs(v) for p in best for v in p),sum(abs(v) for p in best for v in p));updates=0;steps=0
 def normalize(P):
  X=np.array([p[0] for p in P],dtype=float);Y=np.array([p[1] for p in P],dtype=float);X=(X-X[0])/(X[-1]-X[0]);Y=Y-Y[0]-(Y[-1]-Y[0])*X;Y/=max(1,max(abs(Y)));return np.concatenate((X,Y,[0.]))
 def constraints(z):
  X=z[:m];Y=z[m:2*m];d=(X[ib]-X[ia])*(Y[ic]-Y[ia])-(Y[ib]-Y[ia])*(X[ic]-X[ia]);return np.concatenate((sign*d-z[-1],np.diff(X)-z[-1]))
 def jac(z):
  X=z[:m];Y=z[m:2*m];J=np.zeros((len(ids)+m-1,2*m+1));J[row,ia]=sign*(Y[ib]-Y[ic]);J[row,ib]=sign*(Y[ic]-Y[ia]);J[row,ic]=sign*(Y[ia]-Y[ib]);J[row,m+ia]=sign*(X[ic]-X[ib]);J[row,m+ib]=sign*(X[ia]-X[ic]);J[row,m+ic]=sign*(X[ib]-X[ia]);r=len(ids)+np.arange(m-1);J[r,np.arange(m-1)]=-1;J[r,np.arange(1,m)]=1;J[:,-1]=-1;return J
 def accept(z):
  nonlocal best,best_score,updates,steps
  steps+=1
  if time.monotonic()-start>a.seconds:raise Deadline()
  X=z[:m];Y=z[m:2*m]
  if not np.isfinite(z).all() or min(np.diff(X))<=0:return
  for grid in [100,300,1000,3000,10000,30000,100000,300000,1000000,3000000,10000000,100000000,1000000000,10000000000,100000000000]:
   P=[[int(round(x*grid)),int(round(y*grid))] for x,y in zip(X,Y)]
   if any(P[i][0]>=P[i+1][0] for i in range(m-1)):continue
   if all(int(sg)*det(P,*t)>0 for t,sg in zip(triples,sign)):
    gx=math.gcd(*(p[0] for p in P));gy=math.gcd(*(p[1] for p in P));P=[[x//max(gx,1),y//max(gy,1)] for x,y in P];score=(max(abs(v) for p in P for v in p),sum(abs(v) for p in P for v in p))
    if score<best_score:
     best=P;best_score=score;updates+=1
     record={'update':updates,'step':steps,'P':P,'score':score,'seconds':round(time.monotonic()-start,3)}
     with (a.out/'accepted.jsonl').open('a') as f:f.write(json.dumps(record)+'\n')
     (a.out/'best.json').write_text(json.dumps(record,indent=2)+'\n')
    break
 bounds=[(0.,1.)]*m+[(-1.,1.)]*m+[(0.,1.)];bounds[0]=(0.,0.);bounds[m-1]=(1.,1.);bounds[m]=(0.,0.);bounds[2*m-1]=(0.,0.)
 objective=np.zeros(2*m+1);objective[-1]=-1;rng=np.random.default_rng(202611140546);runs=[]
 try:
  for restart in range(30):
   z=normalize(best)
   if restart:
    z[:2*m]+=rng.normal(0,10.**(-4+restart%4),2*m);z[0]=z[m]=z[2*m-1]=0;z[m-1]=1
   res=minimize(lambda z:-z[-1],z,jac=lambda z:objective,method='SLSQP',constraints={'type':'ineq','fun':constraints,'jac':jac},bounds=bounds,callback=accept,options={'maxiter':2000,'ftol':1e-12,'disp':False});accept(res.x)
   runs.append({'restart':restart,'status':int(res.status),'message':str(res.message),'success':bool(res.success),'iterations':int(res.nit),'objective':float(res.fun)})
   (a.out/'runs.json').write_text(json.dumps(runs,indent=2)+'\n')
 except Deadline:runs.append({'stop':'DEADLINE'})
 assert all(int(sg)*det(best,*t)>0 for t,sg in zip(triples,sign))
 out={'label':'COMPUTED exact accepted coordinates; HEURISTIC numerical search','P':best,'m':m,'n':7,'orientation_signs':''.join('+' if s>0 else '-' for s in sign),'steps':steps,'updates':updates,'score':best_score,'seconds':round(time.monotonic()-start,3),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'source_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'minimum_absolute_determinant':min(abs(det(best,*t)) for t in triples),'scope':'Only exact orientation-preserving outputs are accepted; optimizer statuses do not prove feasibility, infeasibility, or optimality.'}
 (a.out/'witness.json').write_text(json.dumps(out,indent=2)+'\n');(a.out/'witness.points').write_text(f'{m} 7\n'+''.join(f'{x} {y}\n' for x,y in best));print(json.dumps({k:out[k] for k in ['P','updates','score','seconds','peak_rss_kib']}),flush=True)
if __name__=='__main__':main()
