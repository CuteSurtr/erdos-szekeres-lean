#!/usr/bin/env python3
"""Bounded successor finder; exact independent replay is a separate obligation."""
from datetime import datetime
import gzip,hashlib,json,os,resource,subprocess,time
from pathlib import Path
resource.setrlimit(resource.RLIMIT_AS,(150<<20,1400<<20))
P=Path('/home/jay/research/data/es308-20261114')
W=Path('/home/jay/research/data/es308-resume-20261114-1104')
deadline=datetime.fromisoformat('2026-11-14T11:11:20+09:00').timestamp()
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
pins={str(p):sha(p) for p in [P/'inputs/s20-v5/rows.txt',P/'inputs/s20-v5/extra.json',P/'inputs/source-2650.json.gz',P/'bin/fastbb2',P/'runs/s20/bb/master.json',P/'runs/s20/bb/master.txt',P/'runs/s20/bb/contexts.json']}
cmd=[str(P/'bin/fastbb2'),'solve',str(P/'inputs/s20-v5/rows.txt'),'34','12','2048',str(W/'bb'),
     '--slice=1','--split-open=1','--on-witness=stop','--time-limit=300','--max-ctx-nodes=50000',
     '--ktop=16','--dtop=8','--klow=4','--sbiter=1000']
def limits():
    resource.setrlimit(resource.RLIMIT_AS,(1400<<20,1400<<20));resource.setrlimit(resource.RLIMIT_CORE,(0,0))
start=time.monotonic();peak=0;reason=None
released={p.name for p in (W/'bb').glob('ctx-*.json.gz')}
(W/'launch.json').write_text(json.dumps({'command':cmd,'input_hashes':pins,'runner_sha256':sha(Path(__file__)),'absolute_stop':'2026-11-14T11:11:20+09:00'},indent=2)+'\n')
with (W/'finder.log').open('x') as out:
    child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,preexec_fn=limits)
    while child.poll() is None:
        try:
            s=dict(x.split(':',1) for x in Path(f'/proc/{child.pid}/status').read_text().splitlines() if ':' in x)
            rss=int(s.get('VmRSS','0 kB').split()[0]);sw=int(s.get('VmSwap','0 kB').split()[0]);peak=max(peak,rss)
            if rss>=1200*1024 or sw:reason='clean RSS/swap stop'
        except (FileNotFoundError,ProcessLookupError):pass
        if time.time()>=deadline:reason='clean absolute deadline'
        for p in (W/'bb').glob('ctx-*.json.gz'):
            if p.name in released:continue
            fd=os.open(p,os.O_RDONLY)
            try:os.fdatasync(fd);os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
            finally:os.close(fd)
            released.add(p.name)
        if reason:
            child.terminate()
            try:child.wait(timeout=4)
            except subprocess.TimeoutExpired:child.kill();child.wait()
            break
        time.sleep(.5)
rc=child.wait();assert all(sha(Path(p))==h for p,h in pins.items())
r={'label':'COMPUTED finder; no exclusion before independent exact replay','exit':rc,'command':cmd,
   'seconds':time.monotonic()-start,'peak_sampled_rss_kib':peak,'stop_reason':reason,
   'input_hashes':pins,'source_packet_unchanged':True,'saved_context_files':len(list((W/'bb').glob('ctx-*.json.gz'))),
   'finished':datetime.now().astimezone().isoformat()}
wp=W/'bb/WITNESS.json'
if wp.exists():
    h=json.loads(wp.read_text())['holes'];H=set(h)
    base=json.loads(gzip.decompress((P/'inputs/source-2650.json.gz').read_bytes()))
    rows=base['constraints']+json.loads((P/'inputs/s20-v5/extra.json').read_text())
    assert len(h)==len(H)==34 and 0 not in H
    assert all(len(H&set(x['support']))>=x['rhs'] for x in rows)
    r['witness']={'holes':h,'exact_row_check':'PASS','rows':len(rows),'scope':'abstract vector only'}
(W/'result.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
