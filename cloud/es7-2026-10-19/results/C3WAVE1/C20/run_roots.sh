#!/bin/bash
# Closes the C20 roots one at a time, in order, until the stop time (epoch seconds in $1).
export PATH=/opt/bin:$PATH
STOP=$1
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C20
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
for ROOT in $(awk '{print $2}' $D/roots.txt); do
  now=$(date +%s); [ $now -ge $STOP ] && break
  H=$(python3 -c "print(round(($STOP-$now)/3600,4))")
  echo "=== $(date -u +%FT%TZ) root $ROOT hours $H" >> $D/driver.log
  python3 close_tree.py /opt/work/base.cnf $D/out.jsonl $ROOT --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $H >> $D/driver.log 2>&1
  echo "=== $(date -u +%FT%TZ) driver exit $? root $ROOT" >> $D/driver.log
  if tail -3 $D/driver.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED"; then echo "=== HALT" >> $D/driver.log; exit 3; fi
done
echo "=== $(date -u +%FT%TZ) runner done" >> $D/driver.log
