#!/usr/bin/env python3
"""Summarize each fully GP-consistent candidate and its retained separation."""
import argparse, json
from pathlib import Path

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--archive',type=Path,required=True)
 ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();root=a.archive
 events=[json.loads(x) for x in (root/'events.jsonl').read_text().splitlines()]
 survivors={x['model_sha256']:dict(x) for x in events if x['event']=='gp_consistent_survivor'}
 for digest,row in survivors.items():
  row['separation']=[]
  for path in (root/'incoming').glob('*/linear_witness.json'):
   if not (path.parent/'approved.json').exists():continue
   witness=json.loads(path.read_text())
   if witness['model_sha256']==digest:
    row['separation'].append({'method':'linear identity','evidence':str(path.relative_to(root)),'terms':len(witness['records'])})
  for path in (root/'iterations').glob('*/cycle/m6_cycle_witness.json'):
   if not (path.parent/'verified.json').exists():continue
   witness=json.loads(path.read_text())
   if witness['model_sha256']==digest:
    row['separation'].append({'method':'product cycle','evidence':str(path.relative_to(root)),'comparisons':len(witness['comparisons'])})
  for path in (root/'incoming').glob('*/sdp_witness.json'):
   if not (path.parent/'approved.json').exists():continue
   witness=json.loads(path.read_text())
   if witness['model_sha256']==digest:
    row['separation'].append({'method':'negative-definite quadratic obstruction','evidence':str(path.relative_to(root)),'terms':len(witness['records'])})
 result={'rigor':'exact computations plus the identity proofs retained with each witness','survivors':list(survivors.values())}
 a.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'fully_GP_consistent_models':len(survivors),'separated':sum(bool(x['separation']) for x in survivors.values()),'pending':sum(not x['separation'] for x in survivors.values())}))
if __name__=='__main__':main()
