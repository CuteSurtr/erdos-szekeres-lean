#!/bin/bash
# leaves.icnf covers shard s of k  <=>  leaves.icnf + (top cubes not in the shard) cover everything,
# since the top cubes are a partition (march_cu output, checked by covercheck on top.icnf alone).
# usage: shard_cover.sh DIR S K
D=$1; S=$2; K=$3; HERE=$(cd "$(dirname "$0")" && pwd); CC=$HERE/../../../Mii-S/scripts/covercheck.py
echo "top alone: $(python3 $CC $D/top.icnf)"
grep '^a' $D/top.icnf | awk -v s=$S -v k=$K '(NR-1)%k!=s' > $D/.others.icnf
echo "leaves+others: $(python3 $CC $D/leaves.icnf $D/.others.icnf)"
echo "others alone (must be NOT COVERED): $(python3 $CC $D/.others.icnf)"
rm -f $D/.others.icnf
