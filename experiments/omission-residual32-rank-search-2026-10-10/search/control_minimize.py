import gc,gzip,hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10')
import model
D=Path('.cache/rank313');source=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz');raw=gzip.decompress(source.read_bytes());data=json.loads(raw);model.D=data;P,mn,mx=model.pair_boxes(data['states']);model.TT=model.triple_table(P,mn,mx);model.cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in data['states']];entry=json.loads((D/'results.json').read_text())['results'][-1];S=entry['support'];witness=entry['strict_row_witness_holes'];model.occupied=set(range(154))-set(witness);records=[]
def run(S,rank,path):
 model.ROOT=D/path;model.ROOT.mkdir(exist_ok=True);tick=time.monotonic();m=model.CompactModel(S,tick+20,source_cup_bound=rank);r=m.probe(time.monotonic()+15);r.update(source_cup_bound=rank,artifact_directory=str(model.ROOT));records.append(r);print(json.dumps(r),flush=True);del m;gc.collect();return r
baseline=run(S,False,'baseline');changed=True
while changed:
 changed=False
 for i in list(S):
  trial=[x for x in S if x!=i];r=run(trial,True,'minimize')
  if r['status']=='unsat':S=trial;changed=True;break
r=run(S,True,'final');out={'scope':'Solver discovery; no proof certification or geometric realization claim.','source':str(source),'source_sha256':hashlib.sha256(raw).hexdigest(),'initial_support':entry['support'],'baseline':baseline,'support':S,'rank_model':r,'strict_row_witness_holes':witness,'results':records};(D/'minimal-core.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'event':'final','support':S,'baseline':baseline['status'],'minimality_all_single_deletions_sat':all(x['status']=='sat' for x in records[-len(S)-1:-1])}),flush=True)
