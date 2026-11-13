#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
for r in 0 1 2 3 4 5 6 7 8 9 10; do timeout 900 $PY z5pairs.py ../sets/lib5/c5_56pts_11layers_centre.pts $r; done
