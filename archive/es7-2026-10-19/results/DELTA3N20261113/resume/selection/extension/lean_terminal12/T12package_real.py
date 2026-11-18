#!/usr/bin/env python3
"""Collect five completed real-stage checks; never invokes Lean."""
from pathlib import Path
import hashlib,json,re,shutil
ROOT=Path(__file__).resolve().parent
REPO=Path('/home/jay/research/lean/erdos-szekeres-lean')
W=Path('/home/jay/research/data/delta3-codex-20261113/extension/lean-terminal12')
D=ROOT/'data'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
runs=[('T12BridgeBase','t12-base-v1'),('T12ConvexBridge','t12-convex-v1'),
      ('T12TerminalReal','t12-terminalreal-v1'),('T12PointSetBridge','t12-pointset-v1'),
      ('T12Real','t12-real-v1')]
checks=[]
for stem,tag in runs:
 p=ROOT/(stem+'.lean');j=json.loads((W/(tag+'.json')).read_text())
 log=(W/(tag+'.log')).read_text()
 assert j['exit_code']==0 and j['stop_reason'] is None
 assert j['source_sha256']==sha(p)
 assert j['rusage_maxrss_kib']<2000*1024 and j['proc_status_peaks_kib_except_threads']['VmSwap']==0
 assert not re.search(r'\b(error|warning)(?:\(|:)',log)
 assert not re.search(r'\b(sorry|admit|native_decide)\b|^\s*axiom\b|Lean\.ofReduceBool',p.read_text(),re.M)
 audits={n:[a.strip() for a in raw.split(',') if a.strip()]
   for n,raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log)}
 audits.update({n:[] for n in re.findall(r"'([^']+)' does not depend on any axioms",log)})
 assert len(audits)==p.read_text().count('#print axioms')
 assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in audits.values())
 for ext in ['.log','.json']:shutil.copyfile(W/(tag+ext),D/(tag+ext))
 checks.append(dict(source=p.name,sha256=sha(p),run=tag,axiom_reports=audits,
   seconds=j['elapsed_seconds'],kernel_maxrss_kib=j['rusage_maxrss_kib'],
   sampled_peaks=j['proc_status_peaks_kib_except_threads'],
   log_sha256=sha(D/(tag+'.log')),record_sha256=sha(D/(tag+'.json'))))
finite=json.loads((D/'finite-manifest.json').read_text())
prerequisites=[]
for c in finite['checks']:
 assert sha(ROOT/c['source'])==c['sha256']
 prerequisites.append(dict(source=c['source'],sha256=c['sha256']))
cache=[]
for module in ['ErdosSzekeres/IntegerCertificates','ErdosSzekeres/OrientationConvexity',
               'ErdosSzekeres/Suk/FourPoint','ErdosSzekeres/OrientationGeometry','ErdosSzekeres/Basic']:
 cache.append(dict(module=module.replace('/','.'),
   source_sha256=sha(REPO/(module+'.lean')),
   olean_sha256=sha(REPO/'.lake/build/lib/lean'/(module+'.olean'))))
m=dict(label='PROVED',status='actual real twelve-point n6 terminal-membership obstruction',
 main_theorem='Delta3.Terminal12.RealBridge.terminal12_real_obstruction',
 existence_theorem='Delta3.Terminal12.RealBridge.exists_real_terminal_obstruction',
 points=12,n=6,cap_exclusion=5,polygon_exclusion=6,hit_polygon_size=5,
 checks=checks,new_source_files=5,new_axiom_audits=sum(len(c['axiom_reports']) for c in checks),
 total_check_seconds=round(sum(c['seconds'] for c in checks),3),
 kernel_peak_rss_kib=max(c['kernel_maxrss_kib'] for c in checks),
 total_packet_modules=19,total_packet_audits=59,standard_axioms_only=True,
 prerequisite_sources=prerequisites,project_cache=cache,
 finite_manifest_sha256=sha(D/'finite-manifest.json'),finite_freeze_sha256=sha(ROOT/'FROZEN_FINITE.json'),
 input_hashes=finite['input_hashes'],toolchain=(REPO/'lean-toolchain').read_text().strip(),
 runner_sha256=sha(ROOT/'T12check_real.py'),replay_sha256=sha(ROOT/'T12replay_real.py'),
 resources=dict(cpu=1,as_gib=4,rss_guard_mib=2000,lean_heap_mib=1000,
   long_unit_memorymax_mib=2600,swap_mib=0,per_module_wall_seconds=27,
   long_unit_deadline_kst='2026-11-14 08:20:00',owner_total_mib_unchanged=6000),
 minimum_or_lower_bound_claim=False,weak_or_uniform_delta_refutation=False,
 cap_definition='explicit all-triples real orientation with proved distinct horizontal coordinates',
 geometry_connection_external=False,parent_fresh_real_replay_pending=True)
assert m['new_axiom_audits']==27
(D/'real-manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print(json.dumps({k:m[k] for k in ['new_source_files','new_axiom_audits','total_check_seconds','kernel_peak_rss_kib']},indent=2))
print('real_manifest_sha256',sha(D/'real-manifest.json'))

