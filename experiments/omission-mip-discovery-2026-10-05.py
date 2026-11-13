from pathlib import Path
import hashlib,json,sys,time
sys.path.insert(0,str(Path('scripts').resolve()))
from omission_row_probe import read_rows,valid_holes
import highspy
name=sys.argv[1];prefix=len(sys.argv)>2 and sys.argv[2]=='prefix'; feasible=len(sys.argv)>2 and sys.argv[2]=='feasible'
source=Path('.cache/schroeder-release/es7_es8_bounds_81_319_v1/certificates')/(name+'.json')
data=json.loads(source.read_text());n,rows=read_rows(data)
model=highspy.Highs();model.setOptionValue('threads',1);model.setOptionValue('time_limit',180.0);model.setOptionValue('mip_rel_gap',0.0)
h=[model.addVariable(lb=0,ub=1,obj=1,type=highspy.HighsVarType.kInteger,name=f'h{i}') for i in range(n)]
for K,a in rows:model.addConstr(model.qsum(h[i] for i in K)>=a)
if feasible:model.addConstr(model.qsum(h)<=data['hole_budget']+1)
prefix_data=None
if prefix:
 prefix_data=json.loads(Path('.cache/omission-cnf/prefix6-v1.json').read_text())
 z=[model.addVariable(lb=0,ub=1,obj=0,type=highspy.HighsVarType.kInteger) for s in prefix_data['state_sets']]
 model.addConstr(model.qsum(z)>=1)
 for v,s in zip(z,prefix_data['state_sets']):
  for i in s:model.addConstr(v+h[i]<=1)
start=time.monotonic();model.run();sol=model.getSolution();info=model.getInfo()
result={'scope':'Floating-point MIP discovery; only reported hole assignments receive exact checks. Numerical lower bounds are not certificates.','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'solver':'HiGHS '+model.version(),'status':str(model.getModelStatus()),'seconds':time.monotonic()-start,'reported_objective':info.objective_function_value,'reported_dual_bound':info.mip_dual_bound,'prefix':prefix,'feasibility_budget':data['hole_budget']+1 if feasible else None,'nodes':info.mip_node_count}
if sol.value_valid and info.primal_solution_status==2:
 vals=sol.col_value[:n]
 holes=[i for i,v in enumerate(vals) if v>0.5]
 assert all(abs(v-round(v))<1e-6 for v in vals)
 assert valid_holes(n,rows,data['hole_budget']+1 if feasible else n,holes)
 if prefix:assert any(set(s).isdisjoint(holes) for s in prefix_data['state_sets'])
 result.update(holes=holes,occupied=n-len(holes),holes_count=len(holes),rows_exactly_verified=True)
out=Path('.cache/omission-cnf')/(name+('-prefix' if prefix else '-feasible' if feasible else '')+'-mip.json');assert not out.exists();out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
