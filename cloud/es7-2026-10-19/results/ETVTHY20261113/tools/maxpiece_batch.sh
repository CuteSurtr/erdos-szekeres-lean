#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 1 2 3 4; do
  for pc in R6 R7 L4 M Y size; do
    $PY maxpiece.py $s $pc 150000 maxpiece.jsonl
    $PY maxpiece.py $((s+100)) $pc 150000 maxpiece.jsonl etv858.json
  done
done > maxpiece.log 2>&1
