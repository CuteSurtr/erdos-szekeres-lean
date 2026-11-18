#!/usr/bin/env python3
"""Collect already-checked real bridge evidence; never invokes Lean."""
import hashlib
import json
from pathlib import Path
import re
import shutil

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/jay/research/lean/erdos-szekeres-lean')
SCRATCH = Path('/home/jay/research/data/delta3-codex-20261113/extension/lean')
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
runs = [
    ('IndexHelpers.lean', 'real-index-v1'),
    ('BridgeBase.lean', 'real-base-v1'),
    ('ConvexBridge.lean', 'real-convex-v1'),
    ('TerminalReal.lean', 'real-terminal-v1'),
    ('PointSetBridge.lean', 'real-pointset-v2'),
    ('RealBalanced15.lean', 'real-balanced15-v1'),
]
checks = []
for name, tag in runs:
    source = ROOT / name
    record = json.loads((SCRATCH / (tag + '.json')).read_text())
    log = (SCRATCH / (tag + '.log')).read_text()
    assert record['exit_code'] == 0 and record['stop_reason'] is None
    assert record['source_sha256'] == digest(source)
    assert record['rusage_maxrss_kib'] < 2000 * 1024
    assert record['proc_status_peaks_kib_except_threads']['VmSwap'] == 0
    assert not re.search(r'\b(error|warning)(?:\(|:)', log)
    assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b|Lean\.ofReduceBool', source.read_text())
    audits = {n: [a.strip() for a in raw.split(',') if a.strip()]
              for n, raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]", log)}
    audits.update({n: [] for n in re.findall(r"'([^']+)' does not depend on any axioms", log)})
    assert len(audits) == source.read_text().count('#print axioms')
    assert all(set(v) <= {'propext', 'Classical.choice', 'Quot.sound'} for v in audits.values())
    for suffix in ['.log', '.json']:
        shutil.copyfile(SCRATCH / (tag + suffix), DATA / (tag + suffix))
    checks.append(dict(source=name, sha256=digest(source), run=tag,
                       axiom_reports=audits, seconds=record['elapsed_seconds'],
                       kernel_maxrss_kib=record['rusage_maxrss_kib'],
                       sampled_peaks=record['proc_status_peaks_kib_except_threads'],
                       log_sha256=digest(DATA / (tag + '.log')),
                       record_sha256=digest(DATA / (tag + '.json'))))
frozen = json.loads((ROOT.parent / 'data/manifest.json').read_text())
prerequisites = []
for entry in frozen['replay_order']:
    path = ROOT.parent / entry['source']
    assert digest(path) == entry['sha256']
    prerequisites.append(dict(source='../' + entry['source'], sha256=entry['sha256']))
for tag in ['real-import-integer-1300', 'real-import-2000']:
    for suffix in ['.log', '.json']:
        shutil.copyfile(SCRATCH / (tag + suffix), DATA / (tag + suffix))
cache = []
for module in ['ErdosSzekeres/IntegerCertificates', 'ErdosSzekeres/OrientationConvexity',
               'ErdosSzekeres/Suk/FourPoint', 'ErdosSzekeres/OrientationGeometry',
               'ErdosSzekeres/Basic']:
    src = REPO / (module + '.lean')
    olean = REPO / '.lake/build/lib/lean' / (module + '.olean')
    cache.append(dict(module=module.replace('/', '.'), source_sha256=digest(src),
                      olean_sha256=digest(olean)))
parent_result = ROOT.parent.parent / 'lean_geometry_parent/data/result.json'
shutil.copyfile(parent_result, DATA / 'finite-parent-result.json')
manifest = dict(
    label='PROVED', status='PASS: actual real-coordinate terminal-membership obstruction',
    main_theorem='Delta3.Balanced15.RealBridge.balanced15_real_obstruction',
    existence_theorem='Delta3.Balanced15.RealBridge.exists_real_terminal_obstruction',
    toolchain=(REPO / 'lean-toolchain').read_text().strip(),
    coordinate_input_sha256=frozen['coordinate_input_sha256'],
    finite_manifest_sha256=digest(ROOT.parent / 'data/manifest.json'),
    finite_freeze_sha256=digest(ROOT.parent / 'FROZEN.json'),
    finite_parent_replay_sha256=digest(parent_result),
    finite_parent_replay_status='PASS: 35 jobs / 50 audits; source hashes rechecked here',
    checks=checks, new_source_files=len(checks),
    new_axiom_audits=sum(len(c['axiom_reports']) for c in checks),
    standard_axioms_only=True,
    total_check_seconds=round(sum(c['seconds'] for c in checks), 3),
    kernel_peak_rss_kib=max(c['kernel_maxrss_kib'] for c in checks),
    prerequisite_sources=prerequisites, project_cache=cache,
    runner_sha256=digest(ROOT / 'check.py'),
    replay_sha256=digest(ROOT / 'replay.py'),
    resource_policy=dict(cpu=1, affinity=[4], lean_j=1, lean_heap_mib=1000,
                         as_gib=4, rss_guard_mib=2000, long_unit_memorymax_mib=2600,
                         swap_mib=0, short_wall_seconds=27,
                         long_unit_deadline_kst='2026-11-14 08:20:00',
                         owner_total_mib_unchanged=6000),
    failed_1300_probe=dict(run='real-import-integer-1300',
                          source='ImportInteger.lean', source_sha256=digest(ROOT / 'ImportInteger.lean'),
                          log_sha256=digest(DATA / 'real-import-integer-1300.log'),
                          record_sha256=digest(DATA / 'real-import-integer-1300.json'),
                          status='controlled RSS stop, no OOM; excluded from proved files'),
    successful_import_probe='real-import-2000',
    excluded_probe_sources=['ImportInteger.lean', 'ImportReal.lean'],
    limits_of_claim=['terminal-pair membership, not envelope safety or the original Delta existence claim',
                     'cap is explicitly defined by real all-triple orientations, not imported HasCap',
                     'no minimality or 12-point theorem in this packet'],
    fresh_parent_real_replay_pending_at_freeze=True)
assert manifest['new_axiom_audits'] == 31
(DATA / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(json.dumps({k:manifest[k] for k in ['label','new_source_files','new_axiom_audits',
      'total_check_seconds','kernel_peak_rss_kib']}, indent=2))
print('manifest_sha256', digest(DATA / 'manifest.json'))

