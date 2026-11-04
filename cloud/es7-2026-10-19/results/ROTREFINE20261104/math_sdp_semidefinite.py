#!/usr/bin/env python3
"""Exact nonpositive-quadratic diagnostic; never queues a numerical result."""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
import math
from pathlib import Path
import time

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def psd(Q):
 A=[[-F(x) for x in row] for row in Q];piv=[]
 for k in range(len(A)):
  p=A[k][k]
  if p<0:return None
  piv.append(p)
  if p==0:
   if any(A[k][j] for j in range(k,len(A))):return None
   continue
  for i in range(k+1,len(A)):
   for j in range(i,len(A)):
    A[i][j]-=A[i][k]*A[k][j]/p;A[j][i]=A[i][j]
 return piv
def main():
 p=argparse.ArgumentParser();p.add_argument('--result',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=float,default=30);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);start=time.monotonic();data=json.loads(a.result.read_text());L=load('linear',Path(__file__).with_name('math_linear.py'));S=load('sdp',Path(__file__).with_name('math_sdp.py'));vs=L.variables(10);ix={v:j for j,v in enumerate(vs)};entries=data['numeric_dual_evidence_only'];seen=set();tried=0
 for scale in list(range(1,2049))+[10**i for i in range(4,13)]:
  if time.monotonic()-start>a.seconds:break
  support=[(r,max(0,int(round(r['dual']*scale)))) for r in entries];support=[(r,w) for r,w in support if w]
  if not support:continue
  common=math.gcd(*(w for r,w in support));support=[(r,w//common) for r,w in support];key=tuple((r['variable'],w) for r,w in support)
  if key in seen:continue
  seen.add(key);tried+=1;layers=sorted({x//6 for r,w in support for x in r['triple']});rows=[{j:c*r['required_sign'] for j,c in L.form(tuple(r['triple']),ix).items()} for r,w in support]
  _,Q=S.negative_definite(rows,[w for r,w in support],vs,layers);piv=psd(Q)
  if piv is not None and any(piv):
   records=[{'triple':r['triple'],'variable':r['variable'],'required_sign':r['required_sign'],'weight':w} for r,w in support]
   witness={'method':'positive orientation combination is negative semidefinite','scope':'prescribed counterclockwise Euclidean sixfold action','m':6,'t':10,'source_layers':layers,'model_sha256':data['model_sha256'],'records':records,'quadratic_matrix_twice':Q,'negative_matrix_exact_ldl_pivots':list(map(str,piv)),'rank':sum(x>0 for x in piv),'candidate_clause':sorted([-r['variable']*r['required_sign'] for r in records],key=abs)}
   raw=(json.dumps(witness,indent=2)+'\n').encode();(a.out/'sdp_semidefinite_witness.json').write_bytes(raw)
   summary={'status':'exact semidefinite candidate found; independent verification and exact54 tests still required','model_sha256':data['model_sha256'],'witness_sha256':hashlib.sha256(raw).hexdigest(),'support':len(records),'source_layers':layers,'rank':witness['rank'],'scale':scale,'tried':tried,'elapsed_seconds':round(time.monotonic()-start,3)};break
 else:summary=None
 if not (a.out/'sdp_semidefinite_witness.json').exists():summary={'status':'no exact semidefinite candidate extracted; no feasibility conclusion','model_sha256':data['model_sha256'],'tried':tried,'elapsed_seconds':round(time.monotonic()-start,3)}
 (a.out/'diagnostic.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
if __name__=='__main__':main()
