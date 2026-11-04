#!/usr/bin/env python3
"""Find and exactly verify a rational point in the linear lift sign cone.

This proves only feasibility of the necessary linear relaxation, never point
realizability. PSD/rank restrictions are not imposed by this program.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time
import warnings


def load(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--model',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(exist_ok=True,parents=True);start=time.monotonic()
 M=load('linear',Path(__file__).with_name('math_linear.py'));G=load('encoder',M.ROOT/'C7UPPER/gen.py');E=G.Enc(6,8,10)
 raw=a.model.read_bytes();pos=set(json.loads(raw));vs=M.variables(10);ix={v:j for j,v in enumerate(vs)}
 rows=[{j:c*(1 if v in pos else -1) for j,c in M.form(q,ix).items()} for q,v in E.tvar.items()]
 from scipy.optimize import linprog
 from scipy.sparse import coo_matrix
 import numpy as np
 rr=[];cc=[];dd=[]
 for k,row in enumerate(rows):
  for j,c in row.items():rr.append(k);cc.append(j);dd.append(-c)
  rr.append(k);cc.append(100);dd.append(1)
 A=coo_matrix((dd,(rr,cc)),shape=(len(rows),101)).tocsr()
 with warnings.catch_warnings():
  warnings.simplefilter('ignore')
  s=linprog(np.r_[np.zeros(100),-1.],A_ub=A,b_ub=np.zeros(len(rows)),bounds=[(-1,1)]*100+[(0,1)],method='highs',options={'threads':1,'time_limit':45})
 result={'model_sha256':hashlib.sha256(raw).hexdigest(),'lp_status':int(s.status),'lp_message':s.message}
 if s.success and s.x[-1]>1e-9:
  values=[F(float(x)).limit_denominator(10**12) for x in s.x[:-1]]
  margins=[sum(c*values[j] for j,c in row.items()) for row in rows]
  assert min(margins)>0
  D=np.zeros((10,10));EE=np.zeros((10,10))
  for key,x in zip(vs,values):
   kind,i,j=key
   if kind=='D':D[i,j]=D[j,i]=float(x)
   else:EE[i,j]=float(x);EE[j,i]=-float(x)
  H=D+1j*np.sqrt(3)*EE
  result.update({'exact_linear_feasible':True,'minimum_exact_margin':str(min(margins)),'numeric_maximum_margin':float(s.x[-1]),
                 'hermitian_eigenvalues_evidence_only':np.linalg.eigvalsh(H).tolist(),
                 'radii_squared_evidence_only':D.diagonal().tolist(),
                 'strict_radius_order_exact':all(values[ix['D',i,i]]>values[ix['D',i+1,i+1]] for i in range(9)),
                 'lift':[[key,str(x)] for key,x in zip(vs,values)]})
 result['elapsed_seconds']=round(time.monotonic()-start,3);result['peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 (a.out/'primal.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='lift'}),flush=True)


if __name__=='__main__':main()
