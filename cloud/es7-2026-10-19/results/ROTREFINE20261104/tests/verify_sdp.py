#!/usr/bin/env python3
"""Exact direct-polynomial and positive-definiteness check of an SDP-found cut.

The numerical search is not trusted. Finite exact54 tests are regression
checks, not the universal proof. Reflection couples direction and sign.
"""
import argparse
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import time

ROOT=Path(__file__).resolve().parents[2]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def det(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def pd(A):
 A=[[F(x) for x in row] for row in A];piv=[]
 for k in range(len(A)):
  p=A[k][k];assert p>0;piv.append(str(p))
  for i in range(k+1,len(A)):
   for j in range(i,len(A)):
    A[i][j]-=A[i][k]*A[k][j]/p;A[j][i]=A[i][j]
 return piv
def known54():
 path=ROOT/'ES8SYM/sets/c6_54pts_9layers.pts';pts=[]
 for line in path.read_text().splitlines():
  if not line or line.startswith('#'):continue
  a,b,c,d,e,f=map(int,line.split());pts.append((2*a+b-c-2*d-e+f,b+c-e-f))
 assert len(pts)==54
 for i in range(9):
  for k in range(6):
   x,y=pts[6*i+k];xx,yy=pts[6*i+(k+1)%6];assert (2*xx,2*yy)==(x-3*y,x+y)
 return path,pts
def mirrored_ccw(pts,mirror):
 return [(pts[6*i+(mirror*k)%6][0],mirror*pts[6*i+(mirror*k)%6][1]) for i in range(9) for k in range(6)]
def main():
 p=argparse.ArgumentParser();p.add_argument('--witness',type=Path,required=True);p.add_argument('--model',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--samples',type=int,default=100);a=p.parse_args();start=time.monotonic()
 w=json.loads(a.witness.read_text());pos=set(json.loads(a.model.read_text()));assert sha(a.model)==w['model_sha256'];V=load('direct',Path(__file__).with_name('verify_linear.py'));G=load('encoder',ROOT/'C7UPPER/gen.py');E=G.Enc(6,8,w['t'])
 layers=w['source_layers'];assert 2<=len(layers)<=9;assert layers==sorted({x//6 for r in w['records'] for x in r['triple']})
 poly={};rev={};pts=V.symbolic_orbits(w['t']);rp=V.symbolic_orbits(w['t'],-1)
 for r in w['records']:
  q=r['triple'];sg=r['required_sign'];weight=r['weight'];assert isinstance(weight,int) and weight>0 and sg in (-1,1)
  assert E.o(*q)==r['variable'] and sg==(1 if r['variable'] in pos else -1)
  poly=V.add(poly,V.scale(V.determinant(*(pts[i] for i in q)),4*sg*weight))
  rev=V.add(rev,V.scale(V.determinant(*(rp[i] for i in q)),-4*sg*weight))
 Q=w['quadratic_matrix_twice'];n=len(layers);assert len(Q)==2*n and all(len(r)==2*n for r in Q)
 names=[2*i for i in layers]+[2*i+1 for i in layers];qp={}
 for i in range(2*n):
  for j in range(2*n):
   assert isinstance(Q[i][j],int) and Q[i][j]==Q[j][i]
   qp=V.add(qp,{tuple(sorted((names[i],names[j]))):F(Q[i][j])})
 assert poly==qp,'direct polynomial differs from certificate matrix'
 assert rev=={m:c*(-1 if sum(i%2 for i in m)%2 else 1) for m,c in poly.items()},'coupled reflection congruence failed'
 piv=pd([[-x for x in r] for r in Q]);assert piv==w['negative_matrix_exact_ldl_pivots']
 # Flipping signs alone produces -Q, which is positive definite, not an obstruction.
 assert Q[0][0]<0 and (-Q[0][0])>0
 cut=sorted([-r['variable']*r['required_sign'] for r in w['records']],key=abs);assert cut==w['candidate_clause']
 source,pts=known54();rng=random.Random(20261104);cases=[];minimum_true=len(w['records']);largest_sum=None
 for sample in range(a.samples):
  targets=rng.sample(range(9),n);offsets=[rng.randrange(6) for _ in layers];direction=(-1,1)[sample%2];mirror=(-1,1)[(sample//2)%2]
  pp=mirrored_ccw(pts,mirror);mapping=dict(zip(layers,zip(targets,offsets)))
  def point(x):
   i,k=divmod(x,6);target,off=mapping[i];return pp[6*target+(direction*k+off)%6]
  values=[det(*(point(x) for x in r['triple'])) for r in w['records']];assert all(values)
  total=sum(v*r['required_sign']*direction*r['weight'] for v,r in zip(values,w['records']));assert total<0
  truecount=sum((v>0)!=(r['required_sign']*direction>0) for v,r in zip(values,w['records']));assert truecount>0
  minimum_true=min(minimum_true,truecount);largest_sum=total if largest_sum is None else max(largest_sum,total)
  cases.append({'targets':targets,'offsets':offsets,'direction_and_sign':direction,'mirror_ccw':mirror,'weighted_determinant_sum':total,'true_cut_literals':truecount})
 result={'status':'PASS','rigor':'exact polynomial plus exact rational positive-definiteness proof; finite exact-set regression tests','witness_sha256':sha(a.witness),'model_sha256':sha(a.model),'source_layers':layers,'support':len(w['records']),'candidate_clause':cut,'direct_symbolic_matrix':True,'exact_negative_definite':True,'coupled_reflection_congruence':True,'independent_sign_flip_positive_definite_negative_control':True,'exact54_sha256':sha(source),'exact54_tests':len(cases),'exact54_test_scope':'deterministic finite injective embeddings, not exhaustive','exact54_forbidden_matches':0,'exact54_min_true_literals':minimum_true,'exact54_largest_weighted_sum':largest_sum,'exact54_cases':cases,'elapsed_seconds':round(time.monotonic()-start,3)}
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='exact54_cases'}),flush=True)
if __name__=='__main__':main()
