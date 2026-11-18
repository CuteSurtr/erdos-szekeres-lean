#!/usr/bin/env python3
"""Check complete SAT assignments, then bounded heuristic coordinate search."""
import hashlib,itertools,json,os,resource,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=Path('/home/jay/research/data/delta3-codex-20261113/boundary')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def model(case):
 info=json.loads((case/'encode.json').read_text());values={}
 for line in (case/'solve/cadical.log').read_text().splitlines():
  if line.startswith('v '):
   for z in map(int,line[2:].split()):
    if z:
     assert abs(z) not in values or values[abs(z)]==(z>0)
     values[abs(z)]=z>0
 assert len(values)==info['variables']
 checked=0
 for line in (case/'input.cnf').read_text().splitlines():
  if line.startswith(('c','p')) or not line.strip():continue
  row=list(map(int,line.split()));assert row.pop()==0
  assert any(values[abs(x)]==(x>0) for x in row);checked+=1
 assert checked==info['clauses']
 nt=len(list(itertools.combinations(range(info['m']),3)))
 return dict(info,signs=''.join('+' if values[i] else '-' for i in range(1,nt+1)),
             model_clauses_checked=checked,cnf_sha256=sha(case/'input.cnf'),
             solver_log_sha256=sha(case/'solve/cadical.log'))
def main():
 resource.setrlimit(resource.RLIMIT_AS,(900<<20,900<<20))
 os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 out=ROOT/'realization';out.mkdir(parents=True,exist_ok=False)
 source=HERE.parent.parent/'pool/realize_signs.py'
 frozen=out/'realize_signs.py';frozen.write_bytes(source.read_bytes())
 (out/'source_hashes.json').write_text(json.dumps({str(p):sha(p) for p in [Path(__file__),source]},indent=2)+'\n')
 for n in (6,7,8):
  for mode in ('old','root'):
   record=model(ROOT/f'sweep/n{n}-{mode}')
   (out/f'n{n}-{mode}.model.json').write_text(json.dumps(record,indent=2)+'\n')
 outcomes=[]
 for n in (6,7,8):
  case=out/f'n{n}-root';case.mkdir()
  cmd=['/usr/bin/timeout','--kill-after=2','20',sys.executable,'-B',str(frozen),
       '--input',str(out/f'n{n}-root.model.json'),'--out',str(case),'--seconds','16']
  (case/'command.json').write_text(json.dumps(cmd,indent=2)+'\n')
  with (case/'run.log').open('w') as f:
   p=subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,timeout=24)
  item={'n':n,'exit':p.returncode,'realized_file_exists':(case/'realized.json').exists()}
  outcomes.append(item);(out/'status.json').write_text(json.dumps(outcomes,indent=2)+'\n');print(json.dumps(item),flush=True)
 (out/'DONE.json').write_text(json.dumps(outcomes,indent=2)+'\n')
if __name__=='__main__':main()
