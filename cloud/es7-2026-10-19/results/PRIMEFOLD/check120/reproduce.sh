#!/bin/bash
# Reproduce the independent check of the 8-fold sets of 104, 112 and 120 points.
# All code in this directory was written from scratch; nothing in producer/ is executed.
set -eu
OUT=$(cd "$(dirname "$0")" && pwd)
C=$OUT/../sets/k9
${CC:-cc} -O2 ${CFLAGS:-} -o $OUT/cvxcount $OUT/cvxcount.c
${CC:-cc} -O2 ${CFLAGS:-} -o $OUT/bf $OUT/bf.c
${CC:-cc} -O2 ${CFLAGS:-} -o $OUT/cvxenum $OUT/cvxenum.c
# 0. primitive unit tests (exact orientation vs float, exact rotation, exact sign of A+B*sqrt2)
python3 -I $OUT/test_prims.py $OUT
for T in c8_120pts_15layers c8_112pts_14layers c8_104pts_13layers; do
  # 1. exact geometry: orbit structure, distinctness, invariance, two exact orientation methods,
  #    radii, nesting, exact (y,x)/(x,y) orders; writes $T.myotab and $T.orders
  python3 -I $OUT/exact_geom.py $C/$T.pts $OUT $T > $OUT/$T.geom.json
  # 2. two DPs (lowest-anchor angular DP; cap+cup DP), k = 3..10
  $OUT/cvxcount $OUT/$T.myotab $OUT/$T.orders 10 > $OUT/$T.cvx.txt
done
# 3. validation of the DPs and of the enumerator against brute force
python3 -I $OUT/test_dp.py $OUT $OUT/c8_120pts_15layers.myotab $OUT/c8_120pts_15layers.orders 160 120 > $OUT/test_dp.log
python3 -I $OUT/test_enum.py $OUT > $OUT/test_enum.log
# 4. third method: exhaustive enumeration of all convex subsets of the 120-point set (several minutes)
$OUT/cvxenum $OUT/c8_120pts_15layers.myotab 10 > $OUT/c8_120pts_15layers.enum10.txt
cat $OUT/*.cvx.txt $OUT/test_dp.log $OUT/test_enum.log $OUT/c8_120pts_15layers.enum10.txt
