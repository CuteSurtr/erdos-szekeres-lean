#!/usr/bin/env python3
"""Collect completed finite checks; does not invoke Lean."""
from pathlib import Path
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parent
W=Path('/home/jay/research/data/delta3-codex-20261113/extension/lean-terminal12')
D=ROOT/'data'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
runs=[
('T12Boolean','t12-boolean-v1'),('T12FiniteModel','t12-model-v1'),
('T12FiniteFacts','t12-facts-v1'),('T12Determinants','t12-determinants-v1'),
('T12IndexHelpers','t12-index-v1'),
('T12SixBlock00','t12-six-block00-v1'),('T12SixBlock01','t12-six-block01-v1'),
('T12SixCover00','t12-six-cover00-v1'),('T12SixCover01','t12-six-cover01-v1'),
('T12SixAggregate','t12-six-aggregate-v1'),
('T12SubsequenceFacts','t12-subsequence-v1'),('T12PredicateSemantics','t12-semantics-v1'),
('T12TerminalBridge','t12-terminal-v1'),('T12Finite','t12-finite-v1')]
checks=[]
for stem,tag in runs:
 p=ROOT/(stem+'.lean')
 j=json.loads((W/(tag+'.json')).read_text());log=(W/(tag+'.log')).read_text()
 assert j['exit_code']==0 and j['stop_reason'] is None
 assert j['source_sha256']==sha(p)
 assert j['rusage_maxrss_kib']<1300*1024 and j['proc_status_peaks_kib_except_threads']['VmSwap']==0
 assert not re.search(r'\b(error|warning)(?:\(|:)',log)
 assert not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\b|Lean\.ofReduceBool',
                      p.read_text(), re.M)
 audits={n:[a.strip() for a in raw.split(',') if a.strip()]
   for n,raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log)}
 audits.update({n:[] for n in re.findall(r"'([^']+)' does not depend on any axioms",log)})
 assert len(audits)==p.read_text().count('#print axioms')
 assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in audits.values())
 for ext in ['.log','.json']: shutil.copyfile(W/(tag+ext),D/(tag+ext))
 checks.append(dict(source=p.name,sha256=sha(p),run=tag,axiom_reports=audits,
   seconds=j['elapsed_seconds'],kernel_maxrss_kib=j['rusage_maxrss_kib'],
   sampled_peaks=j['proc_status_peaks_kib_except_threads'],
   log_sha256=sha(D/(tag+'.log')),record_sha256=sha(D/(tag+'.json'))))
P=json.loads((D/'T12-coordinates.json').read_text())['P']
actual=[[int(x),int(y)] for _,x,y in re.findall(r'\| (\d+|_) => \((-?\d+), (-?\d+)\)',
 (ROOT/'T12FiniteModel.lean').read_text())]
assert actual==P
input_hashes=json.loads((D/'input-hashes.json').read_text())
for name,entry in input_hashes.items():
 assert sha(D/name)==entry['sha256']
 assert sha(Path(entry['source']))==entry['sha256']
shutil.copyfile(W/'boolean-generation.json',D/'T12-boolean-generation.json')
m=dict(label='PROVED',status='finite integer-orientation and Boolean obstruction; real bridge pending',
 main_theorem='Delta3.Terminal12.terminal12_finite_obstruction',points=12,n=6,
 cap_exclusion=5,polygon_exclusion=6,hit_polygon_size=5,
 checks=checks,new_source_files=len(checks),
 new_axiom_audits=sum(len(c['axiom_reports']) for c in checks),
 total_check_seconds=round(sum(c['seconds'] for c in checks),3),
 kernel_peak_rss_kib=max(c['kernel_maxrss_kib'] for c in checks),
 standard_axioms_only=True,coordinate_syntax_matches_input=True,input_hashes=input_hashes,
 prerequisite_sources=[],runner_sha256=sha(ROOT/'T12check_finite.py'),
 replay_sha256=sha(ROOT/'T12replay_finite.py'),
 resources=dict(cpu=1,as_gib=4,rss_guard_mib=1300,lean_heap_mib=1000,
 long_unit_memorymax_mib=1800,swap_mib=0,per_module_wall_seconds=27),
 real_bridge_checked=False,minimum_or_lower_bound_claim=False,
 parent_fresh_replay_pending=True)
assert m['new_source_files']==14 and m['new_axiom_audits']==32
(D/'finite-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
f=dict(status='finite/Boolean sources frozen; real bridge separately pending',
 manifest_sha256=sha(D/'finite-manifest.json'),
 finished_sources={c['source']:c['sha256'] for c in checks},
 runner_sha256=m['runner_sha256'],replay_sha256=m['replay_sha256'])
(ROOT/'FROZEN_FINITE.json').write_text(json.dumps(f,indent=2)+'\n')
print(json.dumps({k:m[k] for k in ['new_source_files','new_axiom_audits','total_check_seconds','kernel_peak_rss_kib']},indent=2))
print('finite_manifest_sha256',sha(D/'finite-manifest.json'))
print('finite_freeze_sha256',sha(ROOT/'FROZEN_FINITE.json'))

