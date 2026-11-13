import gzip,hashlib,json
from pathlib import Path
D=Path('.cache/resume313-primal');P=Path('experiments/omission-residual32-2598-primal-2026-10-10');raw=gzip.decompress((P/'source-2598.json.gz').read_bytes());sha=hashlib.sha256(raw).hexdigest();assert sha=='01d4fde13ae0ca43427540a3d529e7e29b875936332af2cc4ef7d423edee469b';rows=json.loads(raw)['constraints'];c=json.loads((P/'candidates.json').read_text())['candidates'];best=set(c[2]['holes']);seeds=[sorted(best|{a}) for a in rows[205]['support']];old=set(c[0]['holes']);trial=sorted(old|{65});seeds += [trial] if all(len(set(trial)&set(r['support']))>=r['rhs'] for r in rows) else []
for seed in seeds:assert len(seed)==33 and 0 not in seed and all(len(set(seed)&set(r['support']))>=r['rhs'] for r in rows)
lines=[f'154 {len(rows)} {len(seeds)}']+[f"{r['rhs']} {len(r['support'])} "+' '.join(map(str,r['support'])) for r in rows]+[' '.join(map(str,s)) for s in seeds];(D/'feasible33-input.txt').write_text('\n'.join(lines)+'\n');(D/'feasible33-input.json').write_text(json.dumps({'source':str(P/'source-2598.json.gz'),'source_sha256':sha,'seeds':seeds,'input_sha256':hashlib.sha256((D/'feasible33-input.txt').read_bytes()).hexdigest()},indent=2)+'\n')

A=Path('experiments/omission-residual32-sixth-relaxed-2026-10-10/rows.json'); ar=A.read_bytes(); extra=json.loads(ar)['rows']; assert len(extra)==48; augmented=rows+extra
assert all(all(len(set(seed)&set(r['support']))>=r['rhs'] for r in extra) for seed in seeds)
lines=[f'154 {len(augmented)} {len(seeds)}']+[f"{r['rhs']} {len(r['support'])} "+' '.join(map(str,r['support'])) for r in augmented]+[' '.join(map(str,seed)) for seed in seeds]
(D/'feasible33-augmented-input.txt').write_text('\n'.join(lines)+'\n')
(D/'feasible33-augmented-input.json').write_text(json.dumps({'source':str(P/'source-2598.json.gz'),'source_sha256':sha,'additional_rows':str(A),'additional_rows_sha256':hashlib.sha256(ar).hexdigest(),'additional_rows_status':'prospective until separate Lean check','seeds':seeds,'input_sha256':hashlib.sha256((D/'feasible33-augmented-input.txt').read_bytes()).hexdigest()},indent=2)+'\n')
