#!/usr/bin/env python3
"""Parent's independent exact GP-product replay, without any finder import."""
from collections import Counter
from itertools import combinations
from pathlib import Path
import copy,hashlib,json,resource

H=Path(__file__).resolve().parent
S=H.parent/'forced16_realization/data/orientation.signs'
C=H.parent/'forced16_realization/data/certificate.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def bracket_poly(a,b,c):
 # Expanded homogeneous determinant, x_i is2i, y_i is2i+1.
 p=Counter()
 for u,v,sg in [(a,b,1),(b,c,1),(c,a,1),(a,c,-1),(b,a,-1),(c,b,-1)]:
  p[tuple(sorted((2*u,2*v+1)))]+=sg
 return {m:v for m,v in p.items() if v}
def product(p,q):
 r=Counter()
 for a,u in p.items():
  for b,v in q.items():r[tuple(sorted(a+b))]+=u*v
 return r
def identity():
 out=Counter()
 for s,p,q in [(1,(0,1,2),(0,3,4)),(-1,(0,1,3),(0,2,4)),(1,(0,1,4),(0,2,3))]:
  for mon,v in product(bracket_poly(*p),bracket_poly(*q)).items():out[mon]+=s*v
 assert all(v==0 for v in out.values())
 return len(out)
def check(cert,signs):
 assert len(signs)==560 and set(signs)<={'+','-'}
 triples=list(combinations(range(16),3));sg={t:1 if s=='+' else -1 for t,s in zip(triples,signs)}
 def orient(t):
  a,b,c=sorted(t)
  return sg[a,b,c]*(1 if tuple(t) in [(a,b,c),(b,c,a),(c,a,b)] else -1)
 totals=Counter();rows=[]
 for row in cert['rows']:
  a=row['root'];b,c,d,e=row['other'];assert len({a,b,c,d,e})==5 and all(type(v)is int and 0<=v<16 for v in [a,b,c,d,e])
  L=row['large'];T=row['small'];w=row['weight'];assert type(w)is int and w>0 and L in range(3) and T in range(3) and L!=T
  factors=[[(a,b,c),(a,d,e)],[(a,b,d),(a,c,e)],[(a,b,e),(a,c,d)]]
  terms=[orient(p)*orient(q)*(-1 if i==1 else 1) for i,(p,q) in enumerate(factors)]
  assert all(terms[j]==-terms[L] for j in range(3) if j!=L)
  for q in factors[L]:totals[tuple(sorted(q))]+=w
  for q in factors[T]:totals[tuple(sorted(q))]-=w
  rows.append(dict(labels=[a,b,c,d,e],weight=w,larger=[sorted(t) for t in factors[L]],smaller=[sorted(t) for t in factors[T]]))
 assert rows and all(totals[t]==0 for t in triples)
 return rows
def main():
 resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20))
 cert=json.loads(C.read_text());assert cert['signs_sha256']==sha(S);signs=S.read_text().strip();monomials=identity();rows=check(cert,signs)
 mutants=[]
 for kind in ['weight','reverse']:
  bad=copy.deepcopy(cert)
  if kind=='weight':bad['rows'][0]['weight']+=1
  else:bad['rows'][0]['large'],bad['rows'][0]['small']=bad['rows'][0]['small'],bad['rows'][0]['large']
  try:check(bad,signs)
  except AssertionError:mutants.append(kind)
  else:raise AssertionError('corrupted certificate accepted')
 result={'label':'PROVED written algebraic contradiction with parent exact replay','status':'PASS','rows':len(rows),'positive_weight_sum':sum(r['weight'] for r in rows),'minimum_weight':min(r['weight'] for r in rows),'maximum_weight':max(r['weight'] for r in rows),'all_560_exponents_cancel':True,'symbolic_GP_identity_zero':True,'symbolic_monomial_slots':monomials,'rejected_mutants':mutants,'hashes':{'signs':sha(S),'certificate':sha(C),'checker':sha(Path(__file__))},'scope':'This fixed orientation model is nonrealizable over the real plane. Other models and general selection conjectures are not decided. No Lean or cake claim.'}
 (H/'result.json').write_text(json.dumps(result,indent=2)+'\n');(H/'reconstructed_rows.json').write_text(json.dumps(rows,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
