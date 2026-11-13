#!/usr/bin/env python3
"""Reconstruct an exact solver input from its durable base and cut prefix."""
import argparse, hashlib, json, shutil
from pathlib import Path

def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for data in iter(lambda:f.read(1<<20),b''):h.update(data)
 return h.hexdigest()

def main():
 p=argparse.ArgumentParser();p.add_argument('--archive',type=Path,required=True)
 p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
 a=p.parse_args();spec=json.loads(a.input.read_text());base=a.archive/'base.cnf'
 assert digest(base)==spec['base_sha256'];count=0
 assert not a.output.exists(), 'choose a fresh output path'
 with a.output.open('wb') as out:
  out.write(f"p cnf {spec['variables']} {spec['clauses']}\n".encode())
  with base.open('rb') as f:
   header=f.readline().split();assert int(header[2])==spec['variables'];count+=int(header[3]);shutil.copyfileobj(f,out)
  for block in spec['blocks']:
   source=a.archive/block['path'];assert digest(source)==block['sha256']
   with source.open('rb') as f:
    for line in f:out.write(line);count+=1
 assert count==spec['clauses'] and digest(a.output)==spec['cnf_sha256']
 print(json.dumps({'status':'PASS','clauses':count,'sha256':spec['cnf_sha256']}))
if __name__=='__main__':main()
