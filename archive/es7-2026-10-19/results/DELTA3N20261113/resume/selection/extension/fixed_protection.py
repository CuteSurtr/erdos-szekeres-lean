#!/usr/bin/env python3
"""Exact integer geometry and fixed cup/forced membership formulas."""
import argparse,hashlib,itertools,json,resource,time
from collections import Counter
from pathlib import Path
C=itertools.combinations
def det(P,a,b,c):
 return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
def convex(P,q):
 def chain(seq):
  out=[]
  for i in seq:
   while len(out)>1 and det(P,out[-2],out[-1],i)<=0:out.pop()
   out.append(i)
  return out
 return len(chain(q))+len(chain(reversed(q)))-2==len(q)
def upward(m,sets):
 a=bytearray(1<<m)
 for q in sets:a[sum(1<<i for i in q)]=1
 for i in range(m):
  b=1<<i
  for s in range(1<<m):
   if s&b:a[s]|=a[s^b]
 return a
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--n',type=int,default=7);ap.add_argument('--kind',choices=['cup','forced'],required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));resource.setrlimit(resource.RLIMIT_CPU,(25,25));start=time.monotonic();a.out.mkdir(parents=True,exist_ok=False)
 raw=json.loads(a.input.read_text());P=raw['P'];m=len(P);V=range(m);full=(1<<m)-1
 assert all(type(v)is int for p in P for v in p) and all(P[i][0]<P[i+1][0] for i in range(m-1))
 triples=list(C(V,3));dets={q:det(P,*q) for q in triples};assert all(dets.values())
 signs=''.join('+' if dets[t]>0 else '-' for t in triples);assert signs==raw['orientation_signs']
 cup=lambda q:all(dets[t]>0 for t in C(q,3));cap=lambda q:all(dets[t]<0 for t in C(q,3))
 caps=[q for q in C(V,4) if cap(q)];assert not any(cap(q) for q in C(V,5))
 targets=[q for q in C(V,a.n-1) if convex(P,q)];assert not any(convex(P,q) for q in C(V,a.n))
 ends={q[-2:] for q in caps};covered=set()
 for b,c in C(V,2):
  for u,v in ends:
   if a.kind=='cup':works=b<=u and c<=v and cup(tuple(sorted({b,c,u,v})))
   else:works=v>=c and (v==c or det(P,b,c,v)>0) and (u==b or (u>b and det(P,b,u,v)>0) or (u<b and det(P,u,b,c)<0))
   if works:covered.add((b,c));break
 bad=[q for q in triples if dets[q]<0 and q[-2:] not in covered]
 F,D,T=[upward(m,q) for q in [caps,bad,targets]]
 weak=[s for s in range(full+1) if not F[s] and not T[full^s]];good=[s for s in weak if not D[s]]
 rows=[[-i-1 for i in q] for q in caps+bad]+[[i+1 for i in q] for q in targets]
 cnf=a.out/'membership.cnf';cnf.write_text(f'p cnf {m} {len(rows)}\n'+''.join(' '.join(map(str,row))+' 0\n' for row in rows))
 # The second complete replay checks the actual membership clauses.
 for s in range(full+1):
  sat=all(any(bool(s>>(abs(z)-1)&1)==(z>0) for z in row) for row in rows)
  assert sat==(not F[s] and not D[s] and not T[full^s])
 report={'label':'COMPUTED exact integer geometry and exhaustive membership','m':m,'n':a.n,'kind':a.kind,'P':P,'minimum_abs_det':min(map(abs,dets.values())),'caps4':len(caps),'bad_triples':len(bad),'targets':len(targets),'terminal_pairs':len(ends),'covered_pairs':len(covered),'weak_deltas':len(weak),'protected_deltas':len(good),'minimum_weak_size':min(map(int.bit_count,weak),default=None),'minimum_protected_size':min(map(int.bit_count,good),default=None),'all_memberships_checked':full+1,'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),'input_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'seconds':time.monotonic()-start}
 (a.out/'result.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'families.json').write_text(json.dumps(dict(caps=caps,targets=targets,bad=bad,covered=sorted(covered),weak=weak,protected=good))+'\n');print(json.dumps({k:v for k,v in report.items() if k!='P'}))
if __name__=='__main__':main()
