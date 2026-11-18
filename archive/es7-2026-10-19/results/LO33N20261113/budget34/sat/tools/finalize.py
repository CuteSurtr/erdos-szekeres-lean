#!/usr/bin/env python3
"""Freeze integrity/status receipts after all SAT sidecar units have stopped."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess

W = Path('/home/jay/research/data/es308-20261114/sat')
R = Path('/home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/LO33N20261113/budget34/sat')
active = subprocess.check_output(['systemctl', '--user', 'list-units',
    'nov13c-vfy-308-sat-*', '--type=service', '--state=active', '--no-legend', '--plain'], text=True)
assert not active.strip(), 'a SAT sidecar unit is still active'
now = datetime.datetime.now().isoformat()
statuses = {str(p.relative_to(W)): json.loads(p.read_text()) for p in W.rglob('status.json')}
for k, value in statuses.items():
    assert 'running' not in value['label'].lower(), (k, value['label'])
witnesses = []
for p in sorted(W.rglob('witness.json')):
    obj = json.loads(p.read_text())
    assert obj['valid'] and len(obj['hole_bits_index_0_first']) == 154
    assert obj['holes'] == 34 and obj['F_holes'] == 20 and obj['Lo_holes'] == 14 and obj['h0'] == 0
    witnesses.append({k:obj[k] for k in ['hole_bits_index_0_first', 'hole_indices',
        'holes', 'F_holes', 'Lo_holes', 'cnf_clauses_checked', 'cnf_sha256',
        'pool_sha256', 'solution_sha256']} | {'receipt': str(p)})
resource_receipt = {'frozen_at': now, 'active_sat_units': [],
    'scope': 'only this independent SAT sidecar', 'thread_allocation': 1,
    'CPU_affinity': [11], 'address_space_reservation_MiB': 1200,
    'long_unit_MemoryMax_MiB': 1600, 'MemorySwapMax': 0,
    'initial_CaDiCaL_peak_RSS_MiB': 135.13,
    'CP_SAT_peak_RSS_KiB': max(v.get('peak_RSS_KiB', 0) for v in statuses.values()),
    'proof_policy': 'raw and compressed retained; partial research LRAT is not a certificate'}
(W/'resource-receipt.json').write_text(json.dumps(resource_receipt, indent=2)+'\n')
(R/'data/resource-receipt.json').write_text(json.dumps(resource_receipt, indent=2)+'\n')
summary = {'label': 'COMPUTED explicit SAT witnesses; search verdicts separately scoped',
    'frozen_at': now, 'ES8_improvement_established_by_this_track': False,
    'witnesses': witnesses, 'runs': statuses, 'resource_receipt': resource_receipt}
(R/'data/result-summary.json').write_text(json.dumps(summary, indent=2)+'\n')


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1024**2), b''):
            h.update(block)
    return h.hexdigest()


files = []
excluded = {W/'FINAL_MANIFEST.json', R/'data/final-manifest.json'}
for base in (R, W):
    for p in sorted(base.rglob('*')):
        if p.is_file() and p not in excluded:
            files.append({'path': str(p), 'bytes': p.stat().st_size, 'sha256': digest(p)})
manifest = {'label': 'file integrity only; not an additional proof', 'frozen_at': now,
            'files': files, 'file_count': len(files), 'total_bytes': sum(f['bytes'] for f in files)}
encoded = json.dumps(manifest, indent=2)+'\n'
(W/'FINAL_MANIFEST.json').write_text(encoded)
(R/'data/final-manifest.json').write_text(encoded)
print(json.dumps({'frozen_at': now, 'witnesses': len(witnesses),
                  'files_hashed': len(files), 'bytes': manifest['total_bytes'],
                  'active_sat_units': [], 'manifest_sha256': digest(W/'FINAL_MANIFEST.json')}, indent=2))
