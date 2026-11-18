#!/usr/bin/env python3
"""Exclude a simple full-set long-cup solution; retain every outcome."""
import hashlib,itertools,json,os,resource,subprocess,sys
from pathlib import Path
from realize import model
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/boundary')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 resource.setrlimit(resource.RLIMIT_AS,(900<<20,900<<20))
 os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 out=ROOT/'refined';out.mkdir(parents=True,exist_ok=False);src=out/'source';src.mkdir()
 sources=[Path(__file__),HERE/'realize.py',HERE.parent.parent/'pool/run_cnf.py',HERE.parent.parent/'pool/realize_signs.py']
 for p in sources:(src/p.name).write_bytes(p.read_bytes())
 (out/'source_hashes.json').write_text(json.dumps({str(p):sha(p) for p in sources},indent=2)+'\n')
 outcomes=[]
 for n in (6,7,8):
  old=ROOT/f'sweep/n{n}-root';case=out/f'n{n}-root';case.mkdir()
  info=json.loads((old/'encode.json').read_text());m=info['m'];cnf=case/'input.cnf'
  tri={t:i+1 for i,t in enumerate(itertools.combinations(range(m),3))}
  extra=[]
  for t in itertools.combinations(range(m-1),n-2):
   s=t+(m-1,);extra.append([-tri[q] for q in itertools.combinations(s,3)])
  lines=(old/'input.cnf').read_text().splitlines();lines[0]=f'p cnf {info["variables"]} {info["clauses"]+len(extra)}'
  lines.append('c phase no_full_longer_cup')
  lines.extend(' '.join(map(str,row))+' 0' for row in extra);cnf.write_text('\n'.join(lines)+'\n')
  (case/'input.cnf.map').write_bytes((old/'input.cnf.map').read_bytes())
  info.update(refinement='no full-set (n-1)-cup',parent_cnf_sha256=sha(old/'input.cnf'),
              added_clauses=len(extra),clauses=info['clauses']+len(extra),
              literals=info['literals']+sum(map(len,extra)),bytes=cnf.stat().st_size)
  (case/'encode.json').write_text(json.dumps(info,indent=2)+'\n')
  cmd=[sys.executable,'-B',str(src/'run_cnf.py'),'--cnf',str(cnf),'--sha256',sha(cnf),
       '--out',str(case/'solve'),'--seconds','60','--cake-seconds','60','--heap','600','--as-mib','900']
  (case/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
  with (case/'runner.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,check=True,timeout=330)
  result=json.loads((case/'solve/result.json').read_text());item={'n':n,'status':result['status']}
  if result['status']=='SAT_AUDIT_PENDING':
   mdl=case/'model.json';mdl.write_text(json.dumps(model(case),indent=2)+'\n')
   realize=['/usr/bin/timeout','--kill-after=2','20',sys.executable,'-B',str(src/'realize_signs.py'),
            '--input',str(mdl),'--out',str(case/'real'),'--seconds','16']
   (case/'realize_command.json').write_text(json.dumps(realize,indent=2)+'\n')
   with (case/'realize.log').open('w') as f:
    p=subprocess.run(realize,stdout=f,stderr=subprocess.STDOUT,timeout=24)
   item.update(realize_exit=p.returncode,realized_file_exists=(case/'real/realized.json').exists())
  outcomes.append(item);(out/'status.json').write_text(json.dumps(outcomes,indent=2)+'\n');print(json.dumps(item),flush=True)
 (out/'DONE.json').write_text(json.dumps(outcomes,indent=2)+'\n')
if __name__=='__main__':main()
