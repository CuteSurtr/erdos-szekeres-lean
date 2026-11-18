#!/usr/bin/env python3
"""Bounded sequential discovery/certification loop; never labels a tree proved.

The independent auditor owns geometric reconstruction and exact tree replay.
This loop only appends rows having retained literal cake acceptance lines.
"""
import argparse
import hashlib  # v7
from datetime import datetime
import json
import os
from pathlib import Path
import resource
import shutil
import signal
import subprocess
import time

W=Path('/home/jay/research/data/es308-20261114')
TOOLS=Path(__file__).resolve().parent
PY='/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python'
p=argparse.ArgumentParser()
p.add_argument('--deadline',required=True)
p.add_argument('--start-version',type=int,default=3)
p.add_argument('--threads',type=int,default=12)
p.add_argument('--out',required=True)
p.add_argument('--slice',type=int,default=20)  # v4: slice-generic paths
p.add_argument('--discover',action='store_true')
p.add_argument('--discover-always',action='store_true')  # v8: probe35 every round; certify the union with the pool candidates (batch v<k>u)  # v6: probe35 discovery when the pools are exhausted
p.add_argument('--budget',type=int,default=34,choices=[34,35])  # v5: budget-35 slices (runs/b35s<T>, inputs b35s<T>-v<k>)
p.add_argument('--bb',default='bb')  # v3: packet folder under runs/s20 (successor packets)  # v2: new continuation folder name
p.add_argument('--start-receipt',required=True)  # v2: finder receipt of the start version (rows s20-v<start>)
a=p.parse_args()
RUN=f's{a.slice}' if a.budget==34 else f'b{a.budget}s{a.slice}'  # v5: run folder = input prefix
deadline=datetime.fromisoformat(a.deadline).timestamp()
resource.setrlimit(resource.RLIMIT_AS,(100<<20,1600<<20))
out=W/a.out;assert out.parent==W;out.mkdir(exist_ok=False)
events=[];current=a.start_version;stopped=False;active=None
def stamp():return datetime.now().astimezone().isoformat()
def note(event,**kw):
    r={'time':stamp(),'event':event,**kw};events.append(r)
    (out/'events.json').write_text(json.dumps(events,indent=2)+'\n')
    print(json.dumps(r),flush=True)
def stop(sig,frame):
    global stopped
    stopped=True
signal.signal(signal.SIGTERM,stop)
signal.signal(signal.SIGINT,stop)
def call(name,cmd):
    global active
    path=out/(name+'.log');assert not path.exists()
    with path.open('x') as f:
        active=subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT,start_new_session=True)
        while active.poll() is None:
            if stopped or time.time()>deadline+15:
                os.killpg(active.pid,signal.SIGTERM)
                try:active.wait(timeout=4)
                except subprocess.TimeoutExpired:os.killpg(active.pid,signal.SIGKILL);active.wait()
                break
            time.sleep(.25)
        rc=active.wait();active=None
    note('stage',name=name,command=cmd,exit=rc,log=str(path))
    return rc

# Existing version3 is an independent systemd unit: never overlap its workers.
unit=f'nov13c-vfy-308-tree20-v{current}'
note('waiting_for_existing_finder',unit=unit,deadline=a.deadline)
while time.time()<deadline and not stopped:
    q=subprocess.run(['systemctl','--user','show',unit,'-p','ActiveState','--value'],capture_output=True,text=True)
    assert q.returncode==0
    if q.stdout.strip() not in ('active','activating','deactivating'):break
    time.sleep(1)

while time.time()<deadline-30 and not stopped:
    receipt=Path(a.start_receipt) if current==a.start_version else W/f'runs/{RUN}/w{current}.json'
    if not receipt.exists():note('OPEN',reason='finder receipt missing',version=current);break
    r=json.loads(receipt.read_text())
    if r['exit']==0:
        note('COMPUTED_CLOSED',version=current,reason='independent exact replay still required');break
    witness=W/f'runs/{RUN}'/a.bb/'WITNESS.json'
    if r['exit']!=3 or 'witness' not in r or not witness.exists():
        note('OPEN',reason='finder stopped without a complete row witness',version=current,exit=r['exit']);break
    assert r['witness']['independent_exact_row_check']=='PASS'
    for name in ['master.json','contexts.json','WITNESS.json']:
        src=W/f'runs/{RUN}'/a.bb/name;dst=src.with_name(name+f'.v{current}-snapshot')
        if not dst.exists():shutil.copy2(src,dst)
        else:assert dst.read_bytes()==src.read_bytes()
    nxt=current+1;candidate=W/f'candidates-v{nxt}.json';cuts=W/f'cuts-v{nxt}'
    if candidate.exists():  # v7: resume an interrupted round; reuse its pool file only if made for this witness
        assert json.loads(candidate.read_text())['witness_sha256']==hashlib.sha256(witness.read_bytes()).hexdigest()
        note('reused_pool_file',file=str(candidate))
    elif call(f'select-v{nxt}',[PY,'-B',str(TOOLS/'cut34_v4.py'),'select',str(witness),str(candidate),
                            f'--input-folder={RUN}-v{current}','--limit=32']):break
    c=json.loads(candidate.read_text())
    if a.discover_always:  # v8
        probe=W/f'candidates-v{nxt}p.json'
        if call(f'probe-v{nxt}',[PY,'-B',str(TOOLS/'probe35_v2.py'),str(witness),f'{RUN}-v{current}',str(probe),'6','4']):break
        pc=json.loads(probe.read_text());seen={tuple(x['support']) for x in pc['candidates']}
        assert pc['witness_sha256']==c['witness_sha256'] and pc['input_extra_sha256']==c['input_extra_sha256']
        u=dict(pc);u['label']='HEURISTIC candidates: probe35 plus pool selection (union), not accepted rows'
        u['candidates']=pc['candidates']+[x for x in c['candidates'] if tuple(x['support']) not in seen]
        u['available_candidates']=len(u['candidates']);u['union_of']={'probe':str(probe),'pool':str(candidate)}
        candidate=W/f'candidates-v{nxt}u.json';cuts=W/f'cuts-v{nxt}u'
        with candidate.open('x') as f:f.write(json.dumps(u,indent=1)+'\n')
        c=u
    elif not c['candidates'] and a.discover:  # v6: batch name v<nxt>p (the empty pool file is kept unchanged)
        candidate=W/f'candidates-v{nxt}p.json';cuts=W/f'cuts-v{nxt}p'
        if call(f'probe-v{nxt}',[PY,'-B',str(TOOLS/'probe35_v2.py'),str(witness),f'{RUN}-v{current}',str(candidate),'6','4']):break
        c=json.loads(candidate.read_text())
    if not c['candidates']:
        note('OPEN',reason='no violated support in discovery pools',version=current,witness=c['holes']);break
    seconds=min(180,int(deadline-time.time())-35)
    if seconds<15:note('deadline_before_certificate');break
    if call(f'certify-v{nxt}',[PY,'-B',str(TOOLS/'cut34_v4.py'),'certify',str(candidate),str(cuts),
                             f'--seconds={seconds}','--solve-seconds=8','--accept=32']):break
    accepted=cuts/'accepted.json'
    if not accepted.exists() or not json.loads(accepted.read_text()):
        note('OPEN',reason='no newly certified row',version=current);break
    if call(f'append-v{nxt}',[PY,'-B',str(TOOLS/'append_cuts_v2.py'),f'{RUN}-v{current}',str(accepted),f'{RUN}-v{nxt}']):break
    current=nxt
    note('CERTIFIED_ROWS_APPENDED',version=current,accepted=str(accepted),
         count=len(json.loads(accepted.read_text())),independent_audit='pending separately')
    seconds=int(deadline-time.time())-20
    if seconds<15:note('deadline_before_finder',version=current);break
    if call(f'finder-v{current}',[PY,'-B',str(TOOLS/'run_tree_v4.py'),str(a.slice),f'--budget={a.budget}',f'--bb={a.bb}',f'--seconds={seconds}',
                                f'--threads={a.threads}','--contexts=2048',f'--tag=w{current}',
                                f'--input-folder={RUN}-v{current}']):break

note('FINISHED',version=current,stopped=stopped,
     scope='COMPUTED search and individually CERTIFIED rows; no overall bound asserted')
