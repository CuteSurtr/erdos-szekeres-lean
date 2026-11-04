#!/usr/bin/env python3
"""Check a retained complete positive-variable assignment against every CNF clause."""
import argparse,hashlib,json,time
from pathlib import Path


import sys
sys.dont_write_bytecode = True

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cnf',required=True,type=Path);ap.add_argument('--model',required=True,type=Path);ap.add_argument('--out',required=True,type=Path);a=ap.parse_args();start=time.monotonic()
 pos=json.loads(a.model.read_text());h=hashlib.sha256();count=0
 with a.cnf.open('rb') as f:
  hdr=f.readline();h.update(hdr);p,kind,nv,nc=hdr.split();assert p==b'p' and kind==b'cnf';nv,nc=int(nv),int(nc)
  values=bytearray(nv+1)
  for x in pos:assert 1<=x<=nv;values[x]=1
  for line in f:
   h.update(line);cl=list(map(int,line.split()));assert cl and cl[-1]==0 and all(1<=abs(x)<=nv for x in cl[:-1])
   assert any(values[abs(x)]==(x>0) for x in cl[:-1]),count+1
   count+=1
 assert count==nc
 result={'rigor':'exact computation','cnf_sha256':h.hexdigest(),'model_sha256':hashlib.sha256(a.model.read_bytes()).hexdigest(),'variables':nv,'clauses_checked':nc,'all_clauses_satisfied':True,'elapsed_seconds':round(time.monotonic()-start,3)}
 a.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
