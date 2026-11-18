#!/usr/bin/env python3
"""Sequential bounded rooted-CNF discovery and certification; run in a unit."""
import argparse
import hashlib
import json
import os
import resource
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BIN = Path('/home/jay/research/data/delta3-codex-20261113/resume/compact/compact_cnf')
RUNNER = HERE.parent / 'pool/run_cnf.py'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--n', type=int, choices=(7, 8), required=True)
    ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (900 << 20, 900 << 20))
    os.environ.update(OMP_NUM_THREADS='1', OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1')
    a.out.mkdir(parents=True, exist_ok=False)
    frozen = a.out / 'source'
    frozen.mkdir()
    sources = [HERE/'rooted_sweep.py', HERE/'rooted_formula.py', RUNNER,
               HERE.parent/'compact/compact_cnf.cpp', BIN]
    provenance = {}
    for p in sources:
        content = p.read_bytes()
        provenance[str(p)] = hashlib.sha256(content).hexdigest()
        if p.suffix in ('.py', '.cpp'):
            (frozen / p.name).write_bytes(content)
    assert provenance[str(BIN)] == '5bd884acb41434dcc41556f9bab874926397d449efd3b971cb3bb2141379bbe1'
    (a.out/'source_hashes.json').write_text(json.dumps(provenance, indent=2)+'\n')
    outcomes = []
    for m in range(a.n+2, 17):
        case = a.out/f'm{m}'
        case.mkdir()
        full, rooted = case/'full.cnf', case/'rooted.cnf'
        commands = [
            [str(BIN), '--m', str(m), '--n', str(a.n), '--out', str(full), '--map', str(case/'full.map')],
            [sys.executable, '-B', str(frozen/'rooted_formula.py'), '--m', str(m), '--n', str(a.n),
             '--input', str(full), '--output', str(rooted)],
        ]
        for i, cmd in enumerate(commands):
            with (case/f'generate-{i}.log').open('w') as log:
                subprocess.run(['/usr/bin/timeout', '--kill-after=2', '20']+cmd,
                               stdout=log, stderr=subprocess.STDOUT, check=True, timeout=24)
        sha = hashlib.sha256(rooted.read_bytes()).hexdigest()
        cmd = [sys.executable, '-B', str(frozen/'run_cnf.py'), '--cnf', str(rooted), '--sha256', sha,
               '--out', str(case/'solve'), '--seconds', '15' if m <= 12 else '60',
               '--cake-seconds', '60', '--as-mib', '900', '--heap', '600']
        commands.append(cmd)
        (case/'commands.json').write_text(json.dumps(commands, indent=2)+'\n')
        with (case/'runner.log').open('w') as log:
            subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=350)
        result = json.loads((case/'solve/result.json').read_text())
        outcomes.append(dict(m=m, n=a.n, status=result['status'], case=str(case)))
        (a.out/'status.json').write_text(json.dumps(outcomes, indent=2)+'\n')
        print(json.dumps(outcomes[-1]), flush=True)
        if result['status'] == 'SAT_AUDIT_PENDING':
            break
    (a.out/'DONE.json').write_text(json.dumps(dict(outcomes=outcomes, all_completed=True), indent=2)+'\n')


if __name__ == '__main__':
    main()
