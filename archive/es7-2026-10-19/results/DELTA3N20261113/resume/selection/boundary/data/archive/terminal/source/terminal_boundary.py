#!/usr/bin/env python3
"""Failure of terminal-safe selection in the necessary boundary class.

All subsets of size zero through m-n+2 are tested. Unlike ordinary
four-cap-free selections, terminal-safe sets cannot freely grow to three.
"""
import hashlib,itertools,json,os,resource,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/boundary')
C=itertools.combinations
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def mask(t):return sum(1<<i for i in t)
def generate(n,case):
 assert n in (6,7,8)
 base=ROOT/f'sweep/n{n}-old';info=json.loads((base/'encode.json').read_text());m=info['m']
 assert m==2*n-3
 clauses=[];maps=[];nv=info['variables'];phase_counts={};phase=None
 def phase_to(name):
  nonlocal phase
  phase=name;clauses.append('c phase '+name);phase_counts[name]=[0,0]
 def add(row):
  clauses.append(' '.join(map(str,row))+' 0');phase_counts[phase][0]+=1;phase_counts[phase][1]+=len(row)
 def fresh(kind,t):
  nonlocal nv
  nv+=1;maps.append(f'{nv} {kind} {mask(t)}');return nv
 def conjunction(z,ls):
  for a in ls:add([-z,a])
  add([z]+[-a for a in ls])
 tri={t:i+1 for i,t in enumerate(C(range(m),3))}
 Q={}
 for line in (base/'input.cnf.map').read_text().splitlines():
  if line.startswith('#'):continue
  var,kind,s=line.split()
  if kind=='convex':Q[int(s)]=int(var)
 caps={};bad={}
 phase_to('terminal_fourcap_equivalence')
 for t in C(range(m),4):
  z=fresh('boundary_fourcap',t);caps[t]=z
  conjunction(z,[-tri[q] for q in C(t,3)])
 phase_to('terminal_bad_triple_equivalence')
 for t in C(range(m),3):
  a,b,c=t;z=fresh('boundary_bad_triple',t);bad[t]=z
  endpoints=[caps[(u,v,b,c)] for u,v in C(range(b),2)]
  conjunction(z,[-tri[t]]+[-q for q in endpoints])
 phase_to('forall_terminal_safe_delta')
 # Shrinking a larger terminal-safe selection preserves safety and leaves
 # n-2 complement points. Growing smaller selections is NOT presumed safe.
 for size in range(m-n+3):
  for A in C(range(m),size):
   B=tuple(i for i in range(m) if i not in A)
   add([bad[t] for t in C(A,3)]+[Q[mask(t)] for t in C(B,n-1)])
 lines=(base/'input.cnf').read_text().splitlines()
 nc=info['clauses']+sum(p[0] for p in phase_counts.values())
 lines[0]=f'p cnf {nv} {nc}'
 case.mkdir(parents=True,exist_ok=False);cnf=case/'input.cnf'
 cnf.write_text('\n'.join(lines+clauses)+'\n')
 (case/'input.cnf.map').write_text((base/'input.cnf.map').read_text()+'\n'.join(maps)+'\n')
 info.update(mode='old-terminal-failure',variables=nv,clauses=nc,
             literals=info['literals']+sum(p[1] for p in phase_counts.values()),
             bytes=cnf.stat().st_size,added_phases=phase_counts,parent_cnf_sha256=sha(base/'input.cnf'))
 (case/'encode.json').write_text(json.dumps(info,indent=2)+'\n')
 return info
def main():
 resource.setrlimit(resource.RLIMIT_AS,(900<<20,900<<20))
 os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 if len(sys.argv)>1:
  assert len(sys.argv)==4 and sys.argv[1]=='--generate'
  print(json.dumps(generate(int(sys.argv[2]),Path(sys.argv[3]))));return
 out=ROOT/'terminal';out.mkdir(exist_ok=False);src=out/'source';src.mkdir()
 sources=[Path(__file__),HERE.parent.parent/'pool/run_cnf.py',HERE/'complement.cpp',HERE.parent.parent/'compact/compact_cnf.cpp']
 for p in sources:(src/p.name).write_bytes(p.read_bytes())
 (out/'source_hashes.json').write_text(json.dumps({str(p):sha(p) for p in sources},indent=2)+'\n')
 outcomes=[]
 for n in (6,7,8):
  case=out/f'n{n}';info=generate(n,case);cnf=case/'input.cnf'
  cmd=[sys.executable,'-B',str(src/'run_cnf.py'),'--cnf',str(cnf),'--sha256',sha(cnf),
       '--out',str(case/'solve'),'--seconds','90','--cake-seconds','90','--heap','600','--as-mib','900']
  (case/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
  with (case/'runner.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=390)
  r=json.loads((case/'solve/result.json').read_text());item={'n':n,'status':r['status'],'encode':info}
  outcomes.append(item);(out/'status.json').write_text(json.dumps(outcomes,indent=2)+'\n');print(json.dumps(item),flush=True)
 (out/'DONE.json').write_text(json.dumps(outcomes,indent=2)+'\n')
if __name__=='__main__':main()
