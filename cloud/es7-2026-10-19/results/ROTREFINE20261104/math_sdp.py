#!/usr/bin/env python3
"""Numerical PSD feasibility probe with exact rational dual-certificate attempt.

Numerical SDP status alone proves nothing. A retained obstruction is a positive
integer combination of signed orientation quadratic forms whose negative is
proved positive definite by exact rational LDL elimination.
"""
import argparse
from collections import defaultdict
from fractions import Fraction as F
import hashlib
import importlib.util
import itertools as it
import json
from pathlib import Path
import resource
import time


def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def negative_definite(rows,weights,vs,layers):
 # Twice the symmetric matrix of sum(weight*row), in coordinates (u_i,v_i)
 # where the Euclidean seed is (u_i,sqrt(3)*v_i).
 n=len(layers);idx={i:k for k,i in enumerate(layers)};Q=[[0]*(2*n) for _ in range(2*n)]
 coeff=defaultdict(int)
 for row,w in zip(rows,weights):
  for j,c in row.items():coeff[j]+=w*c
 for j,c in coeff.items():
  if not c:continue
  kind,i,k=vs[j];i=idx[i];k=idx[k]
  if kind=='D':
   if i==k:Q[i][i]+=2*c;Q[n+i][n+i]+=6*c
   else:
    Q[i][k]+=c;Q[k][i]+=c;Q[n+i][n+k]+=3*c;Q[n+k][n+i]+=3*c
  else:
   Q[i][n+k]+=c;Q[n+k][i]+=c;Q[n+i][k]-=c;Q[k][n+i]-=c
 A=[[-F(x) for x in row] for row in Q];pivots=[]
 for k in range(2*n):
  p=A[k][k]
  if p<=0:return None,Q
  pivots.append(p)
  for i in range(k+1,2*n):
   for j in range(i,2*n):
    A[i][j]-=A[i][k]*A[k][j]/p;A[j][i]=A[i][j]
 return pivots,Q


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--model',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--layers',default='all');ap.add_argument('--seconds',type=float,default=45);ap.add_argument('--save-dual',action='store_true');a=ap.parse_args();a.out.mkdir(exist_ok=True,parents=True);start=time.monotonic()
 M=load('linear',Path(__file__).with_name('math_linear.py'));G=load('encoder',M.ROOT/'C7UPPER/gen.py');E=G.Enc(6,8,10)
 raw=a.model.read_bytes();pos=set(json.loads(raw));vs=M.variables(10);ix={v:j for j,v in enumerate(vs)}
 layers=list(range(10)) if a.layers=='all' else list(map(int,a.layers.split(',')));ls=set(layers)
 entries=[(q,v,{j:c*(1 if v in pos else -1) for j,c in M.form(q,ix).items()}) for q,v in E.tvar.items() if {x//6 for x in q}<=ls]
 import numpy as np
 from scipy.sparse import coo_matrix
 import cvxpy as cp
 rr=[];cc=[];dd=[]
 for k,(q,v,row) in enumerate(entries):
  for j,c in row.items():rr.append(k);cc.append(j);dd.append(c)
 A=coo_matrix((dd,(rr,cc)),shape=(len(entries),100)).tocsr();x=cp.Variable(100);delta=cp.Variable()
 D=cp.bmat([[cp.reshape(x[ix['D',min(i,j),max(i,j)]],(1,1),order='C') for j in layers] for i in layers])
 EE=cp.bmat([[cp.Constant(np.zeros((1,1))) if i==j else cp.reshape(x[ix['E',min(i,j),max(i,j)]]*(1 if i<j else -1),(1,1),order='C') for j in layers] for i in layers])
 matrix=cp.bmat([[D,-EE],[EE,D/3]])
 orient=A@x>=delta;psd=matrix>>0;trace=cp.trace(D)==1
 problem=cp.Problem(cp.Maximize(delta),[orient,psd,trace])
 problem.solve(solver='CLARABEL',verbose=False,max_threads=1,time_limit=a.seconds,max_iter=200,tol_gap_abs=1e-9,tol_gap_rel=1e-9,tol_feas=1e-9)
 result={'model_sha256':hashlib.sha256(raw).hexdigest(),'source_layers':layers,'constraints':len(entries),'sdp_status':problem.status,
         'maximum_margin_evidence_only':float(delta.value) if delta.value is not None else None,'elapsed_seconds':round(time.monotonic()-start,3)}
 if x.value is not None:
  result['numeric_lift_evidence_only']=[[key,float(value)] for key,value in zip(vs,x.value)]
 if orient.dual_value is not None:
  dual=np.asarray(orient.dual_value).ravel();result['dual_sum_evidence_only']=float(dual.sum());result['exact_negative_definite_certificate']=False
  if a.save_dual:result['numeric_dual_evidence_only']=[{'triple':q,'variable':v,'required_sign':1 if v in pos else -1,'dual':float(z)} for (q,v,row),z in zip(entries,dual)]
  for scale in (10**2,10**3,10**4,10**5,10**6,10**8,10**10,10**12):
   weights=[max(0,int(round(float(z)*scale))) for z in dual];support=[i for i,w in enumerate(weights) if w]
   ww=[weights[i] for i in support];rows=[entries[i][2] for i in support]
   used_layers=sorted({x//6 for i in support for x in entries[i][0]})
   if not used_layers:continue
   pivots,Q=negative_definite(rows,ww,vs,used_layers)
   if pivots is not None:
    records=[]
    for k,weight in zip(support,ww):
     q,v,row=entries[k];records.append({'triple':q,'variable':v,'required_sign':1 if v in pos else -1,'weight':weight})
    w={'method':'positive orientation combination is negative definite','scope':'prescribed counterclockwise Euclidean sixfold action',
       'm':6,'t':10,'source_layers':used_layers,'model_sha256':result['model_sha256'],'records':records,
       'quadratic_matrix_twice':Q,'negative_matrix_exact_ldl_pivots':[str(p) for p in pivots],
       'candidate_clause':sorted([-r['variable']*r['required_sign'] for r in records],key=abs)}
    data=(json.dumps(w,indent=2)+'\n').encode();(a.out/'sdp_witness.json').write_bytes(data)
    result.update({'exact_negative_definite_certificate':True,'support':len(records),'certificate_source_layers':used_layers,'scale':scale,'witness_sha256':hashlib.sha256(data).hexdigest()});break
 result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 (a.out/'sdp_result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('numeric_lift_evidence_only','numeric_dual_evidence_only')}),flush=True)


if __name__=='__main__':main()
