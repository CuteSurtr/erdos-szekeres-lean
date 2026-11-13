#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in $(seq 101 130); do
  for m in box para circ gauss; do
    $PY gen_random.py $s $m 20000 pool_main.jsonl
  done
done > gen_pool.log 2>&1
