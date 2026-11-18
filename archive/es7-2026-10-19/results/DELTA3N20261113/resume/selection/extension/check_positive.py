#!/usr/bin/env python3
"""Independent exact replay of fixed-coordinate uniform-Delta witnesses.

Uses the parent's earlier endpoint-chain DP, not the envelope track's
geometry, SAT, or certificate checker. Reads no solver verdict as evidence.
"""
import argparse,hashlib,importlib.util,json,os,resource,time
from fractions import Fraction as Q
from itertools import combinations as C
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('parent_geometry',HERE.parent/'boundary/check_envelope.py')
G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def release(p):
 with p.open('rb') as f:os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cases',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20));a.out.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();cache={};records=[];counts={'two_support':0,'one_support':0};orientation_groups=set()
 for d in sorted(a.cases.iterdir()):
  if not d.is_dir():continue
  inp=json.loads((d/'input.json').read_text());P=inp['P'];n=inp['n'];m=len(P)
  assert all(len(p)==2 and all(type(z)is int for z in p) for p in P)
  assert all(P[i][0]<P[i+1][0] for i in range(m-1))
  signs=tuple(1 if G.det(P,*t)>0 else -1 if G.det(P,*t)<0 else 0 for t in C(range(m),3))
  assert 0 not in signs;otype=(m,signs);orientation_groups.add(otype)
  A=tuple(json.loads((d/'model.json').read_text())['A']);assert A==tuple(sorted(set(A))) and all(0<=i<m for i in A)
  B=tuple(i for i in range(m) if i not in A)
  def maxima(S):
   key=(otype,tuple(S))
   if key not in cache:cache[key]=G.maxima(P,S)
   return cache[key]
  full=maxima(range(m));sel=maxima(A);blue=maxima(B)
  assert full[0]<5 and full[2]<n and sel[0]<4 and blue[2]<n-1
  expected={t for t in C(A,3) if G.det(P,*t)<0};seen=set()
  cert=json.loads((d/'certificates.json').read_text())
  for row in cert:
   T=tuple(row['triple']);assert T in expected and T not in seen;seen.add(T)
   q=G.line(P,T[-2:]);s=z=Q(0);weights=[];supports=row['supports'];assert 1<=len(supports)<=2
   for item in supports:
    K=tuple(item['fourcap']);assert len(K)==4 and K==tuple(sorted(set(K))) and all(0<=i<m for i in K)
    assert all(G.det(P,*t)<0 for t in C(K,3))
    w=Q(item['weight']);assert w>=0;weights.append(w);ell=G.line(P,K[-2:]);s+=w*ell[0];z+=w*ell[1]
   assert sum(weights)==1 and s>=q[0] and z>=q[1]
   counts['one_support' if len(supports)==1 else 'two_support']+=1
  assert seen==expected
  files=['input.json','model.json','certificates.json']
  rec={'name':d.name,'n':n,'m':m,'A':A,'full_maxima':full,'selected_maxima':sel,'complement_maxima':blue,'cap_triples':len(seen),'hashes':{f:sha(d/f) for f in files}}
  records.append(rec)
  with (a.out/'cases.jsonl').open('a') as f:f.write(json.dumps(rec,sort_keys=True)+'\n')
  for f in files:release(d/f)
  if len(records)%50==0:
   (a.out/'status.json').write_text(json.dumps({'checked':len(records),'seconds':round(time.monotonic()-start,3)})+'\n')
 out={'label':'COMPUTED independent exact positive-witness checks','scope':'Only the explicitly listed fixed realizations, not a universal existence theorem or a full CNF audit.','cases_checked':len(records),'orientation_groups':len(orientation_groups),'certificates':counts,'seconds':round(time.monotonic()-start,3),'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'hashes':{'checker':sha(Path(__file__)),'parent_geometry':sha(HERE.parent/'boundary/check_envelope.py'),'cases.jsonl':sha(a.out/'cases.jsonl')},'verdict':'PASS'}
 (a.out/'DONE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out),flush=True)
if __name__=='__main__':main()
