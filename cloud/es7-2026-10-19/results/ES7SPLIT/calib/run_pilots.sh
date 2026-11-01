#!/bin/bash
# CPU-accounted re-runs of the k=6 hull calibration and the k=7 hexagonal-hull pilots (sequential, 1 process).
# Expects the CNFs written by gen_hull.py in $WORK/cnf (commands in ../README.md); writes $WORK/logs/pilot_*.
# Environment: WORK (default ./hull_work), PY (default python3), CADICAL (default cadical; 3.0.1 was used).
# (The original run first waited for a separate baseline solve to finish; that wait is omitted here.)
HERE=$(cd "$(dirname "$0")" && pwd)
W=${WORK:-./hull_work}
CAD=${CADICAL:-cadical}
PY=${PY:-python3}
cd $W && mkdir -p logs
run() { # name cnf limit
  /usr/bin/time -p $CAD -q -t $3 $2 > logs/pilot_$1.out 2> logs/pilot_$1.time
  echo "$1: $(grep '^s ' logs/pilot_$1.out || echo 's UNKNOWN') user=$(awk '/^user/ {print $2}' logs/pilot_$1.time)s real=$(awk '/^real/ {print $2}' logs/pilot_$1.time)s"
}
run k6_h5 cnf/hull_N17_K6_h5.cnf 600
run k6_h4 cnf/hull_N17_K6_h4.cnf 600
run k6_h3 cnf/hull_N17_K6_h3.cnf 600
run k7_N32_h6 cnf/hull_N32_K7_h6.cnf 300
if grep -q "^s SATISFIABLE" logs/pilot_k7_N32_h6.out; then echo "  model check: $($PY $HERE/check_hull_model.py 32 logs/pilot_k7_N32_h6.out)"; fi
run k7_N33_h6_mirror cnf/hull_N33_K7_h6_m.cnf 900
