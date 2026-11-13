#!/usr/bin/env python3
"""Slice and exactly replay the fresh all-RUP proof, retaining clause semantics."""
from pathlib import Path
import hashlib,json,collections
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent;CACHE=ROOT/'.cache/residual32-sixth-relaxed-2026-10-10'
data=json.loads((HERE/'relaxed-raw.json').read_text());base_count=len(data['clauses']);clauses={i:c['literals'] for i,c in enumerate(data['clauses'],1)};steps={};ordered=[]
for line in (CACHE/'relaxed-raw.lrat').read_text().splitlines():
 t=line.split()
 if t[1]=='d':continue
 nums=list(map(int,t));zero=nums.index(0);cid=nums[0];clause=nums[1:zero];hints=nums[zero+1:-1];assert all(x>0 for x in hints);steps[cid]=(clause,hints);ordered.append(cid)
 if not clause:final=cid
used=set();stack=[final]
while stack:
 cid=stack.pop()
 if cid in used:continue
 used.add(cid)
 if cid in steps:stack.extend(steps[cid][1])
base=sorted(c for c in used if c<=base_count);derived=[c for c in ordered if c in used];variables=sorted({abs(l) for cid in base for l in clauses[cid]}|{abs(l) for cid in derived for l in steps[cid][0]});vid={v:i for i,v in enumerate(variables,1)};cid={v:i for i,v in enumerate(base+derived,1)}
def relabel(xs):return [vid[abs(x)]*(1 if x>0 else -1) for x in xs]
newclauses=[relabel(clauses[c]) for c in base];newsteps=[(cid[c],relabel(steps[c][0]),[cid[h] for h in steps[c][1]]) for c in derived]
db={i:c for i,c in enumerate(newclauses,1)}
for index,clause,hints in newsteps:
 values={};conflict=False
 for lit in clause:
  var=abs(lit);truth=lit<0
  if var in values and values[var]!=truth:conflict=True;break
  values[var]=truth
 if not conflict:
  for hint in hints:
   unknown=[]
   for lit in db[hint]:
    value=values.get(abs(lit))
    if value is None:unknown.append(lit)
    elif value==(lit>0):raise AssertionError(('satisfied hint',index,hint))
   assert len(unknown)<=1,(index,hint,unknown)
   if not unknown:conflict=True;break
   lit=unknown[0];values[abs(lit)]=lit>0
 assert conflict,('no conflict',index)
 db[index]=clause
assert newsteps[-1][1]==[]
cnf=HERE/'relaxed.cnf';lrat=HERE/'relaxed.lrat'
cnf.write_text(f'p cnf {len(variables)} {len(newclauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in newclauses));lrat.write_text(''.join(str(i)+' '+' '.join(map(str,c))+(' ' if c else '')+'0 '+' '.join(map(str,h))+' 0\n' for i,c,h in newsteps))
newdata={'support':data['support'],'variables':[data['variables'][v-1] for v in variables],'clauses':[dict(data['clauses'][c-1],literals=relabel(clauses[c])) for c in base],'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),'lrat_sha256':hashlib.sha256(lrat.read_bytes()).hexdigest(),'exact_python_rup_replay':True,'proof_status':'Exact RUP passed; Lean kernel proof and generalized semantics pending.'}
(HERE/'relaxed.json').write_text(json.dumps(newdata,indent=1)+'\n');print(json.dumps({'variables':len(variables),'clauses':len(base),'steps':len(derived),'kinds':dict(collections.Counter(c['kind'] for c in newdata['clauses']))}))
