#!/usr/bin/env python3
"""Four-family conditional n7/m14 cut exclusions; dependencies recorded, never implicit."""
import argparse,hashlib,itertools,json,resource
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--cnf',type=Path,required=True);ap.add_argument('--map',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20));m=14;ids={};nv=0
 for line in a.map.read_text().splitlines():
  if line.startswith('#'):continue
  raw,kind,mask=line.split();i=int(raw);assert i==nv+1;nv=i
  if kind=='orientation':ids[tuple(j for j in range(m) if int(mask)>>j&1)]=i
 assert set(ids)==set(itertools.combinations(range(m),3))
 rows=[];provenance=[]
 for kind in ('high','low','all_cup','all_cap'):
  for cut in range(1,m):
   row=[]
   for (x,y,z),v in ids.items():
    if not x<cut<=z:continue
    intended=(y<cut) if kind=='high' else (y>=cut) if kind=='low' else kind=='all_cup'
    row.append(-v if intended else v)
   assert len(row)==cut*(m-cut)*(m-2)//2
   key=tuple(row)
   if key not in rows:rows.append(key)
   provenance.append(dict(kind=kind,cut=cut,row_index=rows.index(key),literals=len(row)))
 assert len(rows)==48
 with a.cnf.open() as src,a.out.open('x') as dst:
  p=src.readline().split();assert p[:2]==['p','cnf'] and int(p[2])==nv;nc=int(p[3])
  dst.write(f'p cnf {nv} {nc+len(rows)}\n')
  for line in src:dst.write(line)
  dst.write('c conditional high/low/all-cup/all-cap cut exclusions; see receipt dependencies\n')
  for row in rows:dst.write(' '.join(map(str,row))+' 0\n')
 result={'label':'COMPUTED conditional formula construction','m':m,'n':7,'variables':nv,'base_clauses':nc,'added_clauses':len(rows),'added_literals':sum(map(len,rows)),'cuts':provenance,'dependencies':['accepted n7 terminal existence at every size <=13 (separate explicit coverage)','written high-split reduction','written all-mixed-cup reduction','written exact low-split T7(L) equivalence and easy branches','T7(L) through left size10 via standard low join to a three-cup, of total size <=13','accepted direct T7(L) certificates at left sizes11,12,13 with independent soundness/instance audits','written all-cap nontrivial-cut lemma; singleton endpoints reduce to prior high/low cases','independent audit of these48 cut rows and their base','an accepted cake_lpr proof before any UNSAT conclusion'],'hashes':{k:sha(p) for k,p in dict(base=a.cnf,map=a.map,output=a.out,source=Path(__file__)).items()},'scope':'Only n7/m14. No unconditional propositional equivalence and no all-size low-split theorem.'}
 Path(str(a.out)+'.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cuts'}))
if __name__=='__main__':main()
