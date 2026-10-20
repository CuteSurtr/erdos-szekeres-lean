#!/bin/bash
export PATH=/opt/bin:$PATH
D=/home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3WAVE1/C03
END=$(date -u -d "2026-10-20 11:12" +%s)
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
while read R; do
  now=$(date +%s); [ $now -ge $END ] && break
  H=$(python3 -c "print(round(($END-$now)/3600,3))")
  echo "=== ROOT $R start $(date -u +%T) H=$H" >> $D/driver.log
  timeout $((END-now)) python3 close_tree.py /opt/work/base.cnf $D/out.jsonl $R --jobs 4 --caps 300,300,600 --cadopts=--sat --split-singles --hours $H >> $D/driver.log 2>&1
  rc=$?
  echo "=== ROOT $R end $(date -u +%T) rc=$rc" >> $D/driver.log
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" <(tail -5 $D/driver.log); then echo STOPPED >> $D/driver.log; break; fi
done < $D/roots.txt
echo "=== ALL DONE $(date -u +%T)" >> $D/driver.log
