#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
timeout 900 $PY abstract_recheck.py 40 4001 > abstract_recheck.log 2>&1
./run_certs.sh
for s in 4100 4101 4102; do timeout 600 $PY abstract_conj.py 41 sig 1 $s; done >> abstract_conj.log 2>&1
