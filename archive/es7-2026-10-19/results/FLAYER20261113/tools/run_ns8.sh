#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY bfp.py split_counterexample_5_5_14.json > bfp.log 2>&1
$PY bfp.py nosplit_more.jsonl >> bfp.log 2>&1
$PY bfp.py bfp_control.jsonl >> bfp.log 2>&1
$PY rank.py > rank.log 2>&1
$PY hall.py > hall.log 2>&1
$PY crosscheck4.py 3 300 > crosscheck4.log 2>&1
$PY cegar_more.py 5 5 14 100000 nosplit_all.jsonl 300 > cegar_all.log 2>&1
