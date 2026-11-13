#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
for f in ../sets/lib3/c3_61pts_centre.txt ../sets/lib3/c3_61pts_blowup.txt ../sets/lib3/c3_60pts_nocentre.txt ../sets/lib3/c3_60pts_nocentre_b.txt ../sets/lib3/base60_cost3_minus*.txt; do
  $PY double_exact.py 3 $f all
  case $f in *60pts*|*base60*) $PY double_exact.py 3 $f all --add-centre ;; esac
done
