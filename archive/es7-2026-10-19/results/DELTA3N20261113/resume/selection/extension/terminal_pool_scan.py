#!/usr/bin/env python3
"""Bounded finder on 315 fixed-coordinate terminal membership formulas.

Negative answers are explicitly uncertified until separately reconstructed
and replayed. Positive answers are checked geometrically here.
"""
import argparse,hashlib,importlib.util,json,os,resource,subprocess,time
from itertools import combinations as C
from pathlib import Path
HERE=Path(__file__).resolve().parent
sp=importlib.util.spec_from_file_location('parent_geometry',HERE.parent/'boundary/check_envelope.py');G=importlib.util.module_from_spec(sp);sp.loader.exec_module(G)
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cases',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(700<<20,700<<20));a.out.mkdir(parents=True,exist_ok=False)
 start=time.monotonic();out=[];stop='COMPLETE'
 for d in sorted(a.cases.iterdir()):
  if not d.is_dir() or '-v' in d.name:continue
  if time.monotonic()-start>900:stop='DEADLINE';break
  inp=json.loads((d/'input.json').read_text());P=inp['P'];m=len(P);n=inp['n'];cnf=d/'terminalsafe.cnf';variables=clauses=literals=count=0
  with cnf.open() as f:
   for line in f:
    if line.startswith('p '):_,_,v,c=line.split();variables=int(v);clauses=int(c)
    elif line.strip() and not line.startswith('c'):
     row=list(map(int,line.split()));assert row[-1]==0 and all(0<abs(x)<=m for x in row[:-1]);count+=1;literals+=len(row)-1
  assert variables==m and clauses==count
  estimated=literals*250
  rec={'name':d.name,'m':m,'n':n,'cnf_sha256':digest(cnf),'variables':variables,'clauses':clauses,'literals':literals,'estimated_solver_bytes':estimated}
  if estimated>600*(1<<20):rec['status']='NOT_LAUNCHED_MEMORY_ESTIMATE'
  else:
   dest=a.out/d.name;dest.mkdir();log=dest/'finder.log';cmd=['/usr/bin/timeout','--kill-after=1','5','/usr/bin/cadical','-t','3',str(cnf)];rec['command']=cmd
   with log.open('w') as f:p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=7)
   lines=log.read_text().splitlines();rec['returncode']=p.returncode;rec['finder_sha256']=digest(log)
   if 's UNSATISFIABLE' in lines:rec['status']='UNSAT_UNCERTIFIED'
   elif 's SATISFIABLE' in lines:
    A=tuple(sorted(x-1 for row in lines if row.startswith('v ') for x in map(int,row[2:].split()) if x>0));assert len(A)==len(set(A)) and all(i<m for i in A)
    full=G.maxima(P,range(m));selected=G.maxima(P,A);blue=G.maxima(P,[i for i in range(m) if i not in A]);assert full[0]<5 and full[2]<n and selected[0]<4 and blue[2]<n-1
    ranks={}
    for c in range(1,m):
     for b in range(c):ranks[b,c]=max([2]+[ranks[u,b]+1 for u in range(b) if G.det(P,u,b,c)<0])
    assert all(ranks[t[1],t[2]]>=4 for t in C(A,3) if G.det(P,*t)<0)
    rec.update(status='SAT_EXACT_MODEL_CHECKED',A=A,full_maxima=full,complement_maxima=blue)
   else:rec['status']='UNKNOWN'
  with cnf.open('rb') as f:os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
  out.append(rec)
  with (a.out/'cases.jsonl').open('a') as f:f.write(json.dumps(rec,sort_keys=True)+'\n')
  if len(out)%20==0:(a.out/'status.json').write_text(json.dumps({'checked':len(out),'seconds':round(time.monotonic()-start,3),'negatives':sum(x['status']=='UNSAT_UNCERTIFIED' for x in out)})+'\n')
 counts={s:sum(x['status']==s for x in out) for s in sorted({x['status'] for x in out})}
 result={'label':'COMPUTED','scope':'315 baseline fixed-coordinate instances only; no certificate from this finder.','stop':stop,'counts':counts,'seconds':round(time.monotonic()-start,3),'negative_cases':sorted([x for x in out if x['status']=='UNSAT_UNCERTIFIED'],key=lambda x:(x['n'],x['m'],x['name'])),'hashes':{'driver':digest(Path(__file__)),'cases.jsonl':digest(a.out/'cases.jsonl')}}
 (a.out/'DONE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'counts':counts,'stop':stop}),flush=True)
if __name__=='__main__':main()
