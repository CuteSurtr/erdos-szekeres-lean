#!/usr/bin/env python3
"""Cross-check the export manifests against the per-module kernel records (311 and 313).

For each record: every generated Lean file listed in export.json must have a module record with
exit 0, audited true, axioms within the three standard ones, and source_sha256 equal to the
manifest hash; the module count, part count and leaf sums must agree with the README claims.
Usage: python3 -I records_check.py
"""
import json, lzma, sys, re

import os as _os  # paths are relative to this file; ES_REPO_ROOT overrides the repository root
HERE = _os.path.dirname(_os.path.abspath(__file__))
TOP = _os.path.dirname(_os.path.dirname(HERE))  # cloud/es7-2026-10-19/results/ES8SLACK
ROOT = _os.environ.get('ES_REPO_ROOT') or _os.path.normpath(_os.path.join(TOP, '..', '..', '..', '..'))
REPO = ROOT + '/experiments'
STD = {'propext', 'Classical.choice', 'Quot.sound'}


def check(label, export_path, kernel_path, prefix, exp_parts, exp_leaves, exp_stmt):
    ex = json.load(open(export_path))
    kc = json.loads(lzma.open(kernel_path).read())
    files = ex['files']
    mods = kc['modules']
    out = {'label': label, 'manifest_files': len(files), 'kernel_modules': len(mods),
           'kernel_complete_flag': kc.get('complete')}
    problems = []
    lean_files = {k: v for k, v in files.items() if k.endswith('.lean')}
    out['manifest_lean_files'] = len(lean_files)
    for path, h in lean_files.items():
        assert path.startswith(prefix + '/'), path
        name = path[len(prefix) + 1:-len('.lean')]
        rec = mods.get(name)
        if rec is None:
            problems.append(('missing_module_record', name)); continue
        if rec.get('exit') != 0: problems.append(('nonzero_exit', name))
        if rec.get('audited') is not True: problems.append(('not_audited', name))
        if not set(rec.get('axioms', ['?'])) <= STD: problems.append(('axioms', name, rec.get('axioms')))
        if rec.get('source_sha256') != h: problems.append(('source_hash_mismatch', name))
        if rec.get('stderr'): problems.append(('stderr', name, rec['stderr'][:200]))
        so = rec.get('stdout', '')
        if 'sorryAx' in so or 'ofReduceBool' in so: problems.append(('bad_axiom_in_stdout', name))
        if not re.search(r"depends on axioms: \[propext, Classical\.choice, Quot\.sound\]", so) and \
           not re.search(r"depends on axioms", so):
            problems.append(('no_axiom_line', name))
    extra = set(mods) - {p[len(prefix) + 1:-5] for p in lean_files}
    out['kernel_modules_not_in_manifest'] = sorted(extra)[:10]
    parts = ex.get('parts', [])
    out['parts'] = len(parts)
    out['sum_part_leaves'] = sum(p['leaves'] for p in parts)
    out['exported_leaves_field'] = ex.get('exported_leaves')
    out['exported_parts_field'] = ex.get('exported_parts')
    out['root_stdout'] = mods.get('Root', {}).get('stdout', '').strip()
    out['catalog_stdout'] = mods.get('Catalog', {}).get('stdout', '').strip()
    out['total_seconds'] = round(sum(m.get('seconds', 0) for m in mods.values()))
    out['problems'] = problems[:20]
    out['n_problems'] = len(problems)
    ok = (not problems and len(parts) == exp_parts and out['sum_part_leaves'] == exp_leaves
          and kc.get('complete') is True and exp_stmt in out['root_stdout'] and not extra)
    out['OK'] = ok
    return out, ok


r1, ok1 = check('311 balanced budget 63',
                REPO + '/omission-final311-2026-10-14/certificate/export.json',
                REPO + '/omission-final311-2026-10-14/certificate/kernel-check.json.xz',
                'BalancedCover63Proof', 18066, 782437, 'OmissionBalancedCover63.excludes_budget')
print(json.dumps(r1, indent=1))
r2, ok2 = check('313 residual 2650 zero budget 32',
                REPO + '/omission-final313-2026-10-11/certificate/export.json',
                REPO + '/omission-final313-2026-10-11/certificate/kernel-check.json.xz',
                'Residual2650ZeroProof', 10325, 437579, 'OmissionResidual2650Zero.node1')
print(json.dumps(r2, indent=1))
print('RECORDS CONSISTENT' if ok1 and ok2 else 'RECORD PROBLEM')
