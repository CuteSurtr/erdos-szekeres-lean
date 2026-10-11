#!/usr/bin/env python3
"""Single-worker discovery using proved chronological source-cup bounds."""
import gc,gzip,hashlib,itertools,json,os,random,time
from pathlib import Path
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys;sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10');import model
ROOT=Path('.cache/es313/discovery');ROOT.mkdir(exist_ok=True,parents=True)
SOURCE=Path('experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz');raw=gzip.decompress(SOURCE.read_bytes());SHA=hashlib.sha256(raw).hexdigest();assert SHA=='e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6';data=json.loads(raw);candidates=[{'holes':c['holes'],'violations':[{'row':v} for v in c['violations']]} for c in map(json.loads,open('.cache/es313/near32.jsonl')) if len(c['violations'])==1];n=154
model.ROOT=ROOT;model.D=data;P,mn,mx=model.pair_boxes(data['states']);model.TT=model.triple_table(P,mn,mx);model.cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in data['states']]
rowmasks=[(sum(1<<i for i in r['support']),r['rhs'],len(r['support'])) for r in data['constraints'] if r['rhs']]
def dominated(mask):return any((m&mask).bit_count()>k-r for m,r,k in rowmasks)

unknown=[json.loads(l) for l in open(sys.argv[1]) if l.startswith('{"support"')]
unknown=[u for u in unknown if u['status']=='unknown']
for u in unknown:
 model.occupied=set(range(n))-set(u['strict_row_witness_holes']);tick=time.monotonic()
 try:
  cur=model.CompactModel(u['support'],tick+120,source_cup_bound=True);res=cur.probe(time.monotonic()+150)
 except (TimeoutError,model.z3.Z3Exception,MemoryError) as e:res={'support':u['support'],'status':'unknown','reason':str(e)}
 res['total_seconds']=time.monotonic()-tick;print(json.dumps(res),flush=True)
