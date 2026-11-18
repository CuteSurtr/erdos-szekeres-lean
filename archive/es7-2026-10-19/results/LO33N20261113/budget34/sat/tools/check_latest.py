#!/usr/bin/env python3
"""Check a verified hole vector against the latest announced immutable pool."""
import datetime
import gzip
import hashlib
import json
from pathlib import Path
import sys

holes_file, output = map(Path, sys.argv[1:])
root = Path('/home/jay/research/data/es308-20261114')
events_path = root/'continuation/events.json'
events_bytes = events_path.read_bytes()
events = json.loads(events_bytes)
version = max([3]+[int(e['version']) for e in events
                       if e.get('event') == 'CERTIFIED_ROWS_APPENDED'])
folder = root/f'inputs/s20-v{version}'
extra_bytes = (folder/'extra.json').read_bytes()
extra = json.loads(extra_bytes)
manifest_bytes = (folder/'manifest.json').read_bytes()
manifest = json.loads(manifest_bytes)
extra_sha = hashlib.sha256(extra_bytes).hexdigest()
assert extra_sha == manifest['extra_sha256']
base_bytes = (root/'inputs/source-2650.json.gz').read_bytes()
assert hashlib.sha256(base_bytes).hexdigest() == '8c7fe9ef5264182524095d46ef50ed6bc691cab425efa965756d1870112241aa'
base = json.loads(gzip.decompress(base_bytes))
F = [i for i, s in enumerate(base['states']) if s[0] >= 5]
Lo = [i for i, s in enumerate(base['states']) if s[0] <= 4]
assert extra[:2] == [{'support': F, 'rhs': 20}, {'support': Lo, 'rhs': 14}]
h = json.loads(holes_file.read_text())
assert len(h) == 154 and all(type(v) is int and v in (0, 1) for v in h)
rows = base['constraints']+extra
assert len(rows) == manifest['rows']
lhs, violations = [], []
for i, row in enumerate(rows):
    S, d = row['support'], row['rhs']
    assert len(S) == len(set(S)) and all(type(v) is int and 0 <= v < 154 for v in S)
    assert type(d) is int and 1 <= d <= len(S)
    count = sum(h[v] for v in S)
    lhs.append(count)
    if count < d:
        violations.append({'row': i, 'support': S, 'rhs': d, 'lhs': count})
valid = not violations and h[0] == 0 and sum(h) <= 34
result = {'label': 'COMPUTED latest-pool integer check; '+('SURVIVES' if valid else 'ALREADY EXCLUDED'),
          'checked_at': datetime.datetime.now().isoformat(), 'latest_announced_version': version,
          'extra_path': str(folder/'extra.json'), 'extra_sha256': extra_sha,
          'events_snapshot_sha256': hashlib.sha256(events_bytes).hexdigest(),
          'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
          'row_count': len(rows), 'valid': valid, 'holes': sum(h),
          'F_holes': sum(h[i] for i in F), 'Lo_holes': sum(h[i] for i in Lo),
          'h0': h[0], 'violated_rows': violations, 'row_lhs': lhs,
          'hole_bits_index_0_first': ''.join(map(str, h)),
          'scope': 'abstract finite rows; no point realization claimed'}
output.write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'row_lhs'}, indent=2))
