#!/bin/bash
# runs every (node, method) pair at budget B seconds, node-major; records to /opt/work/records.jsonl
B=${1:-120}
D=$(dirname "$0")
for n in 0s0-1s1_2s1-8s1_6s1-9s0 0s0-1s1_6s0-9s1_5s0-10s1 0s0-1s1_6s1-10s0_2_7s0-9s0 0s0-3s0_4; do
  for m in ref march4 split opt; do
    python3 "$D/c3x.py" /opt/work/base.cnf "$n" "$m" "$B" /opt/work/records.jsonl
  done
done
echo ALLDONE
