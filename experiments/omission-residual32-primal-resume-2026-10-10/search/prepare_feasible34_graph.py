import gzip,hashlib,itertools,json
from pathlib import Path
D=Path('.cache/resume313-primal');P=Path('experiments/omission-residual32-2598-primal-2026-10-10');raw=gzip.decompress((P/'source-2598.json.gz').read_bytes());sha=hashlib.sha256(raw).hexdigest();assert sha=='01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b';base=json.loads(raw)['constraints'];ep=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/rows.json');er=ep.read_bytes();rows=base+json.loads(er)['rows'];seeds=set()
for seed in json.loads((D/'feasible33-input.json').read_text())['seeds']:
 for a in range(1,154):
  if a not in seed:seeds.add(tuple(sorted(seed+[a])))
old=json.loads((P/'candidates.json').read_text())['candidates'][0]['holes'];oldset=set(old);deficient=[r for r in rows if len(oldset&set(r['support']))<r['rhs']]
for a,b in itertools.combinations([i for i in range(1,154) if i not in oldset],2):
 trial=oldset|{a,b}
 if all(len(trial&set(r['support']))>=r['rhs'] for r in deficient):seeds.add(tuple(sorted(trial)))
seeds=sorted(seeds)
for seed in seeds:assert len(seed)==34 and 0 not in seed and all(len(set(seed)&set(r['support']))>=r['rhs'] for r in rows)
lines=[f'154 {len(rows)} {len(seeds)}']+[f"{r['rhs']} {len(r['support'])} "+' '.join(map(str,r['support'])) for r in rows]+[' '.join(map(str,s)) for s in seeds];(D/'feasible34-augmented-input.txt').write_text('\n'.join(lines)+'\n');(D/'feasible34-augmented-input.json').write_text(json.dumps({'source':str(P/'source-2598.json.gz'),'source_sha256':sha,'additional_rows':str(ep),'additional_rows_sha256':hashlib.sha256(er).hexdigest(),'seeds_count':len(seeds),'seeds':seeds,'input_sha256':hashlib.sha256((D/'feasible34-augmented-input.txt').read_bytes()).hexdigest()},indent=2)+'\n');print('feasible34 seeds',len(seeds))
