#!/bin/bash
# random exact soundness tests of the encoders (audit A4); one process at a time
cd "$(dirname "$0")"
V=${PY:-python3}
run() { $V test_encoders.py "$@" > logs/rand_m$1_N$2_$3_s$6.log 2>&1; grep SUMMARY logs/rand_m$1_N$2_$3_s$6.log; }
run 5 10 L 30 30 11
run 4 8 L 30 30 12
run 5 15 L 40 40 13
run 4 12 L 40 40 14
run 5 10 A 30 30 15
run 5 15 A 30 30 16
run 4 16 L 30 30 17
run 5 20 L 25 25 18
run 5 20 A 15 15 19
run 4 20 L 20 20 20
run 4 24 L 8 12 21
run 5 25 L 8 12 22
run 5 25 A 3 6 23
echo CAMPAIGN DONE
