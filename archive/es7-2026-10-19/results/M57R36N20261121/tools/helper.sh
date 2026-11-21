#!/bin/bash
# helper.sh: (1) every 60 s move newly queued jobs of the old drivers to drive2.py (handoff.py), until 14:35 KST;
# (2) when the monolithic case-B run exits with 20, run cake_lpr on its proof (heap 9000 MB) and, on the exact
# line 's VERIFIED UNSAT', stop new case-B cubes in drive2.py (cubes2/SKIP_CASES).
cd "$(dirname "$0")"
mono_done=0
while :; do
  now=$(date +%s)
  if [ "$now" -lt 1795239300 ]; then python3 -B handoff.py >> cubes2/handoff.log 2>&1; fi
  if [ $mono_done -eq 0 ] && grep -q '^exit=' run/c36_tle22.out; then
    mono_done=1
    rc=$(grep '^exit=' run/c36_tle22.out | sed 's/^exit=\([0-9]*\).*/\1/')
    echo "mono exit $rc at $(date '+%H:%M:%S')" >> cubes2/helper.log
    if [ "$rc" = 20 ]; then
      { echo "cake_lpr heap=9000MB start $(date)"; shasum -a 256 run/c36_tle22.cnf run/c36_tle22.lrat; ls -l run/c36_tle22.lrat | awk '{print "lrat_bytes="$5}'; } > run/c36_tle22.cake.meta
      t1=$(date +%s)
      nice -n 5 bin/cake_lpr --CML_HEAP_SIZE=9000 --CML_STACK_SIZE=200 run/c36_tle22.cnf run/c36_tle22.lrat > run/c36_tle22.cake 2>&1
      echo "cake_exit=$? cake_wall=$(( $(date +%s) - t1 )) end $(date)" >> run/c36_tle22.cake.meta
      if grep -qx 's VERIFIED UNSAT' run/c36_tle22.cake; then echo B > cubes2/SKIP_CASES; echo "mono VERIFIED; B cubes skipped from $(date '+%H:%M:%S')" >> cubes2/helper.log; else echo "mono cake NOT verified" >> cubes2/helper.log; fi
    fi
  fi
  [ "$now" -ge 1795240800 ] && break
  sleep 60
done
