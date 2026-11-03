#!/usr/bin/env python3
"""Serial orbit-deletion search; all numerical results remain evidence only."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--seconds',type=float,default=20);a=p.parse_args()
 a.out.mkdir(parents=True,exist_ok=True);layers=list(range(10));events=[];start=time.monotonic()
 while len(layers)>2:
  changed=False
  for remove in layers:
   trial=[i for i in layers if i!=remove];dest=a.out/('layers_'+'_'.join(map(str,trial)))
   if not (dest/'sdp_result.json').exists():
    r=subprocess.run([sys.executable,'-I','-B',str(Path(__file__).with_name('math_sdp.py')),'--model',str(a.model),'--out',str(dest),'--layers',','.join(map(str,trial)),'--seconds',str(a.seconds)],capture_output=True,text=True,timeout=a.seconds+30)
    dest.mkdir(exist_ok=True);(dest/'process.log').write_text(r.stdout+r.stderr)
    if r.returncode:raise RuntimeError(r.stderr)
   data=json.loads((dest/'sdp_result.json').read_text());event={k:data[k] for k in ('source_layers','sdp_status','maximum_margin_evidence_only','exact_negative_definite_certificate','elapsed_seconds')};events.append(event)
   print(json.dumps(event),flush=True);(a.out/'shrink_progress.json').write_text(json.dumps({'remaining_layers':layers,'trials':events},indent=2)+'\n')
   if data.get('exact_negative_definite_certificate'):
    layers=trial;changed=True;break
  if not changed:break
 (a.out/'shrink_summary.json').write_text(json.dumps({'minimal_under_greedy_deletion':layers,'trials':events,'elapsed_seconds':round(time.monotonic()-start,3)},indent=2)+'\n')

if __name__=='__main__':main()
