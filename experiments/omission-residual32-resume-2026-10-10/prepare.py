import gzip,hashlib,json,sys,time
from pathlib import Path
sys.path.insert(0,'scripts')
from omission_row_probe import read_rows
from omission_tree import contexts,leaf_margin,check_tree
out=Path('.cache/residual32-resume-2026-10-10-b'); ex=Path('experiments/omission-residual32-research-2026-10-10'); diag=Path('experiments/omission-residual32-three-row-probe-2026-10-10/diagnostic.json'); ck=json.loads((ex/'checkpoint.json').read_text()); start=time.monotonic()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,h in ck['tracked_artifact_hashes'].items():
 assert sha(ex/name)==h,(name,sha(ex/name),h)
src=Path(ck['source']);tree=Path(ck['cache_tree']['path']);assert sha(src)==ck['source_sha256'];assert sha(tree)==ck['cache_tree']['sha256'];assert gzip.decompress((ex/'source.json.gz').read_bytes())==src.read_bytes()
d=json.loads(diag.read_text());assert d['source_sha256']==sha(src);assert d['parent_tree_sha256']==sha(tree)
source=json.loads(src.read_text());n,rows=read_rows(source)
with gzip.open(tree,'rt') as f:t=json.load(f)
leaves=contexts(n,t['nodes'],t['root']); cs={i:(m,o) for i,m,o in leaves}; cuts=[]
for c in d['cuts_for_original_source']:
 i=c['node'];m,o=cs[i];assert m==set(c['missing']) and o==set(c['occupied']);assert t['nodes'][i]['type']=='pending'
 margin=leaf_margin(n,rows,32,m,o,c['leaf']);assert margin>0
 # Separate direct global-demand inequality from the validator's residual-demand expression.
 loads=[0]*n;demand=0
 for r,w in c['leaf']['weights']:
  s,k=rows[r];demand+=w*k
  for v in s:loads[v]+=w
 cap=c['leaf']['capacity'];upper=sum(loads[v] for v in m)+cap*(32-len(m))+sum(max(loads[v]-cap,0) for v in range(n) if v not in m and v not in o)
 assert demand-upper==c['exact_integer_margin'] and demand>upper
 t['nodes'][i]=c['leaf'];cuts.append({'node':i,'residual_demand_margin':margin,'direct_demand_margin':demand-upper})
print('HASHES_AND_FIVE_CUTS_VERIFIED',json.dumps(cuts),flush=True)
checked=check_tree(n,rows,32,t['nodes'],t['root'],allow_pending=True);assert checked['pending']==19
outsrc=out/'source.json';assert not outsrc.exists();outsrc.write_bytes(src.read_bytes());t.update(source=str(outsrc),source_sha256=sha(outsrc),parent_tree_sha256=sha(tree),checked=checked,complete=False,status='unknown')
seed=out/'seed-five-cuts.json.gz';assert not seed.exists()
with gzip.open(seed,'wt',compresslevel=1) as f:json.dump(t,f,separators=(',',':'))
report={'scope':'Frozen source and checkpoint verified; five original-row cuts copied into new tree only; no Lean claim','source_sha256':sha(outsrc),'parent_tree_sha256':sha(tree),'seed_sha256':sha(seed),'diagnostic_sha256':sha(diag),'cuts':cuts,'checked':checked,'seconds':time.monotonic()-start}
(out/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
