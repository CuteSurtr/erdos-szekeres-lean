#!/bin/sh
# beams from bases with the bottom block removed (explores twin + nested-level combinations not covered by twostep)
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
L=../sets/lib4
timeout 600 $PY beam_inf.py 4 $L/es8sym_52.pts --remove 12 --beam 12 --depth 2
timeout 600 $PY beam_inf.py 4 $L/es8sym_52.pts --remove 0,12 --beam 12 --depth 3
timeout 900 $PY beam_inf.py 4 $L/s13_29_65_S50.pts --remove 10,11,12 --beam 12 --depth 4
timeout 900 $PY beam_inf.py 4 $L/s13_19_10_S40.pts --remove 10,11,12 --beam 12 --depth 4
timeout 900 $PY beam_inf.py 4 $L/c4_56pts_2octagons_B.pts --remove 5,6,7,8,9,10,11,12,13 --beam 12 --depth 9
