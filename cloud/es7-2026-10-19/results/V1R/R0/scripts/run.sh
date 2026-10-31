#!/bin/bash
# run all leaves i ≡ 0 mod 4, 3 at a time, appending to out.jsonl
OUT=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/V1R/R0/out.jsonl
L=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/verify/hull_leaves.icnf
awk 'NR%4==1 {printf "%d", NR-1; for(k=2;k<NF;k++) printf " %s",$k; print ""}' $L |
  xargs -P 3 -L 1 bash -c '/tmp/claude-0/drv/leaf.sh "$@" >> '"$OUT" _
echo DONE > /tmp/claude-0/drv/finished
