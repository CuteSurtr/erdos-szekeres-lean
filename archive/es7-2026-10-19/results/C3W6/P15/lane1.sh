#!/bin/bash
export PATH=/opt/bin:$PATH
END=1792921573
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/units.tsv | cut -f2 | awk 'NR%3==2' | while read U; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if cat /opt/work/driver*.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED"; then echo "=== STOP"; break; fi
  echo "=== UNIT $U start $(date -u +%T)"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out1.jsonl $U --jobs 1 --sigma-split 3 --sigma-levels 2 --caps 900,600 --cadopts=--sat --hours 0.02 > /opt/work/ct1.cur 2>&1
  cat /opt/work/ct1.cur >> /opt/work/ct1.full
  grep -E "SAT FOUND|PROOF NOT ACCEPTED" /opt/work/ct1.cur
  echo "last: $(tail -1 /opt/work/ct1.cur)"
  echo "=== UNIT $U end $(date -u +%T)"
done
echo "=== LANE DONE $(date -u +%T)"
