#!/usr/bin/env python3
"""Replay five T12 real-bridge modules, checking hashes, diagnostics and every axiom audit.

Requires the frozen finite packet's freshly replayed .olean dependencies in scratch.
Run only after allocation under the README's bounded systemd command.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/lean-terminal12')
ap = argparse.ArgumentParser()
ap.add_argument('--prefix', required=True)
args = ap.parse_args()
assert args.prefix.replace('-', '').replace('_', '').isalnum()
manifest = json.loads((ROOT / 'data/real-manifest.json').read_text())
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
for entry in manifest['prerequisite_sources']:
    assert digest((ROOT / entry['source']).resolve()) == entry['sha256'], entry
assert digest(ROOT / 'T12check_real.py') == manifest['runner_sha256']
repo = Path('/home/jay/research/lean/erdos-szekeres-lean')
for entry in manifest['project_cache']:
    stem = entry['module'].replace('.', '/')
    assert digest(repo / (stem + '.lean')) == entry['source_sha256']
    assert digest(repo / '.lake/build/lib/lean' / (stem + '.olean')) == entry['olean_sha256']
checks = []
status = 'FAIL'
try:
    for entry in manifest['checks']:
        source = ROOT / entry['source']
        assert digest(source) == entry['sha256'], source
        tag = args.prefix + '-' + source.stem.lower()
        result = subprocess.run([sys.executable, '-B', str(ROOT / 'T12check_real.py'),
                                 str(source), tag, '--export'], timeout=32, check=False)
        record = json.loads((SCRATCH / (tag + '.json')).read_text())
        log = (SCRATCH / (tag + '.log')).read_text()
        audits = {name: [a.strip() for a in raw.split(',') if a.strip()]
                  for name, raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", log)}
        audits.update({name: [] for name in re.findall(
            r"'([^']+)' does not depend on any axioms", log)})
        checks.append({'source': entry['source'], 'tag': tag,
                       'exit_code': result.returncode, 'axiom_reports': audits})
        assert result.returncode == record['exit_code'] == 0
        assert record['stop_reason'] is None
        assert record['source_sha256'] == entry['sha256']
        assert not re.search(r'\b(error|warning)(?:\(|:)', log), log
        assert audits == entry['axiom_reports'], audits
        assert record['rusage_maxrss_kib'] < 2000 * 1024
    status = 'PASS'
finally:
    (SCRATCH / (args.prefix + '-DONE.json')).write_text(json.dumps(
        {'status': status, 'checks': checks}, indent=2) + '\n')
print('PASS: all five T12 real modules and all 27 axiom reports match the frozen real bridge.')
