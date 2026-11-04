#!/usr/bin/env python3
"""Try exact rational validation of a numerically strict PSD lift.

Rounding and a small diagonal perturbation only propose rational candidates.
Every orientation and rational positive-definiteness pivot is checked exactly.
A successful lift still does not prove the required rank-one realization.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('--result',type=Path,required=True);p.add_argument('--model',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();data=json.loads(a.result.read_text());mh=hashlib.sha256(a.model.read_bytes()).hexdigest();assert mh==data['model_sha256'];assert data['source_layers']==list(range(10));pos=set(json.loads(a.model.read_text()))
 root=Path(__file__).parent;L=load('linear',root/'math_linear.py');V=load('exact',root/'tests/verify_sdp.py');G=load('encoder',L.ROOT/'C7UPPER/gen.py');E=G.Enc(6,8,10);vs=L.variables(10);ix={v:j for j,v in enumerate(vs)}
 base={tuple(key):F(value).limit_denominator(10**9) for key,value in data['numeric_lift_evidence_only']};attempts=[]
 for denom in (10**12,10**10,10**8,10**6,10**5,10**4,10**3):
  x=dict(base)
  for i in range(10):x['D',i,i]+=F(1,denom)
  margins=[]
  for q,var in E.tvar.items():margins.append((1 if var in pos else -1)*sum(c*x[vs[j]] for j,c in L.form(q,ix).items()))
  minimum=min(margins)
  if minimum<=0:attempts.append({'diagonal_perturbation':str(F(1,denom)),'strict_orientations':False});continue
  D=[[x['D',min(i,j),max(i,j)] for j in range(10)] for i in range(10)]
  EE=[[F(0) if i==j else (1 if i<j else -1)*x['E',min(i,j),max(i,j)] for j in range(10)] for i in range(10)]
  M=[D[i]+[-v for v in EE[i]] for i in range(10)]+[EE[i]+[v/3 for v in D[i]] for i in range(10)]
  try:piv=V.pd(M)
  except AssertionError:attempts.append({'diagonal_perturbation':str(F(1,denom)),'strict_orientations':True,'positive_definite':False});continue
  result={'status':'exact positive-definite lift found','model_sha256':mh,'numerical_source_sha256':hashlib.sha256(a.result.read_bytes()).hexdigest(),'scope':'strict orientation and positive-definite Gram relaxation only; rank-one realization unproved','variables':[[key,str(x[key])] for key in vs],'orientation_constraints':len(margins),'minimum_exact_margin':str(minimum),'exact_positive_matrix_ldl_pivots':piv,'positive_decreasing_radii':all(D[i][i]>D[i+1][i+1]>0 for i in range(9)),'diagonal_perturbation':str(F(1,denom)),'prior_attempts':attempts};a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('variables','exact_positive_matrix_ldl_pivots')}));return
 a.out.write_text(json.dumps({'status':'no exact positive-definite lift validated; no infeasibility conclusion','model_sha256':mh,'attempts':attempts},indent=2)+'\n')
if __name__=='__main__':main()
