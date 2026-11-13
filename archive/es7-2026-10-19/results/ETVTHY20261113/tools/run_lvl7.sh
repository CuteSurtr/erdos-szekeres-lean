#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
$PY delta_strong.py 6 etv757.json pool_hept.jsonl > delta6_strong.log 2>&1
for s in 21 22 23 24; do
  $PY adv_search2.py $s 6 6 adv7s.jsonl pool_hept.jsonl etv757.json
done > adv7s.log 2>&1
