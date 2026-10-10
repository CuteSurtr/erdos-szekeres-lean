from pathlib import Path
import collections,hashlib,json,time,z3
ROOT=Path.cwd();CACHE=ROOT/'.cache/residual32-sixth-relaxed-2026-10-10';HERE=ROOT/'experiments/omission-residual32-sixth-relaxed-2026-10-10'
oldpath=ROOT/'.cache/residual32-witness-coupled-2026-10-10/core-raw.json';old=json.loads(oldpath.read_text());original=json.loads((ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10/core13.json').read_text());state_kinds={'empty_direction','domain','fixed_sign'}
ids={tuple(v):i for i,v in enumerate(old['variables'],1)}
def conv(l):return ids[tuple(original['variables'][abs(l)-1])]*(1 if l>0 else -1)
raw=(ROOT/'.cache/residual32-witness-coupled-2026-10-10/core-raw.cnf').read_text().splitlines()[1:]
clauses=[];seen=set()
for i,(kind,detail,line) in enumerate(zip(old['clause_kinds'],old['clause_details'],raw),1):
 if kind in state_kinds or kind=='threshold_monotone':continue
 literals=list(map(int,line.split()))[:-1];key=tuple(sorted(literals))
 if key in seen:continue
 seen.add(key);clauses.append({'kind':kind,'detail':detail,'literals':literals,'original_id':i})
state_start=len(clauses)
for c in original['clauses']:
 if c['kind'] in state_kinds:clauses.append(dict(c,literals=[conv(l) for l in c['literals']]))
data={'support':old['support'],'variables':old['variables'],'clauses':clauses};print('BUILD',len(clauses),state_start,flush=True)
variables=[z3.Bool('x'+str(i)) for i in range(1,len(data['variables'])+1)];lits={i+1:v for i,v in enumerate(variables)};lits.update({-i-1:z3.Not(v) for i,v in enumerate(variables)})
solver=z3.Solver();solver.set(timeout=6000);active={};started=time.monotonic()
for i,c in enumerate(data['clauses']):
 clause=z3.Or([lits[x] for x in c['literals']])
 if c['kind'] in state_kinds:active[i]=z3.Bool('use'+str(i));solver.add(z3.Implies(active[i],clause))
 else:solver.add(clause)
print('BUILT',time.monotonic()-started,flush=True)
selected=list(active);r=solver.check(*[active[i] for i in selected]);print('FIRST',r,time.monotonic()-started,flush=True);assert r==z3.unsat
initial_core={str(x) for x in solver.unsat_core()};selected=[i for i in selected if str(active[i]) in initial_core];print('CORE',len(selected),flush=True)
results=[]
for k,i in enumerate(selected.copy()):
 trial=[j for j in selected if j!=i];t=time.monotonic();r=solver.check(*[active[j] for j in trial]);result={'source_clause':i+1,'kind':data['clauses'][i]['kind'],'detail':data['clauses'][i]['detail'],'status':str(r),'seconds':round(time.monotonic()-t,6)}
 if r==z3.unsat:selected=trial
 results.append(result)
 if k%10==0:print('CHECK',k,str(r),'retained',len(selected),time.monotonic()-started,flush=True)
keep=[i for i,c in enumerate(data['clauses']) if c['kind'] not in state_kinds or i in selected]
out={'scope':'Diagnostic minimization with additional universally valid geometric clauses; no Lean proof yet','source_reference':'experiments/omission-residual32-witness-coupled-2026-10-10/core13.json','source_sha256':hashlib.sha256((ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10/core13.json').read_bytes()).hexdigest(),'raw_source_sha256':hashlib.sha256(oldpath.read_bytes()).hexdigest(),'z3_version':z3.get_version_string(),'initial_state_clauses':len(active),'initial_unsat_core':len(initial_core),'retained_state_clauses':len(selected),'retained_clauses':len(keep),'retained_state_source_indices':[i+1 for i in selected],'retained_kind_counts':dict(collections.Counter(data['clauses'][i]['kind'] for i in keep)),'checks':results,'seconds':round(time.monotonic()-started,6)}
(CACHE/'augmented-minimization.json').write_text(json.dumps(out,indent=2)+'\n');reduced=dict(data);reduced['clauses']=[data['clauses'][i] for i in keep]
(CACHE/'augmented-raw.json').write_text(json.dumps(reduced,separators=(',',':'))+'\n');(CACHE/'augmented-raw.cnf').write_text(f'p cnf {len(variables)} {len(keep)}\n'+''.join(' '.join(map(str,c['literals']))+' 0\n' for c in reduced['clauses']))
print('DONE',out['retained_state_clauses'],out['retained_kind_counts'],out['seconds'],flush=True)
