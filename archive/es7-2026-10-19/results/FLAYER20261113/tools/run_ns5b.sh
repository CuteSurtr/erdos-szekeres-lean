#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
for n in 1 2 3 4 5 6 7; do $PY cegar_split.py 4 5 $n >> cegar45.log 2>&1; done
for n in 1 2 3 4 5 6 7 8 9 10 11; do $PY cegar_split.py 4 6 $n >> cegar46.log 2>&1; done
for n in 1 2 3 4 5 6 7 8 9 10 11; do $PY regen_split_cnf.py 5 5 $n >> regen.log 2>&1; done
$PY describe_cex.py split_counterexample_5_5_14.json > describe_cex.log 2>&1
timeout 240 $PY cegar_split.py 5 5 14 1000000 weak >> cegar55_weak.log 2>&1
$PY cegar_more.py 5 5 14 12 nosplit_more.jsonl 240 > cegar_more.log 2>&1
$PY realize_control.py 6 400000 2 > realize_control.log 2>&1
$PY realize_small.py nosplit_more.jsonl nosplit_more_real.jsonl 12 300000 2 > nosplit_more_real.log 2>&1
