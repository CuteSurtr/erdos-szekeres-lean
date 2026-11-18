#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
for n in 1 2 3 4 5 6 7 8 9 10 11 12 13; do $PY cegar_split.py 5 5 $n 1000000 weak >> cegar55_weak.log 2>&1; done
$PY regen_split_cnf.py 5 5 12 >> regen.log 2>&1
$PY regen_split_cnf.py 5 5 13 >> regen.log 2>&1
$PY cert_cnf.py cert/split_5_5_12.cnf 300 >> cert_split.log 2>&1
$PY cert_cnf.py cert/split_5_5_13.cnf 400 >> cert_split.log 2>&1
for s in 21 22 23 24 25 26; do $PY real_nosplit_anneal.py $s 150000 real_nosplit_5_5_14.json - 0.5 >> ns6.log 2>&1; [ -s real_nosplit_5_5_14.json ] && break; done
