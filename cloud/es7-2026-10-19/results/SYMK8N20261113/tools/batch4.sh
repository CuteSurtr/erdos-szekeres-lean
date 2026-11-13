#!/bin/sh
# usage: batch4.sh LISTFILE START END LOG
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
sed -n "$2,$3p" $1 | while read f; do
  $PY twostep.py 4 $f
  for r in 0 1 2 3 4 5 6 7 8 9 10 11 12; do
    $PY twostep.py 4 $f --remove $r --pairs --maxpairs 200000
  done
done
