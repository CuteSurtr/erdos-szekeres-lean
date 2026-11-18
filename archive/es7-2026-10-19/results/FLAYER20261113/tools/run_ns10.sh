#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY describe_real.py nosplit_sample_real.jsonl > describe_real.log 2>&1
$PY sample56.py 25 1 61 > sample56.log 2>&1
$PY realize_lp.py bfp_control.jsonl 2 1500 lp_control_real.jsonl > realize_lp_control.log 2>&1
timeout 600 $PY realize_lp.py nosplit_sample_real.jsonl 2 1500 lp_known_real.jsonl >> realize_lp_control.log 2>&1
