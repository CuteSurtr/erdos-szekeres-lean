#!/usr/bin/env python3
"""Fresh full replay of one packet: the master and every context checked from scratch by
scripts/omission_tree.check_tree against the stated row version. No receipt of any earlier replay is reused.

Usage: fresh_replay.py PACKET INPUT_FOLDER OUTDIR WORKERS   (e.g. bb-s2 s20-v13 fresh-v13 6)
"""
from datetime import datetime
import gzip
import hashlib
import json
from multiprocessing import Pool
from pathlib import Path
import sys

import replay34_v2 as base
from omission_tree import check_tree
from pool_audit import SOURCE_RAW_SHA

W = Path('/home/jay/research/data/es308-20261114')
BB, INP, OUT, NW = W / 'runs' / sys.argv[1], W / 'inputs' / sys.argv[2], base.AUDIT / sys.argv[3], int(sys.argv[4])  # v2: PACKET = s<T>/<folder>
SRC = W / 'inputs/source-2650.json.gz'
raw = gzip.decompress(SRC.read_bytes())
assert hashlib.sha256(raw).hexdigest() == SOURCE_RAW_SHA, 'source catalog hash'
extra = json.loads((INP / 'extra.json').read_text())
ROWS = [(r['support'], r['rhs']) for r in json.loads(raw)['constraints'] + extra]
_st = json.loads(raw)['states']; _F = [i for i, s in enumerate(_st) if s[0] >= 5]; _LO = [i for i, s in enumerate(_st) if s[0] <= 4]
import re; _m = re.fullmatch(r'(?:b(\d+))?s(\d+)-v\d+', sys.argv[2]); assert _m, 'input folder name'  # v3: budget from b<B>s<T>-v<k>
BUD, T = int(_m[1] or 34), int(_m[2]); assert BUD in (34, 35)
assert extra[0] == {'support': _F, 'rhs': T} and extra[1] == {'support': _LO, 'rhs': BUD - T}
assert sys.argv[1].startswith(f's{T}/' if BUD == 34 else f'b{BUD}s{T}/')
MASTER_RAW = (BB / 'master.json').read_bytes()
MASTER = json.loads(MASTER_RAW)
assert MASTER['budget'] == BUD and type(MASTER['budget']) is int
assert Path(MASTER['source']) == SRC and Path(MASTER['extra']) == INP / 'extra.json', 'master not on this row version'
PATHS = base.frontier(MASTER)
DESC = json.loads((BB / 'contexts.json').read_text())
assert len(DESC) == len(PATHS) and {d['context'] for d in DESC} == set(PATHS)
for d in DESC:
    base.descriptor(d, d['context'], PATHS[d['context']])


def one(c):
    p = BB / f'ctx-{c}.json.gz'
    h = base.sha_drop(p)
    sub = base.read_json(p)
    base.descriptor(sub, c, PATHS[c])
    assert base.natural(sub['root']) and sub['root'] < len(sub['nodes'])
    wrapped, used = base.envelope(sub['nodes'], sub['root'], PATHS[c])
    res = check_tree(154, ROWS, BUD, wrapped, 0, allow_pending=True)
    assert res['pending'] == len(PATHS[c]), (c, 'internal pending leaf')
    assert h == base.sha_drop(p), (c, 'file changed during check')
    return {'context': c, 'sha256': h, 'nodes': len(sub['nodes']), 'leaves': res['leaves'] - len(PATHS[c]),
            'minimum_margin': res['minimum_margin'], 'max_used_row': max(used, default=-1)}


if __name__ == '__main__':
    OUT.mkdir(exist_ok=False)
    started = datetime.now().astimezone().isoformat()
    wrapped, _ = base.envelope(MASTER['nodes'], MASTER['root'], ((0, 0),), master=True)
    top = check_tree(154, ROWS, BUD, wrapped, 0, allow_pending=True)
    assert top['pending'] == len(PATHS) + 1, 'master pending = contexts + state-0-missing'
    present = {int(p.name[4:-8]) for p in BB.glob('ctx-*.json.gz')}
    assert present == set(PATHS), 'context files do not match the master frontier'
    done = []
    with Pool(NW) as pool, (OUT / 'contexts.jsonl').open('x') as led:
        for r in pool.imap_unordered(one, sorted(PATHS), chunksize=8):
            led.write(json.dumps(r) + '\n'); done.append(r)
    margins = [r['minimum_margin'] for r in done if r['minimum_margin'] is not None] + \
              ([top['minimum_margin']] if top['minimum_margin'] is not None else [])
    closed = len(done) == len(PATHS) and margins and min(margins) >= 1
    summary = {'label': 'EXACT TREE (fresh full replay, no receipts reused)' if closed else 'NOT CONFIRMED',
               'packet': str(BB), 'input_folder': str(INP), 'rows': len(ROWS), 'budget': BUD, 'capacity_demands': [T, BUD - T], 'contexts': len(PATHS),
               'contexts_checked': len(done), 'master_nodes': len(MASTER['nodes']),
               'nodes': len(MASTER['nodes']) + sum(r['nodes'] for r in done),
               'leaves': top['leaves'] - len(PATHS) + sum(r['leaves'] for r in done),
               'minimum_margin': min(margins, default=None), 'global_pending': 1,
               'pending_meaning': 'state 0 missing only (discharged in Lean by zero_mem_residualOccupied)',
               'master_sha256': hashlib.sha256(MASTER_RAW).hexdigest(),
               'extra_sha256': hashlib.sha256((INP / 'extra.json').read_bytes()).hexdigest(),
               'checker_sha256': hashlib.sha256((base.ROOT / 'scripts/omission_tree.py').read_bytes()).hexdigest(),
               'tool_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               'started': started, 'finished': datetime.now().astimezone().isoformat()}
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=1) + '\n')
    print(json.dumps(summary, indent=1))
