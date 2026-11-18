#!/usr/bin/env python3
"""Independent invocation of cake_lpr on the retained N66<=56 LRAT.
This checks the artifact, not the encoder's mathematical soundness.
"""
import hashlib,json,os,resource,subprocess,time
from pathlib import Path

W=Path('/home/jay/research/data/verify309-codex-20261113/followup56')
D=Path('/home/jay/research/data/n66-20261113/p2/b13g/it1')
W.mkdir(parents=True,exist_ok=True)
out=W/'replay_existing'
out.mkdir(exist_ok=False)
resource.setrlimit(resource.RLIMIT_AS,(3600<<20,3600<<20))
os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
t=time.monotonic()
r=dict(status='HASHING',label='COMPUTED',cnf=str(D/'trim.cnf'),proof=str(D/'trim.lrat'),
       as_mib=3600,heap=3200,stack=32)
def save():
 r['wall_seconds']=round(time.monotonic()-t,3)
 (out/'result.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
save()
r['cnf_sha256']=sha(D/'trim.cnf');r['lrat_sha256']=sha(D/'trim.lrat')
assert r['cnf_sha256']=='8d4b9099cf045ca72ba5ac56e8ecea00a73a44652d5a9f3d100f63f1f10bc151'
assert r['lrat_sha256']=='ff79c2ef3805255b18917dc0769c5088cca0ee8106c5eefb78b8f212fa487296'
r['cake_binary_sha256']=sha(Path('/home/jay/.local/bin/cake_lpr'))
cmd=['/usr/bin/timeout','--kill-after=2','450','/home/jay/.local/bin/cake_lpr',
     '--CML_HEAP_SIZE=3200','--CML_STACK_SIZE=32',str(D/'trim.cnf'),str(D/'trim.lrat')]
r['command']=cmd;r['status']='CHECKING';save()
with (out/'cake.out').open('w') as f:
 p=subprocess.run(['/usr/bin/time','-v','-o',str(out/'cake.time')]+cmd,stdout=f,stderr=subprocess.STDOUT,timeout=460)
r['exit']=p.returncode
lines=(out/'cake.out').read_text(errors='replace').splitlines()
r['verdict']='s VERIFIED UNSAT' if 's VERIFIED UNSAT' in lines else 'NOT VERIFIED'
r['status']='VERIFIED' if r['verdict']=='s VERIFIED UNSAT' else 'FAILED'
r['label']='CERTIFIED' if r['status']=='VERIFIED' else 'COMPUTED'
r['cake_output_sha256']=sha(out/'cake.out');save()
print(json.dumps(r,sort_keys=True))
if r['status']!='VERIFIED':raise SystemExit(1)
