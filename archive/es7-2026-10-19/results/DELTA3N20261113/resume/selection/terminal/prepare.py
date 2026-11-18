"""Freeze coordinate inputs only; no imports from an earlier geometric checker."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path('/home/jay/research/data/delta3-codex-20261113/selection/terminal')
OUT.mkdir(parents=True, exist_ok=True)
records = []

def add(name, p, source, key='P'):
    assert all(isinstance(c, int) for q in p for c in q)
    p = sorted(p)
    for n in (7, 8):
        stem = f'{name}-n{n}'
        text = f'{len(p)} {n}\n' + ''.join(f'{x} {y}\n' for x, y in p)
        (OUT / f'{stem}.points').write_text(text)
        records.append(dict(stem=stem, n=n, P=p, source=str(source), source_key=key,
                            source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                            points_sha256=hashlib.sha256(text.encode()).hexdigest()))

fixtures = ROOT / 'search/fixtures.json'
for name, record in json.loads(fixtures.read_text()).items():
    add(name, record['P'], fixtures, name + '.P')
for name, relative in [
    ('compact7', 'resume/compact/real_n7m16.json'),
    ('compact8', 'resume/compact/real_n8m16.json'),
    ('target8', 'resume/compact/real_n8m16_targeted.json'),
    ('star12', 'resume/pool/data/maximal/real-star.json'),
    ('cup15', 'coordinator/data/cup15/realized.json')]:
    path=ROOT / relative
    data=json.loads(path.read_text())
    add(name,data['P'],path)
for path in sorted((ROOT.parent / 'DELTA2N20261113/data/cex').glob('*_real.json')):
    data=json.loads(path.read_text())
    if data.get('P'): add(path.stem,data['P'],path)
(OUT / 'inputs.json').write_text(json.dumps(records, indent=2)+'\n')
print(json.dumps([dict(stem=r['stem'],m=len(r['P'])) for r in records]))
