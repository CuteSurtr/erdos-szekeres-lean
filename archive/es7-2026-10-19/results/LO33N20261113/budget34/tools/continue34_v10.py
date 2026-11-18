#!/usr/bin/env python3
"""Bounded batch discovery/certification loop; never labels a tree proved.

v9: the finder runs in --on-witness=continue mode for a time slice (run_tree_v5.py: it ends --slice-seconds after its
first logged witness, or at --max-witnesses witnesses, else at the deadline). Every distinct witness of the
slice (at most --max-witnesses) gets its own batch v<k>w<i>: pool selection + probe35 -> union candidate file ->
certify (at most --accept-per-witness rows). All rows accepted in the round are appended as ONE new input version
(append_cuts_v2.py takes the merged list: it checks every row through the absolute paths in its own receipt).
A witness already cut by a row accepted earlier in the same round gets no batch of its own.
The independent auditor owns geometric reconstruction and exact tree replay (one audit_followup_rows_v4.py process
per batch v<k>w<i>u). This loop only appends rows having retained literal cake acceptance lines.
"""
import argparse
import hashlib
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
p.add_argument('--start-version',type=int,required=True)
p.add_argument('--threads',type=int,default=12)
p.add_argument('--out',required=True)
p.add_argument('--slice',type=int,default=20)
p.add_argument('--budget',type=int,default=34,choices=[34,35])
p.add_argument('--bb',default='bb')
p.add_argument('--start-receipt',default=None)  # v9: optional; without it the loop starts with a finder slice
p.add_argument('--slice-seconds',type=int,default=600)  # v9: the finder ends this long after its first logged WITNESS (or at --max-witnesses), else at the deadline
p.add_argument('--contexts',type=int,default=2048)  # v9: used only when the packet has no master yet
p.add_argument('--max-witnesses',type=int,default=12)
p.add_argument('--accept-per-witness',type=int,default=8)
p.add_argument('--probe-minutes',type=float,default=6)  # v8: fixed 6
p.add_argument('--probe-procs',type=int,default=4)
p.add_argument('--max-ctx-nodes',type=int,default=50000)  # v10: passed to run_tree_v5 (fastbb2 --max-ctx-nodes)  # v8: fixed 4
a=p.parse_args()
RUN=f's{a.slice}' if a.budget==34 else f'b{a.budget}s{a.slice}'
PK=W/f'runs/{RUN}'/a.bb;assert PK.is_dir()
deadline=datetime.fromisoformat(a.deadline).timestamp()
resource.setrlimit(resource.RLIMIT_AS,(100<<20,1600<<20))
out=W/a.out;assert out.parent==W;out.mkdir(exist_ok=False)
events=[];current=a.start_version;stopped=False;active=None
def sha(q):return hashlib.sha256(Path(q).read_bytes()).hexdigest()
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
def finder(version):
    """One finder slice in continue mode on RUN-v<version>; returns its receipt path, or None."""
    seconds=int(deadline-time.time())-20  # no witness-free restarts: they would redo the same contexts on the same rows
    if seconds<15 or stopped:note('deadline_before_finder',version=version);return None
    j=1
    while any((W/f'runs/{RUN}/c{version}s{j}{x}').exists() for x in ('.json','.log')):j+=1
    tag=f'c{version}s{j}'
    if call(f'finder-{tag}',[PY,'-B',str(TOOLS/'run_tree_v5.py'),str(a.slice),f'--budget={a.budget}',f'--bb={a.bb}',f'--max-ctx-nodes={a.max_ctx_nodes}',
                             f'--seconds={seconds}',f'--threads={a.threads}',f'--contexts={a.contexts}',f'--tag={tag}',
                             f'--input-folder={RUN}-v{version}','--on-witness=continue',
                             f'--witness-grace={a.slice_seconds}',f'--stop-witnesses={a.max_witnesses}']):return None
    return W/f'runs/{RUN}/{tag}.json'
def cuts(holes,rows):return any(not set(holes)&set(x['support']) for x in rows)  # rhs-1 row violated iff no hole in it

receipt=Path(a.start_receipt) if a.start_receipt else finder(current)
while receipt and time.time()<deadline-30 and not stopped:
    if not receipt.exists():note('OPEN',reason='finder receipt missing',version=current);break
    r=json.loads(receipt.read_text())
    assert r['command'][2]==str(W/'inputs'/f'{RUN}-v{current}'/'rows.txt') and r['bb']==str(PK),'receipt of another version/packet'
    ws=r.get('witnesses') or ([r['witness']] if 'witness' in r else [])  # run_tree_v4 receipts (stop mode) have one
    if not ws:
        if r['exit']==0:note('COMPUTED_CLOSED',version=current,reason='independent exact replay still required');break
        note('OPEN',reason='finder ended without a witness (deadline, guard, or only too-big contexts left)',version=current,exit=r['exit'],stop_reason=r.get('stop_reason'));break
    assert all(w['independent_exact_row_check']=='PASS' for w in ws)
    for name in ['master.json','contexts.json']:  # v9: the witnesses are kept as WITNESS.json.r<k>w<i> instead
        src=PK/name;dst=src.with_name(name+f'.v{current}-snapshot')
        if not dst.exists():shutil.copy2(src,dst)
        else:assert dst.read_bytes()==src.read_bytes()
    nxt=current+1;accepted=[];batches=[];broken=False
    note('round',version=current,witnesses=len(ws),batched=min(len(ws),a.max_witnesses),receipt=str(receipt))
    for i,w in enumerate(ws[:a.max_witnesses],1):
        tag=f'v{nxt}w{i}';wf=PK/f'WITNESS.json.r{nxt}w{i}'
        body=json.dumps({'holes':w['holes'],'context':w.get('context')})
        if wf.exists():assert wf.read_text()==body  # interrupted round: same witness list
        else:
            with wf.open('x') as f:f.write(body)
        b={'batch':tag,'witness_file':str(wf),'holes':w['holes'],'context':w.get('context')};batches.append(b)
        if cuts(w['holes'],accepted):b['already_cut']=True;note('witness_already_cut',**b);continue
        minutes=min(a.probe_minutes,(deadline-time.time())/60-9)  # reserve: probe minimisation 4 + certify 3 + append 2
        if minutes<1 or stopped:note('deadline_in_round',version=current,batch=tag);break
        wsha=sha(wf);pool=W/f'candidates-{tag}.json';probe=W/f'candidates-{tag}p.json'
        union=W/f'candidates-{tag}u.json';cd=W/f'cuts-{tag}u'
        if not pool.exists() and call(f'select-{tag}',[PY,'-B',str(TOOLS/'cut34_v4.py'),'select',str(wf),str(pool),
                                                    f'--input-folder={RUN}-v{current}','--limit=32']):broken=True;break
        if not probe.exists() and call(f'probe-{tag}',[PY,'-B',str(TOOLS/'probe35_v2.py'),str(wf),f'{RUN}-v{current}',
                                                     str(probe),f'{minutes:.2f}',str(a.probe_procs)]):broken=True;break
        c=json.loads(pool.read_text());pc=json.loads(probe.read_text())
        assert c['witness_sha256']==pc['witness_sha256']==wsha
        assert c['input_extra_sha256']==pc['input_extra_sha256']==sha(W/'inputs'/f'{RUN}-v{current}'/'extra.json')
        done={tuple(x['support']) for x in accepted}  # accepted for an earlier witness of this round: not certified twice
        if not union.exists():
            seen=set(done);cand=[]
            for x in pc['candidates']+c['candidates']:
                if tuple(x['support']) not in seen:seen.add(tuple(x['support']));cand.append(x)
            u=dict(pc);u['label']='HEURISTIC candidates: probe35 plus pool selection (union), not accepted rows'
            u['candidates']=cand;u['available_candidates']=len(cand);u['union_of']={'probe':str(probe),'pool':str(pool)}
            u['excluded_accepted_earlier_in_round']=sorted(map(list,done))
            with union.open('x') as f:f.write(json.dumps(u,indent=1)+'\n')
        u=json.loads(union.read_text());assert u['witness_sha256']==wsha
        b['candidates']=len(u['candidates'])
        if not u['candidates']:note('batch',**b,accepted=0,reason='no violated support found');continue
        if not cd.exists():
            seconds=min(180,int(deadline-time.time())-35)
            if seconds<15:note('deadline_before_certificate',batch=tag);break
            if call(f'certify-{tag}',[PY,'-B',str(TOOLS/'cut34_v4.py'),'certify',str(union),str(cd),
                                      f'--seconds={seconds}','--solve-seconds=8',f'--accept={a.accept_per_witness}']):broken=True;break
        if not (cd/'accepted.json').exists():note('OPEN',reason='certify folder without accepted.json',folder=str(cd));broken=True;break
        got=json.loads((cd/'accepted.json').read_text())
        assert not {tuple(x['support']) for x in got}&done
        accepted+=got;b.update(accepted=len(got),cuts=str(cd),cut_by_round_rows=cuts(w['holes'],accepted))
        note('batch',**b)
    if not accepted:note('OPEN',reason='no newly certified row in the round',version=current,broken=broken);break
    merged=W/f'accepted-v{nxt}m.json';body=json.dumps(accepted,indent=2)+'\n'
    if merged.exists():assert merged.read_text()==body
    else:
        with merged.open('x') as f:f.write(body)
    if call(f'append-v{nxt}',[PY,'-B',str(TOOLS/'append_cuts_v2.py'),f'{RUN}-v{current}',str(merged),f'{RUN}-v{nxt}']):break
    current=nxt;cut=[b['batch'] for b in batches if cuts(b['holes'],accepted)]
    note('CERTIFIED_ROWS_APPENDED',version=current,accepted=str(merged),count=len(accepted),
         batches=[b['batch'] for b in batches],witnesses_cut=cut,witnesses_not_cut=[b['batch'] for b in batches if b['batch'] not in cut],
         witnesses_left_out=len(ws)-len(batches),round_incomplete=broken,independent_audit='pending separately (one process per batch)')
    if broken:break
    if not cuts(ws[0]['holes'],accepted):note('warning',reason='w1 (the packet WITNESS.json) not cut: the resumed finder stops at once on it')
    receipt=finder(current)

note('FINISHED',version=current,stopped=stopped,
     scope='COMPUTED search and individually CERTIFIED rows; no overall bound asserted')
