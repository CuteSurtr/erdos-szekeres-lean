#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
$PY crosscheck.py > ../logs/crosscheck.txt 2>&1
$PY hier_all.py 4 8 6 > ../logs/hier_all.txt 2>&1
$PY hier_all.py 4 7 5 >> ../logs/hier_all.txt 2>&1
$PY hier_all.py 4 6 4 >> ../logs/hier_all.txt 2>&1
./batch_beam2.sh > ../logs/beam2.log 2>&1
