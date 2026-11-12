#!/bin/sh
W=${W:-<lb-k9oct-work-dir>}; cd $W/ctrl15   # set W to the work directory
run() { name=$1; shift; cat "$@" > $name.units; $W/tools/withunits.sh BASE15dec.cnf $name.units $name.cnf; sha256sum $name.cnf > $name.sha256
  t0=$(date +%s); timeout 1500 cadical -q $name.cnf > $name.out 2>&1; ec=$?; echo "$name exit $ec seconds $(( $(date +%s) - t0 )) $(grep -m1 '^s ' $name.out)" >> results.txt; rm -f $name.cnf; }
run P5_dec_c0_c8_120_mirror c0.units c8_120pts_15layers_mirror.units
run P6_dec_c0_f_del0_mirror c0.units f_del0_mirror.units
run P7_dec_c0_free c0.units
