import gc,gzip,hashlib,json,os,sys,time
from pathlib import Path
for k in ['OPENBLAS_NUM_THREADS','OMP_NUM_THREADS','MKL_NUM_THREADS']:os.environ[k]='1'
sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10');import model
ROOT=Path('.cache/rank313');SOURCE=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz');raw=gzip.decompress(SOURCE.read_bytes());SHA=hashlib.sha256(raw).hexdigest();data=json.loads(raw);model.D=data;P,mn,mx=model.pair_boxes(data['states']);model.TT=model.triple_table(P,mn,mx);model.cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in data['states']];entries=json.loads((ROOT/'candidates.json').read_text());finished={tuple(r['support']) for r in json.loads((ROOT/'results.json').read_text())['results']};results=[];baseline_results=[];deadline=time.monotonic()+600
for entry in entries:
 if tuple(entry['support']) in finished:continue
 if time.monotonic()>deadline-20:break
 model.ROOT=ROOT/'continue';model.ROOT.mkdir(exist_ok=True);model.occupied=set(range(154))-set(entry['strict_row_witness_holes']);tick=time.monotonic();m=None;print(json.dumps({'event':'build','support':entry['support']}),flush=True)
 try:
  m=model.CompactModel(entry['support'],min(deadline,tick+20),source_cup_bound=True);r=m.probe(min(deadline,time.monotonic()+10));r['cuts_list']=[list(s) for s in sorted(m.cuts)]
 except (TimeoutError,model.z3.Z3Exception,MemoryError) as e:r={'support':entry['support'],'status':'unknown','reason':str(e)}
 r.update(near_row=entry['near_row'],faces=entry['faces'],total_seconds=time.monotonic()-tick,strict_row_witness_holes=entry['strict_row_witness_holes'],source_cup_bound=True);results.append(r);print(json.dumps(r),flush=True);del m;gc.collect()
 if r['status']=='unsat':
  model.ROOT=ROOT/'continue-baseline';model.ROOT.mkdir(exist_ok=True);tick=time.monotonic();m=model.CompactModel(entry['support'],min(deadline,tick+20),source_cup_bound=False);base=m.probe(min(deadline,time.monotonic()+15));base.update(source_cup_bound=False,artifact_directory=str(model.ROOT));r['baseline_status']=base['status'];baseline_results.append(base);print(json.dumps({'event':'baseline',**base}),flush=True);del m;gc.collect()
 out={'scope':'Rank-aware discovery only; all results need separate exact proof and geometry verification.','source':str(SOURCE),'source_sha256':SHA,'results':results,'baseline_results':baseline_results};(ROOT/'continue-results.json').write_text(json.dumps(out,indent=2)+'\n')
 if r['status']=='unsat' and r.get('baseline_status')=='sat':print(json.dumps({'event':'rank_essential_discovery','support':entry['support']}),flush=True);break
print(json.dumps({'event':'done','results':len(results)}),flush=True)
