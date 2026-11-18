#!/usr/bin/env python3
"""Sequential bounded replay. Run under the documented systemd resource unit."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/lean')
RUNNER = ROOT.parent / 'lean/check.py'
ap = argparse.ArgumentParser()
ap.add_argument('--prefix', required=True)
args = ap.parse_args()
assert args.prefix.replace('-', '').replace('_', '').isalnum()
manifest = json.loads((ROOT / 'data/manifest.json').read_text())
checks = []
for entry in manifest['replay_order']:
    source = (ROOT / entry['source']).resolve()
    assert hashlib.sha256(source.read_bytes()).hexdigest() == entry['sha256']
    tag = args.prefix + '-' + source.stem.lower()
    result = subprocess.run([sys.executable, '-B', str(RUNNER), str(source), tag, '--export'],
                            timeout=32, check=False)
    record = json.loads((SCRATCH / (tag + '.json')).read_text())
    checks.append({'source': entry['source'], 'tag': tag, 'exit_code': result.returncode})
    if result.returncode or record['exit_code'] or record['stop_reason']:
        (SCRATCH / (args.prefix + '-DONE.json')).write_text(json.dumps(
            {'status': 'FAIL', 'checks': checks}, indent=2) + '\n')
        raise SystemExit(1)
(SCRATCH / (args.prefix + '-DONE.json')).write_text(json.dumps(
    {'status': 'PASS', 'checks': checks}, indent=2) + '\n')
print('PASS: all sequential module checks completed; inspect each axiom log.')
