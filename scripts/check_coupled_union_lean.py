#!/usr/bin/env python3
"""Sequentially kernel-check the 57-row union, nine witnesses and 48 implications.

Run under lake env. Build products go in an ignored output directory. The
record is complete only after every module, standard-axiom audit, and unchanged
input snapshot succeeds. No search or new geometric compatibility check occurs.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from check_axioms import audit_output

NS = 'ErdosSzekeres.Omission.CoupledUnion.'
MODULES = [
    ('UnionCatalog', ['matches_literal', 'first_covered', 'second_covered',
        'distinct_support', 'card_thirteen', 'classification', 'independent_indices_injective',
        'redundant_indices_injective', 'classes_disjoint', 'all_rows']),
    ('Redundancy', ['forced_hole_of_deficit', 'redundant_deficits', 'redundant_rows_implied']),
    *[(f'Independent{k:02}', [f'original_rows_{k:02}']) for k in range(9)],
    ('Independence', ['original_rows', 'prior_additional_rows', 'prior_block_rows',
                     'other_union_rows', 'witness_hole_count', 'independent_each_selected_row']),
]


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(catalog, output, memory=1500, timeout=180):
    repo = Path(__file__).resolve().parents[1]
    artifact = repo / 'experiments/omission-coupled-union-2026-10-10'
    catalog, output = Path(catalog).resolve(), Path(output).resolve()
    if output == catalog or output.is_relative_to(catalog) or catalog.is_relative_to(output):
        raise ValueError('Output must be separate from the preserved catalog')
    output.mkdir(parents=True, exist_ok=True)
    expected_objects = {name + '.olean' for name, _ in MODULES}
    if any(p.name not in expected_objects for p in output.glob('*.olean')):
        raise ValueError('Unexpected output object could shadow an import')
    if any(p.is_dir() for p in output.iterdir()):
        raise ValueError('Unexpected directory could shadow a library import')
    manifest = json.loads((catalog / 'export.json').read_text())
    prior_check = json.loads((catalog / 'kernel-check.json').read_text())
    checked_catalog = prior_check['modules']['Catalog']
    exact = json.loads((artifact / 'exact-check.json').read_text())
    if (manifest['namespace'], manifest['states'], manifest['rows']) != ('OmissionResidual', 154, 1187):
        raise ValueError('Wrong original residual catalog')
    if manifest['source_sha256'] != exact['expanded_original_source_sha256']:
        raise ValueError('Exact controls and preserved catalog refer to different source data')
    if (checked_catalog.get('exit') != 0 or not checked_catalog.get('audited') or
            digest(catalog / 'Catalog.lean') != manifest['files']['Catalog.lean'] or
            digest(catalog / 'Catalog.lean') != checked_catalog['source_sha256'] or
            digest(catalog / 'Catalog.olean') != checked_catalog['olean_sha256']):
        raise ValueError('Preserved catalog check does not bind its current source and object')
    audit_output(checked_catalog['stdout'], 'OmissionResidual.code_correct')
    snapshot = {}
    def pin(path):
        path = Path(path).resolve()
        snapshot[str(path)] = digest(path)
    seen = set()
    def dependency(module):
        if module in seen:
            return
        seen.add(module)
        if module == 'Catalog':
            source, obj = catalog / 'Catalog.lean', catalog / 'Catalog.olean'
        elif module in dict(MODULES):
            source, obj = artifact / (module + '.lean'), None
        elif module.startswith('ErdosSzekeres.'):
            relative = module.replace('.', '/')
            source, obj = repo / (relative + '.lean'), repo / '.lake/build/lib/lean' / (relative + '.olean')
        else:
            return
        pin(source)
        if obj is not None:
            pin(obj)
        for line in source.read_text().splitlines():
            match = re.fullmatch(r'import\s+([A-Za-z0-9_.]+)', line.strip())
            if match:
                dependency(match.group(1))
    for name, _ in MODULES:
        dependency(name)
    for path in [catalog / 'export.json', catalog / 'kernel-check.json',
                 Path(__file__), repo / 'scripts/check_axioms.py', repo / 'lean-toolchain',
                 repo / 'lake-manifest.json', artifact / 'exact-check.json']:
        pin(path)
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join([str(output), str(catalog), env.get('LEAN_PATH', '')])
    version = subprocess.check_output(['lean', '--version'], text=True, env=env).strip()
    record = dict(scope='57 checked necessary rows; nine individually independent additions and '
                        '48 implications from single original rows. No population bound.',
                  lean=version, inputs=snapshot, modules={}, complete=False)
    path = output / 'kernel-check.json'
    def save():
        temp = path.with_suffix('.json.tmp')
        temp.write_text(json.dumps(record, indent=2) + '\n')
        temp.replace(path)
    save()
    for module, declarations in MODULES:
        source, obj = artifact / (module + '.lean'), output / (module + '.olean')
        started = time.monotonic()
        try:
            process = subprocess.run(['lean', '-j', '1', '-s', '32768', '-M', str(memory),
                                      str(source), '-o', str(obj)], capture_output=True, text=True,
                                     cwd=repo, env=env, timeout=timeout)
            result = dict(exit=process.returncode, stdout=process.stdout, stderr=process.stderr,
                          seconds=round(time.monotonic()-started, 3), source_sha256=digest(source),
                          audited=False)
        except subprocess.TimeoutExpired:
            record['modules'][module] = dict(exit='timeout', seconds=timeout, audited=False)
            save()
            raise
        if process.returncode == 0:
            result['axioms'] = {NS + name: audit_output(process.stdout, NS + name)
                                for name in declarations}
            result['olean_sha256'] = digest(obj)
            result['audited'] = True
        record['modules'][module] = result
        save()
        print(f"{module}: exit={result['exit']}, audited={result['audited']}, {result['seconds']}s", flush=True)
        if not result['audited']:
            raise RuntimeError(process.stdout + process.stderr)
    for name, expected in snapshot.items():
        if digest(name) != expected:
            raise ValueError(f'Input changed during check: {name}')
    record['complete'] = True
    save()
    return record


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--memory', type=int, default=1500)
    parser.add_argument('--timeout', type=int, default=180)
    result = run(**vars(parser.parse_args()))
    print(json.dumps({'complete': result['complete']}))
