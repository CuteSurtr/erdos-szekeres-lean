import gc,gzip,hashlib,itertools,json,os,random,sys,time
from pathlib import Path
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10');import model
ROOT=Path('.cache/rank313/survivors');ROOT.mkdir(exist_ok=True);raw=gzip.decompress(Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz').read_bytes());data=json.loads(raw);source_sha=hashlib.sha256(raw).hexdigest();surv=json.loads(Path('.cache/rank313-root/surviving33.json').read_text());vertices=surv['vertices'];assert len(vertices)==16;common=set(range(1,154))-set().union(*map(set,vertices));H=set(vertices[0]);assert all(all(len(set(v)&set(r['support']))>=r['rhs'] for r in data['constraints']) and set(v)&set(surv['core']) for v in vertices)
model.ROOT=ROOT;model.D=data;model.occupied=set(range(154))-H;P,mn,mx=model.pair_boxes(data['states']);model.TT=model.triple_table(P,mn,mx);model.cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in data['states']]
faces=sorted({tuple(sorted(set(r['support'])&common)) for r in data['constraints'] if len(r['support'])-r['rhs']==7 and len(set(r['support'])&common)==7});fm=[sum(1<<i for i in f) for f in faces];pool={}
for a,b in itertools.combinations(fm,2):
 mask=a|b;k=mask.bit_count()
 if k<10 or k>14 or mask in pool:continue
 pool[mask]=sum(mask&f==f for f in fm)
rng=random.Random(31316);ranked=sorted(pool,key=lambda m:(-pool[m],m.bit_count(),m))[:120]
for mask in ranked:
 for f in rng.sample(fm,min(80,len(fm))):
  m=mask|f;k=m.bit_count()
  if k not in [15,16] or m in pool:continue
  pool[m]=sum(m&g==g for g in fm)
entries=[]
for k in range(10,17):
 group=sorted([m for m in pool if m.bit_count()==k],key=lambda m:(-pool[m],m))[:20]
 for rank,m in enumerate(group):entries.append({'support':[i for i in range(154) if m>>i&1],'rank':rank,'size':k,'faces':pool[m]})
entries.sort(key=lambda e:(e['rank'],e['size']));(ROOT/'candidates.json').write_text(json.dumps({'common_occupied':sorted(common),'countermodel_holes':sorted(H),'entries':entries},indent=2)+'\n');print(json.dumps({'common_occupied':len(common),'faces':len(faces),'candidates':len(entries)}),flush=True);results=[];deadline=time.monotonic()+240
for e in entries:
 if time.monotonic()>deadline-12:break
 tick=time.monotonic();m=None;print(json.dumps({'event':'build',**e}),flush=True)
 try:
  m=model.CompactModel(e['support'],min(deadline,tick+20),source_cup_bound=True);r=m.probe(min(deadline,time.monotonic()+10));r['cuts_list']=[list(c) for c in sorted(m.cuts)]
 except (TimeoutError,model.z3.Z3Exception,MemoryError) as error:r={'support':e['support'],'status':'unknown','reason':str(error)}
 r.update(total_seconds=time.monotonic()-tick,strict_row_witness_holes=sorted(H),surviving33_vertices_cut=16,source_cup_bound=True);results.append(r);print(json.dumps({k:v for k,v in r.items() if k!='cuts_list'}),flush=True);(ROOT/'results.json').write_text(json.dumps({'scope':'Discovery only. Every candidate is occupied in all16saved33vertices that survivedCoreOne. No global32exclusion claim.','source_sha256':source_sha,'prior_core':surv['core'],'results':results},indent=2)+'\n')
 if r['status']=='unsat':break
 del m;gc.collect()
print(json.dumps({'event':'done','results':len(results)}),flush=True)
