#!/usr/bin/env python3
"""Build the residual32 continuation from source on either macOS or Linux.

Run with ``lake env python3 scripts/check_residual32_continuation.py`` after
the maintained library has built. This gate never reuses experiment objects
or compares platform-specific object hashes. It independently compiles the
literal catalog, witness, and geometric proofs, and audits their conclusions.
It does not assert the 313-point theorem.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[1]
OLD = ROOT/'experiments/omission-residual32-context-certificates-2026-10-10'
WITNESS = ROOT/'experiments/omission-residual32-case4-2026-10-10'
COUPLED = ROOT/'experiments/omission-residual32-witness-coupled-2026-10-10'
FOURTH = ROOT/'experiments/omission-residual32-fourth-global-variants-2026-10-10'
SIXTH = ROOT/'experiments/omission-residual32-sixth-variants-2026-10-10'
ADDED = ROOT/'experiments/omission-residual32-added-rows-2026-10-10'
PRIMAL = ROOT/'experiments/omission-residual32-2598-primal-2026-10-10'
RELAXED = ROOT/'experiments/omission-residual32-sixth-relaxed-2026-10-10'
RANK = ROOT/'experiments/omission-residual-rank-attainment-2026-10-10'
RANK_CORES = ROOT/'experiments/omission-residual32-rank-certificates-2026-10-10'
NORMALIZATION = ROOT/'experiments/omission-residual-rank-normalization-2026-10-10'
STANDARD = {'propext','Classical.choice','Quot.sound'}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def import_file(name, path):
    spec = importlib.util.spec_from_file_location(name,path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def unit_plan():
    old_manifest = json.loads((OLD/'manifest.json').read_text())
    import_file('catalog_preflight', OLD/'check.py').preflight(old_manifest)
    units = [(OLD,'Residual32ContextsProof.Catalog',
              ['OmissionResidual32Contexts.code_correct'])]
    for bundle, prefix in [(WITNESS,''),(COUPLED,''),(SIXTH,''),
                           (FOURTH,'FourthGlobalProof.'),(ADDED,''),(RELAXED,''),(RANK,''),
                           (RANK_CORES,''),(NORMALIZATION,'')]:
        if bundle == RELAXED:
            import_file('relaxed_preflight',bundle/'check.py').check()
        if bundle == RANK:
            import_file('rank_preflight',bundle/'check.py').preflight()
        if bundle in (RANK_CORES,NORMALIZATION):
            import_file('new_rank_preflight_'+bundle.name.replace('-','_'),bundle/'check.py').check()
        if bundle in (FOURTH,ADDED):
            manifest = json.loads((bundle/'manifest.json').read_text())
            import_file('row_preflight',bundle/'check.py').preflight(manifest)
        record = json.loads((bundle/'kernel-check.json').read_text())
        if not record['complete']:
            raise ValueError(f'Incomplete local proof record: {bundle}')
        if bundle == WITNESS and sha(bundle/'witness.json') != record['witness_json_sha256']:
            raise ValueError('Witness JSON differs from its kernel-check record')
        modules = {'AddedRows':record} if bundle == ADDED else record['modules']
        for name, details in modules.items():
            name = prefix+name
            source = bundle/Path(*name.split('.')).with_suffix('.lean')
            if sha(source) != details['source_sha256']:
                raise ValueError(f'Source differs from its checked record: {source}')
            units.append((bundle,name,list(details['axioms'])))
    return units


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    cache = ROOT/'.cache'
    cache.mkdir(exist_ok=True)
    output = (args.output.resolve() if args.output else
              Path(tempfile.mkdtemp(prefix='residual32-ci-',dir=cache)))
    output.mkdir(parents=True,exist_ok=True)
    if any(output.rglob('*.olean')):
        raise ValueError('Use a fresh output directory without Lean objects')
    units = unit_plan()
    exporter = import_file('coupled_export', ROOT/'scripts/export_omission_coupled_sized.py')
    regenerated = output/'LeanCore-regenerated.lean'
    exporter.export(COUPLED/'core13.json',regenerated,'CoupledCoreSixth',COUPLED.name,'core13')
    expected = regenerated.read_text().replace('../../experiments/'+COUPLED.name+'/','')
    if expected != (COUPLED/'LeanCore.lean').read_text():
        raise ValueError('Coupled core differs from regenerated clause semantics')
    for bundle, filename in [(WITNESS,'test_check.py'),(COUPLED,'test_check.py'),
                             (FOURTH,'test_preflight.py'),(ADDED,'test_preflight.py'),
                             (PRIMAL,'test_check.py'),(RELAXED,'test_check.py'),
                             (RANK,'test_check.py'),(RANK_CORES,'test_check.py'),
                             (NORMALIZATION,'test_check.py')]:
        test = bundle/filename
        if not test.is_file():
            raise ValueError(f'Missing expected finite controls: {test}')
        subprocess.run([sys.executable,str(test)],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(COUPLED/'check.py')],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(SIXTH/'check.py')],cwd=ROOT,check=True)
    subprocess.run([sys.executable,str(PRIMAL/'check.py')],cwd=ROOT,check=True)
    env = dict(os.environ)
    env['LEAN_PATH'] = str(output)+os.pathsep+env.get('LEAN_PATH','')
    env['LEAN_NUM_THREADS'] = '1'
    version = subprocess.check_output(['lean','--version'],text=True,env=env).strip()
    if 'version 4.24.0,' not in version:
        raise ValueError('Use the pinned Lean 4.24.0 toolchain')
    report = {'scope':'Fresh standalone witness, geometric-row and attained-rank checks; no 313-point theorem.',
              'lean':version,'complete':False,'modules':{}}
    audit = []
    total = time.monotonic()
    for bundle, module, names in units:
        relative = Path(*module.split('.'))
        source = bundle/relative.with_suffix('.lean')
        target = output/relative.with_suffix('.olean')
        target.parent.mkdir(parents=True,exist_ok=True)
        raw = source.read_text()
        if re.search(r'\b(?:sorry|admit|sorryAx|native_decide)\b|^\s*(?:private\s+)?axiom\s',raw,re.M):
            raise ValueError(f'Forbidden proof token: {source}')
        tick = time.monotonic()
        proc = subprocess.run(['lean','-j1','-s','32768','-M','14000',
                               '--root='+str(bundle),'-o',str(target),str(source)],
                              cwd=ROOT,env=env,text=True,capture_output=True)
        log = proc.stdout+proc.stderr
        (output/(module+'.log')).write_text(log)
        entry = {'source':str(source.relative_to(ROOT)),'source_sha256':sha(source),
                 'exit':proc.returncode,'seconds':round(time.monotonic()-tick,3),'axioms':{}}
        report['modules'][module] = entry
        if proc.returncode or 'warning:' in log:
            print(log,file=sys.stderr)
            (output/'check.json').write_text(json.dumps(report,indent=2)+'\n')
            raise RuntimeError(f'Lean failed or warned in {module}')
        observed = dict(re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log))
        for name, body in observed.items():
            axioms = {a.strip() for a in body.split(',') if a.strip()}
            if not axioms <= STANDARD:
                raise ValueError(f'Unexpected axioms in {name}: {axioms}')
        for name in names:
            if name in observed:
                entry['axioms'][name] = sorted(a.strip() for a in observed[name].split(',') if a.strip())
            elif f"'{name}' does not depend on any axioms" in log:
                entry['axioms'][name] = []
            else:
                raise ValueError(f'Missing expected audit: {name}')
        audit.append(log)
        print(f'{module}: passed ({entry["seconds"]}s, {len(names)} audited roots)',flush=True)
        (output/'check.json').write_text(json.dumps(report,indent=2)+'\n')
    report['complete'] = True
    report['seconds'] = round(time.monotonic()-total,3)
    (output/'axioms.txt').write_text('\n'.join(audit))
    (output/'check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(f'Fresh residual32 continuation checks passed; record: {output}/check.json',flush=True)


if __name__ == '__main__':
    main()
