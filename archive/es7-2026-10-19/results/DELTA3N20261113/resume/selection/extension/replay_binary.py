#!/usr/bin/env python3
"""Bounded repeat of a retained binary LRAT proof, with cache and hash checks."""
import argparse,hashlib,json,os,resource,subprocess,time
from pathlib import Path

def drop(p):
 with p.open('rb') as f:os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_DONTNEED)
def sha(p):
 h=hashlib.sha256();total=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):
   h.update(b);total+=len(b)
   if total%(64<<20)==0:os.posix_fadvise(f.fileno(),total-(64<<20),64<<20,os.POSIX_FADV_DONTNEED)
 drop(p);return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--as-mib',type=int,default=800);ap.add_argument('--heap',type=int,default=550);ap.add_argument('--seconds',type=int,default=360);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(a.as_mib<<20,a.as_mib<<20));a.out.mkdir(parents=True,exist_ok=False);start=time.monotonic()
 cnf=a.run/'input.cnf';proof=a.run/'proof.blrat';cake=Path('/home/jay/.local/bin/cake_lpr');old=json.loads((a.run/'result.json').read_text());before={p.name:sha(p) for p in (cnf,proof,cake)}
 assert all(before[k]==old['hashes'][k] for k in ('input.cnf','proof.blrat','cake_lpr'))
 cmd=['/usr/bin/time','-v','-o',str(a.out/'cake.time'),'/usr/bin/timeout','--kill-after=2',str(a.seconds),str(cake),'--CML_HEAP_SIZE='+str(a.heap),'--CML_STACK_SIZE=32',str(cnf),str(proof)]
 with (a.out/'cake.log').open('w') as f:
  proc=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
  while proc.poll() is None:
   drop(proof);drop(cnf);time.sleep(.25)
 after={p.name:sha(p) for p in (cnf,proof,cake)};assert before==after
 accepted='s VERIFIED UNSAT' in (a.out/'cake.log').read_text().splitlines()
 result={'label':'CERTIFIED' if accepted else 'COMPUTED','status':'UNSAT_CERTIFIED' if accepted else 'CHECK_NOT_ACCEPTED','source_run':str(a.run),'command':cmd,'exit':proc.returncode,'seconds':round(time.monotonic()-start,3),'as_mib':a.as_mib,'heap_mib':a.heap,'hashes_before':before,'hashes_after':after,'source_sha256':sha(Path(__file__))}
 (a.out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
