#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 1 2 3 4 5 6; do
  $PY adv_search.py $s 7 6 adv7.jsonl
  $PY adv_search.py $((s+50)) 7 6 adv7.jsonl pool_main.jsonl
done > adv7.log 2>&1
