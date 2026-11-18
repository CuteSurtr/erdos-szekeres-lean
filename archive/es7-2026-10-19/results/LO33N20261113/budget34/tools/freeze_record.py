#!/usr/bin/env python3
"""Freeze small research records, check local links, and re-read every hash.

This is artifact integrity checking, not another mathematical proof replay.
Large CNF/LRAT/tree identities are bound by the existing independent audits.
"""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import resource
import subprocess

resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20))
ROOT=Path('/home/jay/research/lean/erdos-szekeres-lean')
B=ROOT/'cloud/es7-2026-10-19/results/LO33N20261113/budget34'
S=ROOT/'cloud/es7-2026-10-19/results/STATUS20261114_1100'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def files(folder):
    output=subprocess.check_output(['rg','--files','--hidden','--no-ignore',str(folder)],text=True)
    return sorted(Path(x) for x in output.splitlines())
paths=files(B)+files(S)
checked=[];failed=[]
for p in paths:
    if p.suffix!='.md':continue
    for raw in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)',p.read_text()):
        link=raw.strip().split(' "',1)[0].strip('<>')
        if not link or link.startswith(('#','http:','https:','mailto:','plugin:')):continue
        target=link.split('#',1)[0]
        q=(p.parent/target).resolve()
        r={'source':str(p.relative_to(ROOT)),'target':link,'exists':q.exists()}
        checked.append(r)
        if not q.exists():failed.append(r)
assert not failed,failed
(B/'data/local-links.json').write_text(json.dumps({'label':'PASS: local Markdown targets exist','checked':len(checked),'links':checked},indent=2)+'\n')
state=subprocess.check_output(['git','--no-optional-locks','-c','index.threads=1',
                               '-c','core.preloadIndex=false','-c','core.fsmonitor=false',
                               'status','--short','--branch','--untracked-files=no'],cwd=ROOT,text=True)
assert state.splitlines()==['## es7-night-2026-11-01...origin/es7-night-2026-11-01'],state
(B/'data/git-final.txt').write_text(state)
units=subprocess.check_output(['systemctl','--user','list-units','nov13c-*','p2-*','memguard*','--state=running','--plain','--no-legend'],text=True)
assert not units.strip(),units
(B/'data/units-final.txt').write_text('No running nov13c-*, p2-*, or memguard* units.\n')
manifest=B/'FINAL_MANIFEST.json';sums=B/'SHA256SUMS'
assert not manifest.exists() and not sums.exists()
records=[{'path':str(p.relative_to(B)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in files(B)]
result={'label':'FROZEN small-record integrity manifest; proof acceptance is in the independent audit',
        'frozen_at':datetime.now().astimezone().isoformat(),'record':str(B),
        'file_count':len(records),'total_bytes':sum(r['bytes'] for r in records),'files':records}
manifest.write_text(json.dumps(result,indent=2)+'\n')
with sums.open('x') as f:
    for r in records:f.write(r['sha256']+'  '+r['path']+'\n')
    f.write(sha(manifest)+'  FINAL_MANIFEST.json\n')
for r in records:
    p=B/r['path'];assert p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
assert set(files(B))=={B/r['path'] for r in records}|{manifest,sums}
handoff=S/'SHA256SUMS';assert not handoff.exists()
handoff.write_text(sha(S/'README.md')+'  README.md\n'+sha(manifest)+'  ../LO33N20261113/budget34/FINAL_MANIFEST.json\n')
print(json.dumps({'record_files':len(records),'record_bytes':result['total_bytes'],
                  'local_links':len(checked),'manifest_sha256':sha(manifest),
                  'readback':'PASS','git_tracked_changes':False,'running_research_units':0},indent=2))
