#!/bin/bash
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/etvthy-20261113
D=/home/jay/research/lean/erdos-szekeres-lean/experiments/es8-lower-bound-search-2026-10-11
$PY split2.py $D/saturation/witness8.txt $D/family/sets/*.txt > split2.log 2>&1
