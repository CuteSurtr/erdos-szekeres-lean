#!/bin/sh
# usage: exact_check.sh SET.pts OUTDIR K   -- exact checks of an 8-fold set (all exact; floats not used)
#  1. label8.py: orbit structure (row 8o+k = zeta^k row 8o), distinct points, strictly decreasing radii, exact
#     orientation of every triple-orbit representative (Z[sqrt2]) nonzero, exact labelling for the encoder
#  2. exact_geom.py (PRIMEFOLD/check120, independent): two exact orientation methods on all triples, table + orders
#  3. cvxcount: two DPs (lowest anchor; cap+cup), convex k-gons for k = 3..K
#  4. verify_cfg.py --pts (PRIMEFOLD producer: methods A/B/C) + cvx2 (two more DPs)
set -e
T=$(cd "$(dirname "$0")" && pwd)
P=$1; O=$2; K=${3:-10}; B=$(basename $P .pts)
mkdir -p $O
python3 $T/label8.py $P $O/$B.label.json
python3 -I $T/check/exact_geom.py $P $O $B > $O/$B.geom.json
$T/check/cvxcount $O/$B.myotab $O/$B.orders $K > $O/$B.cvxcount.txt
cat $O/$B.cvxcount.txt
(cd $O && python3 -I $T/check/verify_cfg.py --pts $P 8 0 9 $B.vc > $B.vc.log 2>&1; tail -n 6 $B.vc.log; $T/check/cvx2 $B.vc 9 | tail -n 6)
sha256sum $P
