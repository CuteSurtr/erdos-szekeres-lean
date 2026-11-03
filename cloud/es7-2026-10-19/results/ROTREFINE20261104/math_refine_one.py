#!/usr/bin/env python3
"""Separate one immutable model, verify a certificate, and queue a family.

Uses one serial compute lane. Stops at the supplied UTC deadline. A queue
approval is published only after exact polynomial and exact54 checks succeed.
Search order is small linear restrictions, full linear/shrink, then PSD/shrink.
"""
import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--incoming',type=Path,required=True);ap.add_argument('--index',type=int,required=True)
    ap.add_argument('--deadline',required=True);ap.add_argument('--sizes',default='2,3,4');a=ap.parse_args()
    root=Path(__file__).resolve().parent;a.out.mkdir(parents=True,exist_ok=True)
    deadline=dt.datetime.fromisoformat(a.deadline.replace('Z','+00:00'))
    def run(script,args,name):
        left=(deadline-dt.datetime.now(dt.timezone.utc)).total_seconds()
        if left<70:raise TimeoutError('insufficient time before compute deadline')
        with (a.out/name).open('w') as log:
            subprocess.run([sys.executable,'-I','-B',str(root/script),*map(str,args)],stdout=log,stderr=subprocess.STDOUT,check=True,timeout=left)
    run('math_scan.py',['--model',a.model,'--out',a.out,'--sizes',a.sizes,'--limit',1,'--seconds',120],'scan_console.jsonl')
    scan=json.loads((a.out/'scan_summary.json').read_text())
    if not scan['witnesses']:
        print(json.dumps({'model_sha256':scan['model_sha256'],'status':'no small linear witness; probing full linear then PSD','restrictions_tried':scan['restrictions_tried']}),flush=True)
        run('math_linear_large_one.py',['--model',a.model,'--out',a.out/'large_linear','--incoming',a.incoming,'--index',a.index,'--deadline',a.deadline],'large_linear_console.jsonl')
        if list((a.out/'large_linear').rglob('queue_receipt.json')):return
        run('math_sdp_refine_one.py',['--model',a.model,'--out',a.out/'psd','--incoming',a.incoming,'--index',a.index,'--deadline',a.deadline],'psd_console.jsonl');return
    directory=a.out/scan['witnesses'][0]['directory'];w=directory/'linear_witness.json';v=directory/'verified.json'
    run('tests/verify_linear.py',['--model',a.model,'--witness',w,'--out',v],'verify_console.jsonl')
    witness=json.loads(w.read_text());ordered=len(witness['source_layers'])>=4
    family=directory/('family_ordered' if ordered else 'family')
    args=['--witness',w,'--verified',v,'--out',family]+(['--order-preserving'] if ordered else [])
    run('math_embed_linear.py',args,'family_console.jsonl')
    run('math_queue.py',['--family',family,'--incoming',a.incoming,'--index',a.index],'queue_console.jsonl')
    receipt=json.loads((directory/'queue_receipt.json').read_text())
    print(json.dumps({'status':'verified and queued','source_layers':witness['source_layers'],'candidate_clause':witness['candidate_clause'],
                      'witness':str(w.relative_to(a.out)),**receipt}),flush=True)


if __name__=='__main__':main()
