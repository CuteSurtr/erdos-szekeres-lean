#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY cert.py 5 5 15 plain >> q2.log 2>&1
$PY cert.py 4 5 8 plain >> q2.log 2>&1
$PY cert.py 4 4 5 plain >> q2.log 2>&1
$PY fls.py 6 6 51 none 0 420 >> q2.log 2>&1
$PY fls.py 6 6 56 none 0 300 >> q2.log 2>&1
