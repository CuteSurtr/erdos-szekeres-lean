#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
H=$(cat last_vec.json)
$PY -u precompute_static.py 20 20
$PY -u probe_big.py "$H" 18 18 60 4 120
$PY -u probe_big.py "$H" 20 20 40 4 180
