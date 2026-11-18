"""Small paperwork validation and exclusive manifest creation; no research search."""
from pathlib import Path
from datetime import datetime, timezone, timedelta
import argparse
import hashlib
import json
import re


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--t7-independent-receipt', type=Path)
    args = ap.parse_args(); root = Path(__file__).resolve().parents[1]
    assert not (root/'SHA256SUMS').exists()
    assert '**FROZEN:' in (root/'README.md').read_text()
    controls = {
        'rooted_named.json':'rooted_controls.py',
        'rooted_grid.json':'rooted_controls.py',
        'rooted_longcup.json':'rooted_longcup_controls.py',
        'all_cap_controls.json':'all_cap_controls.py',
    }
    for name, script in controls.items():
        r = json.loads((root/'data'/name).read_text())
        assert r['status'] in ('PASS', 'PASS_COMPLETE_GRID')
        assert r['source_sha256'] == digest(root/'tools'/script)
        if 'helper_sha256' in r:
            assert r['helper_sha256'] == digest(root/'tools/rooted_controls.py')
    parent_control = root/'../../data/all-cap-parent-controls.json'
    r = json.loads(parent_control.read_text())
    assert r['status'] == 'PASS' and r['total_selections'] == 68
    assert r['input_sha256'] == digest(root/'data/all_cap_controls.json')
    cap = json.loads((root/'data/capacity_pass_receipt.json').read_text())
    assert cap['status'] == 'PASS' and len(cap['checks']) == 2
    reports = 0
    for c in cap['checks']:
        assert c['exit_code'] == 0 and c['stop_reason'] is None
        assert digest(Path(c['source'])) == c['source_sha256']
        for axioms in c['axiom_reports'].values():
            assert set(axioms) == {'propext', 'Classical.choice', 'Quot.sound'}
            reports += 1
    assert reports == 5
    link_count = 0
    for md in root.glob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', md.read_text()):
            if '://' not in target:
                assert (md.parent/target.split('#')[0]).exists(), (md, target)
                link_count += 1
    relatives = [
        '../../structure2/low_split.md', '../../../../../a4/theory.md',
        '../../low_split_audit/VERIFY_LOW_SPLIT.md',
        '../../low_split_audit/replay/README.md',
        '../../low_split_audit/n6/VERIFY_LOW6.md',
        '../../low_split_audit/left15/VERIFY_LEFT15.md',
        '../../terminal12_audit/VERIFY_TERMINAL12.md',
        '../../low_split_audit/left16_replay/README.md',
        '../../low_split_audit/left16_replay/data/recovery/result.json',
        '../../low_split_audit/left16_longcup/VERIFY_LONGCUP16.md',
        '../Capacity11.lean', '../Capacity16.lean',
        '../capacity_checks/README.md', '../capacity_checks/pass/result.json',
        '../capacity_checks/attempt-rss3000/result.json',
        '../../data/all-cap-parent-controls.json',
    ]
    sources = [(str(p), root/p) for p in relatives]
    t7_status = 'parent CERTIFIED; independent proof closure pending'
    if args.t7_independent_receipt:
        p = args.t7_independent_receipt.resolve(); receipt = json.loads(p.read_text())
        assert receipt.get('status') == 'PASS'
        sources.append((str(p), p)); t7_status = 'independent proof closure PASS'
    now = datetime.now(timezone(timedelta(hours=9))).isoformat()
    snapshot = {'time_kst':now, 'scope':'small source/receipt hashes, not proof replays',
                'sources':[{'path':label, 'bytes':p.stat().st_size, 'sha256':digest(p)} for label,p in sources]}
    with (root/'data/source_snapshot.json').open('x') as f:
        json.dump(snapshot, f, indent=2); f.write('\n')
    freeze = dict(status='FROZEN', completed_at_kst=now,
        scope='selection/extension/low_split/consequences only',
        universal_T6='closed: audited finite chain and checked geometric capacity11',
        universal_T7_review=t7_status,
        all_cap='written proof reviewed by parent; 24 fixtures, 68 selections, independent parent PASS',
        internal_cuts='written Option1 proof for four-cap-free sets; no new encoder',
        pure_geometric_universal_T7='not proved here; compatibility candidate explicitly unproved',
        mechanical_validation=dict(control_outputs=4, control_source_hashes='PASS',
            parent_all_cap_input_hash='PASS', capacity_source_hashes='PASS',
            standard_axiom_reports=reports, markdown_links=link_count),
        own_active_jobs=0, reservation_released='one CPU / AS150MiB short-check allowance')
    with (root/'FREEZE.json').open('x') as f:
        json.dump(freeze, f, indent=2); f.write('\n')
    files = sorted(p for p in root.rglob('*') if p.is_file())
    with (root/'SHA256SUMS').open('x') as f:
        for p in files:
            f.write(f'{digest(p)}  {p.relative_to(root)}\n')
    for line in (root/'SHA256SUMS').read_text().splitlines():
        h, name = line.split('  ', 1); assert digest(root/name) == h
    print(json.dumps({'status':'FROZEN', 'time_kst':now, 'files':len(files),
                      'manifest_sha256':digest(root/'SHA256SUMS'), 'T7_review':t7_status}))


if __name__ == '__main__':
    main()
