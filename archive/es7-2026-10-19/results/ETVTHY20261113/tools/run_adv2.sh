#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 31 32 33 34 35 36; do
  $PY adv_search2.py $s 7 7 adv8s.jsonl pool_main.jsonl maxpiece.jsonl maxpiece_dr.jsonl etv858.json
done > adv8s.log 2>&1
