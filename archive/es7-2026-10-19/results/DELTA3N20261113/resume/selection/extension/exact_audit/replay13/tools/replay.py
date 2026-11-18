#!/usr/bin/env python3
"""Independent bounded replay with stable streamed hashes and cache release."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import signal
import subprocess
import time

ROOT=Path('/home/jay/research/lean/erdos-szekeres-lean')
RECORD=ROOT/'cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/exact_audit/replay13'
DATA=RECORD/'data'
PARENT=Path('/home/jay/research/data/delta3-codex-20261113/extension/finite13-b')
CAKE=Path('/home/jay/.local/bin/cake_lpr')
CHUNK=64<<20
LIMIT=900<<20
EXPECTED={
 PARENT/'input.cnf':'3ec4b75d9076b6f257fed83f3cbb17b8372a43f53f1c0fc8d30730e4c5d35b87',
 PARENT/'proof.blrat':'d54f53ee64be1b7ddbc4c0eab2aa53ec41899112e319ff0272b3b24ddf8bca64',
 PARENT/'proof.blrat.zst':'61aff8b5a0f8e7deb851fd286a6063303f59461d08f7ca02becbec82ac5e7514',
 CAKE:'c14ff49853e890436d6a2fbf66a85b9492dad1dcd2d76254f16a89f2236c8a54'}
CG=Path('/sys/fs/cgroup')/Path('/proc/self/cgroup').read_text().strip().split('::',1)[1].lstrip('/')
hash_release_calls=0

def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def save(name,obj):
    with (DATA/name).open('x') as f:json.dump(obj,f,indent=2);f.write('\n')
def memory():
    values={k:int(v) for k,v in (line.split() for line in (CG/'memory.stat').read_text().splitlines())}
    return dict(current=int((CG/'memory.current').read_text()),peak=int((CG/'memory.peak').read_text()),
        anon=values['anon'],file=values['file'],swap=int((CG/'memory.swap.current').read_text()))
def snapshot(p):
    s=p.stat();return (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)
def drop(fd,start=0,length=0):os.posix_fadvise(fd,start,length,os.POSIX_FADV_DONTNEED)
def hashed(p):
    global hash_release_calls
    before=snapshot(p);h=hashlib.sha256();offset=0;released=0
    with p.open('rb',buffering=0) as f:
        os.posix_fadvise(f.fileno(),0,0,os.POSIX_FADV_SEQUENTIAL)
        while True:
            b=f.read(1<<20)
            if not b:break
            h.update(b);offset+=len(b)
            if offset-released>=CHUNK:
                drop(f.fileno(),released,CHUNK);released+=CHUNK;hash_release_calls+=1
                assert memory()['current']<LIMIT,'memory_threshold_during_hash'
        drop(f.fileno(),0,0);hash_release_calls+=1
    assert before==snapshot(p),'input_changed_while_hashing'
    return dict(sha256=h.hexdigest(),bytes=before[0],mtime_ns=before[1],inode=before[2],device=before[3])
def stop(proc):
    if proc.poll() is None:
        proc.terminate()
        try:proc.wait(timeout=2)
        except subprocess.TimeoutExpired:proc.kill();proc.wait()
def main():
    started=time.monotonic();parent=json.loads((PARENT/'result.json').read_text())
    assert parent['finished'] and parent['status']=='UNSAT_CERTIFIED'
    save('parent-result.json',parent)
    save('start.json',dict(started=now(),pid=os.getpid(),affinity=sorted(os.sched_getaffinity(0)),
         limits=Path('/proc/self/limits').read_text(),cgroup=str(CG),memory=memory(),allocation_AS_bytes=LIMIT,
         heap_mib=650,stack_mib=32,hash_cache_release_bytes=CHUNK,monitor_period_seconds=0.1))
    before={str(p):hashed(p) for p in EXPECTED}
    save('hashes-before.json',before)
    assert all(before[str(p)]['sha256']==h for p,h in EXPECTED.items()),'input_hash_mismatch'
    command=[str(CAKE),'--CML_HEAP_SIZE=650','--CML_STACK_SIZE=32',str(PARENT/'input.cnf'),str(PARENT/'proof.blrat')]
    save('command.json',command)
    descriptors=[os.open(PARENT/name,os.O_RDONLY) for name in ('input.cnf','proof.blrat')]
    for fd in descriptors:drop(fd)
    t=time.monotonic();last_drop=t;last_sample=t;last_rchar=0;periodic=0;progress_releases=0;max_current=0
    with (DATA/'cake.stdout').open('x') as out,(DATA/'cake.stderr').open('x') as err,(DATA/'memory.jsonl').open('x') as mon:
        proc=subprocess.Popen(command,stdout=out,stderr=err)
        try:
            while proc.poll() is None:
                clock=time.monotonic()
                assert clock-t<480,'cake_wall_deadline'
                try:
                    io=dict(line.split(':',1) for line in Path(f'/proc/{proc.pid}/io').read_text().splitlines())
                    rchar=int(io['rchar'])
                except (FileNotFoundError,ProcessLookupError):rchar=last_rchar
                crossed=rchar-last_rchar>=CHUNK
                if crossed or clock-last_drop>=1:
                    for fd in descriptors:drop(fd)
                    periodic+=1;progress_releases+=crossed
                    last_drop=clock;last_rchar=rchar
                mem=memory();max_current=max(max_current,mem['current'])
                if mem['current']>=LIMIT:
                    for fd in descriptors:drop(fd)
                    mem=memory()
                    assert mem['current']<LIMIT,'memory_guard_threshold_900MiB'
                assert mem['swap']==0,'unexpected_swap'
                if clock-last_sample>=1:
                    mon.write(json.dumps(dict(seconds=clock-t,rchar=rchar,**mem))+'\n');mon.flush();last_sample=clock
                time.sleep(0.1)
        except BaseException:
            stop(proc);raise
        finally:
            for fd in descriptors:drop(fd);os.close(fd)
    elapsed=time.monotonic()-t
    usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    lines=(DATA/'cake.stdout').read_text().splitlines()
    accepted=lines.count('s VERIFIED UNSAT')==1
    outcome=dict(returncode=proc.returncode,exact_acceptance_line=accepted,seconds=elapsed,
        peak_rss_kib=usage.ru_maxrss,user_seconds=usage.ru_utime,system_seconds=usage.ru_stime,
        periodic_cache_releases=periodic,progress_64MiB_releases=progress_releases,
        max_sampled_cgroup_current=max_current,memory=memory(),finished=now())
    save('cake-result.json',outcome)
    after={str(p):hashed(p) for p in EXPECTED};save('hashes-after.json',after)
    assert before==after,'replay_inputs_changed'
    assert proc.returncode==0 and accepted,'cake_did_not_verify'
    final=dict(label='CERTIFIED',status='VERIFIED_UNSAT',independent_replay=True,
        exact_acceptance_line='s VERIFIED UNSAT',stable_inputs=True,proof_bytes=before[str(PARENT/'proof.blrat')]['bytes'],
        cnf_sha256=EXPECTED[PARENT/'input.cnf'],proof_sha256=EXPECTED[PARENT/'proof.blrat'],
        compressed_proof_sha256=EXPECTED[PARENT/'proof.blrat.zst'],cake_sha256=EXPECTED[CAKE],
        compressed_proof_retained=(PARENT/'proof.blrat.zst').exists(),hash_cache_release_calls=hash_release_calls,
        cake=outcome,final_memory=memory(),total_seconds=time.monotonic()-started,finished=now(),
        semantic_dependency='../VERIFY_EXACT.md',no_resolve=True)
    save('result.json',final);print(json.dumps(final),flush=True)
if __name__=='__main__':
    try:main()
    except BaseException as e:
        save('failure.json',dict(status='FAILED',when=now(),error=repr(e),hash_cache_release_calls=hash_release_calls))
        raise
