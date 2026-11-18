#!/usr/bin/env python3
"""Independent low11--14 cake replays; hash/cache/resource guards retained."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time

R=Path(__file__).resolve().parents[1]
W=Path('/home/jay/research/data/delta3-codex-20261113/extension')
CAKE=Path('/home/jay/.local/bin/cake_lpr')
CHUNK=64 << 20
M=int(sys.argv[1]);assert M in (11,12,13,14)
LONG=M==14
LIMIT=(700 if LONG else 300) << 20
HEAP=450 if LONG else 128
DATA=R/'data'/f'm{M}'
CASE=W/f'low{M}-n7-{"b" if LONG else "a"}'
CG=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
hash_releases=0

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
    with (DATA/name).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def drop(fd,start=0,size=0):os.posix_fadvise(fd,start,size,os.POSIX_FADV_DONTNEED)
def memory():
    if not LONG:return None
    stat={k:int(v) for k,v in (line.split() for line in (CG/'memory.stat').read_text().splitlines())}
    return {'current':int((CG/'memory.current').read_text()),'peak':int((CG/'memory.peak').read_text()),
            'anon':stat['anon'],'file':stat['file'],'swap':int((CG/'memory.swap.current').read_text())}
def snapshot(p):
    s=p.stat();return (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)
def hashed(p):
    global hash_releases
    old=snapshot(p);h=hashlib.sha256();offset=0;released=0
    with p.open('rb',buffering=0) as f:
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_SEQUENTIAL)
        for b in iter(lambda:f.read(1 << 20),b''):
            h.update(b);offset+=len(b)
            if offset-released>=CHUNK:
                drop(f.fileno(),released,CHUNK);released+=CHUNK;hash_releases+=1
                if LONG:assert memory()['current']<LIMIT,'memory threshold during hashing'
        drop(f.fileno());hash_releases+=1
    assert old==snapshot(p),'hash input changed'
    return {'sha256':h.hexdigest(),'bytes':old[0],'mtime_ns':old[1],'inode':old[2],'device':old[3]}
def stop(proc):
    if proc.poll() is None:
        proc.terminate()
        try:proc.wait(timeout=1)
        except subprocess.TimeoutExpired:proc.kill();proc.wait()

def main():
    resource.setrlimit(resource.RLIMIT_AS,(LIMIT,LIMIT))
    DATA.mkdir(exist_ok=False)
    if LONG:assert 'nov13c-vfy-delta6-low14-independent' in str(CG),'wrong unit cgroup'
    started=time.monotonic()
    provenance=json.loads((R.parent/'data/parent-certificate-provenance.json').read_text())['cases'][str(M)]
    expected={CASE/name:provenance['hashes_recomputed_streaming'][name]
              for name in ('input.cnf','proof.blrat','proof.blrat.zst')}
    expected[CAKE]='c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54'
    save('start.json',{'started':now(),'pid':os.getpid(),'affinity':sorted(os.sched_getaffinity(0)),
        'limits':Path('/proc/self/limits').read_text(),'cgroup':str(CG),'memory':memory(),
        'AS_MiB':LIMIT>>20,'heap_MiB':HEAP,'stack_MiB':32,'CPU_count':1,
        'cake_wall_seconds':360 if LONG else 17,'hash_cache_release_bytes':CHUNK,
        'cache_release_period_seconds':1,'monitor_period_seconds':0.1})
    before={str(p):hashed(p) for p in expected};save('hashes-before.json',before)
    assert all(before[str(p)]['sha256']==v for p,v in expected.items())
    command=[str(CAKE),f'--CML_HEAP_SIZE={HEAP}','--CML_STACK_SIZE=32',str(CASE/'input.cnf'),str(CASE/'proof.blrat')]
    save('command.json',command)
    fds=[os.open(CASE/name,os.O_RDONLY) for name in ('input.cnf','proof.blrat')]
    for fd in fds:drop(fd)
    periodic=progress=0;max_current=0;t=time.monotonic();last_drop=t;last_sample=t;last_rchar=0
    with (DATA/'cake.stdout').open('x') as out,(DATA/'cake.stderr').open('x') as err,(DATA/'memory.jsonl').open('x') as mon:
        proc=subprocess.Popen(command,stdout=out,stderr=err)
        try:
            while proc.poll() is None:
                tick=time.monotonic();assert tick-t<(360 if LONG else 17),'cake wall deadline'
                try:
                    io=dict(line.split(':',1) for line in Path(f'/proc/{proc.pid}/io').read_text().splitlines())
                    rchar=int(io['rchar'])
                except (FileNotFoundError,ProcessLookupError):rchar=last_rchar
                crossed=rchar-last_rchar>=CHUNK
                if crossed or tick-last_drop>=1:
                    for fd in fds:drop(fd)
                    periodic+=1;progress+=crossed;last_drop=tick;last_rchar=rchar
                mem=memory()
                if LONG:
                    max_current=max(max_current,mem['current'])
                    if mem['current']>=LIMIT:
                        for fd in fds:drop(fd)
                        mem=memory();assert mem['current']<LIMIT,'700MiB own memory guard'
                    assert mem['swap']==0,'unexpected swap'
                if tick-last_sample>=1:
                    mon.write(json.dumps({'seconds':tick-t,'rchar':rchar,'memory':mem})+'\n');mon.flush();last_sample=tick
                time.sleep(0.1)
        except BaseException:stop(proc);raise
        finally:
            for fd in fds:drop(fd);os.close(fd)
    usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    accepted=(DATA/'cake.stdout').read_text().splitlines().count('s VERIFIED UNSAT')==1
    outcome={'returncode':proc.returncode,'exact_verdict_line':accepted,'seconds':time.monotonic()-t,
        'peak_rss_KiB':usage.ru_maxrss,'CPU_user_seconds':usage.ru_utime,'CPU_system_seconds':usage.ru_stime,
        'cache_release_rounds':periodic,'progress64MiB_rounds':progress,
        'max_sampled_cgroup_current':max_current if LONG else None,'final_memory':memory()}
    save('cake-result.json',outcome)
    after={str(p):hashed(p) for p in expected};save('hashes-after.json',after)
    assert before==after,'replay inputs changed'
    assert proc.returncode==0 and accepted,'cake did not certify'
    result={'status':'PASS','label':'CERTIFIED','left_m':M,'n':7,'fresh_independent_replay':True,
        'exact_acceptance_line':'s VERIFIED UNSAT','before':before,'after':after,'stable_inputs':True,
        'cnf_sha256':expected[CASE/'input.cnf'],'proof_sha256':expected[CASE/'proof.blrat'],
        'compressed_proof_retained':True,'cake':outcome,'hash_cache_release_calls':hash_releases,
        'AS_MiB':LIMIT>>20,'heap_MiB':HEAP,'stack_MiB':32,'CPU_count':1,
        'total_seconds':time.monotonic()-started,'finished':now(),'semantic_dependency':'../../VERIFY_LOW_SPLIT.md'}
    save('result.json',result);print(json.dumps(result),flush=True)

if __name__=='__main__':
    try:main()
    except BaseException as e:
        if DATA.exists() and not (DATA/'failure.json').exists():save('failure.json',{'status':'FAIL','error':repr(e),'when':now()})
        raise
