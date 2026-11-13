#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
$PY delta_test2.py 7 pool_main.jsonl maxpiece.jsonl > delta7.log 2>&1
