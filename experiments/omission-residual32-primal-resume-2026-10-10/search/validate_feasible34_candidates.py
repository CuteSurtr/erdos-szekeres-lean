import gzip,hashlib,json
from pathlib import Path
D=Path('.cache/resume313-primal');P=Path('experiments/omission-residual32-2598-primal-2026-10-10');raw=gzip.decompress((P/'source-2598.json.gz').read_bytes());base=json.loads(raw)['constraints'];A=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/rows.json');ar=A.read_bytes();extra=json.loads(ar)['rows'];rows=base+extra;events=[json.loads(line) for line in (D/'feasible34-augmented-5m-events.jsonl').read_text().splitlines()];out=[]
for e in events:
 if e['event']!='new_single_deficit':continue
 holes=e['holes'];S=set(holes);b=sum(1<<i for i in holes);assert len(S)==len(holes)==32 and 0 not in S
 violations=[{'row':j,'count':len(S&set(r['support'])),'rhs':r['rhs']} for j,r in enumerate(rows) if len(S&set(r['support']))<r['rhs']]
 assert len(violations)==1 and violations[0]['row']==e['row'] and violations[0]['rhs']-violations[0]['count']==1
 assert all((b&sum(1<<i for i in r['support'])).bit_count()==len(S&set(r['support'])) for r in rows)
 out.append({'holes':holes,'violations':violations,'satisfied_rows':2645,'exact_set_and_bitset_replay':True})
record={'scope':'Distinct-row near-models, not satisfying witnesses. Every candidate has32holes and fails exactly one of2646rows by1.','source':str(P/'source-2598.json.gz'),'source_sha256':hashlib.sha256(raw).hexdigest(),'additional_rows':str(A),'additional_rows_sha256':hashlib.sha256(ar).hexdigest(),'candidates':out};(D/'feasible34-checked-near-models.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
