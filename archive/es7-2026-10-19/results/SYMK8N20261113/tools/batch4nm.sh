#!/bin/sh
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
cd /home/jay/research/data/symk8-20261113/tools
L=../sets/lib4
$PY needle_test.py 1 || true
# (1) new scale level at every block position, all 15 known 52-point sets, blocks = free cuts (exact, complete arcs)
while read f cuts; do
  nb=$(echo "$cuts" | awk -F, '{print NF+1}'); [ -z "$cuts" ] && nb=1
  for pos in $(seq 0 $nb); do $PY addon_exact.py 4 $f "$cuts" $pos | tail -1; done
done << 'LIST'
../sets/lib4/es8sym_52.pts 1,12
../sets/lib4/s13_19_10_S40.pts 10,12
../sets/lib4/s13_2_67_S40.pts 10,12
../sets/lib4/s13_27_30_S40.pts 10,12
../sets/lib4/s13_29_65_S50.pts 1,10,12
../sets/lib4/s13_33_230_S40.pts 10,12
../sets/lib4/s13_43_32_S40.pts 1,10,12
../sets/lib4/s13_45_74_S40.pts 1,10,12
../sets/lib4/s13_46_30_S40.pts 10,12
../sets/lib4/s13_47_100_S40.pts 10,12
../sets/lib4/s13_54_145_S40.pts 10,12
../sets/lib4/s13_60_156_S50.pts 1,10,12
../sets/lib4/s13_74_127_l1point_S50.pts 1,10,12
../sets/lib4/s13_78_210_S50.pts 10,12
../sets/lib4/s13_79_39_l1point_S50.pts 1,10,12
LIST
# (2) near misses: remove one layer of each twin pair (12 layers, octagon-free), then all pairs of infinitesimal orbits
for r in 10,12 10,13 11,12 11,13; do $PY twostep.py 4 $L/c4_56pts_2octagons_A.pts --remove $r --pairs --maxpairs 300000; done
for r in 7,12 7,13 8,12 8,13; do $PY twostep.py 4 $L/c4_56pts_2octagons_B.pts --remove $r --pairs --maxpairs 300000; done
