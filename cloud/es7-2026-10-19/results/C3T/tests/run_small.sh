#!/bin/bash
# Small-instance tests of close_node.py and close_tree.py, old (results/C3-S/tools) vs new
# (results/C3T/tools), via tests/small.py.  Output: $W/*.jsonl
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19
W=${1:-/opt/work/small}
mkdir -p $W
OLD=$R/results/C3-S/tools; NEW=$R/results/C3T/tools; S=$R/results/C3T/tests/small.py
part=${2:-node}
if [ $part = node ]; then
  for mk in "5 6" "7 5" "6 6"; do set -- $mk; m=$1; k=$2
    python3 $NEW/gen_case.py $m $k none -o $W/base_m${m}k${k}.cnf > /dev/null
    nodes=$(python3 -c "
import sys; sys.path.insert(0, '$NEW'); import hullcase as h
from hullcase import layers_name as n
print(' '.join(['0s0'] + [n(c) for c in h.tree_children($m, $k, [[(0, 0)]])]))")
    for run in old new new2; do
      T=$NEW; [ $run = old ] && T=$OLD
      rm -f $W/node_m${m}k${k}_$run.jsonl
      python3 $S $T $m $k close_node $W/base_m${m}k${k}.cnf $W/node_m${m}k${k}_$run.jsonl 600 $nodes > /dev/null
    done
  done
else
  # close_tree from the H3 root with a deterministic conflict limit, so the root and some depth-2
  # nodes come back UNKNOWN and are split; then the same tree again with the new tools
  m=7; k=6
  python3 $NEW/gen_case.py $m $k none -o $W/base_tree.cnf > /dev/null
  for run in old new new2; do
    T=$NEW; [ $run = old ] && T=$OLD
    rm -f $W/tree_m${m}k${k}_$run.jsonl
    python3 $S $T $m $k close_tree $W/base_tree.cnf $W/tree_m${m}k${k}_$run.jsonl 0s0 --jobs 1 --caps 600 --cadopts=-c,3000 > /dev/null
  done
fi
