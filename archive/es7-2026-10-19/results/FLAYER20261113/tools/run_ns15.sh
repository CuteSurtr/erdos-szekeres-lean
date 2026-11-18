#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY - <<'PYEOF' > ns15_extract.log 2>&1
import json
best = None
for line in open('sets_pE.jsonl'):
    r = json.loads(line)
    if best is None or r['value'] > best['value']: best = r
json.dump(best['P'], open('init_Ebest.json', 'w')); print('best E set: value', best['value'], 'n', len(best['P']), 'seed', best['seed'])
PYEOF
$PY verify_levels.py init_Ebest.json init_E31.json > verify_levels.log 2>&1
$PY gen2.py 61 1300000 pEuA init_Ebest.json "f[0]==4 or f[3]>=1" 0.7 > ns15.log 2>&1
