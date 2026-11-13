#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
$PY -c "
import sys,json; sys.path.insert(0,'.')
from etvcon import etv
from pyexact import summary
P=etv(7,5,7); print('ETV757',len(P),summary(P)); json.dump([[x,y] for x,y in sorted(P)],open('etv757.json','w'))
P=etv(6,5,6); print('ETV656',len(P),summary(P)); json.dump([[x,y] for x,y in sorted(P)],open('etv656.json','w'))
"
for s in $(seq 201 240); do
  for m in box para gauss; do
    $PY gen_random.py $s $m 20000 pool_hept.jsonl 4,6,7
  done
done > gen_hept.log 2>&1
$PY delta_test2.py 6 etv757.json pool_hept.jsonl > delta6.log 2>&1
