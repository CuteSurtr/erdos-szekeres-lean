#!/usr/bin/env python3
"""Archive the independently closed slice19 without changing the live packet."""
import hashlib
import json
import os
from pathlib import Path
import resource
import tarfile

resource.setrlimit(resource.RLIMIT_AS,(200<<20,200<<20))
W=Path('/home/jay/research/data/es308-20261114')
R=Path('/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/LO33N20261113/budget34')
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def release(p):
    fd=os.open(p,os.O_RDONLY)
    try:os.fdatasync(fd);os.posix_fadvise(fd,0,0,os.POSIX_FADV_DONTNEED)
    finally:os.close(fd)
summary=R/'audit/s19-summary.json';s=json.loads(summary.read_text())
assert s['label']=='EXACT TREE' and s['contexts_replayed']==s['contexts_total']==3643
assert s['sole_pending_state0_missing'] and s['global_pending']==1
bb=W/'runs/s19/bb'
files=sorted(bb.glob('ctx-*.json.gz'))
assert len(files)==3643
files += [bb/n for n in ['master.txt','master.json','contexts.json']]
files += [W/'inputs/s19'/n for n in ['extra.json','rows.txt']]
files += [W/'inputs/source-2650.json.gz',W/'inputs/pool812.json']
(W/'archive').mkdir(exist_ok=True)
out=W/'archive/s19-exact.tar';assert not out.exists()
members={}
with tarfile.open(out,'w') as tf:
    for p in files:
        name=str(p.relative_to(W))
        members[name]={'sha256':sha(p),'bytes':p.stat().st_size}
        tf.add(p,arcname=name,recursive=False);release(p)
release(out)
with tarfile.open(out,'r') as tf:
    actual={}
    for entry in tf:
        assert entry.isfile()
        h=hashlib.sha256();f=tf.extractfile(entry)
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
        actual[entry.name]={'sha256':h.hexdigest(),'bytes':entry.size}
assert actual==members
manifest={'archive':str(out),'archive_sha256':sha(out),'archive_bytes':out.stat().st_size,
          'roundtrip':'PASS: every member hash and length matches original',
          'proof_summary_sha256':sha(summary),'members':members}
release(out)
(R/'data/s19-archive.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='members'},indent=2))
