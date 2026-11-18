#!/usr/bin/env python3
"""Collect small completed-run evidence; retain large external traces in place."""
import datetime
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/resume')
N66 = ROOT.parents[1] / 'VERIFY309N20261113/followup56'
N66_SCRATCH = Path('/home/jay/research/data/verify309-codex-20261113/followup56')


def digest(p):
    h = hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    data = ROOT / 'data'
    data.mkdir(exist_ok=True)
    inventory = []

    def copy(p, dest):
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, dest)
        inventory.append(dict(source=str(p), archived=str(dest),
                              bytes=p.stat().st_size, sha256=digest(dest)))

    # Pool files are small enough to hash completely. Preserve larger CNFs,
    # binaries, and SAT search traces externally, with exact paths and hashes.
    for p in sorted((SCRATCH / 'pool').rglob('*')):
        if not p.is_file():
            continue
        rel = p.relative_to(SCRATCH / 'pool')
        if p.stat().st_size <= 2_000_000 and p.suffix in {
                '.json', '.jsonl', '.out', '.log', '.time', '.lrat', '.zst', '.cnf'}:
            copy(p, ROOT / 'pool/data' / rel)
        else:
            inventory.append(dict(source=str(p), archived=None,
                                  bytes=p.stat().st_size, sha256=digest(p)))

    outcomes = {}
    for n in (7, 8):
        src = SCRATCH / f'compact/scheduled-n{n}m16'
        result = json.loads((src / 'result.json').read_text())
        assert result['status'] == 'UNKNOWN'
        assert result['compressed_roundtrip_verified']
        outcomes[f'compact_n{n}_m16'] = result
        for p in src.iterdir():
            if p.suffix in {'.json', '.log', '.time'}:
                copy(p, data / f'compact-n{n}m16' / p.name)
        outcomes[f'pool_n{n}_m16'] = json.loads(
            (SCRATCH / f'pool/n{n}m16-b128/result.json').read_text())

    fresh = N66_SCRATCH / 'fresh'
    fresh_result = json.loads((fresh / 'result.json').read_text())
    assert fresh_result['status'] == 'UNKNOWN'
    assert fresh_result['compressed_roundtrip_verified']
    for p in fresh.iterdir():
        if p.suffix in {'.json', '.log', '.time'}:
            copy(p, N66 / 'data/fresh_main' / p.name)
    copy(ROOT / 'pool/run_cnf.py', N66 / 'data/fresh_main/run_cnf.py')
    audit_status = json.loads((N66 / 'data/audit_status.json').read_text())
    audit_status.update(fresh_main_solve=False, fresh_main_attempt_status='UNKNOWN',
                        fresh_main_attempt='data/fresh_main/result.json',
                        parent_review='COMPLETE; preferred ES309 chain updated',
                        limits='Written soundness + exact computations + cake_lpr; not Lean-checked.')
    (N66 / 'data/audit_status.json').write_text(json.dumps(audit_status, indent=2) + '\n')

    roundtrips = []
    for p in sorted((N66_SCRATCH / 'new_rows').rglob('*.lrat.zst')):
        plain = Path(str(p)[:-4])
        expected = digest(plain)
        h = hashlib.sha256()
        with subprocess.Popen(['/usr/bin/zstd', '-q', '-d', '-c', str(p)],
                              stdout=subprocess.PIPE) as proc:
            for b in iter(lambda: proc.stdout.read(1 << 20), b''):
                h.update(b)
            assert proc.wait() == 0
        assert h.hexdigest() == expected
        roundtrips.append(dict(proof=str(plain), sha256=expected,
                               compressed_sha256=digest(p), roundtrip_verified=True))
    assert len(roundtrips) == 8
    (N66 / 'data/new_rows_roundtrips.json').write_text(json.dumps(roundtrips, indent=2) + '\n')

    units = ['nov13c-vfy-delta3r-*', 'nov13c-vfy-n66-56-*']
    journal = subprocess.check_output(
        ['journalctl', '--user', '-u', units[0], '-u', units[1],
         '--since', '2026-11-13 23:57:00', '--no-pager'], text=True)
    (data / 'units.log').write_text(journal)
    guard = Path('/home/jay/research/data/memguard-20261113/memguard.log').read_text()
    own = [line for line in guard.splitlines()
           if 'nov13c-vfy-delta3r-' in line or 'nov13c-vfy-n66-56-' in line]
    assert not any(' STOP ' in line for line in own)
    (data / 'memory_guard.log').write_text('\n'.join(own) + '\n')
    live = subprocess.check_output(['systemctl', '--user', 'list-units',
                                    'nov13c-*', 'p2-*', 'memguard*',
                                    '--state=running', '--no-pager'], text=True)
    (data / 'live_final.txt').write_text(live)
    assert not any('nov13c-vfy-' in line for line in live.splitlines())
    summary = dict(completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                   weak_D57='OPEN', weak_D58='OPEN', all_new_units_finished=True,
                   new_units_guard_stops=0, outcomes=outcomes,
                   extra_n66_fresh_solve=fresh_result['status'],
                   n66_retained_main_replay='CERTIFIED',
                   proof_deletions=0, git_mutations=False)
    (data / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    (data / 'archive_manifest.json').write_text(json.dumps(inventory, indent=2) + '\n')
    print(json.dumps(dict(archived_or_hashed=len(inventory),
                          new_row_roundtrips=len(roundtrips), new_jobs_finished=True)))


if __name__ == '__main__':
    main()
