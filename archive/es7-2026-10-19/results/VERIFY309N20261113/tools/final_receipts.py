"""Aggregate required successful evidence; refuses to finalize incomplete coverage."""
import collections, hashlib, json, pathlib, shutil, sys
ROOT=pathlib.Path(__file__).resolve().parents[5]
R=ROOT/'cloud/es7-2026-10-19/results/VERIFY309N20261113'
V=pathlib.Path('/home/jay/research/data/verify309-codex-20261113')
def read(p): return [json.loads(l) for l in p.open()]
n=read(V/'rows/certificates.jsonl'); r=read(V/'residual/certificates.jsonl')
nc=collections.Counter(x['result'] for x in n); rc=collections.Counter(x['result'] for x in r)
assert len(n)==len({x['full_sha256'] for x in n})==621
assert len(r)==len({tuple(x['support']) for x in r})==578
assert nc['CERTIFIED']==272 and rc['CERTIFIED']==448
assert nc['INHERITED independently verified identical CNF']==349
assert rc['INHERITED independently verified identical CNF']==130
assert 's VERIFIED UNSAT' in (V/'cake57.log').read_text().splitlines()
for row in n:
    if row['result']=='CERTIFIED': assert 's VERIFIED UNSAT' in (V/'rows'/(row['full_sha256']+'.cake.log')).read_text().splitlines()
for row in r:
    assert row['cnf_matches_record']
    if row['result']=='CERTIFIED': assert 's VERIFIED UNSAT' in (V/'residual'/(row['cnf_sha256']+'.cake.log')).read_text().splitlines()
mono=read(R/'logs/mono.jsonl')[-1]; tree=json.loads((R/'logs/s20-summary.json').read_text()); real=read(R/'logs/real.jsonl')[-1]
assert mono['result']=='ALL CLAUSES RECOGNIZED' and mono['clauses']==206705
assert tree['verdict']=='EXACT TREE' and tree['pending']==1 and tree['minimum_margin']==1
for sub,name in [('rows','n66-row-certificates.jsonl'),('residual','residual-row-certificates.jsonl')]:
    shutil.copyfile(V/sub/'certificates.jsonl',R/'logs'/name)
out={'verdict':'ALL THREE REQUIRED LINKS CONFIRMED','N66_bound':57,'N66_certificate_coverage':dict(nc),'residual_certificate_coverage':dict(rc),'residual_fresh_lrat_hash_matches':sum(x.get('lrat_matches_record',False) for x in r),'main_cnf_sha256':mono['trim_sha256'],'fresh_main_lrat_sha256':(V/'fresh57.lrat.sha256').read_text().split()[0],'slice20':{k:v for k,v in tree.items() if k not in ('context_hashes',)},'real_controls':real,'scope':'computer-assisted proof, not a fully Lean-checked theorem'}
(R/'logs/final-summary.json').write_text(json.dumps(out,indent=2)+'\n')
bins={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [pathlib.Path('/usr/bin/cadical'),pathlib.Path('/home/jay/.local/bin/cake_lpr')]}
(R/'logs/binary-hashes.json').write_text(json.dumps(bins,indent=2)+'\n')
print(json.dumps(out,indent=2))
