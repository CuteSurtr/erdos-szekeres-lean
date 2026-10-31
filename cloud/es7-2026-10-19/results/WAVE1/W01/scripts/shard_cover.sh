#!/bin/bash
# Coverage of shard part by its cake_lpr-verified leaves, with results/Mii-S/scripts/covercheck.py:
#  (1) per top cube c of the shard: leaves extending c, with c's literals removed, must be COVERED;
#  (2) whole case: leaves.icnf + the top cubes of the other shards must be COVERED.
# usage: shard_cover.sh DIR SHARD NSHARDS   (DIR has top.icnf and leaves.icnf)
D=$1; S=$2; K=$3; CC=$(dirname "$0")/../../../Mii-S/scripts/covercheck.py; T=$(mktemp -d)
awk -v s=$S -v k=$K '(NR-1)%k==s' $D/top.icnf > $T/mine
awk -v s=$S -v k=$K '(NR-1)%k!=s' $D/top.icnf > $T/others
i=0; while read -r line; do
  c=$(echo "$line" | sed 's/^a //; s/ 0$//')
  python3 - "$c" $D/leaves.icnf > $T/sub <<'PY'
import sys
c=list(map(int,sys.argv[1].split())); n=len(c)
for l in open(sys.argv[2]):
    x=list(map(int,l.split()[1:-1]))
    if x[:n]==c: print("a "+" ".join(map(str,x[n:]+[0])))
PY
  echo "top[$((i*K+S))] $(python3 $CC $T/sub)"; i=$((i+1))
done < $T/mine
echo "whole-case (leaves + other shards' top cubes): $(python3 $CC $D/leaves.icnf $T/others)"
rm -rf $T
