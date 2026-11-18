#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/flayer-20261113
$PY cert.py 4 7 17 plain 150 > q4a.log 2>&1
$PY cert.py 4 7 17 inj 150 >> q4a.log 2>&1
