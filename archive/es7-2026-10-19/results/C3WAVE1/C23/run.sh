#!/bin/bash
R=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C23
END=$(( 1792481758 + 4*3600 - 25*60 ))
JOBS=${JOBS:-3}
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
for root in $(awk '{print $2}' $R/roots.txt); do
  now=$(date +%s); left=$(( END - now ))
  [ $left -le 60 ] && { echo "TIME UP before $root" >> /opt/work/driver.log; break; }
  H=$(python3 -c "print(round($left/3600,4))")
  echo "=== ROOT $root start $(date -u +%T) H=$H" >> /opt/work/driver.log
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $root --jobs $JOBS --caps 300,300,600 --cadopts=--sat --split-singles --hours $H >> /opt/work/driver.log 2>&1
  echo "=== ROOT $root end $(date -u +%T) rc=$?" >> /opt/work/driver.log
  if tail -5 /opt/work/driver.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED\|Traceback"; then echo HALT >> /opt/work/driver.log; break; fi
done
echo RUNNER DONE >> /opt/work/driver.log
