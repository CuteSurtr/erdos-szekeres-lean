#!/usr/bin/env python3
"""Fresh bounded LRAT runs for the three frozen coordinate obstructions."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path('/home/jay/research/data/delta3-codex-20261113/selection/certificates')
CASES = [
    ('terminal', 'terminal/data/witness.core.cnf', '5318a34178cd3aa6acb9f83de54f4e9510b0a968a98fc0c8eb40b20ce135d0dd'),
    ('repair7', 'repair/data/rightmost-n7-one.cnf', 'ef26f775f629af551be837b84e9f106948b4163e674018e9980fd225b5df0edd'),
    ('repair8', 'repair/data/rightmost-n8-one.cnf', '6517d49858bbaf2ae7cd743fb1d4597f62f8320ad05642a9952ea8ae65950f74'),
]
OUT.mkdir(parents=True, exist_ok=False)
results = []
for tag, relative, expected in CASES:
    source = HERE / relative
    assert hashlib.sha256(source.read_bytes()).hexdigest() == expected
    cmd = [sys.executable, '-B', str(HERE.parent/'pool/run_cnf.py'), '--cnf', str(source),
           '--sha256', expected, '--out', str(OUT/tag), '--seconds', '10',
           '--cake-seconds', '15', '--as-mib', '400', '--heap', '128']
    subprocess.run(cmd, check=True, timeout=50)
    r = json.loads((OUT/tag/'result.json').read_text())
    assert r['status'] == 'UNSAT_CERTIFIED'
    results.append(dict(tag=tag, cnf_sha256=expected, status=r['status'],
                        proof_sha256=r['hashes']['proof.lrat']))
(OUT/'DONE.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results))
