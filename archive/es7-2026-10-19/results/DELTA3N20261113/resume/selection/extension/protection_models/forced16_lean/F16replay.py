#!/usr/bin/env python3
"""Sequential short replay; place the entire driver under the README's 20-second timeout."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parent
WORK=ROOT/'work'
ap=argparse.ArgumentParser()
ap.add_argument('--prefix',required=True)
args=ap.parse_args()
assert args.prefix.replace('-','').replace('_','').isalnum()
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((ROOT/'data/manifest.json').read_text())
assert sha(ROOT/'F16check_light.py')==m['runner_sha256']
checks=[]
status='FAIL'
try:
 for entry in m['checks']:
  p=ROOT/entry['source'];assert sha(p)==entry['sha256']
  tag=args.prefix+'-'+p.stem.lower()
  rc=subprocess.run([sys.executable,'-B',str(ROOT/'F16check_light.py'),str(p),tag,'--export'],
                    timeout=20,check=False).returncode
  j=json.loads((WORK/(tag+'.json')).read_text());log=(WORK/(tag+'.log')).read_text()
  audits={n:[a.strip() for a in raw.split(',') if a.strip()]
    for n,raw in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log)}
  audits.update({n:[] for n in re.findall(r"'([^']+)' does not depend on any axioms",log)})
  checks.append({'source':p.name,'tag':tag,'exit_code':rc,'axiom_reports':audits})
  assert rc==j['exit_code']==0 and j['stop_reason'] is None
  assert j['source_sha256']==entry['sha256'] and audits==entry['axiom_reports']
  assert not re.search(r'\b(error|warning)(?:\(|:)',log)
  assert j['rusage_maxrss_kib']<480*1024
  assert j['proc_status_peaks_kib_except_threads']['VmSwap']==0
 status='PASS'
finally:
 (WORK/(args.prefix+'-DONE.json')).write_text(json.dumps(
   {'status':status,'checks':checks,'fixed_model_Lean_claim':False},indent=2)+'\n')
print('PASS: all five generic algebra modules and 29 axiom reports match.')
