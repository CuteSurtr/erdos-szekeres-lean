#!/usr/bin/env python3
"""Portable serial kernel replay for the attained source-cup bound."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from check_axioms import audit_output


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight(manifest=None):
    """Validate the frozen source identities without requiring Lean objects."""
    if manifest is None:
        manifest = json.loads((HERE / 'manifest.json').read_text())
    for name, expected in manifest['bundle_inputs'].items():
        if sha(HERE / name) != expected:
            raise ValueError(f'Changed bundle input: {name}')
    for name, expected in manifest['external_inputs'].items():
        if sha(ROOT / name) != expected:
            raise ValueError(f'Changed external input: {name}')
    for module in manifest['modules']:
        source = HERE / (module['name'] + '.lean')
        if re.search(r'\b(sorry|admit|native_decide|sorryAx|axiom)\b', source.read_text()):
            raise ValueError(f'Forbidden proof token: {module["name"]}')
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preflight-only', action='store_true')
    parser.add_argument('--manifest', type=Path, default=HERE / 'manifest.json')
    parser.add_argument('--output', type=Path,
                        default=ROOT / '.cache/residual-rank-attainment-2026-10-10')
    args = parser.parse_args()
    manifest = preflight(json.loads(args.manifest.read_text()))
    if args.preflight_only:
        print('Source identity and proof-token preflight passed.')
        return

    args.output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env['LEAN_PATH'] = str(args.output.resolve()) + os.pathsep + env.get('LEAN_PATH', '')
    env['LEAN_NUM_THREADS'] = '1'
    imported_objects = {}
    for name in manifest['external_inputs']:
        if name.startswith('ErdosSzekeres/') and name.endswith('.lean'):
            obj = ROOT / '.lake/build/lib/lean' / Path(name).with_suffix('.olean')
            if not obj.is_file():
                raise ValueError(f'Missing built dependency: {name}; run lake build first')
            imported_objects[str(obj.relative_to(ROOT))] = sha(obj)
    record = {
        'schema': 'residual-rank-attainment-kernel-check-v1',
        'scope': manifest['scope'],
        'lean': subprocess.check_output(['lean', '--version'], env=env, text=True).strip(),
        'checker_sha256': sha(Path(__file__)),
        'manifest_sha256': sha(args.manifest),
        'external_sources': manifest['external_inputs'],
        'imported_objects': imported_objects,
        'modules': {},
        'complete': False,
    }
    record_path = HERE / 'kernel-check.json'

    def save():
        record_path.write_text(json.dumps(record, indent=2) + '\n')

    save()
    audit_logs = []
    for module in manifest['modules']:
        name = module['name']
        source = HERE / (name + '.lean')
        obj = args.output / (name + '.olean')
        started = time.monotonic()
        proc = subprocess.run(
            ['lean', '-j1', '-s32768', '-M10000', '--root=' + str(HERE),
             str(source.relative_to(ROOT)), '-o', str(obj)],
            cwd=ROOT, env=env, text=True, capture_output=True)
        output = (proc.stdout + proc.stderr).replace(str(ROOT) + os.sep, '')
        log = args.output / (name + '.log')
        log.write_text(output)
        item = {'exit': proc.returncode, 'seconds': round(time.monotonic() - started, 3),
                'source_sha256': sha(source), 'log_sha256': sha(log), 'axioms': {}}
        if proc.returncode == 0:
            item['olean_sha256'] = sha(obj)
            for theorem in module['theorems']:
                item['axioms'][theorem] = audit_output(output, theorem)
            audit_logs.append(output)
        record['modules'][name] = item
        save()
        print(name, proc.returncode, item['seconds'], flush=True)
        if proc.returncode:
            print(output)
            raise SystemExit(proc.returncode)

    for name, expected in manifest['external_inputs'].items():
        if sha(ROOT / name) != expected:
            raise ValueError(f'External source changed during build: {name}')
    for name, expected in imported_objects.items():
        if sha(ROOT / name) != expected:
            raise ValueError(f'Imported object changed during build: {name}')
    for name, expected in manifest['bundle_inputs'].items():
        if sha(HERE / name) != expected:
            raise ValueError(f'Bundle input changed during build: {name}')
    audit = HERE / 'axioms.txt'
    audit.write_text('\n'.join(audit_logs))
    record['axioms_sha256'] = sha(audit)
    record['complete'] = True
    save()
    print('Both modules checked; all six theorem roots use only standard axioms.')


if __name__ == '__main__':
    main()
