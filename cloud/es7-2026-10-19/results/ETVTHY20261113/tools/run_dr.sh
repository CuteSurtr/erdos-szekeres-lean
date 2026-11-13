#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 1 2 3 4 5 6; do
  $PY maxpiece.py $s DR 300000 maxpiece_dr.jsonl
  $PY maxpiece.py $((s+100)) DR 300000 maxpiece_dr.jsonl etv858.json
  $PY maxpiece.py $((s+200)) DRL4 200000 maxpiece_dr.jsonl
done > maxpiece_dr.log 2>&1
