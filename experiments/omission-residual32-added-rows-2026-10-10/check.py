#!/usr/bin/env python3
"""Validate frozen source identities and freshly compile the129-row bridge."""
import argparse
import gzip
import hashlib
import json
import os
import re
import subprocess
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CACHE = ROOT / '.cache/residual32-added-rows-2026-10-10'
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def preflight(manifest):
    checked = {}
    for name, expected in manifest['external_inputs'].items():
        actual = sha(ROOT / name)
        if actual != expected:
            raise ValueError('Changed external source: ' + name)
        checked[name] = actual
    for name, expected in manifest['files'].items():
        actual = sha(HERE / name)
        if actual != expected:
            raise ValueError('Changed bridge source: ' + name)
        checked[str((HERE / name).relative_to(ROOT))] = actual
    parsed = []
    for field in ('source', 'old_source'):
        raw = gzip.decompress((ROOT / manifest[field]).read_bytes())
        if hashlib.sha256(raw).hexdigest() != manifest[field + '_uncompressed_sha256']:
            raise ValueError('Changed decompressed ' + field)
        parsed.append(json.loads(raw))
    source, old = parsed
    if source['states'] != old['states'] or source['constraints'][:2469] != old['constraints']:
        raise ValueError('Frozen2469 prefix changed')
    if len(source['constraints']) != 2598 or len(old['constraints']) != 2469:
        raise ValueError('Unexpected source dimensions')
    bindings = [{'local_row': i, 'source_row': 2469 + i, **r}
                for i, r in enumerate(source['constraints'][2469:])]
    if manifest['bindings'] != bindings:
        raise ValueError('Ordered129 tail binding changed')
    fourth = json.loads((ROOT / 'experiments/omission-residual32-fourth-global-variants-2026-10-10/row-bindings.json').read_bytes())['rows']
    core = json.loads((ROOT / 'experiments/omission-residual32-witness-coupled-2026-10-10/core13.json').read_bytes())['support']
    expected_tail = [{'support': core, 'rhs': 1}] + [{'support': r['support'], 'rhs': r['rhs']} for r in fourth]
    if source['constraints'][2469:] != expected_tail:
        raise ValueError('Tail differs from checked geometric families')
    return checked


def imported_objects():
    paths, identities = [], {}
    for bundle, prefix, names in [
        ('context-certificates', 'Residual32ContextsProof/', ['Catalog']),
        ('case4', '', ['Witness']),
        ('witness-coupled', '', ['LeanCore', 'Geometry']),
        ('fourth-global-variants', 'FourthGlobalProof/', ['Data'] + [f'Part{i:02}' for i in range(8)] + ['Root']),
    ]:
        path = ROOT / f'.cache/residual32-{bundle}-2026-10-10'
        paths.append(path)
        record_path = ROOT / f'experiments/omission-residual32-{bundle}-2026-10-10/kernel-check.json'
        record = json.loads(record_path.read_bytes())
        if not record.get('complete', record.get('all_modules_passed', False)):
            raise ValueError('Incomplete imported proof: ' + bundle)
        modules = record['modules']
        if isinstance(modules, list):
            modules = {r['module'].split('.')[-1]: r for r in modules}
        for name in names:
            obj = path / (prefix + name + '.olean')
            actual = sha(obj)
            if actual != modules[name]['olean_sha256']:
                raise ValueError('Imported object differs from checked record: ' + str(obj))
            identities[str(obj.relative_to(ROOT))] = actual
        identities[str(record_path.relative_to(ROOT))] = sha(record_path)
    return paths, identities


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preflight-only', action='store_true')
    parser.add_argument('--output', type=Path, default=CACHE)
    args = parser.parse_args()
    manifest = json.loads((HERE / 'manifest.json').read_text())
    checked = preflight(manifest)
    if args.preflight_only:
        print(json.dumps({'passed': True, 'identities': len(checked), 'literal_tail_rows': 129}))
        return
    paths, objects = imported_objects()
    cache = args.output.resolve()
    cache.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env['LEAN_PATH'] = os.pathsep.join(map(str, [cache] + paths)) + os.pathsep + env.get('LEAN_PATH', '')
    env['LEAN_NUM_THREADS'] = '1'
    version = subprocess.check_output(['lean', '--version'], text=True).strip()
    if 'version 4.24.0,' not in version:
        raise ValueError('Use pinned Lean4.24.0')
    source, obj = HERE / 'AddedRows.lean', cache / 'AddedRows.olean'
    start = time.monotonic()
    result = subprocess.run(['lean', '-j1', '-s', '32768', '-M', '14000', '--root=' + str(HERE),
                             '-o', str(obj), str(source)], cwd=ROOT, env=env, text=True, capture_output=True)
    output = result.stdout + result.stderr
    log = cache / 'AddedRows.log'
    log.write_text(output)
    report = {'scope': manifest['scope'], 'complete': False, 'lean': version,
              'manifest_sha256': sha(HERE / 'manifest.json'), 'checker_sha256': sha(Path(__file__)),
              'validated_identities': checked, 'imported_checked_objects': objects,
              'source_sha256': sha(source), 'exit': result.returncode,
              'seconds': round(time.monotonic() - start, 3), 'log_sha256': sha(log)}
    (HERE / 'kernel-check.json').write_text(json.dumps(report, indent=2) + '\n')
    if result.returncode or 'warning:' in output:
        raise RuntimeError(output)
    matches = dict(re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output))
    report['axioms'] = {}
    for short in ('literal_binding', 'all_rows'):
        name = manifest['namespace'] + '.' + short
        if name not in matches:
            raise ValueError('Missing theorem audit: ' + name)
        axioms = {a.strip() for a in matches[name].split(',') if a.strip()}
        if not axioms <= STANDARD:
            raise ValueError('Unexpected axioms: ' + str(axioms))
        report['axioms'][name] = sorted(axioms)
    (HERE / 'axioms.txt').write_text(output)
    report.update(complete=True, olean_sha256=sha(obj), axioms_sha256=sha(HERE / 'axioms.txt'))
    (HERE / 'kernel-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'complete': True, 'seconds': report['seconds'], 'axioms': report['axioms']}))


if __name__ == '__main__':
    main()
