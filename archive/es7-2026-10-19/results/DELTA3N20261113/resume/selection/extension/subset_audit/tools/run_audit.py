#!/usr/bin/env python3
"""Bounded orchestration only; imports no finder or prior verifier."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import time

ROOT = Path('/home/jay/research/lean/erdos-szekeres-lean')
SEL = ROOT / 'cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection'
OUT = SEL / 'extension/subset_audit'
DATA = OUT / 'data'
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/subset-audit')
PARENT = SCRATCH.parent
BIN = SCRATCH / 'audit'
POINTS = PARENT / 'terminal-subsets/input.points'
ROWS = PARENT / 'terminal-subsets/all13-17.jsonl'
WITNESS = SEL / 'terminal/data/witness.points'

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def save(name, obj):
    path = DATA / name
    with path.open('x') as f:
        json.dump(obj, f, indent=2)
        f.write('\n')

def digest(path):
    before = path.stat()
    h = hashlib.sha256()
    with path.open('rb') as f:
        while True:
            block = f.read(1 << 20)
            if not block:
                break
            h.update(block)
    after = path.stat()
    assert (before.st_size, before.st_mtime_ns, before.st_ino) == (after.st_size, after.st_mtime_ns, after.st_ino)
    return dict(sha256=h.hexdigest(), bytes=after.st_size, mtime_ns=after.st_mtime_ns)

def run(name, args, expected=0, message=None, seconds=20):
    stdout, stderr = DATA / (name + '.stdout'), DATA / (name + '.stderr')
    timing = DATA / (name + '.time')
    cmd = ['/usr/bin/time', '-v', '-o', str(timing), '/usr/bin/timeout', '-k', '1', str(seconds),
           '/usr/bin/prlimit', '--as=314572800', '--cpu=' + str(max(1, seconds - 1)),
           '/usr/bin/taskset', '-c', '5', str(BIN), *map(str, args)]
    start = time.monotonic()
    with stdout.open('x') as out, stderr.open('x') as err:
        result = subprocess.run(cmd, stdout=out, stderr=err, check=False)
    receipt = dict(name=name, command=cmd, returncode=result.returncode,
                   expected_returncode=expected, seconds=time.monotonic()-start,
                   stdout_sha256=digest(stdout)['sha256'], stderr_sha256=digest(stderr)['sha256'])
    with (DATA / 'commands.jsonl').open('a') as f:
        f.write(json.dumps(receipt) + '\n')
    assert result.returncode == expected, receipt
    if message is not None:
        assert 'FAIL: ' + message in stderr.read_text(), (name, stderr.read_text())
    return receipt

def point_list(path):
    words = path.read_text().split()
    n, target = map(int, words[:2])
    assert target == 7 and len(words) == 2+2*n
    return [list(map(int, words[i:i+2])) for i in range(2, len(words), 2)]

def main():
    save('start.json', dict(started=now(), pid=os.getpid(),
         limits=Path('/proc/self/limits').read_text(), affinity=sorted(os.sched_getaffinity(0)),
         AS_bytes=resource.getrlimit(resource.RLIMIT_AS)[0], label='IN PROGRESS'))
    prior = [
        SEL / 'terminal/data/witness.json', WITNESS,
        SEL / 'terminal/data/witness.core.cnf',
        SEL / 'terminal/data/certification/result.json',
        SEL / 'terminal/data/certification/cake.log',
        SEL / 'terminal/data/certification/proof.lrat.zst',
        SEL / 'boundary/audit/VERIFY_BOUNDARY.md',
        SEL / 'boundary/audit/data/replay-n7.json',
        SEL / 'boundary/audit/data/replay-n7.log',
        SEL / 'extension/audit/VERIFY_EXTENSION.md',
        SEL / 'extension/audit/data/replay-n7m12.json',
        SEL / 'extension/audit/data/replay-n7m12.log',
        PARENT / 'envelope/full-v1/cases/n7-i076/input.json',
    ]
    inputs = [POINTS, ROWS, BIN, OUT / 'tools/audit.cpp', OUT / 'tools/run_audit.py', *prior]
    before = {str(p): digest(p) for p in inputs}
    save('inputs-before.json', before)
    for path in (POINTS, WITNESS):
        shutil.copyfile(path, DATA / ('ambient.points' if path == POINTS else 'witness18.points'))
    p = point_list(POINTS)
    witness = json.loads((SEL / 'terminal/data/witness.json').read_text())
    parent_case = json.loads((PARENT / 'envelope/full-v1/cases/n7-i076/input.json').read_text())
    assert p == parent_case['P'] == witness['source']['P']
    q = point_list(WITNESS)
    assert q == witness['P'] and len(q) == 18
    ix = [p.index(pt) for pt in q]
    assert ix == witness['source_indices'] and len(set(ix)) == 18
    save('mapping.json', dict(status='PASS', parent_case=parent_case['name'],
         all_23_coordinates_identical=True, witness18_coordinates_identical=True,
         source_indices=ix, W=sum(1 << i for i in ix)))
    for log in [SEL / 'terminal/data/certification/cake.log',
                SEL / 'boundary/audit/data/replay-n7.log',
                SEL / 'extension/audit/data/replay-n7m12.log']:
        assert log.read_text().splitlines().count('s VERIFIED UNSAT') == 1
    save('inherited-evidence.json', dict(
        fresh_cake_run=False,
        through_11='boundary/audit/VERIFY_BOUNDARY.md, Encoders and coverage; replay-n7.json and .log',
        size_12='extension/audit/VERIFY_EXTENSION.md, Independent certificate replay; replay-n7m12.json and .log',
        size_18='terminal/data/witness.core.cnf and terminal/data/certification/result.json and cake.log',
        exact_acceptance_lines_present=True,
        caution='This audit cites prior certificate replays and does not recertify them.'))
    run('controls', ['controls', POINTS])
    mutations = DATA / 'mutations'
    mutations.mkdir()
    raw = POINTS.read_text().splitlines()
    edits = {
        'coordinate-bound': ([raw[0], f'{(1 << 40)+1} 0', *raw[2:]], 'coordinate_bound'),
        'x-order': ([raw[0], raw[2], raw[1], *raw[3:]], 'x_order'),
        'collinear': ([raw[0], *[line.split()[0]+' 0' for line in raw[1:4]], *raw[4:]], 'collinear'),
        'extra-points': ([*raw, '0 0'], 'extra point data'),
        'missing-points': (raw[:-1], 'missing/noninteger'),
        'noninteger': ([raw[0], '1.5 2', *raw[2:]], 'missing/noninteger'),
        'bad-header': (['24 7', *raw[1:]], 'requires 1..23'),
    }
    negative = []
    for name, (lines, err) in edits.items():
        path = mutations / (name + '.points')
        path.write_text('\n'.join(lines) + '\n')
        negative.append(run(name, ['geometry', path], 1, err))
    with ROWS.open() as f:
        row1 = json.loads(next(f))
    row_cases = {
        'duplicate': ([row1, row1], 'duplicate_W='),
        'missing-coverage': ([row1], 'coverage_mismatch_W='),
        'nonpositive-result': ([dict(row1, result=0)], 'result_not_one'),
        'wrong-size': ([dict(row1, m=16)], 'm_popcount_mismatch'),
        'outside-A': ([dict(row1, A=1 << 22)], 'A_not_subset_W'),
        'unhit': ([dict(row1, A=0)], 'unhit_hexagon='),
        'oversize-W': ([dict(row1, W=1 << 23)], 'W_out_of_range'),
        'extra-size': ([dict(row1, W=(1 << 18)-1, m=18)], 'm_out_of_range'),
    }
    for name, (rows, err) in row_cases.items():
        path = mutations / (name + '.jsonl')
        path.write_text(''.join(json.dumps(row)+'\n' for row in rows))
        negative.append(run(name, ['run', POINTS, path, 13, 17, WITNESS], 1, err))
    save('negative-controls.json', dict(status='PASS', cases=negative))
    run('audit', ['run', POINTS, ROWS, 13, 17, WITNESS], seconds=1100)
    results = [json.loads(line) for line in (DATA / 'audit.stdout').read_text().splitlines()]
    assert len(results) == 2 and all(r['status']=='PASS' for r in results)
    assert results[0]['rows']==2797674 and results[1]['terminal_safe_Deltas']==0
    after = {str(p): digest(p) for p in inputs}
    save('inputs-after.json', after)
    assert before == after, 'an input changed during the audit'
    save('result.json', dict(label='COMPUTED', status='PASS', finished=now(),
        inputs_stable=True, stream=results[0], mapped_obstruction=results[1],
        inherited_evidence='inherited-evidence.json', minimum_obstruction_size_within_this_fixed_23_set=18,
        global_minimum_claim=False, fresh_cake_run=False,
        controls=json.loads((DATA / 'controls.stdout').read_text()), external_negative_controls=len(negative)))

if __name__ == '__main__':
    try:
        main()
    except BaseException as e:
        save('failure.json', dict(status='FAIL', when=now(), error=repr(e)))
        raise
