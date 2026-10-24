#!/bin/bash
# C3U2 copy of results/C3U/tests/restart_test.sh: T points to results/C3U2/tools
# close_tree restart with sigma splits: cut a finished sig_* run after N lines, run close_tree again
# on the cut file with the same options, and check the result with check_small.py.
# usage: restart_test.sh W m k c K N
W=$1; m=$2; k=$3; c=$4; K=$5; N=$6
T=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3U2/tools; H=$(dirname $(readlink -f $0))
src=$W/sig_m${m}k${k}c${c}K${K}.jsonl; dst=$W/restart_m${m}k${k}c${c}K${K}_N$N.jsonl
head -n $N $src > $dst
C3U_WORK=$W/wk_restart python3 $H/small.py $T $m $k close_tree $W/base_m${m}k${k}.cnf $dst 0s0 --jobs 2 --caps 600 --cadopts=-c,$c --sigma-split $K > $dst.log 2>&1
echo "restart from $N of $(wc -l < $src) lines: rc $? -> $(wc -l < $dst) lines; $(tail -1 $dst.log)"
python3 $H/check_small.py $T $m $k $W/base_m${m}k${k}.cnf $dst
