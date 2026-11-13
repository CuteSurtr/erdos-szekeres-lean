#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
for K in 6 7 8; do $PY hier_dfs.py 4 --K $K --maxdepth 20 | grep -E "^DONE|^example"; done
for K in 6 7; do $PY hier_dfs.py 3 --K $K --maxdepth 30 | grep -E "^DONE|^example"; $PY hier_dfs.py 3 --K $K --centre --maxdepth 30 | grep -E "^DONE|^example"; done
$PY hier_all.py 4 8 6
$PY arch3.py ../sets/lib3/*.txt
