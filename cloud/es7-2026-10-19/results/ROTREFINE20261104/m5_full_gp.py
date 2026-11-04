#!/usr/bin/env python3
"""Check every five-point GP sign relation of a fivefold model."""
import argparse, hashlib, importlib.util, json, math, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--model',type=Path,required=True)
    ap.add_argument('--checker',type=Path,required=True);ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--layers',type=int,default=12);ap.add_argument('--max-output',type=int,default=100000)
    a=ap.parse_args();n=5*a.layers
    if not 5<=n<=80:raise ValueError('C checker dimension')
    spec=importlib.util.spec_from_file_location('encoder',HERE.parent/'C7UPPER/gen.py')
    g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);e=g.Enc(5,8,a.layers)
    pos=set(json.loads(a.model.read_text()));values=[]
    for p in range(n):
        for b in range(n):
            for c in range(n):
                if len({p,b,c})<3:values.append('0')
                else:
                    lit=e.o(p,b,c);values.append(str((1 if lit>0 else -1)*(1 if abs(lit) in pos else -1)))
    data=str(n)+'\n'+' '.join(values)+'\n'
    r=subprocess.run([str(a.checker.resolve()),str(a.max_output)],input=data,text=True,capture_output=True,check=True)
    words=r.stderr.split()
    if len(words)!=4 or words[0]!='relations' or words[2]!='violated':raise ValueError('checker output')
    count,violations=int(words[1]),int(words[3])
    if count!=5*math.comb(n,5):raise ValueError('incomplete enumeration')
    a.out.mkdir(parents=True,exist_ok=True);f=a.out/'full_gp_violations.txt';f.write_text(r.stdout)
    record={'m':5,'layers':a.layers,'model_sha256':sha(a.model),'checker_sha256':sha(a.checker),
        'checker_source_sha256':sha(HERE/'m6_gpcheck.c'),'relations_checked':count,
        'violations':violations,'retained_violations':len(r.stdout.splitlines()),
        'violations_sha256':sha(f),'scope':'complete GP sign check only, not geometric realization'}
    (a.out/'full_gp_check.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
if __name__=='__main__':main()
