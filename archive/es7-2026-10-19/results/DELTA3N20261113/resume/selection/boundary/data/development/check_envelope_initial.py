#!/usr/bin/env python3
"""Independent checks of the envelope track's positive exact witnesses.

No track geometry code is imported. Target exclusion uses endpoint chain
dynamic programming, whereas the track enumerates convex hulls.
"""
from fractions import Fraction as Q
from itertools import combinations as C
import hashlib,json,resource
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def det(P,a,b,c):
 return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
def cap(P,S):return all(det(P,*t)<0 for t in C(S,3))
def maxima(P,S):
 S=list(S)
 if len(S)<2:return len(S),len(S),len(S)
 maxcap=maxcup=maxgon=2
 for ia,a in enumerate(S[:-1]):
  up={};lo={}
  for ic in range(ia+1,len(S)):
   c=S[ic];up[(a,c)]=lo[(a,c)]=2
   for ib in range(ia+1,ic):
    b=S[ib]
    up[(b,c)]=max([up[(p,b)]+1 for p in S[ia:ib] if det(P,p,b,c)<0],default=0)
    lo[(b,c)]=max([lo[(p,b)]+1 for p in S[ia:ib] if det(P,p,b,c)>0],default=0)
   u=max(up[(b,c)] for b in S[ia:ic]);l=max(lo[(b,c)] for b in S[ia:ic])
   maxcap=max(maxcap,u);maxcup=max(maxcup,l);maxgon=max(maxgon,u+l-2)
 return maxcap,maxcup,maxgon
def line(P,pair):
 a,b=pair;s=Q(P[b][1]-P[a][1],P[b][0]-P[a][0])
 return s,Q(P[b][1])+s*(P[-1][0]-P[b][0])
def certificates(P,A,rows):
 expected={t for t in C(A,3) if cap(P,t)};seen=set()
 for row in rows:
  t=tuple(row['triple']);assert t in expected and t not in seen;seen.add(t)
  q=line(P,t[-2:]);assert q==tuple(map(Q,row['line']))
  weights=[];s=z=Q(0)
  for item in row['supports']:
   K=item['ambient_fourcap'];pair=item['pair'];assert len(K)==4 and cap(P,K) and K[-2:]==pair
   ell=line(P,pair);assert ell==tuple(map(Q,item['line']))
   w=Q(item['weight']);assert w>=0;weights.append(w);s+=w*ell[0];z+=w*ell[1]
  assert len(weights) in (1,2) and sum(weights)==1 and s>=q[0] and z>=q[1]
 assert seen==expected
 return len(seen)
def main():
 resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20));resource.setrlimit(resource.RLIMIT_CPU,(18,18))
 data=HERE/'envelope/data';inputs=json.loads((data/'inputs.json').read_text());results=[]
 for r in inputs:
  P=r['P'];n=r['n'];m=len(P);report=json.loads((data/f'cases/{r["name"]}.json').read_text())
  assert all(type(z)is int for p in P for z in p)
  assert all(P[i][0]<P[i+1][0] for i in range(m-1))
  assert all(det(P,*t) for t in C(range(m),3))
  full=maxima(P,range(m));assert full[0]<5 and full[2]<n
  assert report['result']['outcome']=='SAT_EXACT_MODEL_CHECKED'
  A=report['result']['A'];assert maxima(P,A)[0]<4
  blue=tuple(i for i in range(m) if i not in A);remaining=maxima(P,blue)
  assert remaining[2]<n-1
  count=certificates(P,A,report['all_X_certificates'])
  results.append({'name':r['name'],'m':m,'n':n,'A':A,'full_maxima':full,
                  'complement_maxima':remaining,'all_X_cap_triples_checked':count,
                  'report_sha256':sha(data/f'cases/{r["name"]}.json')})
 small=json.loads((data/'cases/small_controls.json').read_text())
 s=small['fourcap_clauses_needed'];P=s['P'];A=s['A']
 assert cap(P,A) and maxima(P,range(len(P)))[0]<5
 certificates(P,A,s['certificates'])
 z=small['uniform_repair'];P=z['P'];A=z['A'];B=z['repaired_A']
 assert maxima(P,A)[0]<4 and maxima(P,B)[0]<4
 assert maxima(P,[i for i in range(len(P)) if i not in B])[2]<z['n']-1
 out={'label':'COMPUTED independent positive-witness verification',
      'script_sha256':sha(Path(__file__)),'inputs_sha256':sha(data/'inputs.json'),
      'cases':results,'old_fourcap_is_independent_requirement':True,'repair_control':True,
      'scope':'Positive Delta models and rational domination certificates; not all exposure classifications or CNF clauses.'}
 (HERE/'data/envelope_parent_checks.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps({'positive_cases':len(results),'cap_triple_certificates':sum(r['all_X_cap_triples_checked'] for r in results),'small_controls':'PASS'}))
if __name__=='__main__':main()
