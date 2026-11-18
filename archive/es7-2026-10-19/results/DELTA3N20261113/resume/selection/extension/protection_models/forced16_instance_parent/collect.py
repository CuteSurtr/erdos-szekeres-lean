#!/usr/bin/env python3
"""Independent parent transcription and fresh Lean-receipt collection."""
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import resource
import shutil

resource.setrlimit(resource.RLIMIT_AS,(150<<20,150<<20))
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'forced16_instance_lean'
RAW=HERE.parent/'forced16_realization/data'
WORK=Path('/home/jay/research/data/delta3-codex-20261113/extension/forced16-instance-parent-a')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((SOURCE/'data/manifest.json').read_text())
freeze=json.loads((SOURCE/'FROZEN.json').read_text())
assert sha(SOURCE/'data/manifest.json')==freeze['manifest_sha256']
assert sha(RAW/'certificate.json')==manifest['certificate_sha256']
assert sha(RAW/'orientation.signs')==manifest['signs_sha256']
text=(SOURCE/'F16IData.lean').read_text()


def literal_body(name,typ):
    marker=f'def {name} : List {typ} := ['
    assert text.count(marker)==1
    return text.split(marker,1)[1].split('\n]',1)[0]


def tuples(name,typ,width):
    body=literal_body(name,typ)
    result=[]
    for raw in re.findall(r'⟨([0-9, ]+)⟩',body):
        row=tuple(map(int,raw.split(',')))
        assert len(row)==width
        result.append(row)
    rest=re.sub(r'⟨[0-9, ]+⟩','',body)
    assert not rest.replace(',','').strip()
    return result


triples=tuples('triples','Triple',3)
assert triples==list(combinations(range(16),3))
indices={t:i for i,t in enumerate(triples)}
body=literal_body('signs','Bool')
signs=[v=='true' for v in re.findall(r'\b(true|false)\b',body)]
assert not re.sub(r'\b(true|false)\b','',body).replace(',','').strip()
assert signs==[v=='+' for v in (RAW/'orientation.signs').read_text().strip()]
rows=tuples('rows','Row',13)
certificate=json.loads((RAW/'certificate.json').read_text())
assert len(rows)==len(certificate['rows'])==387
for emitted,raw in zip(rows,certificate['rows']):
    a=raw['root'];b,c,d,e=raw['other'];large=raw['large'];small=raw['small']
    factors=[[(a,b,c),(a,d,e)],[(a,b,d),(a,c,e)],[(a,b,e),(a,c,d)]]
    big=[indices[tuple(sorted(t))] for t in factors[large]]
    little=[indices[tuple(sorted(t))] for t in factors[small]]
    expected=(a,b,c,d,e,large,small,3-large-small,*big,*little,raw['weight'])
    assert emitted==expected

progress=json.loads((WORK/'data/replay-progress.json').read_text())
expected_modules=[m['module'] for m in manifest['modules']]
assert progress['passed_so_far'] and [r['module'] for r in progress['results']]==expected_modules
assert len(expected_modules)==338
all_audits={}
checks=[]
(HERE/'data/logs').mkdir(parents=True,exist_ok=True)
for entry in manifest['modules']:
    name=entry['module'];src=SOURCE/(name+'.lean')
    assert sha(src)==entry['source_sha256']
    receipt_path=WORK/'work'/(name+'-final.json')
    log_path=WORK/'work'/(name+'-final.log')
    receipt=json.loads(receipt_path.read_text());log=log_path.read_text()
    assert receipt['exit_code']==0 and receipt['stop_reason'] is None
    assert receipt['source_sha256']==entry['source_sha256']
    assert receipt['rusage_maxrss_kib']<950*1024
    assert receipt['proc_status_peaks_kib_except_threads'].get('VmSwap',0)==0
    assert not re.search(r'\b(error|warning)(?:\(|:)',log)
    reports={n:[a.strip() for a in raw.split(',') if a.strip()]
             for n,raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log)}
    reports.update({n:[] for n in re.findall(r"'([^']+)' does not depend on any axioms",log)})
    assert not set(reports)&set(all_audits)
    all_audits.update(reports)
    checks.append({'module':name,'source_sha256':sha(src),'seconds':receipt['elapsed_seconds'],
                   'peak_rss_kib':receipt['rusage_maxrss_kib'],
                   'olean_matches_worker':sha(WORK/'work'/(name+'.olean'))==entry['olean_sha256']})
    shutil.copy2(receipt_path,HERE/'data/logs'/receipt_path.name)
    shutil.copy2(log_path,HERE/'data/logs'/log_path.name)
expected_audits={r['theorem']:r['axioms'] for r in manifest['axiom_reports']}
assert len(expected_audits)==len(manifest['axiom_reports'])==354
assert all_audits==expected_audits and len(all_audits)==354
for report in manifest['axiom_reports']:
    module_log=(WORK/'work'/(report['module']+'-final.log')).read_text()
    assert "'"+report['theorem']+"'" in module_log
for dep in manifest['dependencies']:
    for kind in ['source','olean']:
        assert sha(Path(dep[kind]))==dep[kind+'_sha256']
result={'status':'PASS','label':'PROVED Lean finite/conditional certificate; fresh parent replay',
        'modules':338,'axiom_reports':354,'exact_axiom_lists_match':True,
        'transcription':{'triples':560,'signs':560,'rows':387,'all_raw_labels_slots_factors_weights_match':True},
        'seconds':sum(r['seconds'] for r in checks),'maximum_rss_kib':max(r['peak_rss_kib'] for r in checks),
        'checks':checks,'manifest_sha256':sha(SOURCE/'data/manifest.json'),
        'collector_sha256':sha(Path(__file__)),
        'scope':'No fully formal actual-coordinate or Mathlib-Real adapter is claimed. The fixed product inequalities and numerical certificate are checked.'}
(HERE/'data/result.json').write_text(json.dumps(result,indent=2)+'\n')
shutil.copy2(SOURCE/'data/manifest.json',HERE/'data/worker-manifest.json')
shutil.copy2(SOURCE/'FROZEN.json',HERE/'data/worker-freeze.json')
print(json.dumps({k:result[k] for k in ['status','modules','axiom_reports','seconds','maximum_rss_kib','transcription']}))
