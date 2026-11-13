import gzip,json,hashlib,time
from pathlib import Path
from pyscipopt import Model,quicksum
base=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/source-2646.json.gz'); raw=gzip.decompress(base.read_bytes());data=json.loads(raw)
new=[[33,43,53,65,74,77,85,89,91,96,107,110,125],[1,2,7,12,18,20,27,30,33,34,39,43,53],[33,43,53,65,75,77,87,89,91,99,110,111,118]]
rows=data['constraints']+[{'support':s,'rhs':1} for s in new]
model=Model('residual2649');model.setParam('limits/time',600);model.setParam('parallel/maxnthreads',1);model.setParam('randomization/randomseedshift',19);model.setParam('display/verblevel',4)
h=[model.addVar(vtype='B',name=f'h{i}') for i in range(154)];model.addCons(h[0]==0)
for row in rows:model.addCons(quicksum(h[i] for i in row['support'])>=row['rhs'])
model.addCons(quicksum(h)<=32)
start=time.monotonic();model.optimize();result={'scope':'Exploratory integer feasibility probe, not an exact certificate or Lean theorem. New rows prospective until separate kernel audits pass.','base':str(base),'base_decompressed_sha256':hashlib.sha256(raw).hexdigest(),'rows':len(rows),'new_supports':new,'hole_budget':32,'occupied_required':[0],'limit_seconds':600,'status':str(model.getStatus()),'seconds':time.monotonic()-start,'nodes':model.getNNodes(),'solver':'SCIP','version':f'{model.getMajorVersion()}.{model.getMinorVersion()}.{model.getTechVersion()}','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
if model.getNSols():
 holes=[i for i in range(154) if model.getVal(h[i])>.5]
 assert len(set(holes))==len(holes)<=32 and 0 not in holes and all(len(set(holes)&set(r['support']))>=r['rhs'] for r in rows)
 result.update(holes=holes,exact_integer_replay=True)
Path('.cache/rank313-root/scip2649-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
