#!/usr/bin/env python3
"""Discovery probe of the 2,650-row catalog around saved one-row 32-hole near-models.

Adapted from experiments/omission-residual32-rank-search-2026-10-10/probe.py: only the
source catalog, candidate input, output directory and time limit differ. SAT/UNSAT here
are solver reports about a necessary abstract model, not Lean results."""
import gc,gzip,hashlib,itertools,json,os,random,time
from pathlib import Path
for key in ('OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS'):os.environ[key]='1'
import sys;sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10');import model
ROOT=Path('.cache/es313/discovery');ROOT.mkdir(exist_ok=True,parents=True)
SOURCE=Path('experiments/omission-residual32-rank-global-2026-10-10/source-2650.json.gz');raw=gzip.decompress(SOURCE.read_bytes());SHA=hashlib.sha256(raw).hexdigest();assert SHA=='e800d5f8a6c5cc45c73ddcc1e57488f2ca8f2ffb704a1515ff7444d589c682f6';data=json.loads(raw);saved=json.loads(Path('experiments/omission-residual32-primal-resume-2026-10-10/feasible34-checked-near-models.json').read_text())['candidates']
viol=lambda H:[j for j,r in enumerate(data['constraints']) if len(set(H)&set(r['support']))<r['rhs']]
candidates=[{'holes':c['holes'],'violations':[{'row':v} for v in viol(c['holes'])]} for c in saved if len(viol(c['holes']))==1];n=154
model.ROOT=ROOT;model.D=data;P,mn,mx=model.pair_boxes(data['states']);model.TT=model.triple_table(P,mn,mx);model.cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in data['states']]
rowmasks=[(sum(1<<i for i in r['support']),r['rhs'],len(r['support'])) for r in data['constraints'] if r['rhs']]
def dominated(mask):return any((m&mask).bit_count()>k-r for m,r,k in rowmasks)
rng=random.Random(20261010313);entries=[];seen=set()
for candidate in candidates:
 holes=set(candidate['holes']);occupied=set(range(1,n))-holes;failed=candidate['violations'][0]['row'];faces=sorted({tuple(sorted(set(r['support'])&occupied)) for r in data['constraints'] if len(r['support'])-r['rhs']==7 and len(set(r['support'])&occupied)==7});fmask=[sum(1<<i for i in f) for f in faces];pool={}
 for x,y in itertools.combinations(fmask,2):
  mask=x|y;k=mask.bit_count()
  if k<11 or k>14 or mask in pool or dominated(mask):continue
  pool[mask]=sum(mask&f==f for f in fmask)
 ranked=sorted(pool,key=lambda m:(-pool[m],m.bit_count(),m));top=ranked[:120]
 for mask in top:
  for f in rng.sample(fmask,min(80,len(fmask))):
   joined=mask|f;k=joined.bit_count()
   if k not in [15,16] or joined in pool or dominated(joined):continue
   pool[joined]=sum(joined&g==g for g in fmask)
 groups={k:sorted([m for m in pool if m.bit_count()==k],key=lambda m:(-pool[m],m))[:12] for k in range(11,17)}
 for k,group in groups.items():
  for rank,mask in enumerate(group):
   if mask in seen:continue
   support=[i for i in range(n) if mask>>i&1];seen.add(mask)
   # Because the base near-model fails only one row, a repair outside the
   # support gives a checked Boolean witness of strict row independence.
   add=next(i for i in data['constraints'][failed]['support'] if i not in holes and not(mask>>i&1));witness=sorted(holes|{add});assert len(witness)==33 and not(set(support)&set(witness));assert all(len(set(witness)&set(r['support']))>=r['rhs'] for r in data['constraints'])
   entries.append({'support':support,'size':k,'rank':rank,'faces':pool[mask],'near_row':failed,'strict_row_witness_holes':witness})
entries.sort(key=lambda e:(e['rank'],e['size'],e['near_row']));(ROOT/'candidates.json').write_text(json.dumps(entries,indent=2)+'\n');print(json.dumps({'candidates':len(entries),'source_sha256':SHA}),flush=True)
started=time.monotonic();deadline=started+int(os.environ.get('PROBE_SECONDS','900'));results=[]
for entry in entries:
 if time.monotonic()>deadline-10:break
 tick=time.monotonic();current=None;model.occupied=set(range(n))-set(entry['strict_row_witness_holes']);print(json.dumps({'event':'build','support':entry['support'],'near_row':entry['near_row'],'faces':entry['faces']}),flush=True)
 try:
  current=model.CompactModel(entry['support'],min(deadline,tick+30),source_cup_bound=True);result=current.probe(min(deadline,time.monotonic()+12))
 except (TimeoutError,model.z3.Z3Exception,MemoryError) as error:result={'support':entry['support'],'status':'unknown','reason':str(error)}
 result.update(near_row=entry['near_row'],faces=entry['faces'],total_seconds=time.monotonic()-tick,strict_row_witness_holes=entry['strict_row_witness_holes'],source_cup_bound=True);results.append(result);print(json.dumps(result),flush=True);(ROOT/'results.json').write_text(json.dumps({'scope':'Discovery only; no geometric realization or new bound claim. Each candidate avoids all single-row implications and has a33-hole Boolean countermodel for the proposed support row.','source':str(SOURCE),'source_sha256':SHA,'results':results},indent=2)+'\n')
 
 del current;gc.collect()
print(json.dumps({'event':'done','results':len(results),'seconds':time.monotonic()-started}),flush=True)
