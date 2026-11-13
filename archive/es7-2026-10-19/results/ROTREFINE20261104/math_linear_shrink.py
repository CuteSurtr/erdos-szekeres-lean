#!/usr/bin/env python3
"""Greedily reduce orbit support of an exact full linear dependency."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

def main():
 p=argparse.ArgumentParser();p.add_argument('--model',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True);layers=list(range(10));events=[]
 while len(layers)>2:
  changed=False
  for remove in layers:
   trial=[i for i in layers if i!=remove];dest=a.out/('layers_'+'_'.join(map(str,trial)));dest.mkdir(exist_ok=True)
   r=subprocess.run([sys.executable,'-I','-B',str(Path(__file__).with_name('math_linear.py')),'--model',str(a.model),'--out',str(dest),'--layers',','.join(map(str,trial)),'--seconds','15'],capture_output=True,text=True,timeout=30)
   (dest/'process.log').write_text(r.stdout+r.stderr);assert r.returncode==0
   data=json.loads(r.stdout.strip().splitlines()[-1]);events.append(data);print(json.dumps(data),flush=True)
   if data.get('exact_dependency'):layers=trial;changed=True;break
  if not changed:break
 (a.out/'shrink_summary.json').write_text(json.dumps({'minimal_under_greedy_deletion':layers,'trials':events},indent=2)+'\n')
if __name__=='__main__':main()
