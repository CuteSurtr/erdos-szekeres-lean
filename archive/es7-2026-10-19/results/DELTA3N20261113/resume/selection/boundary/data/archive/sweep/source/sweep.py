#!/usr/bin/env python3
"""Bounded complementary-cup discovery; run as a research systemd unit."""
import hashlib,json,os,resource,subprocess,sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/boundary')
RUNNER=HERE.parent.parent/'pool/run_cnf.py'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 resource.setrlimit(resource.RLIMIT_AS,(900<<20,900<<20))
 os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 out=ROOT/'sweep';out.mkdir(parents=True,exist_ok=False)
 src=out/'source';src.mkdir()
 sources=[Path(__file__),HERE/'complement.cpp',HERE.parent.parent/'compact/compact_cnf.cpp',RUNNER,ROOT/'complement']
 hashes={str(p):sha(p) for p in sources}
 for p in sources:
  if p.suffix in ('.cpp','.py'):(src/p.name).write_bytes(p.read_bytes())
 (out/'source_hashes.json').write_text(json.dumps(hashes,indent=2)+'\n')
 outcomes=[]
 for n in (6,7,8):
  for mode in ('old','root'):
   case=out/f'n{n}-{mode}';case.mkdir();cnf=case/'input.cnf'
   generate=[str(ROOT/'complement'),str(n),mode,str(cnf)]
   with (case/'encode.json').open('w') as f:subprocess.run(generate,stdout=f,check=True,timeout=20)
   cmd=[sys.executable,'-B',str(src/'run_cnf.py'),'--cnf',str(cnf),'--sha256',sha(cnf),'--out',str(case/'solve'),'--seconds','60','--cake-seconds','60','--heap','600','--as-mib','900']
   (case/'commands.json').write_text(json.dumps([generate,cmd],indent=2)+'\n')
   with (case/'runner.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=330)
   res=json.loads((case/'solve/result.json').read_text())
   item={'n':n,'mode':mode,'status':res['status'],'case':str(case)};outcomes.append(item)
   (out/'status.json').write_text(json.dumps(outcomes,indent=2)+'\n');print(json.dumps(item),flush=True)
   if mode=='old' and res['status']=='UNSAT_CERTIFIED':break
 (out/'DONE.json').write_text(json.dumps(outcomes,indent=2)+'\n')
if __name__=='__main__':main()
