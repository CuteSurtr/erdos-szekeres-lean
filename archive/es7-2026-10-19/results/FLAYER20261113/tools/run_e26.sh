#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
for n in 30 32 34 36; do $PY fls.py 6 6 $n E 26 240 >> e26.log 2>&1; done
