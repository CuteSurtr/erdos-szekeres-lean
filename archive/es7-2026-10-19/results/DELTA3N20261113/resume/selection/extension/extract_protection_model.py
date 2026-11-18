#!/usr/bin/env python3
"""Stream-check a SAT assignment, then export its ordered orientation signs."""
import argparse,hashlib,itertools,json,resource,time
from pathlib import Path

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--map',type=Path,required=True);ap.add_argument('--m',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));resource.setrlimit(resource.RLIMIT_CPU,(25,25));start=time.monotonic();a.out.mkdir(parents=True,exist_ok=False)
 assignment={};sat=False
 with (a.run/'cadical.log').open() as f:
  for line in f:
   if line.strip()=='s SATISFIABLE':sat=True
   if not line.startswith('v '):continue
   for z in map(int,line.split()[1:]):
    if not z:continue
    assert abs(z) not in assignment or assignment[abs(z)]==(z>0)
    assignment[abs(z)]=z>0
 assert sat
 rows=0
 with (a.run/'input.cnf').open() as f:
  for line in f:
   if line.startswith('c') or not line.strip():continue
   if line.startswith('p'):
    _,_,nv,nc=line.split();nv=int(nv);nc=int(nc);continue
   row=list(map(int,line.split()));assert row[-1]==0
   assert any(assignment[abs(z)]==(z>0) for z in row[:-1]),rows
   rows+=1
 assert rows==nc and set(assignment)==set(range(1,nv+1))
 signs={}
 with a.map.open() as f:
  for line in f:
   if line.startswith('#'):continue
   i,k,s=line.split()
   if k=='orientation':signs[int(s)]=assignment[int(i)]
 triples=list(itertools.combinations(range(a.m),3));assert len(signs)==len(triples)
 ordered=''.join('+' if signs[sum(1<<i for i in t)] else '-' for t in triples)
 (a.out/'orientation.signs').write_text(ordered+'\n')
 result={'label':'COMPUTED','status':'SAT_MODEL_FULL_CLAUSE_REPLAY_PASS','m':a.m,'variables':nv,'clauses':nc,'orientation_count':len(signs),'seconds':round(time.monotonic()-start,3),'hashes':{str(p):sha(p) for p in [a.run/'input.cnf',a.run/'cadical.log',a.map,Path(__file__),a.out/'orientation.signs']},'scope':'Full Boolean model replay only. Exact realization and geometric protection predicates still require separate checks.'}
 (a.out/'model.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
