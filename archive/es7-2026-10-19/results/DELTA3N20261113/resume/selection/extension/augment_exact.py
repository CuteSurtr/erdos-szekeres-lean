#!/usr/bin/env python3
"""Add reverse child implications to already reviewed containment lattices.

Every actual terminal counterexample has the canonical exact containment
assignment, so it satisfies these added rows. No geometric premise is added.
This alternative is for solver experiments; accepted results need an audit.
"""
import argparse,hashlib,json,resource
from pathlib import Path
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cnf',type=Path,required=True);ap.add_argument('--n',type=int,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(300<<20,300<<20));assert 5<=a.n<=8
 mapping=Path(str(a.cnf)+'.map');ids={};nodes=[];nv=0
 for line in mapping.read_text().splitlines():
  if line.startswith('#'):continue
  raw,kind,mask=line.split();v=int(raw);s=int(mask);assert v==nv+1;nv=v
  if kind in ['bad_contains','target_contains']:nodes.append((v,kind,s));ids[kind,s]=v
  elif kind=='terminal_bad_triple':ids['bad_contains',s]=v
  elif kind=='convex' and s.bit_count()==a.n-1:ids['target_contains',s]=v
 extra=[]
 for parent,kind,s in nodes:
  rem=s
  for _ in range(4 if kind=='bad_contains' else a.n):
   bit=rem&-rem;assert bit;rem^=bit;child=ids[kind,s^bit];assert child<parent;extra.append((-child,parent))
 with a.cnf.open() as f:
  header=f.readline().split();assert header[:2]==['p','cnf'] and int(header[2])==nv;old=int(header[3])
  with a.out.open('x') as out:
   out.write(f'p cnf {nv} {old+len(extra)}\n')
   for line in f:out.write(line)
   out.write('c phase reverse_containment_implications\n')
   for c in extra:out.write(' '.join(map(str,c))+' 0\n')
 receipt={'label':'COMPUTED formula construction','n':a.n,'variables':nv,'old_clauses':old,'added_clauses':len(extra),'clauses':old+len(extra),'hashes':{'base':sha(a.cnf),'map':sha(mapping),'output':sha(a.out),'augmenter':sha(Path(__file__))},'scope':'Canonical real counterexamples satisfy every reverse child implication; no symmetry or extra geometric assumption.'}
 Path(str(a.out)+'.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
if __name__=='__main__':main()
