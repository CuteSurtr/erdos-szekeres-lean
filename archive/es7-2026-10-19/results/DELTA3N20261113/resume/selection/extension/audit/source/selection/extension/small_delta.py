#!/usr/bin/env python3
"""Literal subformula search for terminal-safe Deltas of small cardinality.

SAT excludes only the tested small selections, not all terminal-safe Deltas.
"""
import hashlib,json,os,resource,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/extension')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def filter_formula(source,m,n,k,out):
 masks=[s for s in range(1<<m) if s.bit_count()<=m-n+2]
 lines=[];phase='';index=0;clauses=0;nv=None;retained=[]
 for line in source.read_text().splitlines():
  if line.startswith('p '):nv=int(line.split()[2]);continue
  if line.startswith('c phase '):phase=line.split()[2]
  if line.startswith('c ') or not line.strip():lines.append(line);continue
  if phase=='forall_terminal_delta':
   assert index<len(masks);s=masks[index];index+=1
   if s.bit_count()>k:continue
   retained.append(s)
  lines.append(line);clauses+=1
 assert index==len(masks) and retained==[s for s in masks if s.bit_count()<=k]
 out.write_text(f'p cnf {nv} {clauses}\n'+'\n'.join(lines)+'\n')
 return {'m':m,'n':n,'max_delta_size':k,'variables':nv,'clauses':clauses,
         'retained_selection_rows':len(retained),'parent_sha256':sha(source),'cnf_sha256':sha(out),
         'scope':'Failure only of terminal-safe Delta selections of size <=k.'}
def main():
 resource.setrlimit(resource.RLIMIT_AS,(400<<20,400<<20))
 os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 out=ROOT/'small-delta';out.mkdir(exist_ok=False);src=out/'source';src.mkdir()
 sources=[Path(__file__),HERE.parent.parent/'pool/run_cnf.py']
 for p in sources:(src/p.name).write_bytes(p.read_bytes())
 (out/'source_hashes.json').write_text(json.dumps({str(p):sha(p) for p in sources},indent=2)+'\n')
 outcomes=[]
 for n,m,k in [(7,11,2),(7,11,3),(7,12,3),(7,12,4),(8,13,3),(8,13,4)]:
  case=out/f'n{n}m{m}k{k}';case.mkdir();cnf=case/'input.cnf'
  parent=ROOT/f'terminal{n}-a/m{m}/input.cnf';info=filter_formula(parent,m,n,k,cnf)
  (case/'encode.json').write_text(json.dumps(info,indent=2)+'\n')
  cmd=[sys.executable,'-B',str(src/'run_cnf.py'),'--cnf',str(cnf),'--sha256',sha(cnf),
       '--out',str(case/'solve'),'--seconds','15','--cake-seconds','20','--heap','128','--as-mib','400']
  (case/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
  with (case/'runner.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=240)
  r=json.loads((case/'solve/result.json').read_text());item={'n':n,'m':m,'k':k,'status':r['status']}
  outcomes.append(item);(out/'status.json').write_text(json.dumps(outcomes,indent=2)+'\n');print(json.dumps(item),flush=True)
 (out/'DONE.json').write_text(json.dumps(outcomes,indent=2)+'\n')
if __name__=='__main__':main()
