#!/usr/bin/env python3
"""Independent exact replay of proof bytes, compatibility, and row classification."""
from pathlib import Path
import gzip,hashlib,itertools,json,re
ROOT=Path(__file__).resolve().parents[2];HERE=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def require(ok,message):
 if not ok:raise ValueError(message)
def check_rup(data,cnf_text,lrat_text):
 lines=cnf_text.splitlines();head=lines.pop(0).split();require(head==['p','cnf','361','1029'],'CNF dimensions')
 clauses=[list(map(int,line.split())) for line in lines];require(all(c[-1]==0 for c in clauses),'CNF terminators');clauses=[c[:-1] for c in clauses]
 require(clauses==[c['literals'] for c in data['clauses']],'CNF metadata');db=dict(enumerate(clauses,1));steps=0
 for line in lrat_text.splitlines():
  nums=list(map(int,line.split()));zero=nums.index(0);index,clause,hints=nums[0],nums[1:zero],nums[zero+1:-1]
  require(nums[-1]==0 and index not in db and all(h>0 and h in db for h in hints),'LRAT identities');values={};conflict=False
  for lit in clause:
   require(1<=abs(lit)<=361,'Literal range');truth=lit<0
   if abs(lit) in values and values[abs(lit)]!=truth:conflict=True;break
   values[abs(lit)]=truth
  if not conflict:
   for hint in hints:
    unknown=[]
    for lit in db[hint]:
     if abs(lit) not in values:unknown.append(lit)
     else:require(values[abs(lit)]!=(lit>0),'Satisfied LRAT hint')
    require(len(unknown)<=1,'Non-unit LRAT hint')
    if not unknown:conflict=True;break
    values[abs(unknown[0])]=unknown[0]>0
  require(conflict,'LRAT step has no contradiction');db[index]=clause;steps+=1
 require(clause==[] and steps==1032,'Missing final contradiction');return steps

def check_rows(core,rows,source):
 criteria=[c for c in core['clauses'] if c['kind'] in ['empty_direction','domain','fixed_sign']];require(len(criteria)==41,'Compatibility count')
 cells=[{(i+1,j) for i,h in enumerate(s[:4]) for j in range(1,h+1)} for s in source['states']]
 def positive(q):
  for perm in itertools.permutations(range(3)):
   a,b,c=[q[i] for i in perm];ab=cells[b]-cells[a];bc=cells[c]-cells[b];ac=cells[c]-cells[a]
   if not ab or not bc or not ac:continue
   parity=sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))%2
   if max(z[parity] for z in bc)>min(z[parity] for z in ab):return False
  return True
 seen=set()
 for i,row in enumerate(rows):
  mapping=row['map'];support=row['support'];require(row['index']==i and row['rhs']==1,'Row identity');require(len(mapping)==len(set(mapping))==13 and all(type(x) is int and 0<=x<154 for x in mapping),'Injective map');require(sorted(mapping)==support,'Map image');require(tuple(support) not in seen,'Duplicate support');seen.add(tuple(support))
  for c in criteria:
   q=c['detail'];a,b=mapping[q[0]],mapping[q[1]]
   if c['kind']=='fixed_sign':require(positive((a,b,mapping[q[2]]) if q[3] else (a,mapping[q[2]],b)),'Fixed sign')
   elif c['kind']=='empty_direction':require(not(cells[b]-cells[a]-{(1,6)}),'Empty direction')
   else:require((q[2],q[3]) not in cells[b]-cells[a]-{(1,6)},'Domain exclusion')
  require(not any(r['rhs']>len(set(r['support'])-set(support)) for r in source['constraints']),'Single-row domination')
 require(len(rows)==48,'Row count');return 48

def check():
 manifest=json.loads((HERE/'manifest.json').read_text())
 for name,h in manifest['files'].items():require(sha((HERE/name).read_bytes())==h,'Bundle input '+name)
 for name,h in manifest['external_inputs'].items():require(sha((ROOT/name).read_bytes())==h,'External input '+name)
 data=json.loads((HERE/'augmented.json').read_text());cnf=(HERE/'augmented.cnf').read_bytes();lrat=(HERE/'augmented.lrat').read_bytes();require(sha(cnf)==data['cnf_sha256'] and sha(lrat)==data['lrat_sha256'],'Proof input hashes')
 steps=check_rup(data,cnf.decode(),lrat.decode());raw=gzip.decompress((ROOT/'experiments/omission-residual32-2598-primal-2026-10-10/source-2598.json.gz').read_bytes());require(sha(raw)==manifest['source_sha256'],'Frozen2598source');source=json.loads(raw);rows=json.loads((HERE/'rows.json').read_text());require(rows['core_sha256']==sha((HERE/'augmented.json').read_bytes()),'Row/core binding');require(rows['source_sha256']==sha(raw),'Row/source binding');count=check_rows(data,rows['rows'],source)
 # Bind the literal Lean maps to the row order used by the arithmetic source.
 literal=(HERE/'SixthRelaxedProof/Data.lean').read_text()
 parsed=re.findall(r'def state([0-9]{3}) : Fin 13 → Fin 154 := !\[([^]]+)\]',literal)
 require([(int(i),[int(v.strip()) for v in vals.split(',')]) for i,vals in parsed]==[(r['index'],r['map']) for r in rows['rows']],'Lean literal map binding')
 expected='def maps : Fin 48 → Fin 13 → Fin 154 := !['+', '.join(f'state{i:03d}' for i in range(48))+']'
 require(expected in literal,'Lean map order')
 catalog=json.loads((HERE/'catalog-manifest.json').read_text());archive=(HERE/catalog['source_reference']).read_bytes();newraw=gzip.decompress(archive)
 require(sha(archive)==catalog['source_archive_sha256'] and sha(newraw)==catalog['source_uncompressed_sha256'],'Augmented catalog hashes')
 require(sha((HERE/'rows.json').read_bytes())==catalog['rows_sha256'] and sha((HERE/'catalog.py').read_bytes())==catalog['generator_sha256'],'Catalog generator bindings')
 require(sha((ROOT/catalog['base_reference']).read_bytes())==catalog['base_archive_sha256'] and sha(raw)==catalog['base_uncompressed_sha256'],'Catalog base bindings')
 newsource=json.loads(newraw);require(newsource['states']==source['states'],'Augmented state identity');require(newsource['constraints'][:2598]==source['constraints'],'Original2598prefix');require(newsource['constraints'][2598:]==[{'support':r['support'],'rhs':1} for r in rows['rows']],'Ordered48row tail')
 expected_binding=[{'family_row':i,'source_row':2598+i,'support':r['support'],'rhs':1,'ordered_mapping':r['map']} for i,r in enumerate(rows['rows'])]
 require(newsource['research_sixth_relaxed_binding']==expected_binding,'Augmented catalog map binding')
 return {'complete':True,'scope':'Exact finite replay only; the Lean proof is recorded separately. No logical-independence or global313 claim.','proof_steps':steps,'compatibility_tests_per_map':41,'literal_rows':count,'single_row_dominated':0,'checker_sha256':sha(Path(__file__).read_bytes())}
if __name__=='__main__':print(json.dumps(check(),indent=2))
