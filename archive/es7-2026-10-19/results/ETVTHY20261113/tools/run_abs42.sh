#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in 4200 4201 4202 4203; do timeout 900 $PY abstract_conj.py 42 sig 1 $s; done >> abstract_conj.log 2>&1
for s in 4300 4301; do timeout 900 $PY abstract_conj.py 43 sig 1 $s; done >> abstract_conj.log 2>&1
