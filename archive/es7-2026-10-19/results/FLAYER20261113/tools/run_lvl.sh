#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY fls.py 6 6 40 EuA 36 200 >> lvl.log 2>&1
$PY fls.py 6 6 38 E 30 200 >> lvl.log 2>&1
$PY fls.py 6 6 44 EuA 40 200 >> lvl.log 2>&1
$PY fls.py 6 6 40 E 33 200 >> lvl.log 2>&1
$PY fls.py 6 6 40 EnA 20 200 >> lvl.log 2>&1
$PY fls.py 6 6 46 none 0 200 >> lvl.log 2>&1
$PY fls.py 6 6 50 none 0 300 >> lvl.log 2>&1
