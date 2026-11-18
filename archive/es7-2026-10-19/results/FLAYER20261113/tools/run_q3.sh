#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
# (a) abstract witnesses with |E| >= 26 on 30 points, then realization attempts
$PY sample_fl.py 30 1,2,3 samples_E26.jsonl E 26 > q3a.log 2>&1
# (b) real FL(5,5) sets: maximize |E| (conjecture-value 7, abstract maximum 9)
for s in 1 2 3 4; do $PY anneal_ab.py 5 5 E $s 150000 sets_fl55_E.jsonl >> q3b.log 2>&1; done
for s in 1 2; do $PY anneal_ab.py 5 5 EuA $s 150000 sets_fl55_EuA.jsonl >> q3b.log 2>&1; done
# controls of the two certification modes on known cases
$PY cert.py 5 5 15 inj >> q3c.log 2>&1
$PY cert.py 4 6 12 plain >> q3c.log 2>&1
$PY cert.py 4 6 12 inj >> q3c.log 2>&1
