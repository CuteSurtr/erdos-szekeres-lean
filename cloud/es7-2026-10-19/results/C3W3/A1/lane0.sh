#!/bin/bash
export PATH=/opt/bin:$PATH
K=0
END=$(date -u -d '2026-10-21 06:25:01' +%s)
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
while read R; do
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP (flag in a driver log)"; break; fi
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min(0.5, ($END-$NOW)/3600), 3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
done < /opt/work/roots$K.txt
echo "=== RUNNER DONE $(date -u +%T)"
