#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
for s in 21 22 23; do $PY gen2.py $s 500000 pE - "f[0]==4" >> gen3.log 2>&1; done
for s in 24 25; do $PY gen2.py $s 500000 pX - "f[0]==4 and f[3]>=1" >> gen3.log 2>&1; done
for s in 26 27 28; do $PY gen2.py $s 800000 psize - size >> gen3.log 2>&1; done
