#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
for s in $(seq 801 820); do for m in box para gauss; do $PY gen_random.py $s $m 15000 pool_oct.jsonl 7,7,7 > /dev/null; done; done
for s in $(seq 821 850); do for m in box para gauss; do $PY gen_random.py $s $m 8000 pool_hex.jsonl 7,5,7 > /dev/null; $PY gen_random.py $s $m 10000 pool_hep.jsonl 7,6,7 > /dev/null; done; done
{
$PY split_gen.py 7 pool_oct.jsonl
$PY split_gen.py 6 pool_hep.jsonl
$PY split_gen.py 5 pool_hex.jsonl
} > split_gen.log 2>&1
