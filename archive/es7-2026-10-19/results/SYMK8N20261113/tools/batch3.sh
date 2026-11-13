#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
L=../sets/lib3
for f in $L/c3_61pts_centre.txt $L/c3_61pts_blowup.txt; do $PY twostep.py 3 $f; done
for f in $L/c3_60pts_nocentre.txt $L/c3_60pts_nocentre_b.txt $L/base60_cost3_minus*.txt; do $PY twostep.py 3 $f; done
for f in $L/c3_61pts_centre.txt $L/c3_61pts_blowup.txt; do
  for r in $(seq 0 19); do $PY twostep.py 3 $f --remove $r --pairs --maxpairs 100000; done
done
