#!/usr/bin/env python3
"""Generate all sixteen sound GP sign clauses for reported violated identities.

Every emitted clause receives six exact tests on the certified54 point set.
The proof is the determinant GP identity: three nonzero summands cannot all
have the same sign. Tests corroborate the implementation of that argument.
"""
import argparse,hashlib,importlib.util,itertools,json
from pathlib import Path


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--model',required=True,type=Path);ap.add_argument('--violations',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 results=Path(__file__).resolve().parent.parent
 spec=importlib.util.spec_from_file_location('reference',results/'C7UPPER/gen.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 e=mod.Enc(6,8,10);positive=set(json.loads(a.model.read_text()));clauses=set();relations=0
 for line in a.violations.read_text().splitlines():
  p,b,c,d,f=map(int,line.split())
  ll=[e.o(p,b,c),e.o(p,d,f),e.o(p,b,d),e.o(p,c,f),e.o(p,b,f),e.o(p,c,d)]
  sg=[(1 if l>0 else -1)*(1 if abs(l) in positive else -1) for l in ll]
  assert sg[0]*sg[1]==-sg[2]*sg[3]==sg[4]*sg[5];relations+=1
  for s in (-1,1):
   for b1,b2,b3 in itertools.product((-1,1),repeat=3):
    vals=(b1,b1*s,b2,-b2*s,b3,b3*s)
    assert vals[0]*vals[1]==-vals[2]*vals[3]==vals[4]*vals[5]
    cl=set(-l if v>0 else l for l,v in zip(ll,vals))
    if not any(-l in cl for l in cl):clauses.add(tuple(sorted(cl,key=lambda x:(abs(x),x))))
 ordered=sorted(clauses);dest=a.out/'gp_refinement.clauses';dest.write_text(''.join(' '.join(map(str,c))+' 0\n' for c in ordered))
 raw=(results/'ES8SYM/sets/c6_54pts_9layers.pts').read_bytes();pts=[]
 for line in raw.decode().splitlines():
  if not line.strip() or line.startswith('#'):continue
  x,y,z,u,v,w=map(int,line.split());pts.append((2*x+y-z-2*u-v+w,y+z-v-w))
 det=lambda a,b,c:(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0]);reps={v:q for q,v in e.tvar.items()};checks=0
 for cl in ordered:
  layers=sorted({x//6 for v in cl for x in reps[abs(v)]});assert len(layers)<=5
  for offset in (0,2,4):
   mapping={layer:(i+offset)%9 for i,layer in enumerate(layers)}
   for flip in (-1,1):
    def val(v):
     q=reps[abs(v)];d=det(*(pts[6*mapping[x//6]+x%6] for x in q));assert d
     return (d*flip>0)==(v>0)
    assert any(val(v) for v in cl);checks+=1
 summary={'model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),'violations_sha256':hashlib.sha256(a.violations.read_bytes()).hexdigest(),'verified_violated_relations':relations,'unique_clauses':len(ordered),'direct_exact54_clause_tests':checks,'exact54_sha256':hashlib.sha256(raw).hexdigest(),'family_sha256':hashlib.sha256(dest.read_bytes()).hexdigest(),'proof':'GP identity, uniform brackets and exact literal substitution'}
 (a.out/'gp_refinement_verified.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,sort_keys=True))
if __name__=='__main__':main()
