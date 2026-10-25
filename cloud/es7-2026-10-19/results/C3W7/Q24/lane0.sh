#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792940482
k=0
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | cut -f2 | awk -v k=$k '(NR-1) % 3 == k' | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP"; break; fi
  echo "=== UNIT $U start $(date -u +%T)"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$k.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 3 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct$k.cur 2>&1
  cat /opt/work/ct$k.cur >> /opt/work/full$k.log
  tail -n 1 /opt/work/ct$k.cur
  grep -h "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/ct$k.cur
  echo "=== UNIT $U end $(date -u +%T)"
done
echo "=== LANE DONE $(date -u +%T)"
