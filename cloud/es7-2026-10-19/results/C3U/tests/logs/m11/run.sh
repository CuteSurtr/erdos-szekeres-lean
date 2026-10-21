#!/bin/bash
T=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3U/tools
for N in 0s0-1s1_2s0-9s0 0s0-1s1_3s0-10s0; do
  echo "=== $N start $(date -u +%FT%TZ)"
  python3 $T/close_tree.py /opt/work/base.cnf /opt/work/m11/tree_$N.jsonl $N --sigma-split 3 --caps 1,300,300 --jobs 2 --cadopts=--sat
  echo "=== $N end $(date -u +%FT%TZ)"
done
echo DONE
