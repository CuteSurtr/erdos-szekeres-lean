#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
timeout 300 $PY realize_small.py pairs.jsonl pairs_real.jsonl 100000 30000 2 > pairs_real.log 2>&1
for n in 6 8 10 11 12 13 14; do $PY cegar_split.py 5 5 $n >> cegar55.log 2>&1; done
$PY gen2.py 31 1200000 pE - "f[0]==4" 0.4 > q5_pE.log 2>&1
