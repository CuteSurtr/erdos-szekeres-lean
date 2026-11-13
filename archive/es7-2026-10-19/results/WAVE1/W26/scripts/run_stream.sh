#!/bin/bash
# run_stream.sh JOBS CASE... : close each case in order with close_march.py until the deadline in /home/user/work/END
J=$1; shift
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/WAVE1/W26
for c in "$@"; do
  H=$(python3 -c "import time;print(max(0,($(cat /home/user/work/END)-time.time())/3600))")
  BIN=/home/user/bin python3 $R/scripts/close_march.py /home/user/work/cnf/$c.cnf $R/$c --depth 7 --timeout 300 \
     --split-depth 6 --jobs $J --whole 60 --hours $H > /home/user/work/$c.out 2>&1
  echo "$c $(tail -1 /home/user/work/$c.out)"
done
