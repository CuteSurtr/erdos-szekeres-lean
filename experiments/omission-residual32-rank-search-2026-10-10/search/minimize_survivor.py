import gc,gzip,hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,'experiments/omission-residual32-rank-search-2026-10-10');import model
R=Path('.cache/rank313');C=R/'survivor-minimize';C.mkdir(exist_ok=True);raw=gzip.decompress(Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz').read_bytes());data=json.loads(raw);model.D=data;P,mn,mx=model.pair_boxes(data['states']);model.TT=model.triple_table(P,mn,mx);model.cells=[{(i+1,y) for i,h in enumerate(s[:4]) for y in range(1,h+1)} for s in data['states']];e=json.loads((R/'survivors/results.json').read_text())['results'][-1];S=e['support'];H=e['strict_row_witness_holes'];model.ROOT=C;model.occupied=set(range(154))-set(H);deadline=time.monotonic()+150;records=[];last_unsat=e
while True:
 changed=False
 for x in list(S):
  if time.monotonic()>deadline-12:break
  T=[i for i in S if i!=x];m=model.CompactModel(T,min(deadline,time.monotonic()+15),source_cup_bound=True);r=m.probe(min(deadline,time.monotonic()+7));r['cuts_list']=[list(t) for t in sorted(m.cuts)];records.append(r);print(json.dumps({k:v for k,v in r.items() if k!='cuts_list'}),flush=True);del m;gc.collect()
  if r['status']=='unsat':S=T;last_unsat=r;changed=True;break
 if not changed:break
m=model.CompactModel(S,time.monotonic()+20,source_cup_bound=True);r=m.probe(time.monotonic()+20);r['cuts_list']=[list(t) for t in sorted(m.cuts)];assert r['status']=='unsat';prior=[json.loads((R/f).read_text())['support'] for f in ['minimal-core.json','core-two-input.json','core-three-input.json']];assert all(set(H)&set(p) for p in prior);assert all(len(set(H)&set(row['support']))>=row['rhs'] for row in data['constraints']);V=json.loads(Path('.cache/rank313-root/surviving33.json').read_text())['vertices'];assert all(not(set(S)&set(v)) for v in V);out={'scope':'Prospective fourth omission core; exact literals and Lean checks pending. Local survivor elimination is not a global cardinality result.','source_sha256':hashlib.sha256(raw).hexdigest(),'support':S,'rhs':1,'strict_row_witness_holes':H,'witness_satisfies_previous_supports':prior,'surviving33_vertices_cut':16,'rank_model':r,'deletion_results':records};(R/'core-four-input.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'event':'final','support':S,'cuts':len(r['cuts_list']),'deletion_statuses':[v['status'] for v in records]}),flush=True)
