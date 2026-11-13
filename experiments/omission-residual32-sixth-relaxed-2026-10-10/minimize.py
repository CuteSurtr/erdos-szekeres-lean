#!/usr/bin/env python3
"""Weaken Sixth prerequisites by exact SAT queries; Lean reproof is separate."""
from pathlib import Path
import collections,hashlib,json,time
import z3
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
source=ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10/core13.json';raw=source.read_bytes();data=json.loads(raw)
state_kinds={'empty_direction','domain','fixed_sign'}
variables=[z3.Bool('x'+str(i)) for i in range(1,len(data['variables'])+1)]
solver=z3.Solver();solver.set(timeout=3000)
active={}
for i,c in enumerate(data['clauses']):
 clause=z3.Or([variables[abs(x)-1] if x>0 else z3.Not(variables[abs(x)-1]) for x in c['literals']])
 if c['kind'] in state_kinds:
  active[i]=z3.Bool('use'+str(i));solver.add(z3.Implies(active[i],clause))
 else:solver.add(clause)
selected=list(active);assert solver.check(*[active[i] for i in selected])==z3.unsat
initial_core={str(x) for x in solver.unsat_core()};selected=[i for i in selected if str(active[i]) in initial_core]
results=[];started=time.monotonic()
for i in selected.copy():
 trial=[j for j in selected if j!=i];t=time.monotonic();r=solver.check(*[active[j] for j in trial]);result={'source_clause':i+1,'kind':data['clauses'][i]['kind'],'detail':data['clauses'][i]['detail'],'status':str(r),'seconds':round(time.monotonic()-t,6)}
 if r==z3.unsat:selected=trial
 results.append(result)
keep=[i for i,c in enumerate(data['clauses']) if c['kind'] not in state_kinds or i in selected]
out={'scope':'Exact SAT-assisted prerequisite minimization; not a Lean proof','source_reference':str(source.relative_to(ROOT)),'source_sha256':hashlib.sha256(raw).hexdigest(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'z3_version':z3.get_version_string(),'initial_state_clauses':len(active),'initial_unsat_core':len(initial_core),'retained_state_clauses':len(selected),'retained_clauses':len(keep),'retained_source_indices':[i+1 for i in keep],'retained_state_source_indices':[i+1 for i in selected],'retained_kind_counts':dict(collections.Counter(data['clauses'][i]['kind'] for i in keep)),'checks':results,'seconds':round(time.monotonic()-started,6)}
(HERE/'minimization.json').write_text(json.dumps(out,indent=2)+'\n')
reduced=dict(data);reduced['clauses']=[data['clauses'][i] for i in keep];reduced['proof_status']='Reduced clauses await exact new LRAT and Lean proof';reduced.pop('cnf_sha256');reduced.pop('lrat_sha256');reduced.pop('exact_python_rup_replay',None)
(HERE/'relaxed-raw.json').write_text(json.dumps(reduced,indent=1)+'\n')
(HERE/'relaxed-raw.cnf').write_text(f'p cnf {len(variables)} {len(keep)}\n'+''.join(' '.join(map(str,c['literals']))+' 0\n' for c in reduced['clauses']))
print(json.dumps({k:v for k,v in out.items() if k not in ['checks','retained_source_indices','retained_state_source_indices']},indent=2))
