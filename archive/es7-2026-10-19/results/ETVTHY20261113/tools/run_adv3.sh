#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 51 52 53 54 55 56; do
  $PY adv_search3.py $s 8 adv8h.jsonl pool_main.jsonl maxpiece.jsonl maxpiece_dr.jsonl
done > adv8h.log 2>&1
