#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
L=../sets/lib4
$PY arch.py $L/*.pts > ../logs/arch.txt 2>&1
# Problem B: strict needle (10-orbit ES profile) + infinitesimal moves (twins, outer/inner levels), with/without centre
timeout 900 $PY beam_inf.py 3 NEEDLE --beam 10 --depth 12
timeout 900 $PY beam_inf.py 3 NEEDLE --add-centre --beam 10 --depth 12
# Problem A: beams from un-doubled cores of the twin-rich calibration sets (target 14 layers)
timeout 1200 $PY beam_inf.py 4 $L/s13_29_65_S50.pts --remove 2,4,6,8 --beam 12 --depth 5
timeout 900 $PY beam_inf.py 4 $L/s13_78_210_S50.pts --remove 2,4,8 --beam 12 --depth 4
# hierarchical (scale-separated) 3-fold, K = 8
timeout 900 $PY hier_dfs.py 3 --K 8 --maxdepth 40
timeout 600 $PY hier_dfs.py 3 --K 8 --centre --maxdepth 40
