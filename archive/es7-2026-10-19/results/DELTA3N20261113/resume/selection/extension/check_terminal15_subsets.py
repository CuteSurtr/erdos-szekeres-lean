#!/usr/bin/env python3
"""Replay all recorded 13/14-point restrictions using independent exact geometry."""
import hashlib
import importlib.util
from itertools import combinations as C
import json
from pathlib import Path
import resource
import shutil

H = Path(__file__).resolve().parent
W = Path('/home/jay/research/data/delta3-codex-20261113/extension')
resource.setrlimit(resource.RLIMIT_AS, (300 << 20, 300 << 20))
spec = importlib.util.spec_from_file_location('geometry', H.parent / 'boundary/check_envelope.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)
P = json.loads((H / 'terminal15/data/balanced.json').read_text())['P']
out = H / 'terminal15/subsets'
out.mkdir(exist_ok=False)
mask = lambda points: sum(1 << i for i in points)
vertices = lambda bits: [i for i in range(15) if bits >> i & 1]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
cap4 = [K for K in C(range(15), 4) if all(G.det(P, *t) < 0 for t in C(K, 3))]
results = []
for size in (13, 14):
    path = W / f'terminal-subsets/model15-size{size}.jsonl'
    records = [json.loads(line) for line in path.read_text().splitlines()]
    seen = set()
    certificates = []
    for row in records:
        bits, selected = row['W'], row['A']
        assert bits not in seen and row['m'] == size and row['result'] == 1
        assert bits.bit_count() == size and selected & ~bits == 0
        seen.add(bits)
        A = vertices(selected)
        assert G.maxima(P, A)[0] < 4
        assert G.maxima(P, vertices(bits ^ selected))[2] < 6
        tails = {tuple(K[-2:]): K for K in cap4 if mask(K) & bits == mask(K)}
        support = []
        for t in C(A, 3):
            if G.det(P, *t) < 0:
                assert t[-2:] in tails
                support.append({'selected_cap_triple': t, 'ambient_fourcap': tails[t[-2:]]})
        certificates.append({'W': vertices(bits), 'A': A, 'terminal_certificates': support})
    assert seen == {mask(points) for points in C(range(15), size)}
    shutil.copyfile(path, out / path.name)
    (out / f'witnesses{size}.json').write_text(json.dumps(certificates, indent=2) + '\n')
    results.append({'size': size, 'cases': len(records), 'input_sha256': sha(path),
                    'terminal_cap_triples_checked': sum(len(c['terminal_certificates']) for c in certificates)})
receipt = {'label': 'COMPUTED independent positive-witness replay', 'status': 'PASS',
           'results': results, 'all_13_and_14_restrictions_checked': True,
           'script_sha256': sha(Path(__file__)), 'geometry_sha256': sha(H.parent / 'boundary/check_envelope.py'),
           'coordinate_sha256': sha(H / 'terminal15/data/balanced.json'),
           'finder_sha256': sha(H / 'terminal_subsets.cpp'),
           'scope': 'These 120 subsets of this fixed realization only. Smaller sizes use the separate theorem; no global 14-point claim.'}
(out / 'replay.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
