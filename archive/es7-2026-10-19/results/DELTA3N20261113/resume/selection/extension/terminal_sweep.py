#!/usr/bin/env python3
"""Autonomous bounded terminal-safe sweep; a result is not an audit."""
import argparse,datetime,hashlib,json,os,resource,shutil,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/extension')
DEADLINE=datetime.datetime.fromisoformat('2026-11-14T08:20:00+09:00').timestamp()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--n',type=int,choices=(7,8),required=True)
 ap.add_argument('--last',type=int,default=16);ap.add_argument('--seconds',type=int,default=600)
 ap.add_argument('--tag',required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(1200<<20,1200<<20))
 os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 out=ROOT/a.tag;out.mkdir(parents=True,exist_ok=False);src=out/'source';src.mkdir()
 sources=[Path(__file__),HERE/'terminal_general.cpp',HERE.parent.parent/'compact/compact_cnf.cpp',
          HERE.parent.parent/'pool/run_cnf.py',ROOT/'terminal_general']
 for p in sources:shutil.copyfile(p,src/p.name)
 (src/'terminal_general').chmod(0o755)
 (out/'source_hashes.json').write_text(json.dumps({str(p):sha(p) for p in sources},indent=2)+'\n')
 outcomes=[];stop='COMPLETED'
 for m in range(2*a.n-3,a.last+1):
  secs=60 if m==2*a.n-3 else a.seconds
  if time.time()+secs+600>DEADLINE:stop='DEADLINE_NO_NEW_JOB';break
  stats=json.loads(subprocess.check_output([str(src/'terminal_general'),str(m),str(a.n),'--stats'],text=True,timeout=20))
  estimate=stats['literals']*250
  if estimate>700*(1<<20):
   outcomes.append({'m':m,'n':a.n,'status':'NOT_LAUNCHED_MEMORY_ESTIMATE','stats':stats,'estimated_bytes':estimate});stop='ESTIMATE_LIMIT';break
  case=out/f'm{m}';case.mkdir();cnf=case/'input.cnf'
  cmd=[str(src/'terminal_general'),str(m),str(a.n),str(cnf)]
  with (case/'encode.json').open('w') as f:subprocess.run(cmd,stdout=f,check=True,timeout=20)
  run=[sys.executable,'-B',str(src/'run_cnf.py'),'--cnf',str(cnf),'--sha256',sha(cnf),
       '--out',str(case/'solve'),'--seconds',str(secs),'--cake-seconds','300','--heap','800','--as-mib','1200']
  (case/'commands.json').write_text(json.dumps([cmd,run],indent=2)+'\n')
  with (case/'runner.log').open('w') as f:subprocess.run(run,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=secs+800)
  result=json.loads((case/'solve/result.json').read_text());item={'n':a.n,'m':m,'status':result['status'],'case':str(case)}
  outcomes.append(item);(out/'status.json').write_text(json.dumps(outcomes,indent=2)+'\n');print(json.dumps(item),flush=True)
  if result['status']=='SAT_AUDIT_PENDING':stop='SAT_NEEDS_REVIEW';break
 (out/'DONE.json').write_text(json.dumps({'stop':stop,'outcomes':outcomes,'time':datetime.datetime.now().astimezone().isoformat()},indent=2)+'\n')
if __name__=='__main__':main()
