#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
H="[12, 13, 22, 25, 29, 38, 39, 41, 42, 44, 45, 53, 54, 56, 66, 67, 68, 69]"
$PY -u probe_big.py "$H" 18 18 120 4 120
$PY -u probe_big.py "$H" 20 20 80 4 180
