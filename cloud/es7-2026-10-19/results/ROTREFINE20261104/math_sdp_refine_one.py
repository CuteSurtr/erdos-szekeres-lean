#!/usr/bin/env python3
"""Serial PSD separation with exact independent checks before queueing."""
import argparse
import datetime as dt
import json
from pathlib import Path
import subprocess
import sys

def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--incoming',type=Path,required=True);p.add_argument('--index',type=int,required=True);p.add_argument('--deadline',required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);root=Path(__file__).resolve().parent;deadline=dt.datetime.fromisoformat(a.deadline.replace('Z','+00:00'))
 def run(script,args,log):
  left=(deadline-dt.datetime.now(dt.timezone.utc)).total_seconds()
  if left<70:raise TimeoutError('insufficient time before compute deadline')
  with log.open('w') as out:subprocess.run([sys.executable,'-I','-B',str(root/script),*map(str,args)],stdout=out,stderr=subprocess.STDOUT,check=True,timeout=left)
 full=a.out/'full';run('math_sdp.py',['--model',a.model,'--out',full,'--seconds',20],a.out/'full_console.jsonl');initial=json.loads((full/'sdp_result.json').read_text())
 if not initial.get('exact_negative_definite_certificate'):
  print(json.dumps({'status':'no exact PSD obstruction; no realization conclusion','source_model_sha256':initial['model_sha256']}),flush=True);return
 shrink=a.out/'shrink';run('math_sdp_shrink.py',['--model',a.model,'--out',shrink,'--seconds',15],a.out/'shrink_console.jsonl');summary=json.loads((shrink/'shrink_summary.json').read_text());layers=summary['minimal_under_greedy_deletion']
 if len(layers)>9:
  print(json.dumps({'status':'exact full obstruction but no tested <=9-orbit source','source_model_sha256':initial['model_sha256']}),flush=True);return
 source=shrink/('layers_'+'_'.join(map(str,layers)));w=source/'sdp_witness.json';v=source/'verified.json';ind=source/'independent_verified.json'
 run('tests/verify_sdp.py',['--model',a.model,'--witness',w,'--out',v],a.out/'verify_console.jsonl')
 run('tests/check_sdp_symbolic.py',['--model',a.model,'--witness',w],ind)
 run('math_embed_sdp.py',['--model',a.model,'--witness',w,'--verified',v,'--independent',ind,'--out',source/'family','--incoming',a.incoming,'--index',a.index],a.out/'family_console.jsonl')
 receipt=json.loads((source/'queue_receipt.json').read_text());print(json.dumps({'status':'PSD certificate verified independently and queued','source_layers':layers,**receipt}),flush=True)
if __name__=='__main__':main()
