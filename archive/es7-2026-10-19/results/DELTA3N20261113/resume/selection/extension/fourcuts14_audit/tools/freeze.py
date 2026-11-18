#!/usr/bin/env python3
import datetime,hashlib,json
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
r=json.loads((R/'data/result.json').read_text());assert r['status']=='PASS' and r['stable_inputs']
for path,h in r['input_sha256'].items():assert sha(Path(path))==h,path
c=json.loads((R/'data/controls.json').read_text());assert c['status']=='PASS' and len(c['cases'])==52 and c['selections']==185
assert '19.00' in (R/'data/attemptA/time.txt').read_text() and 'signal 9' in (R/'data/attemptA/time.txt').read_text()
with (R/'data/completion.json').open('x') as f:
 json.dump(dict(status='PASS',label='COMPUTED formula/controls; PROVED written projection',frozen_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),all48_rows=True,unchanged_base=True,source_inputs_stable=True,proof_replay=False,parent_result_report='At08:23 parent reports fourcuts14 UNKNOWN, archive roundtrip verified; no certificate. This packet does not independently replay that archive.',own_active_units=0,limits=dict(AS_MiB=150,CPU_count=1,wall_seconds=20,cpu_seconds=19)),f,indent=2);f.write('\n')
files=sorted(p for p in R.rglob('*') if p.is_file() and p!=R/'SHA256SUMS')
with (R/'SHA256SUMS').open('x') as f:
 for p in files:f.write(sha(p)+'  '+str(p.relative_to(R))+'\n')
print(json.dumps(dict(status='PASS',files=len(files),manifest_sha256=sha(R/'SHA256SUMS'),own_active_units=0)))
