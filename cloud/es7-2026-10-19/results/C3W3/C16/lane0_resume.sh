#!/bin/bash
export PATH=/opt/bin:$PATH
K=0
FIRSTEND=$(date -u -d '2026-10-21 06:44:48' +%s)
END=$(date -u -d '2026-10-21 10:27:53' +%s)
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
while read R; do
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP (flag in a driver log)"; break; fi
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min(2.0, ($END-$NOW)/3600), 3))"); [ "$R" = 0s0-2s1_1s0-8s0 ] && S=$(python3 -c "print(round(min(($FIRSTEND-$NOW)/3600, ($END-$NOW)/3600), 3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
done < /opt/work/roots$K.txt
echo "=== RUNNER DONE $(date -u +%T)"
