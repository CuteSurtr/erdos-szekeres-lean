#!/usr/bin/env python3
"""Serial source compilation after exact finite replay and input preflight."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from check import HERE, ROOT, check, preflight, sha
sys.path.insert(0, str(ROOT / 'scripts'))
from check_axioms import audit_output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        default=ROOT / '.cache/residual32-rank-certificates-2026-10-10')
    args = parser.parse_args()
    finite = check()
    manifest = preflight()
    args.output.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env['LEAN_PATH'] = str(args.output.resolve()) + os.pathsep + env.get('LEAN_PATH', '')
    env['LEAN_NUM_THREADS'] = '1'
    objects = {}
    for name in manifest['external_inputs']:
        if name.startswith('ErdosSzekeres/') and name.endswith('.lean'):
            obj = ROOT / '.lake/build/lib/lean' / Path(name).with_suffix('.olean')
            if not obj.is_file():
                raise ValueError('Build the maintained library before replay: ' + name)
            objects[str(obj.relative_to(ROOT))] = sha(obj)
    record = {'schema': 'rank-search-coupled-core-kernel-v1', 'scope': manifest['scope'],
              'lean': subprocess.check_output(['lean', '--version'], text=True).strip(),
              'manifest_sha256': sha(HERE / 'manifest.json'), 'checker_sha256': sha(Path(__file__)),
              'finite_check': finite, 'external_inputs': manifest['external_inputs'],
              'imported_objects': objects, 'modules': {}, 'complete': False}

    def save():
        (HERE / 'kernel-check.json').write_text(json.dumps(record, indent=2) + '\n')

    save()
    logs = []
    for module in manifest.get('dependency_modules', []) + manifest['modules']:
        name = module['name']
        dependency = 'source' in module
        source = ROOT / module['source'] if dependency else HERE / (name + '.lean')
        if re.search(r'\b(sorry|admit|native_decide|sorryAx|axiom)\b', source.read_text()):
            raise ValueError('Forbidden proof token: ' + name)
        obj = args.output / (name + '.olean')
        started = time.monotonic()
        result = subprocess.run(['lean', '-j1', '-s32768', '-M10000', '--root=' + str(source.parent),
                                 str(source.relative_to(ROOT)), '-o', str(obj)],
                                cwd=ROOT, env=env, text=True, capture_output=True)
        output = (result.stdout + result.stderr).replace(str(ROOT) + os.sep, '')
        log = args.output / (name + '.log')
        log.write_text(output)
        item = {'exit': result.returncode, 'seconds': round(time.monotonic() - started, 3),
                'source_sha256': sha(source), 'log_sha256': sha(log), 'axioms': {}}
        if result.returncode == 0:
            if 'warning:' in output:
                raise ValueError('Lean emitted a warning in ' + name + ': ' + output)
            item['olean_sha256'] = sha(obj)
            item['axioms'] = {theorem: audit_output(output, theorem) for theorem in module['theorems']}
            logs.append(output)
        if dependency:
            record.setdefault('dependency_modules', {})[name] = item
        else:
            record['modules'][name] = item
        save()
        print(name, result.returncode, item['seconds'], flush=True)
        if result.returncode:
            print(output)
            raise SystemExit(result.returncode)
    preflight(manifest)
    for name, digest in objects.items():
        if sha(ROOT / name) != digest:
            raise ValueError('Imported object changed during compilation: ' + name)
    audit = HERE / 'axioms.txt'
    audit.write_text('\n'.join(logs))
    record['axioms_sha256'] = sha(audit)
    record['complete'] = True
    save()
    print('All eight certificate modules checked; sixteen roots audited, plus rank dependencies.', flush=True)


if __name__ == '__main__':
    main()
