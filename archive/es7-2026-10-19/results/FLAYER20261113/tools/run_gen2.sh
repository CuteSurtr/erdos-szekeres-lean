#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY sub64.py 7 12 pool_sub64.jsonl >> gen2.log 2>&1
# size-preserving walks from the ETV 50-point set (moves only matter; adds are rarely valid)
for s in 1 2; do $PY gen2.py $s 150000 etvwalk etv668.json size 0.05 44 >> gen2.log 2>&1; done
# targeted pieces from scratch
$PY gen2.py 11 120000 pX - "f[0]==4 and f[3]>=1" >> gen2.log 2>&1
$PY gen2.py 12 120000 pE - "f[0]==4" >> gen2.log 2>&1
$PY gen2.py 13 120000 pEuA - "f[0]==4 or f[3]>=1" >> gen2.log 2>&1
$PY gen2.py 14 120000 pZ - "f[0]<=3 and f[3]==0" >> gen2.log 2>&1
