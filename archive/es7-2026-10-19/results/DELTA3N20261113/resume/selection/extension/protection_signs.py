#!/usr/bin/env python3
"""Recompute all selections from triple signs, without SAT auxiliary flags."""
import argparse,hashlib,itertools,json,resource,time
from collections import Counter
from pathlib import Path
C=itertools.combinations
def bits(S):return sum(1<<i for i in S)
def upward(m,seeds):
 a=bytearray(1<<m)
 for s in seeds:a[s]=1
 for i in range(m):
  b=1<<i
  for s in range(1<<m):
   if s&b:a[s]|=a[s^b]
 return a
def analyze(signs,m,n):
 triples=list(C(range(m),3));assert len(signs)==len(triples)
 t={q:1 if s=='+' else -1 for q,s in zip(triples,signs)}
 def ori(a,b,c):
  q=(a,b,c);return t[tuple(sorted(q))]*(-1 if sum(q[i]>q[j] for i in range(3) for j in range(i+1,3))%2 else 1)
 def cup(q):return all(t[z]>0 for z in C(q,3))
 def cap(q):return all(t[z]<0 for z in C(q,3))
 def convex4(q):
  for p in q:
   a,b,c=(v for v in q if v!=p)
   v=[ori(a,b,p),ori(b,c,p),ori(c,a,p)]
   if v[0]==v[1]==v[2]:return False
  return True
 nonconvex=upward(m,[bits(q) for q in C(range(m),4) if not convex4(q)])
 caps4=[q for q in C(range(m),4) if cap(q)]
 caps5=[q for q in C(range(m),5) if cap(q)]
 targets=[q for q in C(range(m),n-1) if not nonconvex[bits(q)]]
 ngons=[q for q in C(range(m),n) if not nonconvex[bits(q)]]
 assert not caps5 and not ngons
 ends={q[-2:] for q in caps4};pairs=list(C(range(m),2));cov={'terminal':ends,'cup':set(),'forced':set()}
 for b,c in pairs:
  for u,v in ends:
   if b<=u and c<=v and cup(tuple(sorted({b,c,u,v}))):cov['cup'].add((b,c))
   if v>=c and (v==c or t[b,c,v]>0) and (u==b or (u>b and t[b,u,v]>0) or (u<b and t[u,b,c]<0)):
    cov['forced'].add((b,c))
 assert cov['terminal']<=cov['cup']<=cov['forced']
 bad={k:[q for q in triples if t[q]<0 and q[-2:] not in pairs] for k,pairs in cov.items()}
 F=upward(m,map(bits,caps4));T=upward(m,map(bits,targets));full=(1<<m)-1
 families={'weak':[s for s in range(1<<m) if not F[s] and not T[full^s]]}
 for k in cov:
  D=upward(m,map(bits,bad[k]));families[k]=[s for s in families['weak'] if not D[s]]
 report={'m':m,'n':n,'caps4':len(caps4),'caps5':len(caps5),'targets':len(targets),'ngons':len(ngons),'ambient_terminal_pairs':len(ends),'covered_pairs':{k:len(v) for k,v in cov.items()},'bad_triples':{k:len(v) for k,v in bad.items()},'all_memberships':1<<m,'families':{k:{'count':len(v),'minimum':min(map(int.bit_count,v),default=None),'size_counts':dict(sorted(Counter(s.bit_count() for s in v).items())),'one_minimum':min(v,key=lambda s:(s.bit_count(),s)) if v else None} for k,v in families.items()}}
 return report,dict(caps4=caps4,targets=targets,bad=bad,families=families)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--signs',type=Path,required=True);ap.add_argument('--m',type=int,required=True);ap.add_argument('--n',type=int,default=7);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));resource.setrlimit(resource.RLIMIT_CPU,(25,25));start=time.monotonic();a.out.mkdir(parents=True,exist_ok=False)
 report,families=analyze(a.signs.read_text().strip(),a.m,a.n);report.update(label='COMPUTED abstract orientation semantics',seconds=time.monotonic()-start,source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),signs_sha256=hashlib.sha256(a.signs.read_bytes()).hexdigest(),scope='No real geometry claim before exact realization; no uniform-envelope claim from these orientation-only predicates.')
 (a.out/'report.json').write_text(json.dumps(report,indent=2)+'\n');(a.out/'families.json').write_text(json.dumps(families)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
