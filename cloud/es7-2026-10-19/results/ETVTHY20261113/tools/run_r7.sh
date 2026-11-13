#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
$PY - << 'PYEOF'
import json
recs=[json.loads(l) for l in open('maxpiece.jsonl')]
best=sorted((r for r in recs if r['piece']=='R7'), key=lambda r:-r['value'])[:3]
for i,r in enumerate(best): json.dump(r['P'], open(f'r7seed{i}.json','w'))
PYEOF
for s in 1 2 3; do
  $PY maxpiece.py $((s+500)) R7 1500000 maxpiece_r7.jsonl r7seed$((s-1)).json
done > maxpiece_r7.log 2>&1
for s in 4 5; do
  $PY maxpiece.py $((s+500)) R7 1500000 maxpiece_r7.jsonl
done >> maxpiece_r7.log 2>&1
