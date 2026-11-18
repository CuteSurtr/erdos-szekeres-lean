#!/usr/bin/env python3
"""Archive completed parent-run selection evidence, never deleting traces."""
import datetime
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/selection')
OUT = HERE/'data'


def sha(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    OUT.mkdir(exist_ok=True)
    manifest, outcomes = [], []
    def copy(p, target):
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, target)
        manifest.append(dict(source=str(p), copy=str(target), bytes=p.stat().st_size,
                             sha256=sha(target)))
    for n in (7, 8):
        root = SCRATCH/f'rooted/sweep{n}'
        done = json.loads((root/'DONE.json').read_text())
        for case in done['outcomes']:
            d = Path(case['case'])
            r = json.loads((d/'solve/result.json').read_text())
            assert r['status'] in ('UNSAT_CERTIFIED', 'UNKNOWN')
            assert r['compressed_roundtrip_verified']
            outcomes.append(dict(method='filtered', m=case['m'], n=n,
                                 result=r, input_generation=json.loads((d/'rooted.generation.json').read_text())))
        for p in root.rglob('*'):
            if p.is_file() and p.suffix in ('.json', '.log', '.time', '.py', '.cpp'):
                assert p.stat().st_size < 2_000_000
                copy(p, OUT/f'sweep{n}'/p.relative_to(root))
        for name in (f'full-n{n}.pool', f'full-n{n}.jsonl', f'full-n{n}-sources.json'):
            copy(SCRATCH/'rooted'/name, OUT/'real_pool'/name)
    for tag, m, n in [('fast14-7',14,7), ('fast15-8',15,8)]:
        root = SCRATCH/'rooted'/tag
        r = json.loads((root/'solve/result.json').read_text())
        assert r['status'] == 'UNKNOWN' and r['compressed_roundtrip_verified']
        outcomes.append(dict(method='specialized', m=m, n=n, result=r))
        for p in root.rglob('*'):
            if p.is_file() and p.suffix in ('.json', '.log', '.time'):
                copy(p, OUT/tag/p.relative_to(root))
    for p in (SCRATCH/'certificates').rglob('*'):
        if p.is_file():
            assert p.stat().st_size < 2_000_000
            copy(p, OUT/'certificates'/p.relative_to(SCRATCH/'certificates'))
    # The ten-second specialized probe preceded the scheduled run; preserve
    # its incomplete trace's exact hash without promoting it to a certificate.
    probe = SCRATCH/'rooted/fast14-7/probe.lrat'
    manifest.append(dict(source=str(probe), copy=None, bytes=probe.stat().st_size,
                         sha256=sha(probe), status='UNKNOWN incomplete trace'))
    for p in (SCRATCH/'rooted/rooted', SCRATCH/'rooted/rooted_fast'):
        manifest.append(dict(source=str(p), copy=None, bytes=p.stat().st_size, sha256=sha(p)))
    unit_log = subprocess.check_output(['journalctl','--user','-u','nov13c-vfy-delta4-*',
                                       '--since','2026-11-14 00:55:00','--no-pager'],text=True)
    (OUT/'units.log').write_text(unit_log)
    guard = Path('/home/jay/research/data/memguard-20261113/memguard.log').read_text()
    own = [line for line in guard.splitlines() if 'nov13c-vfy-delta4-' in line]
    assert not any(' STOP ' in line for line in own)
    (OUT/'memory_guard.log').write_text('\n'.join(own)+'\n')
    live = subprocess.check_output(['systemctl','--user','list-units','nov13c-*','p2-*',
                                    'memguard*','--state=running','--no-pager'],text=True)
    assert not any('nov13c-vfy-delta4-' in line for line in live.splitlines())
    (OUT/'live_final.txt').write_text(live)
    summary = dict(label='COMPUTED inventory', collected_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   weak_D57='OPEN', weak_D58='OPEN', filtered_certified=10,
                   filtered_unknown=5, specialized_unknown=2,
                   fixed_obstructions_certified=3, real_rooted_positive_sets=315,
                   all_new_long_jobs_finished=True, guard_stops=0, outcomes=outcomes)
    (OUT/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    (OUT/'archive_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps(dict(archived=len(manifest), outcomes=len(outcomes), all_new_jobs_finished=True)))


if __name__ == '__main__':
    main()
