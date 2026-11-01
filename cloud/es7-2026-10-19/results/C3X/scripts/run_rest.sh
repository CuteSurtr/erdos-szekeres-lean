#!/bin/bash
# second runner (after reprioritising for time): waits for the running c3x.py, then the remaining pairs
D=$(dirname "$0")
while pgrep -f "c3x.py /opt/work/base.cnf" >/dev/null; do sleep 5; done
for nm in "0s0-1s1_2s1-8s1_6s1-9s0 opt" "0s0-1s1_6s0-9s1_5s0-10s1 ref" "0s0-1s1_6s0-9s1_5s0-10s1 opt" "0s0-1s1_6s0-9s1_5s0-10s1 march2" \
          "0s0-1s1_6s1-10s0_2_7s0-9s0 ref" "0s0-1s1_6s1-10s0_2_7s0-9s0 opt" "0s0-3s0_4 opt" "0s0-1s1_6s0-9s1_5s0-10s1 split"; do
  set -- $nm
  python3 "$D/c3x.py" /opt/work/base.cnf "$1" "$2" 120 /opt/work/records.jsonl
done
echo ALLDONE
