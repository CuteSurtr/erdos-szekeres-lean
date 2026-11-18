#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY fls.py 4 6 11 none 0 > sat_small.log 2>&1
$PY fls.py 4 7 16 none 0 >> sat_small.log 2>&1
$PY -c "
import etvcon
from esgeo import quick
P = etvcon.etv(6,5,5); print('etv(6,5,5):', len(P), 'points, (gon, maxcap, maxcup) =', quick(P))
P = etvcon.etv(7,5,6); print('etv(7,5,6):', len(P), 'points, (gon, maxcap, maxcup) =', quick(P))
" >> sat_small.log 2>&1
$PY splitcount.py maximal_5_5_14.json > splitcount.log 2>&1
for n in 1 2 3 4 5 7 9; do $PY cegar_split.py 5 5 $n >> cegar55.log 2>&1; done
for n in 1 2 3 4 5 6 7 8 9 10 11 12 13; do $PY cert_cnf.py cert/split_5_5_$n.cnf 600 >> cert_split.log 2>&1; done
for n in 1 2 3 4 5 6 7; do $PY cegar_split.py 4 5 $n >> cegar45.log 2>&1; done
for n in 1 2 3 4 5 6 7 8 9 10 11; do $PY cegar_split.py 4 6 $n >> cegar46.log 2>&1; done
for n in 8 10 12 13 14; do $PY cegar_split.py 5 5 $n 1000000 weak >> cegar55_weak.log 2>&1; done
$PY cegar_more.py 5 5 14 12 nosplit_more.jsonl 300 > cegar_more.log 2>&1
