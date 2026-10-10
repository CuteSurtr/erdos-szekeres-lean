from pathlib import Path
import json,hashlib,collections
root=Path('.cache/rank313');source=root/'core-raw';meta=json.loads(source.with_suffix('.json').read_text());raw=source.with_suffix('.cnf').read_text().splitlines();header=raw[0].split();base_count=int(header[3]);clauses={i:list(map(int,line.split()))[:-1] for i,line in enumerate(raw[1:],1)};steps={};ordered=[]
for line in source.with_suffix('.lrat').read_text().splitlines():
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
# Independent exact RUP replay. No solver or floating arithmetic is used.
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
out=root/'core-one';cnf=out.with_suffix('.cnf');lrat=out.with_suffix('.lrat')
cnf.write_text(f'p cnf {len(variables)} {len(newclauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in newclauses));lrat.write_text(''.join(str(i)+' '+' '.join(map(str,c))+(' ' if c else '')+'0 '+' '.join(map(str,h))+' 0\n' for i,c,h in newsteps))
out.with_suffix('.json').write_text(json.dumps({'support':meta['support'],'variables':[meta['variables'][v-1] for v in variables],'clauses':[{'original_id':c,'kind':meta['clause_kinds'][c-1],'detail':meta['clause_details'][c-1],'literals':relabel(clauses[c])} for c in base],'cnf_sha256':hashlib.sha256(cnf.read_bytes()).hexdigest(),'lrat_sha256':hashlib.sha256(lrat.read_bytes()).hexdigest(),'exact_python_rup_replay':True,'proof_status':'LRAT awaits Lean kernel checking; geometry-to-CNF remains an explicit separate proof obligation.'},indent=1)+'\n')
print('TRIMMED',len(variables),'variables',len(base),'base clauses',len(derived),'derived steps; exact RUP replay passed')
print(collections.Counter(meta['clause_kinds'][c-1] for c in base))
