#!/usr/bin/env python3
"""Bounded binary-LRAT run with literal cake verdict and frequent phase-aware cache release."""
import argparse,hashlib,json,os,resource,shutil,subprocess,time
from pathlib import Path
def drop(p,keep=0):
 if not p.exists():return
 with p.open('rb') as f:
  os.fsync(f.fileno());size=max(0,p.stat().st_size-keep)
  if size:os.posix_fadvise(f.fileno(),0,size,os.POSIX_FADV_DONTNEED)
def sha(p):
 h=hashlib.sha256();offset=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):
   h.update(b);offset+=len(b)
   if offset%(64<<20)==0:os.posix_fadvise(f.fileno(),max(0,offset-(64<<20)),64<<20,os.POSIX_FADV_DONTNEED)
 drop(p);return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cnf',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seconds',type=int,default=5400);ap.add_argument('--cake-seconds',type=int,default=600);ap.add_argument('--heap',type=int,default=650);ap.add_argument('--as-mib',type=int,default=900);ap.add_argument('--cadopt',action='append',default=[]);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(a.as_mib<<20,a.as_mib<<20));os.environ.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
 a.out.mkdir(parents=True,exist_ok=False);cnf=a.out/'input.cnf';shutil.copyfile(a.cnf,cnf);shutil.copyfile(Path(__file__),a.out/'run_binary.py');start=time.monotonic()
 r={'label':'COMPUTED','status':'STARTED','source_cnf':str(a.cnf),'proof_format':'binary LRAT','limits':{'as_mib':a.as_mib,'heap_mib':a.heap,'stack_mib':32,'solver_seconds':a.seconds,'cake_seconds':a.cake_seconds},'hashes':{'input.cnf':sha(cnf),'run_binary.py':sha(Path(__file__)),'cadical':sha(Path('/usr/bin/cadical')),'cake_lpr':sha(Path('/home/jay/.local/bin/cake_lpr'))},'runs':{},'commands':[],'cache_releases':0}
 proof=a.out/'proof.blrat';compressed=a.out/'proof.blrat.zst'
 def save():
  r['seconds']=round(time.monotonic()-start,3);(a.out/'result.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
 def run(tag,cmd,seconds):
  full=['/usr/bin/time','-v','-o',str(a.out/(tag+'.time')),'/usr/bin/timeout','--kill-after=2',str(seconds)]+cmd;r['commands'].append(full);save();t=time.monotonic();last=t
  with (a.out/(tag+'.log')).open('w') as f:
   proc=subprocess.Popen(full,stdout=f,stderr=subprocess.STDOUT)
   while proc.poll() is None:
    now=time.monotonic()
    if now-last >= (2 if tag == 'cadical' else .25):
     drop(proof,32<<20);drop(compressed,32<<20);r['cache_releases']+=1;last=now;save()
    time.sleep(.1)
  r['runs'][tag]={'exit':proc.returncode,'seconds':round(time.monotonic()-t,3)};drop(proof);drop(compressed);save()
  return (a.out/(tag+'.log')).read_text(errors='replace').splitlines()
 r['status']='SOLVING';lines=run('cadical',['/usr/bin/cadical']+a.cadopt+['-t',str(a.seconds),'--lrat=true','--binary=true',str(cnf),str(proof)],a.seconds+3)
 if 's UNSATISFIABLE' in lines:
  r['status']='UNSAT_UNCERTIFIED';checked=run('cake',['/home/jay/.local/bin/cake_lpr','--CML_HEAP_SIZE='+str(a.heap),'--CML_STACK_SIZE=32',str(cnf),str(proof)],a.cake_seconds)
  if 's VERIFIED UNSAT' in checked:r['status']='UNSAT_CERTIFIED';r['label']='CERTIFIED'
 elif 's SATISFIABLE' in lines:r['status']='SAT_AUDIT_PENDING'
 else:r['status']='UNKNOWN'
 save()
 if proof.exists():
  r['proof_bytes']=proof.stat().st_size;r['hashes']['proof.blrat']=sha(proof);save()
  run('compress',['/usr/bin/zstd','-q','-T1','-3','-k',str(proof)],600)
  if compressed.exists() and r['runs']['compress']['exit']==0:
   r['compressed_bytes']=compressed.stat().st_size;r['hashes'][compressed.name]=sha(compressed);h=hashlib.sha256();read=0
   with subprocess.Popen(['/usr/bin/zstd','-q','-d','-c',str(compressed)],stdout=subprocess.PIPE) as proc:
    for b in iter(lambda:proc.stdout.read(1<<20),b''):
     h.update(b);read+=len(b)
     if read%(64<<20)==0:drop(compressed)
    assert proc.wait()==0
   assert h.hexdigest()==r['hashes']['proof.blrat'];r['compressed_roundtrip_verified']=True;drop(compressed)
 for p in a.out.glob('*.log'):r['hashes'][p.name]=sha(p)
 r['finished']=True;save();print(json.dumps({k:r[k] for k in ['label','status','seconds']}),flush=True)
if __name__=='__main__':main()
