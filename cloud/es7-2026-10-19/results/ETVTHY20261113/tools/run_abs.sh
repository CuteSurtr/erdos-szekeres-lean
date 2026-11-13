#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for n in 32 36 38 40; do
  $PY abstract_conj.py $n sig 6 $((n*100))
done > abstract_conj.log 2>&1
