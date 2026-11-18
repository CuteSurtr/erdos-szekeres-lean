#!/bin/bash
# usage: vxcheck.sh NAME POINTS K [Bfull=1000] [Bneg=300] -> VX2's checker, unchanged binary, full run + negative control (drop point 0)
set -u
B=/home/jay/research/data/roadmap-20261115/pm1115/vx2/vx2sat2; O=/home/jay/research/data/roadmap-20261115/pm1115/sat3/vx
name=$1 f=$2 k=$3 bf=${4:-1000} bn=${5:-300}
{ echo "name $name file $f sha256 $(sha256sum $f | cut -c1-64) K $k vx2sat2_sha256 $(sha256sum $B | cut -c1-64) start $(date '+%F %T %Z')"; } > $O/$name.info
/usr/bin/time -v $B $f $k -1 $bf 1 > $O/final_$name.log 2> $O/final_$name.time
/usr/bin/time -v $B $f $k 0 $bn 1 > $O/neg_$name.log 2> $O/neg_$name.time
echo "end $(date '+%F %T %Z') final: $(grep VERDICT $O/final_$name.log) neg: $(grep VERDICT $O/neg_$name.log)" >> $O/$name.info
