#!/usr/bin/env python3
"""A separate restricted n7/m14 experiment, with explicit no-six-cup rows."""
import argparse,hashlib,itertools,json,resource
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cnf',type=Path,required=True);ap.add_argument('--map',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20));ids={};nv=0
 for line in a.map.read_text().splitlines():
  if line.startswith('#'):continue
  raw,k,mask=line.split();assert int(raw)==nv+1;nv=int(raw)
  if k=='orientation':ids[tuple(i for i in range(14) if int(mask)>>i&1)]=nv
 assert set(ids)==set(itertools.combinations(range(14),3))
 rows=[[-ids[t] for t in itertools.combinations(q,3)] for q in itertools.combinations(range(14),6)]
 assert len(rows)==3003 and all(len(r)==20 for r in rows)
 with a.cnf.open() as f,a.out.open('x') as g:
  h=f.readline().split();assert h[:2]==['p','cnf'] and int(h[2])==nv;old=int(h[3]);g.write(f'p cnf {nv} {old+len(rows)}\n')
  for line in f:g.write(line)
  g.write('c additional geometric premise: no six-cup\n')
  for row in rows:g.write(' '.join(map(str,row))+' 0\n')
 result={'label':'COMPUTED restricted formula construction','n':7,'m':14,'extra_hypothesis':'no six-cup','base_clauses':old,'added_clauses':len(rows),'added_literals':sum(map(len,rows)),'hashes':{k:sha(p) for k,p in dict(base=a.cnf,map=a.map,output=a.out,source=Path(__file__)).items()},'scope':'Only14-point no-five-cap/no-six-cup/no-seven-gon sets. No unrestricted theorem or complementary six-cup-present branch is claimed.'}
 Path(str(a.out)+'.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
