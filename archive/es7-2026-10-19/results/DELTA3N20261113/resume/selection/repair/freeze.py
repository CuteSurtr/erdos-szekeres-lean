#!/usr/bin/env python3
"""Hash this track and retained scratch, and pin the parent's completed certificates.

Read-only outside this track; does not run any solver, checker or search.
"""
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
SCRATCH=Path('/home/jay/research/data/delta3-codex-20261113/selection/repair')
CERTS=SCRATCH.parent/'certificates'
def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()
certs=[]
for n in (7,8):
    path=CERTS/f'repair{n}'
    result=json.loads((path/'result.json').read_text())
    assert result['status']=='UNSAT_CERTIFIED'
    assert 's VERIFIED UNSAT' in (path/'cake.log').read_text().splitlines()
    assert sha(Path(result['cnf']))==result['hashes']['input.cnf']
    for name in ('proof.lrat','proof.lrat.zst','cake.log'):
        assert sha(path/name)==result['hashes'][name]
    certs.append(dict(n=n,label='CERTIFIED by parent',source=str(path/'result.json'),
                      cnf=result['cnf'],hashes=result['hashes'],cake_line='s VERIFIED UNSAT',
                      proof_bytes=result['proof_bytes'],compressed_bytes=result['compressed_bytes'],
                      compressed_roundtrip_verified_by_parent=result['compressed_roundtrip_verified'],
                      local_action='Read logs and matched hashes; no local cake replay'))
parent=HERE.parent/'data/parent_obstructions.json'
parent_rows=[r for r in json.loads(parent.read_text()) if r['kind'] in ('repair7','repair8')]
assert len(parent_rows)==2
for row in parent_rows:
    assert sha(HERE.parent/row['source'])==row['source_sha256']
    assert sha(HERE.parent/row['cnf'])==row['cnf_sha256']
data=dict(certificates=certs,parent_independent_audit=str(parent),parent_audit_sha256=sha(parent),parent_audit_entries=parent_rows)
(HERE/'data/PARENT_CERTIFICATES.json').write_text(json.dumps(data,indent=2)+'\n')
controls=json.loads((HERE/'data/controls.json').read_text())
result=dict(status='FROZEN',track='repair',labels=['PROVED written lemmas','COMPUTED independently confirmed real predicates','CERTIFIED full one-blue CNFs by parent'],
            conclusion='One-old-blue repair fails even at a rightmost point for n7/m14 and n8/m16; exact minimum is two.',
            frozen=controls['frozen'],positive_theorem='For n>=5, five-cap-free S and |S|<=n+2, every old weak Delta has repair cost at most one; no extreme-root or convex-n-gon-free assumption.',
            scope='No weak Delta existence refutation; no global minimality or universal two-blue sufficiency claim.',
            jobs_remaining=0,parent_certificates='data/PARENT_CERTIFICATES.json')
(HERE/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
files=[]
for base,kind in ((HERE,'track'),(SCRATCH,'scratch')):
    for p in sorted(base.rglob('*')):
        if p.is_file() and p.name!='MANIFEST.json':files.append(dict(kind=kind,path=str(p),bytes=p.stat().st_size,sha256=sha(p)))
(HERE/'MANIFEST.json').write_text(json.dumps(dict(files=files,scope='repair track and retained scratch only; excludes this manifest'),indent=2)+'\n')
print(json.dumps(dict(files=len(files),certificates=[dict(n=c['n'],label=c['label']) for c in certs])))
