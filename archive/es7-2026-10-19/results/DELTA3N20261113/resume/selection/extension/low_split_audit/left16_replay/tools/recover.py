#!/usr/bin/env python3
"""Complete posthashes after monitor failure; never relabel failed wrapper."""
import datetime,hashlib,json,os,resource,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];A=R/'data/replay';D=R/'data/recovery'
EXPECTED={'input.cnf':'2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8',
 'proof.blrat':'247f64c822609e878be490e059fb7e0c96e5e71fde0e265de74c7be36cd8dd42',
 'proof.blrat.zst':'9b34ae9a407ce304f0ed82b9dbc6947a0219419a46145a326cfa189dd772b206',
 'cake_lpr':'c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54'}
releases=0
def save(name,obj):
 with (D/name).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def hashed(p):
 global releases
 a=p.stat();h=hashlib.sha256();off=last=0
 with p.open('rb',buffering=0) as f:
  for b in iter(lambda:f.read(1<<20),b''):
   h.update(b);off+=len(b)
   if off-last>=64<<20:os.posix_fadvise(f.fileno(),last,off-last,os.POSIX_FADV_DONTNEED);last=off;releases+=1
  os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED);releases+=1
 b=p.stat();assert (a.st_size,a.st_mtime_ns,a.st_ino,a.st_dev)==(b.st_size,b.st_mtime_ns,b.st_ino,b.st_dev)
 return dict(sha256=h.hexdigest(),bytes=a.st_size,mtime_ns=a.st_mtime_ns,inode=a.st_ino,device=a.st_dev)
def main():
 resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20));D.mkdir(exist_ok=False);start=time.monotonic()
 failure=json.loads((A/'failure.json').read_text());assert failure['status']=='FAIL' and failure['error']=="PermissionError(13, 'Permission denied')"
 assert (A/'cake.stdout').read_text().splitlines()==['s VERIFIED UNSAT']
 assert not(A/'cake.stderr').read_bytes()
 unit=(R/'data/unit-attempt1-final.txt').read_text();assert 'ExecMainStatus=1' in unit and 'ActiveState=failed' in unit
 before=json.loads((A/'hashes-before.json').read_text());assert len(before)==4
 for p,entry in before.items():assert entry['sha256']==EXPECTED[Path(p).name]
 after={p:hashed(Path(p)) for p in before};save('hashes-after.json',after);assert after==before
 result={'status':'PASS','label':'CERTIFIED','fresh_independent_replay':True,'n':7,'left_m':16,
  'exact_acceptance_line':'s VERIFIED UNSAT','acceptance_basis':'fresh checker exact stdout and stable pre/post hashes',
  'checker_exit_status_recorded':False,'wrapper_status':'FAIL preserved, PermissionError reading /proc child io at completion',
  'wrapper_failure':failure,'before':before,'after':after,'stable_inputs':True,'hash_cache_release_calls':releases,
  'recovery_AS_MiB':150,'CPU_count':1,'posthash_seconds':time.monotonic()-start,
  'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'limits':Path('/proc/self/limits').read_text(),'affinity':sorted(os.sched_getaffinity(0)),
  'no_checker_rerun_in_recovery':True,'checker_stdout_sha256':hashlib.sha256((A/'cake.stdout').read_bytes()).hexdigest()}
 save('result.json',result);print(json.dumps({k:v for k,v in result.items() if k not in ('before','after','limits')}))
if __name__=='__main__':main()
