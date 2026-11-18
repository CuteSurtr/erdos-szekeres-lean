#!/usr/bin/env python3
"""Release only our retained proof-file cache, without deleting file data.

The existing memory guard accounts anonymous memory. Retained streaming
proofs can separately fill the nominal cgroup high watermark with cache.
Periodically sync and advise away the completed prefix, keeping the newest
32 MiB of active traces. Bounded by --seconds and parent units' lifetimes.
"""
import argparse,json,os,resource,subprocess,time
from pathlib import Path
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--seconds',type=int,default=7200);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(64<<20,64<<20));a.out.mkdir(parents=True,exist_ok=False);t=time.monotonic();rounds=0;total=0
 while time.monotonic()-t<a.seconds:
  released=0
  for tag in ['terminal7-a','terminal8-a']:
   for p in (a.root/tag).glob('m*/solve/*'):
    if not p.is_file() or p.suffix not in ['.lrat','.zst']:continue
    size=p.stat().st_size;prefix=max(0,size-(32<<20))
    if not prefix:continue
    with p.open('rb') as f:
     os.fsync(f.fileno());os.posix_fadvise(f.fileno(),0,prefix,os.POSIX_FADV_DONTNEED)
    released+=prefix
  rounds+=1;total+=released
  (a.out/'status.json').write_text(json.dumps({'rounds':rounds,'last_advised_bytes':released,'total_advised_bytes':total,'seconds':round(time.monotonic()-t,3)})+'\n')
  states=[subprocess.run(['systemctl','--user','is-active','--quiet','nov13c-vfy-delta6-terminal'+str(n)],check=False).returncode for n in [7,8]]
  if all(states):break
  time.sleep(20)
 (a.out/'DONE.json').write_text(json.dumps({'rounds':rounds,'seconds':round(time.monotonic()-t,3),'data_deleted':False})+'\n')
if __name__=='__main__':main()
