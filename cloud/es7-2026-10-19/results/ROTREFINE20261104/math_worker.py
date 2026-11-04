#!/usr/bin/env python3
"""Serial deadline-bounded exact separation of waiting immutable m6 models.

Reads m6 events/models and writes only its math archive and reserved immutable
incoming folders. Tries small/full linear then PSD certificates through its
helper; absence of a certificate never proves realizability. One compute lane.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--m6',type=Path,required=True);ap.add_argument('--math',type=Path,required=True)
    ap.add_argument('--next-index',type=int,default=1005);ap.add_argument('--deadline',required=True);a=ap.parse_args()
    deadline=dt.datetime.fromisoformat(a.deadline.replace('Z','+00:00'));here=Path(__file__).resolve().parent
    a.math.mkdir(parents=True,exist_ok=True);stop={'requested':False};child=None;next_index=a.next_index
    for sig in (signal.SIGTERM,signal.SIGINT):signal.signal(sig,lambda *_:stop.update(requested=True))
    def stopping():return stop['requested'] or (a.math/'STOP').exists() or dt.datetime.now(dt.timezone.utc)>=deadline
    log=(a.math/'worker_events.jsonl').open('a',buffering=1)
    def event(kind,**data):
        r={'event':kind,'utc':dt.datetime.now(dt.timezone.utc).isoformat(),**data}
        line=json.dumps(r);log.write(line+'\n');print(line,flush=True)
    seen=set()
    for p in a.math.rglob('queue_receipt.json'):
        seen.add(json.loads(p.read_text())['source_model_sha256'])
    event('worker_started',pid=os.getpid(),next_index=next_index,deadline=a.deadline,already_queued_models=len(seen))
    try:
        while not stopping():
            events=[]
            for line in (a.m6/'events.jsonl').read_text().splitlines():
                try:events.append(json.loads(line))
                except json.JSONDecodeError:pass
            idx=next((i for i in range(len(events)-1,-1,-1) if events[i].get('event')=='awaiting_verified_separation'),None)
            pending=None
            if idx is not None and not any(e.get('event') in ('block_added','candidate_assessed') for e in events[idx+1:]):
                rel=events[idx]['model'];model=a.m6/rel
                raw=model.read_bytes();mh=hashlib.sha256(raw).hexdigest()
                if mh not in seen:pending=(model,mh)
            if pending is None:time.sleep(2);continue
            model,mh=pending
            if (deadline-dt.datetime.now(dt.timezone.utc)).total_seconds()<80:break
            dest=a.math/(model.stem+'_scan')
            if dest.exists():
                event('manual_review_needed',reason='uncompleted prior directory exists',model=model.name,model_sha256=mh);break
            dest.mkdir()
            cmd=[sys.executable,'-I','-B',str(here/'math_refine_one.py'),'--model',str(model),'--out',str(dest),
                 '--incoming',str(a.m6/'incoming'),'--index',str(next_index),'--deadline',a.deadline]
            event('separation_started',model=model.name,model_sha256=mh,queue_index=next_index)
            with (dest/'worker_console.jsonl').open('w') as out:
                child=subprocess.Popen(cmd,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
                while child.poll() is None:
                    if stopping():
                        os.killpg(child.pid,signal.SIGTERM)
                        try:child.wait(timeout=5)
                        except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
                        break
                    time.sleep(1)
                rc=child.returncode;child=None
            if stopping():break
            if rc:
                event('manual_review_needed',reason='separation helper failed',returncode=rc,model=model.name,model_sha256=mh);break
            receipts=list(dest.rglob('queue_receipt.json'))
            if not receipts:
                event('manual_review_needed',reason='no queued linear or exact PSD obstruction; inspect helper logs; no realizability conclusion',model=model.name,model_sha256=mh);break
            assert len(receipts)==1
            r=json.loads(receipts[0].read_text());seen.add(mh)
            event('family_queued',model=model.name,**r);next_index+=1
    finally:
        if child is not None and child.poll() is None:
            os.killpg(child.pid,signal.SIGTERM)
            try:child.wait(timeout=5)
            except subprocess.TimeoutExpired:os.killpg(child.pid,signal.SIGKILL);child.wait()
        event('worker_stopped',next_index=next_index,stop_requested=stop['requested'],deadline_reached=dt.datetime.now(dt.timezone.utc)>=deadline)
        log.close()


if __name__=='__main__':main()
