#!/usr/bin/env python3
"""Reproduce the additional-row independence proofs under ``lake env``.

The literal catalog is taken from the already attributed geometric artifact.
No search program or numerical optimizer is part of the proof. Build the main
library first. All compiled objects and logs go into the ignored work directory.
"""
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

from check_axioms import audit_output

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / 'experiments/omission-additional-rows-2026-10-10'
CATALOG = ROOT / 'experiments/omission-residual-geometry-2026-10-09/Catalog.lean.gz'
CATALOG_SHA = 'f94c74ecade3b2714f961cd3ee7826ad0804342886f0e86ab2ca3908f86cb7da'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def run(work, output):
    work = work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    catalog = gzip.decompress(CATALOG.read_bytes())
    if digest(catalog) != CATALOG_SHA:
        raise ValueError('Unexpected original catalog')
    sources = {'Catalog': catalog, **{
        name: (ARTIFACT / (name + '.lean')).read_bytes()
        for name in ['CycleIndependence', 'BlockIndependence', 'Irredundancy']}}
    env = dict(os.environ)
    env['LEAN_PATH'] = str(work) + os.pathsep + env.get('LEAN_PATH', '')
    report = {'scope': 'Additional geometric rows and their abstract irredundancy; no population bound',
              'lean': subprocess.check_output(['lean', '--version'], text=True).strip(),
              'catalog_sha256': CATALOG_SHA,
              'library_source_sha256': digest((ROOT / 'ErdosSzekeres/Omission/AdditionalResidualRows.lean').read_bytes()),
              'library_object_sha256': digest((ROOT / '.lake/build/lib/lean/ErdosSzekeres/Omission/AdditionalResidualRows.olean').read_bytes()),
              'modules': {}, 'complete': False}
    for name, data in sources.items():
        source, obj = work / (name + '.lean'), work / (name + '.olean')
        source.write_bytes(data)
        started = time.monotonic()
        result = subprocess.run(['lean', '-j1', '-s32768', '-M4000', str(source), '-o', str(obj)],
                                env=env, cwd=ROOT, text=True, capture_output=True)
        (work / (name + '.log')).write_text(result.stdout + result.stderr)
        if result.returncode:
            raise RuntimeError(f'{name} failed; see {work / (name + ".log")}')
        # Reports can use unqualified names in source; Lean prints full names.
        names = re.findall(r"^'([^']+)' (?:depends on axioms:|does not depend on any axioms)",
                           result.stdout, re.MULTILINE)
        count = len(re.findall(r'^#print axioms ', data.decode(), re.MULTILINE))
        if len(names) != count or count == 0 or len(set(names)) != count:
            raise ValueError(f'Incomplete axiom audit in {name}')
        audits = {theorem: audit_output(result.stdout, theorem) for theorem in names}
        report['modules'][name] = {'source_sha256': digest(data), 'olean_sha256': digest(obj.read_bytes()),
                                  'exit': result.returncode, 'seconds': round(time.monotonic()-started, 3),
                                  'axioms': audits, 'stdout': result.stdout}
        output.write_text(json.dumps(report, indent=2) + '\n')
        print(f'{name}: checked {count} roots', flush=True)
    report['complete'] = True
    output.write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args()
    run(a.work, a.output)
