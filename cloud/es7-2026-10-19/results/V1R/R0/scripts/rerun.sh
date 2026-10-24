#!/bin/bash
L=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/verify/hull_leaves.icnf
awk 'BEGIN{split("0 4 8 64 68 72 384 388 392",a); for(k in a) w[a[k]]=1} ((NR-1) in w) {printf "%d", NR-1; for(k=2;k<NF;k++) printf " %s",$k; print ""}' $L |
  xargs -P 3 -L 1 bash -c '/tmp/claude-0/drv/leaf.sh "$@" > /tmp/claude-0/drv/re_$1.json' _
echo DONE > /tmp/claude-0/drv/refinished
