#!/usr/bin/env python3
"""Parent's independent exact cup-support witness and finite-count replay."""
import argparse,hashlib,importlib.util,json,resource,time
from itertools import combinations as C
from fractions import Fraction as Q
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('parent_geometry',HERE.parent/'boundary/check_envelope.py');G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cup_supports(P,A,cert):
 expected={t for t in C(A,3) if G.det(P,*t)<0};seen=set();nonterminal=0
 for row in cert:
  T=tuple(row['triple']);assert T in expected and T not in seen;seen.add(T);b,c=T[-2:]
  assert len(row['supports'])==1;s=row['supports'][0];K=tuple(s['fourcap']);assert len(K)==4 and K==tuple(sorted(set(K))) and all(0<=v<len(P) for v in K)
  assert all(G.det(P,*t)<0 for t in C(K,3)) and Q(s['weight'])==1
  u,v=K[-2:]
  if (u,v)!=(b,c):
   assert u>=b and v>=c and all(G.det(P,*t)>0 for t in C(sorted(set((b,c,u,v))),3));nonterminal+=1
  q=G.line(P,(b,c));ell=G.line(P,(u,v));assert ell[0]>=q[0] and ell[1]>=q[1]
 assert seen==expected;return len(seen),nonterminal
def full_count(P,n):
 m=len(P);allmask=(1<<m)-1
 def cap(t):return all(G.det(P,*s)<0 for s in C(t,3))
 def convex(q):
  def chain(order):
   st=[]
   for v in order:
    while len(st)>=2 and G.det(P,st[-2],st[-1],v)<=0:st.pop()
    st.append(v)
   return st
  return len(chain(q))+len(chain(reversed(q)))-2==len(q)
 caps=[t for t in C(range(m),4) if cap(t)];targets=[t for t in C(range(m),n-1) if convex(t)];ends={K[-2:] for K in caps}
 bad=[]
 for T in C(range(m),3):
  if not cap(T):continue
  b,c=T[-2:]
  ok=(b,c) in ends or any(u>=b and v>=c and all(G.det(P,*t)>0 for t in C(sorted(set((b,c,u,v))),3)) for u,v in ends)
  if not ok:bad.append(T)
 def contains(family):
  B=bytearray(1<<m)
  for t in family:B[sum(1<<i for i in t)]=1
  for i in range(m):
   bit=1<<i
   for s in range(1<<m):
    if s&bit:B[s]|=B[s^bit]
  return B
 ca,ta,ba=map(contains,(caps,targets,bad));ordinary=protected=0;minimum=m+1;mincount=0
 for s in range(1<<m):
  if ca[s] or ta[allmask^s]:continue
  ordinary+=1
  if ba[s]:continue
  protected+=1;k=s.bit_count()
  if k<minimum:minimum=k;mincount=0
  if k==minimum:mincount+=1
 return {'ordinary_count':ordinary,'cup_protected_count':protected,'minimum_cup_protected_size':minimum,'minimum_cardinality_count':mincount,'assignments_checked':1<<m}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(350<<20,350<<20));a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic();rows=[];total=nonterminal=0
 dirs=sorted((a.root/'pool-v1/cases').iterdir())+sorted((a.root/'known-v1/cases').iterdir())+[a.root/'real15-v1/cup']
 for d in dirs:
  x=json.loads((d/'input.json').read_text());P=x['P'];n=x['n'];m=len(P);A=tuple(json.loads((d/'model.json').read_text())['A'])
  assert all(type(z)is int for p in P for z in p) and all(P[i][0]<P[i+1][0] for i in range(m-1));assert all(G.det(P,*t)!=0 for t in C(range(m),3));assert A==tuple(sorted(set(A))) and all(0<=i<m for i in A)
  full=G.maxima(P,range(m));selected=G.maxima(P,A);blue=G.maxima(P,[i for i in range(m) if i not in A]);assert full[0]<5 and full[2]<n and selected[0]<4 and blue[2]<n-1
  count,proper=cup_supports(P,A,json.loads((d/'certificates.json').read_text()));total+=count;nonterminal+=proper
  rows.append({'case':str(d),'m':m,'n':n,'A':A,'full_maxima':full,'cap_triples_checked':count,'nonterminal_supports':proper,'hashes':{f:sha(d/f) for f in ['input.json','model.json','certificates.json']}})
  with (a.out/'cases.jsonl').open('a') as f:f.write(json.dumps(rows[-1])+'\n')
 counts=[]
 for p in sorted((a.root/'structure-v1').glob('*_exact_counts.json')):
  x=json.loads(p.read_text());got=full_count(x['P'],x['n']);assert all(got[k]==x[k] for k in got);cup_supports(x['P'],x['minimum_A'],x['certificates']);counts.append({'source':str(p),'source_sha256':sha(p),**got})
 out={'label':'COMPUTED independent exact positive-witness and finite-enumeration replay','verdict':'PASS','cases':len(rows),'cap_triples_checked':total,'nonterminal_supports':nonterminal,'full_enumerations':counts,'seconds':round(time.monotonic()-start,3),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'hashes':{'checker':sha(Path(__file__)),'parent_geometry':sha(HERE.parent/'boundary/check_envelope.py'),'cases.jsonl':sha(a.out/'cases.jsonl')},'scope':'Explicit fixed inputs only. Orientation-cell persistence additionally uses the written cup-domination lemma.'}
 (a.out/'DONE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
