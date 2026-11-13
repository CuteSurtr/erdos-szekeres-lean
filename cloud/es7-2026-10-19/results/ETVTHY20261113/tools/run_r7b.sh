#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 601 602 603 604 605 606 607 608; do
  $PY maxpiece.py $s R7 3000000 maxpiece_r7.jsonl r7seed20.json
done > maxpiece_r7b.log 2>&1
