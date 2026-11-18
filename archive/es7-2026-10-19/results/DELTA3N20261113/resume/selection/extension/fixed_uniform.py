#!/usr/bin/env python3
"""Exact fixed geometry/envelopes, with independent line-intersection replay."""
import argparse,hashlib,importlib.util,itertools,json,resource,time
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
from fixed_protection import det,convex,upward
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--n',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20));resource.setrlimit(resource.RLIMIT_CPU,(25,25));start=time.monotonic();a.out.mkdir(parents=True,exist_ok=False)
 src=Path(__file__).parent/'envelope/tools/exact.py';spec=importlib.util.spec_from_file_location('envelope_exact',src);E=importlib.util.module_from_spec(spec);spec.loader.exec_module(E)
 P=json.loads(a.input.read_text())['P'];m=len(P);C=itertools.combinations;V=range(m);full=(1<<m)-1;d={t:det(P,*t) for t in C(V,3)};assert all(d.values()) and all(P[i][0]<P[i+1][0] for i in range(m-1))
 cap=lambda q:all(d[t]<0 for t in C(q,3))
 assert not any(cap(q) for q in C(V,5)) and not any(convex(P,q) for q in C(V,a.n))
 g={'m':m,'n':a.n,'caps3':[t for t,z in d.items() if z<0],'caps4':[q for q in C(V,4) if cap(q)],'targets':[q for q in C(V,a.n-1) if convex(P,q)]}
 report,states=E.build(P,g)
 def line(pair):
  u,v=pair;s=F(P[v][1]-P[u][1],P[v][0]-P[u][0]);return s,F(P[v][1])+s*(P[-1][0]-P[v][0])
 lines={q[-2:]:line(q[-2:]) for q in g['caps4']};tests={F(0)}
 for (s,z),(u,w) in C(lines.values(),2):
  if s!=u:
   t=(w-z)/(s-u)
   if t>0:tests.add(t)
 for pair,state in states.items():
  s,z=line(pair);safe=bool(lines) and s<=max(u for u,w in lines.values()) and all(s*t+z<=max(u*t+w for u,w in lines.values()) for t in tests)
  assert safe==state['safe']
  if safe:
   supports=[(tuple(pair),F(weight)) for pair,weight in state['supports']];assert sum(w for p,w in supports)==1 and all(w>=0 for p,w in supports)
   assert sum(lines[p][0]*w for p,w in supports)>=s and sum(lines[p][1]*w for p,w in supports)>=z
  else:
   t=F(state['witness_t']);assert t>0 and all(s*t+z>u*t+w for u,w in lines.values())
 CA,TA,BA=[upward(m,g[k] if k!='bad' else report['exposed_triples']) for k in ['caps4','targets','bad']]
 weak=[s for s in range(full+1) if not CA[s] and not TA[full^s]];uniform=[s for s in weak if not BA[s]]
 minimum=min(map(int.bit_count,uniform),default=None);mins=[s for s in uniform if s.bit_count()==minimum]
 A=[i for i in V if mins and mins[0]>>i&1];cert=E.certificate(P,g,states,A) if mins else None
 clauses=[[-i-1 for i in q] for q in g['caps4']+report['exposed_triples']]+[[i+1 for i in q] for q in g['targets']]
 cnf=a.out/'uniform.cnf';cnf.write_text(f'p cnf {m} {len(clauses)}\n'+''.join(' '.join(map(str,r))+' 0\n' for r in clauses))
 result={'label':'COMPUTED exact geometry, rational envelopes, complete fixed memberships','m':m,'n':a.n,'P':P,'weak_count':len(weak),'uniform_count':len(uniform),'uniform_minimum':minimum,'minimum_count':len(mins),'minimum_witness':A if mins else None,'minimum_certificate':cert,'exposed_triples':len(report['exposed_triples']),'ambient_lines':len(lines),'safe_pair_count':sum(v['safe'] for v in states.values()),'tested_terminal_pairs':len(states),'independent_intersection_tests':len(tests),'all_pair_certificates_replayed':True,'seconds':time.monotonic()-start,'hashes':{'input':hashlib.sha256(a.input.read_bytes()).hexdigest(),'source':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'envelope_source':hashlib.sha256(src.read_bytes()).hexdigest(),'cnf':hashlib.sha256(cnf.read_bytes()).hexdigest()},'scope':'Exactly this coordinate set and n. No global selection or existence-invariance claim.'}
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(a.out/'exposure.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'families.json').write_text(json.dumps(dict(weak=weak,uniform=uniform,minimum=mins))+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['P','minimum_certificate']}))
if __name__=='__main__':main()
