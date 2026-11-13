#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
timeout 900 $PY abstract_recheck.py 42 4200 > abstract_recheck42.log 2>&1
timeout 1200 $PY min_l4.py etv858.json pool_main.jsonl maxpiece.jsonl > min_l4.log 2>&1
