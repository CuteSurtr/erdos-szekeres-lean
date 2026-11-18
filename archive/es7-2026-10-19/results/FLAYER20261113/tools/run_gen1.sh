#!/bin/bash
# data generation batch 1 (one thread)
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
for s in $(seq 101 130); do $PY gen66.py anneal $s 300000 pool_size.jsonl >> gen1.log 2>&1; done
$PY gen66.py sub64 7 40 pool_sub64.jsonl >> gen1.log 2>&1
