#!/bin/sh
# cube-level positive controls at t = 15 (expected SAT)
W=${W:-<lb-k9oct-work-dir>}; cd $W/ctrl15   # set W to the work directory
run() { name=$1; shift; cat "$@" > $name.units; $W/tools/withunits.sh BASE15.cnf $name.units $name.cnf; sha256sum $name.cnf > $name.sha256
  t0=$(date +%s); timeout 1500 cadical -q $name.cnf > $name.out 2>&1; ec=$?; echo "$name exit $ec seconds $(( $(date +%s) - t0 )) $(grep -m1 '^s ' $name.out)" >> results.txt; rm -f $name.cnf; }
: > results.txt
run P1_c14_c8_120 c14.units $W/ctrl/c8_120pts_15layers.units
run P2_c13_blowup3orb c13.units $W/ctrl/c8_120pts_blowup3orb.units
run P3_c14_free c14.units
run P4_c13_free c13.units
