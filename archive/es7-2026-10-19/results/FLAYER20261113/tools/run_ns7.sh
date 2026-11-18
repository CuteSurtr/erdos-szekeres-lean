#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
for n in 1 2 3 4 5 6 7 8 9 10 11 12 13 14; do $PY regen_split_cnf.py 5 5 $n weak >> regen_weak.log 2>&1; done
for s in 21 22 23 24 25 26 27 28; do $PY real_nosplit_anneal.py $s 150000 real_nosplit_5_5_14.json - 0.5 >> ns7.log 2>&1; [ -s real_nosplit_5_5_14.json ] && break; done
