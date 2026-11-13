#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 1 2 3 4 5 6; do $PY adv_a4.py $s 6; done > adv_a4.log 2>&1
