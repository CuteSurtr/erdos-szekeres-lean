import argparse
import hashlib
import json
from pathlib import Path

ap=argparse.ArgumentParser();ap.add_argument('--full-run',type=Path,required=True);ap.add_argument('--cup-root',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args()
args.out.mkdir(parents=True,exist_ok=False)
records=[{'name':'relation-control','n':7,'P':[[0,0],[10,0],[20,13],[30,1],[40,40],[50,100]],'source':'user supplied raw relation control'}]
for source,name in [(args.cup_root/'known-v1/cases/known18/input.json','known18'),(args.cup_root/'real15-v1/cup/input.json','real15')]:
 r=json.loads(source.read_text());r.update(name=name,source_input=str(source),source_input_sha256=hashlib.sha256(source.read_bytes()).hexdigest());records.append(r)
records.extend(json.loads((args.full_run/'inputs.json').read_text()))
(args.out/'inputs.json').write_text(json.dumps(records,indent=2)+'\n')
with (args.out/'input.txt').open('x') as f:
 f.write(f'CUPCOMPARE1 {len(records)}\n')
 for r in records:
  f.write(f'{r["name"]} {r["n"]} {len(r["P"])}\n')
  for x,y in r['P']:f.write(f'{x} {y}\n')
print(json.dumps({'inputs':len(records),'geometry_scope':317,'relation_control':1}))
