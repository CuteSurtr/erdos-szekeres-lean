#!/usr/bin/env python3
"""Exact restrictions of a retained realization; no size monotonicity inference."""
import argparse,hashlib,itertools,json,resource,time
from pathlib import Path
from protection_signs import analyze
def det(P,a,b,c):return (P[b][0]-P[a][0])*(P[c][1]-P[a][1])-(P[b][1]-P[a][1])*(P[c][0]-P[a][0])
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--input',type=Path,required=True);ap.add_argument('--size',type=int,required=True);ap.add_argument('--n',type=int,default=7);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20));resource.setrlimit(resource.RLIMIT_CPU,(25,25));start=time.monotonic();a.out.mkdir(parents=True,exist_ok=False)
 P=json.loads(a.input.read_text())['P'];results=[]
 for case,old in enumerate(itertools.combinations(range(len(P)),a.size)):
  Q=[P[i] for i in old];values=[det(Q,*t) for t in itertools.combinations(range(a.size),3)];assert all(values)
  signs=''.join('+' if v>0 else '-' for v in values);report,families=analyze(signs,a.size,a.n)
  row=dict(case=case,local_to_original=old,P=Q,orientation_signs=signs,**report);results.append(row)
  if not families['families']['terminal']:
   d=a.out/str(case);d.mkdir();(d/'witness.json').write_text(json.dumps(row,indent=2)+'\n')
   for kind in ['terminal','cup','forced']:
    clauses=[[-i-1 for i in q] for q in families['caps4']+families['bad'][kind]]+[[i+1 for i in q] for q in families['targets']]
    (d/(kind+'.cnf')).write_text(f'p cnf {a.size} {len(clauses)}\n'+''.join(' '.join(map(str,C))+' 0\n' for C in clauses))
 result={'label':'COMPUTED exact sign enumeration on real restrictions','size':a.size,'n':a.n,'cases':results,'failures':{k:[r['case'] for r in results if not r['families'][k]['count']] for k in ['terminal','cup','forced']},'seconds':time.monotonic()-start,'input_sha256':hashlib.sha256(a.input.read_bytes()).hexdigest(),'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'semantic_checker_sha256':hashlib.sha256((Path(__file__).parent/'protection_signs.py').read_bytes()).hexdigest()}
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'}))
if __name__=='__main__':main()
