#!/usr/bin/env python3
"""Replay every GP sign relation of a saved model using the retained C checker."""
import argparse,hashlib,importlib.util,json,subprocess
from pathlib import Path


import sys
sys.dont_write_bytecode = True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--model',required=True,type=Path);ap.add_argument('--checker',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);ap.add_argument('--max-output',type=int,default=1000);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
 results=Path(__file__).resolve().parent.parent
 spec=importlib.util.spec_from_file_location('ref',results/'C7UPPER/gen.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
 e=mod.Enc(6,8,10);pos=set(json.loads(a.model.read_text()));vals=[]
 for p in range(60):
  for b in range(60):
   for c in range(60):
    if len({p,b,c})<3:vals.append('0')
    else:
     l=e.o(p,b,c);s=(1 if l>0 else -1)*(1 if abs(l) in pos else -1);vals.append(str(s))
 data='60\n'+' '.join(vals)+'\n'
 r=subprocess.run([str(a.checker.resolve()),str(a.max_output)],input=data,text=True,capture_output=True,check=True)
 (a.out/'full_gp_violations.txt').write_text(r.stdout)
 metadata={'model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),'checker_sha256':hashlib.sha256(a.checker.read_bytes()).hexdigest(),'checker_source_sha256':hashlib.sha256((results/'ROT456/tools/gpcheck.c').read_bytes()).hexdigest(),'verdict':r.stderr.strip(),'max_retained_violations':a.max_output}
 (a.out/'full_gp_check.json').write_text(json.dumps(metadata,indent=2)+'\n');print(json.dumps(metadata,sort_keys=True))
if __name__=='__main__':main()
