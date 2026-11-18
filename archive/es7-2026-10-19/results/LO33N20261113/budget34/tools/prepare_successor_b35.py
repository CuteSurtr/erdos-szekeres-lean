#!/usr/bin/env python3
"""Make a successor packet runs/b35s20/<dst> from runs/b35s20/<src> without touching <src> (b35 copy of prepare_successor.py).

Closed context files are hard-linked (fastbb only creates ctx files via .tmp + rename and never rewrites them);
master.json, contexts.json and master.txt are real copies, because --split-open rewrites them in place.
Usage: prepare_successor.py SRC DST
"""
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

RUN = Path('/home/jay/research/data/es308-20261114/runs/b35s20')  # b35 copy (18 Nov): only this path differs from prepare_successor.py
src, dst = RUN / sys.argv[1], RUN / sys.argv[2]
assert src.is_dir() and not dst.exists() and src.parent == dst.parent == RUN
busy = subprocess.run(['pgrep', '-f', 'fastbb2 solve'], capture_output=True, text=True).stdout.strip()
assert not busy, 'a finder is running: ' + busy
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

dst.mkdir()
masters = {}
for name in ('master.json', 'contexts.json', 'master.txt'):
    shutil.copyfile(src / name, dst / name)
    assert not os.path.samefile(src / name, dst / name) and sha(src / name) == sha(dst / name)
    masters[name] = sha(dst / name)
ctx = {}
for p in sorted(src.glob('ctx-*.json.gz')):
    os.link(p, dst / p.name)
    assert os.path.samefile(p, dst / p.name)
    ctx[p.name] = sha(p)
assert sorted(q.name for q in dst.glob('ctx-*.json.gz')) == sorted(ctx)
receipt = {'made': datetime.now().astimezone().isoformat(), 'source': str(src), 'masters_copied_sha256': masters,
           'contexts_hardlinked': len(ctx), 'context_sha256': ctx, 'tool_sha256': sha(Path(__file__))}
(dst / 'SUCCESSOR.json').write_text(json.dumps(receipt, indent=1) + '\n')
print(json.dumps({k: v for k, v in receipt.items() if k != 'context_sha256'}, indent=1))
