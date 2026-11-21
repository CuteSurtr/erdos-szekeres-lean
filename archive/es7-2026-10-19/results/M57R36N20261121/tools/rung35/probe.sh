#!/bin/bash
# probe.sh -- at most 120 s per CNF, one at a time, nice -n 15, no proof output.
cd "$(dirname "$0")"
CAD=SCRATCH/r36/bin/cadical
R36=SCRATCH/r36/run
for spec in "c35_rle12_qle12:run/c35_rle12_qle12.cnf" "c35_rle12_ule22:run/c35_rle12_ule22.cnf" \
            "c35_tle22_qle12:run/c35_tle22_qle12.cnf" "c35_tle22_ule22:run/c35_tle22_ule22.cnf" \
            "c35_full:run/c35_full.cnf" "c36_rle13(r36,read-only):$R36/c36_rle13.cnf" "c36_tle22(r36,read-only):$R36/c36_tle22.cnf"; do
  name=${spec%%:*}; cnf=${spec#*:}; tag=${name%%(*}
  [ -f probe/STOP ] && break
  echo "start $name $(date +%T) load=$(uptime | awk -F'load averages: ' '{print $2}')" >> probe/probe.log
  nice -n 15 $CAD -t 120 "$cnf" > probe/$tag.log 2>&1
  ec=$?
  conf=$(grep -E '^c conflicts:' probe/$tag.log | awk '{print $3}')
  ptime=$(grep -E 'total process time since initialization' probe/$tag.log | awk '{print $(NF-1)}')
  rtime=$(grep -E 'total real time since initialization' probe/$tag.log | awk '{print $(NF-1)}')
  st=$(grep -E '^s ' probe/$tag.log | head -1)
  echo "done $name exit=$ec [$st] conflicts=$conf process_s=$ptime real_s=$rtime $(date +%T)" >> probe/probe.log
done
echo "ALL PROBES DONE $(date +%T)" >> probe/probe.log
