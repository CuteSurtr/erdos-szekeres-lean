#!/usr/bin/env python3
"""Make a new immutable row-file version; existing inputs are never rewritten."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import resource

resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20))
W=Path('/home/jay/research/data/es308-20261114')
p=argparse.ArgumentParser()
p.add_argument('previous');p.add_argument('accepted',type=Path);p.add_argument('new')
a=p.parse_args()
old=W/'inputs'/a.previous;out=W/'inputs'/a.new
assert old.resolve().is_relative_to(W/'inputs') and out.resolve().is_relative_to(W/'inputs')
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
source=W/'inputs/source-2650.json.gz'
assert sha(source)=='8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa'
base=json.loads(gzip.decompress(source.read_bytes()))
extra=json.loads((old/'extra.json').read_text())
F=[i for i,s in enumerate(base['states']) if s[0]>=5]
Lo=[i for i,s in enumerate(base['states']) if s[0]<=4]
assert extra[0]['support']==F and extra[1]['support']==Lo
assert extra[0]['rhs']+extra[1]['rhs'] in (34,35)  # v2: budget-35 slices
seen={(tuple(sorted(r['support'])),r['rhs']) for r in base['constraints']+extra}
accepted=json.loads(a.accepted.read_text());added=[];bindings=[]
for r in accepted:
    assert r['label']=='CERTIFIED' and r['verdict']=='s VERIFIED UNSAT' and r['rhs']==1
    support=r['support']
    assert support==sorted(set(support)) and all(type(i) is int and 0<=i<154 for i in support)
    assert (tuple(support),1) not in seen
    stage=r['stages'][-1];cake=Path(stage['log'])
    assert 's VERIFIED UNSAT' in cake.read_text().splitlines()
    assert sha(cake)==stage['log_sha256']
    for path,identity in r['files'].items():
        assert sha(path)==identity['sha256'] and Path(path).stat().st_size==identity['bytes']
    assert r['generation']['support']==support
    assert r['generation']['cnf_sha256']==sha(cake.with_name('system.cnf'))
    seen.add((tuple(support),1));added.append({'support':support,'rhs':1})
    bindings.append({'support':support,'cnf_sha256':sha(cake.with_name('system.cnf')),
                     'lrat_sha256':sha(cake.with_name('system.lrat')),'cake_log_sha256':sha(cake),
                     'acceptance_receipt':str(cake.with_name('receipt.json'))})
assert added
newextra=extra+added;rows=base['constraints']+newextra
assert rows[:len(base['constraints'])+len(extra)]==base['constraints']+extra
out.mkdir(exist_ok=False)
ep=out/'extra.json';ep.write_text(json.dumps(newextra,indent=1)+'\n')
rp=out/'rows.txt'
with rp.open('w') as f:
    f.write('FASTBB-ROWS 1\n')
    f.write(f'source {source}\nsource_sha256 {sha(source)}\n')
    f.write(f'extra {ep}\nextra_sha256 {sha(ep)}\nstates 154\nbase_rows 2650\nrows {len(rows)}\n')
    for r in rows:f.write(f'{r["rhs"]} {len(r["support"])} '+' '.join(map(str,r['support']))+'\n')
manifest={'previous':str(old),'previous_extra_sha256':sha(old/'extra.json'),
          'previous_rows_sha256':sha(old/'rows.txt'),'accepted_source':str(a.accepted),
          'accepted_source_sha256':sha(a.accepted),'appended_rows':len(added),'rows':len(rows),
          'extra_sha256':sha(ep),'rows_sha256':sha(rp),'bindings':bindings,
          'status':'CERTIFIED appended rows; independent replay recorded separately'}
(out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({k:v for k,v in manifest.items() if k!='bindings'},indent=2))
