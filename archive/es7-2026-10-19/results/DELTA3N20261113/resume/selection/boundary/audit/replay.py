#!/usr/bin/env python3
"""Read-only independent cake_lpr replay, one explicitly allocated short job."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
ROOT = Path('/home/jay/research/data/delta3-codex-20261113/boundary/terminal')
CAKE = Path('/home/jay/.local/bin/cake_lpr')


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


n = int(sys.argv[1])
assert n in (6, 7, 8)
cnf, proof = ROOT/f'n{n}/input.cnf', ROOT/f'n{n}/solve/proof.lrat'
paths = [cnf, proof, CAKE]
before = {str(p): sha(p) for p in paths}
cmd = ['/usr/bin/timeout', '20s', '/usr/bin/prlimit', '--as=838860800', '--cpu=18',
       str(CAKE), '--CML_HEAP_SIZE=600', '--CML_STACK_SIZE=32', str(cnf), str(proof)]
log = HERE/f'data/replay-n{n}.log'
timing = HERE/f'data/replay-n{n}.time'
start = time.monotonic()
with log.open('w') as f:
    completed = subprocess.run(['/usr/bin/time', '-v', '-o', str(timing)]+cmd,
                               stdout=f, stderr=subprocess.STDOUT)
after = {str(p): sha(p) for p in paths}
lines = log.read_text().splitlines()
accepted = before == after and 's VERIFIED UNSAT' in lines
record = dict(n=n, label='CERTIFIED' if accepted else 'NOT CONFIRMED',
              command=cmd, exit_code=completed.returncode, exact_verdict_line='s VERIFIED UNSAT' in lines,
              input_hashes_before=before, input_hashes_after=after, stable=before == after,
              log_sha256=sha(log), replay_source_sha256=sha(Path(__file__)),
              proof_bytes=proof.stat().st_size, seconds=round(time.monotonic()-start, 3))
(HERE/f'data/replay-n{n}.json').write_text(json.dumps(record, indent=2)+'\n')
print(json.dumps(record))
assert accepted, 'cake verdict or stable-input check failed; exit zero alone is insufficient'
