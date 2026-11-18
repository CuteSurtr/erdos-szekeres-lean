#!/usr/bin/env python3
"""Own fresh original low16 replay with streamed hashes, cache release and clean guards."""
import datetime,hashlib,json,os,resource,subprocess,time
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'data/replay'
W=Path('/home/jay/research/data/delta3-codex-20261113/extension');CASE=W/'low16-n7-a'
CAKE=Path('/home/jay/.local/bin/cake_lpr');LIMIT=3100<<20;CHUNK=64<<20
DEADLINE=datetime.datetime.fromisoformat('2026-11-14T08:22:30+09:00').timestamp()
CG=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
releases=0
def save(name,o):
 with (D/name).open('x') as f:json.dump(o,f,indent=2);f.write('\n')
def mem():
 stat=dict(line.split() for line in (CG/'memory.stat').read_text().splitlines())
 return dict(current=int((CG/'memory.current').read_text()),peak=int((CG/'memory.peak').read_text()),
             anon=int(stat['anon']),file=int(stat['file']),swap=int((CG/'memory.swap.current').read_text()))
def drop(fd,start=0,size=0):os.posix_fadvise(fd,start,size,os.POSIX_FADV_DONTNEED)
def guard():
 assert time.time()<DEADLINE,'absolute08:22:30 deadline'
 state=mem();assert state['current']<LIMIT and state['swap']==0,'own3100MiB/no-swap guard'
def hashed(p):
 global releases
 a=p.stat();h=hashlib.sha256();off=last=0
 with p.open('rb',buffering=0) as f:
  os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_SEQUENTIAL)
  for b in iter(lambda:f.read(1<<20),b''):
   h.update(b);off+=len(b)
   if off-last>=CHUNK:drop(f.fileno(),last,off-last);last=off;releases+=1;guard()
  drop(f.fileno());releases+=1
 b=p.stat();assert (a.st_size,a.st_mtime_ns,a.st_ino,a.st_dev)==(b.st_size,b.st_mtime_ns,b.st_ino,b.st_dev)
 return dict(sha256=h.hexdigest(),bytes=a.st_size,mtime_ns=a.st_mtime_ns,inode=a.st_ino,device=a.st_dev)
def stop(p):
 if p.poll() is None:
  p.terminate()
  try:p.wait(timeout=1)
  except subprocess.TimeoutExpired:p.kill();p.wait()
def main():
 resource.setrlimit(resource.RLIMIT_AS,(LIMIT,LIMIT));D.mkdir(exist_ok=False);start=time.monotonic()
 assert 'nov13c-vfy-delta6-low16-independent' in str(CG)
 base=json.loads((R.parent/'left16_longcup/data/base-instance.json').read_text());assert base['status']=='PASS' and base['variables']==128297 and base['clauses']==903593
 assert '2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8' in base['hashes'].values()
 save('start.json',{'started_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'limits':Path('/proc/self/limits').read_text(),
  'AS_MiB':3100,'heap_MiB':2800,'stack_MiB':32,'CPU_count':1,'affinity':sorted(os.sched_getaffinity(0)),
  'cgroup':str(CG),'initial_memory':mem(),'absolute_deadline_KST':'2026-11-14T08:22:30+09:00',
  'monitor_seconds':.1,'cache_release_seconds':1,'cache_release_progress_bytes':CHUNK,'cake_deadline_seconds':660})
 expected={CASE/'input.cnf':'2e233545d18e3a9acf9a253b80a102935828bee27c079ba18946dfbd4efd53d8',
  CASE/'proof.blrat':'247f64c822609e878be490e059fb7e0c96e5e71fde0e265de74c7be36cd8dd42',
  CASE/'proof.blrat.zst':'9b34ae9a407ce304f0ed82b9dbc6947a0219419a46145a326cfa189dd772b206',
  CAKE:'c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54'}
 before={str(p):hashed(p) for p in expected};save('hashes-before.json',before)
 assert all(before[str(p)]['sha256']==h for p,h in expected.items());guard()
 command=[str(CAKE),'--CML_HEAP_SIZE=2800','--CML_STACK_SIZE=32',str(CASE/'input.cnf'),str(CASE/'proof.blrat')]
 save('command.json',command);fds=[os.open(CASE/n,os.O_RDONLY) for n in ('input.cnf','proof.blrat')]
 for fd in fds:drop(fd)
 t=time.monotonic();last=sample=t;lastchar=0;periodic=progress=maximum=0
 with (D/'cake.stdout').open('x') as out,(D/'cake.stderr').open('x') as err,(D/'memory.jsonl').open('x') as mon:
  p=subprocess.Popen(command,stdout=out,stderr=err)
  try:
   while p.poll() is None:
    tick=time.monotonic();assert tick-t<660 and time.time()<DEADLINE-15,'cake time deadline'
    try:rchar=int(dict(line.split(':',1) for line in Path(f'/proc/{p.pid}/io').read_text().splitlines())['rchar'])
    except (FileNotFoundError,ProcessLookupError):rchar=lastchar
    crossed=rchar-lastchar>=CHUNK
    if crossed or tick-last>=1:
     for fd in fds:drop(fd)
     periodic+=1;progress+=crossed;last=tick;lastchar=rchar
    state=mem();maximum=max(maximum,state['current'])
    if state['current']>=LIMIT:
     for fd in fds:drop(fd)
     guard()
    assert state['swap']==0,'unexpected swap'
    if tick-sample>=1:
     mon.write(json.dumps({'seconds':tick-t,'rchar':rchar,'memory':state})+'\n');mon.flush();sample=tick
    time.sleep(.1)
  except BaseException:stop(p);raise
  finally:
   for fd in fds:drop(fd);os.close(fd)
 usage=resource.getrusage(resource.RUSAGE_CHILDREN)
 outcome=dict(returncode=p.returncode,exact_acceptance_line=(D/'cake.stdout').read_text().splitlines()==['s VERIFIED UNSAT'],
  seconds=time.monotonic()-t,peak_RSS_KiB=usage.ru_maxrss,user_seconds=usage.ru_utime,system_seconds=usage.ru_stime,
  cache_release_rounds=periodic,progress64MiB_rounds=progress,max_sampled_cgroup_current=maximum,final_memory=mem())
 save('cake-result.json',outcome)
 after={str(p):hashed(p) for p in expected};save('hashes-after.json',after)
 assert before==after and p.returncode==0 and outcome['exact_acceptance_line'],'replay not accepted/stable'
 save('result.json',{'status':'PASS','label':'CERTIFIED','fresh_independent_replay':True,'n':7,'left_m':16,
  'before':before,'after':after,'stable_inputs':True,'cake':outcome,'hash_cache_release_calls':releases,
  'AS_MiB':3100,'heap_MiB':2800,'stack_MiB':32,'CPU_count':1,'total_seconds':time.monotonic()-start,
  'finished_UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()})
 print(json.dumps({'status':'PASS','label':'CERTIFIED','cake':outcome,'total_seconds':time.monotonic()-start}),flush=True)
if __name__=='__main__':
 try:main()
 except BaseException as e:
  if D.exists() and not(D/'failure.json').exists():save('failure.json',{'status':'FAIL','error':repr(e),'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat()})
  raise
