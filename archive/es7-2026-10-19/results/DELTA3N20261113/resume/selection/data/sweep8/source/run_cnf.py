#!/usr/bin/env python3
"""Bounded solve, literal cake verdict, hashes, and retained compressed proof.

Unlike the repository helper, this explicitly bounds both CakeML heap and
stack and retains partial traces on SAT/UNKNOWN. It never launches a unit.
"""
import argparse,hashlib,json,os,resource,subprocess,time
from pathlib import Path

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser()
 ap.add_argument('--cnf',type=Path,required=True);ap.add_argument('--sha256',required=True)
 ap.add_argument('--out',type=Path,required=True)
 ap.add_argument('--seconds',type=int,default=900);ap.add_argument('--cake-seconds',type=int,default=300)
 ap.add_argument('--heap',type=int,default=800);ap.add_argument('--as-mib',type=int,default=1000)
 a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False)
 resource.setrlimit(resource.RLIMIT_AS,(a.as_mib<<20,a.as_mib<<20))
 os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 t=time.monotonic();r=dict(label='COMPUTED',status='STARTED',cnf=str(a.cnf),hashes={},runs={},commands=[],limits=vars(a).copy())
 r['limits']={k:str(v) if isinstance(v,Path) else v for k,v in r['limits'].items()}
 def save():
  r['seconds']=round(time.monotonic()-t,3);(a.out/'result.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 def run(tag,cmd,limit):
  full=['/usr/bin/timeout','--kill-after=2',str(limit)]+cmd;r['commands'].append(full);save();b=time.monotonic()
  with (a.out/(tag+'.log')).open('w') as f:
   p=subprocess.run(['/usr/bin/time','-v','-o',str(a.out/(tag+'.time'))]+full,stdout=f,stderr=subprocess.STDOUT,timeout=limit+6)
  r['runs'][tag]=dict(exit=p.returncode,seconds=round(time.monotonic()-b,3));save()
  return (a.out/(tag+'.log')).read_text(errors='replace').splitlines()
 r['hashes']['input.cnf']=sha(a.cnf);assert r['hashes']['input.cnf']==a.sha256
 r['hashes']['run_cnf.py']=sha(Path(__file__));r['hashes']['cadical']=sha(Path('/usr/bin/cadical'))
 r['hashes']['cake_lpr']=sha(Path('/home/jay/.local/bin/cake_lpr'));save()
 proof=a.out/'proof.lrat';r['status']='SOLVING'
 lines=run('cadical',['/usr/bin/cadical','-t',str(a.seconds),'--lrat=true','--binary=false',str(a.cnf),str(proof)],a.seconds+3)
 if 's UNSATISFIABLE' in lines:
  r['status']='UNSAT_UNCERTIFIED';save()
  checked=run('cake',['/home/jay/.local/bin/cake_lpr','--CML_HEAP_SIZE='+str(a.heap),'--CML_STACK_SIZE=32',str(a.cnf),str(proof)],a.cake_seconds)
  if 's VERIFIED UNSAT' in checked:r['status']='UNSAT_CERTIFIED';r['label']='CERTIFIED'
 elif 's SATISFIABLE' in lines:r['status']='SAT_AUDIT_PENDING'
 else:r['status']='UNKNOWN'
 if proof.exists():
  r['hashes']['proof.lrat']=sha(proof);r['proof_bytes']=proof.stat().st_size;save()
  run('compress',['/usr/bin/zstd','-q','-T1','-3','-k',str(proof)],180)
  z=Path(str(proof)+'.zst')
  if z.exists():
   r['hashes'][z.name]=sha(z);r['compressed_bytes']=z.stat().st_size
   cmd=['/usr/bin/zstd','-q','-d','-c',str(z)];h=hashlib.sha256()
   with subprocess.Popen(cmd,stdout=subprocess.PIPE) as p:
    for b in iter(lambda:p.stdout.read(1<<20),b''):h.update(b)
    assert p.wait()==0
   assert h.hexdigest()==r['hashes']['proof.lrat'];r['compressed_roundtrip_verified']=True
 for name in ('cadical.log','cake.log'):
  p=a.out/name
  if p.exists():r['hashes'][name]=sha(p)
 save();print(json.dumps({k:r[k] for k in ('status','label','seconds')}))

if __name__=='__main__':main()
