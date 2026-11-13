#!/bin/sh
# near-miss surgery: remove one orbit of a 3-fold near miss (63/64 points, 3 octagons) and add one infinitesimal orbit
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
L=../sets/lib3
for f in $L/c3_64pts_3octagons.txt $L/c3_63pts_3octagons_nocentre.txt $L/control_cost3_63pts.txt; do
  for r in $(seq 0 20); do $PY twostep.py 3 $f --remove $r; done
done
