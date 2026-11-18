#!/usr/bin/env python3
"""Bounded integrity/index check for the parent checkpoint; no proof reruns."""
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
import resource

resource.setrlimit(resource.RLIMIT_AS, (150 << 20, 150 << 20))
ROOT = Path(__file__).resolve().parent


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


expected = {
    'low_split/capacity_checks/pass/result.json': 'PASS',
    'low_split_audit/left16_replay/data/retryB/result.json': 'PASS',
    'lean_terminal12_parent/real/data/result.json': 'PASS',
    'lean_terminal12_parent/finite/data/result.json': 'PASS',
    'lean_real_parent/data/result.json': 'PASS',
    'protection_models/forced16_parent/result.json': 'PASS',
    'protection_models/forced16_instance_parent/data/result.json': 'PASS',
    'fourcuts14_audit/data/result.json': 'PASS',
    'fourcuts14/data/result.json': 'UNKNOWN',
    'low_split/rooted_parent/result.json': 'PASS',
}
receipts = {}
for rel, status in expected.items():
    data = json.loads((ROOT / rel).read_text())
    assert data['status'] == status, (rel, data['status'])
    receipts[rel] = {'status': status, 'sha256': digest(ROOT / rel)}

fixed = json.loads((ROOT / 'protection_models/forced16_instance_parent/data/result.json').read_text())
assert fixed['modules'] == 338 and fixed['axiom_reports'] == 354
assert fixed['exact_axiom_lists_match']
assert fixed['transcription']['all_raw_labels_slots_factors_weights_match']
last = json.loads((ROOT / 'fourcuts14/data/result.json').read_text())
assert last['finished'] and last['compressed_roundtrip_verified']
assert last['hashes']['input.cnf'] == '3c6c1f83e2cf426ca13eb2e9ba7e363a1da42f1138cc3b9503c57601678e5788'

frozen = {}
for rel in ['fourcuts14_audit', 'low_split_audit/left16_replay', 'low_split/consequences']:
    packet = ROOT / rel
    manifest = packet / 'SHA256SUMS'
    entries = manifest.read_text().splitlines()
    for line in entries:
        if line.strip():
            assert digest(packet / line[66:]) == line[:64], (rel, line[66:])
    frozen[rel] = {'manifest_sha256': digest(manifest), 'files': len(entries)}

documents = [
    'README.md', 'RESULTS.md', 'NEXT_STEPS.md', 'RESOURCES.md',
    'low_split/CLOSURE.md', 'low_split/README.md',
    'low_split/longcup16/README.md', 'fourcuts14/README.md',
    'protection_models/forced16_instance_parent/README.md',
    'low_split/rooted_parent/README.md',
    'low_split/rooted_parent/COROLLARY.md',
]
links = 0
for rel in documents:
    path = ROOT / rel
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        if '://' in target or target.startswith('#'):
            continue
        assert (path.parent / target.split('#', 1)[0]).exists(), (rel, target)
        links += 1

files = {ROOT / rel for rel in documents}
files.update(ROOT / rel for rel in expected)
for rel in [
    'finalize_record.py', 'low_split/Capacity11.lean', 'low_split/Capacity16.lean',
    'low_split/capacity_check.py', 'augment_fourcuts14.py',
    'augment_left16_longcup.py', 'archive_cache_watch.py',
    'run_binary_cache.py', 'run_binary_options.py',
    'check_obstruction_cuts.py', 'check_allcap_controls.py',
    'data/final-shutdown.json', 'data/obstruction-cuts.json',
    'data/final-completion.json',
    'data/all-cap-parent-controls.json', 'data/final-frozen-packet-checks.json',
    'protection_models/forced16_instance_lean/data/manifest.json',
    'protection_models/forced16_instance_lean/FROZEN.json',
    'protection_models/forced16_lean/data/manifest.json',
]:
    files.add(ROOT / rel)
for rel in [
    'low_split/capacity_checks/pass', 'fourcuts14/data',
    'protection_models/forced16_parent',
    'protection_models/forced16_lean_parent',
    'protection_models/forced16_instance_parent',
    'lean_terminal12_parent', 'lean_real_parent',
    'low_split/rooted_parent',
]:
    for path in (ROOT / rel).rglob('*'):
        if path.is_file() and path.suffix in {'.py', '.json', '.md', '.log', '.txt', '.time'}:
            files.add(path)
manifest = {
    'status': 'PASS',
    'label': 'COMPUTED checkpoint integrity; not an additional proof',
    'checked_at': datetime.now().astimezone().isoformat(),
    'receipt_statuses': receipts,
    'handoff': {'path': str(ROOT.parents[3] / 'STATUS20261114_0840/README.md'),
                'sha256': digest(ROOT.parents[3] / 'STATUS20261114_0840/README.md')},
    'frozen_packets': frozen,
    'checked_local_links': links,
    'scope': 'Selected parent integration files, evidence receipts, and three final frozen packets. Large proofs remain pinned in their own accepted replay records.',
    'files': {str(p.relative_to(ROOT)): {'sha256': digest(p), 'bytes': p.stat().st_size}
              for p in sorted(files)},
}
(ROOT / 'data/final-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'files': len(files), 'local_links': links,
                  'frozen_packets': len(frozen), 'receipts': len(receipts),
                  'manifest_sha256': digest(ROOT / 'data/final-manifest.json')}))
