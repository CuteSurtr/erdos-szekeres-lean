#!/usr/bin/env python3
"""Audit successful bounded kernel receipts and freeze this finite packet only."""
import hashlib
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

generation=json.loads((HERE/'data/generation.json').read_text())
names=generation['modules']+['F16IPairs','F16ITable']
modules=[]
axioms=[]
allowed={'propext','Classical.choice','Quot.sound'}
for name in names:
    source=HERE/(name+'.lean')
    receipt_path=HERE/'work'/(name+'-final.json')
    log_path=HERE/'work'/(name+'-final.log')
    receipt=json.loads(receipt_path.read_text())
    text=source.read_text();log=log_path.read_text()
    assert receipt['exit_code']==0 and receipt['stop_reason'] is None,name
    assert receipt['source_sha256']==sha(source),name
    assert not re.search(r'\berror:|\bwarning:',log),name
    assert not re.search(r'\b(sorry|admit|native_decide|axiom)\b|Lean\.ofReduceBool',text),name
    found=[]
    for theorem,used in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",log):
        used=[a.strip() for a in used.split(',') if a.strip()]
        assert set(used)<=allowed
        found.append(theorem)
        axioms.append(dict(theorem=theorem,axioms=used,module=name))
    for theorem in re.findall(r"'([^']+)' does not depend on any axioms",log):
        found.append(theorem)
        axioms.append(dict(theorem=theorem,axioms=[],module=name))
    expected=re.findall(r'#print axioms\s+(\w+)',text)
    assert len(found)==len(expected) and {n.rsplit('.',1)[-1] for n in found}==set(expected),name
    modules.append(dict(module=name,source_sha256=sha(source),
        olean_sha256=sha(HERE/'work'/(name+'.olean')),
        receipt_sha256=sha(receipt_path),log_sha256=sha(log_path),
        elapsed_seconds=receipt['elapsed_seconds'],
        peak_rss_kib=receipt['rusage_maxrss_kib'],
        peaks=receipt['proc_status_peaks_kib_except_threads']))
dependencies=[]
for name in ['F16Products','F16Cancellation']:
    p=HERE.parent/'forced16_lean'
    dependencies.append(dict(module=name,source=str(p/(name+'.lean')),
        source_sha256=sha(p/(name+'.lean')),olean=str(p/'work'/(name+'.olean')),
        olean_sha256=sha(p/'work'/(name+'.olean'))))
for f,key in [('certificate.json','certificate_sha256'),('orientation.signs','signs_sha256')]:
    assert sha(HERE.parent/'forced16_realization/data'/f)==generation[key]
result=dict(status='PASS: finite kernel certificate and conditional product infeasibility',
    module_count=len(modules),axiom_report_count=len(axioms),
    modules=modules,axiom_reports=axioms,dependencies=dependencies,
    certificate_sha256=generation['certificate_sha256'],signs_sha256=generation['signs_sha256'],
    max_passed_rss_kib=max(m['peak_rss_kib'] for m in modules),
    total_lean_elapsed_seconds=round(sum(m['elapsed_seconds'] for m in modules),3),
    lean_version='4.24.0',constraints=dict(cpu=1,as_gib=3,rss_guard_mib=950,
        allocation_mib=1000,heap_mib=500,unit_memory_max_mib=1300,swap=0),
    boundary='No theorem yet derives these inequalities from actual coordinates realizing the sign table.',
    scripts={f.name:sha(f) for f in HERE.glob('*.py')},readme_sha256=sha(HERE/'README.md'))
(HERE/'data/manifest.json').write_text(json.dumps(result,indent=2)+'\n')
(HERE/'FROZEN.json').write_text(json.dumps(dict(status='FROZEN',
    scope=result['status'],manifest_sha256=sha(HERE/'data/manifest.json'),
    module_count=len(modules),axiom_report_count=len(axioms),
    no_full_real_model_claim=True),indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','module_count','axiom_report_count',
    'max_passed_rss_kib','total_lean_elapsed_seconds']}))
