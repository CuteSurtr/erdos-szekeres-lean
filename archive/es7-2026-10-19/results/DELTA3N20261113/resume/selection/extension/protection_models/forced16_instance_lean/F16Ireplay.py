#!/usr/bin/env python3
"""Sequential replay through the bounded watcher; requires an allocated Lean slot."""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
WORK = Path(os.environ.get('F16I_WORK_DIR', str(HERE / 'work'))).resolve()
RECORD = Path(os.environ.get('F16I_RECORD_DIR', str(HERE / 'data'))).resolve()
WORK.mkdir(parents=True, exist_ok=True)
RECORD.mkdir(parents=True, exist_ok=True)
if (HERE / 'FROZEN.json').exists():
    frozen = json.loads((HERE / 'FROZEN.json').read_text())
    manifest_bytes = (HERE / 'data/manifest.json').read_bytes()
    assert hashlib.sha256(manifest_bytes).hexdigest() == frozen['manifest_sha256']
    manifest = json.loads(manifest_bytes)
    for m in manifest['modules']:
        assert hashlib.sha256((HERE / (m['module']+'.lean')).read_bytes()).hexdigest() == m['source_sha256']
    for d in manifest['dependencies']:
        for kind in ['source', 'olean']:
            assert hashlib.sha256(Path(d[kind]).read_bytes()).hexdigest() == d[kind+'_sha256']
modules = json.loads((HERE / 'data/generation.json').read_text())['modules']
modules.append('F16IPairs')
modules.append('F16ITable')
if len(sys.argv) > 1:
    selected = sys.argv[1:]
    assert all(m in modules for m in selected)
    modules = selected
started = time.monotonic()
results = []
for name in modules:
    source = HERE / (name + '.lean')
    text = source.read_text()
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b|Lean\.ofReduceBool', text)
    cmd = [sys.executable, '-B', str(HERE / 'F16Icheck1000.py'), str(source), name+'-final', '--export']
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    print(proc.stdout, end='', flush=True)
    receipt = json.loads((WORK / (name+'-final.json')).read_text())
    log = (WORK / (name+'-final.log')).read_text()
    audits = re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log)
    empty = re.findall(r"'([^']+)' does not depend on any axioms", log)
    audit_names = [n for n,_ in audits] + empty
    assert set(audit_names) == set(re.findall(r'#print axioms\s+(\w+)', text)) or (
        {n.rsplit('.',1)[-1] for n in audit_names} == set(re.findall(r'#print axioms\s+(\w+)', text)))
    allowed = {'propext','Classical.choice','Quot.sound'}
    for _, ax in audits:
        assert {a.strip() for a in ax.split(',') if a.strip()} <= allowed
    result = dict(module=name, receipt=receipt, audit_names=audit_names,
                  source_sha256=hashlib.sha256(source.read_bytes()).hexdigest())
    results.append(result)
    passed = proc.returncode == 0 and receipt['exit_code'] == 0 and not receipt['stop_reason']
    passed = passed and not re.search(r'\berror:|\bwarning:', log)
    (RECORD / 'replay-progress.json').write_text(json.dumps(dict(
        elapsed_seconds=time.monotonic()-started, passed_so_far=passed, results=results),indent=2)+'\n')
    if not passed:
        raise SystemExit('stopped at '+name)
print(json.dumps({'status':'PASS', 'modules':len(results),
    'audits':sum(len(r['audit_names']) for r in results),
    'elapsed_seconds':round(time.monotonic()-started,3)}),flush=True)
