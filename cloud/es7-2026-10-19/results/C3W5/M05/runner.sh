#!/bin/bash
export PATH=/opt/bin:$PATH
END=$((1792858343 + 10800 - 900))
cd /opt/c3u2/cloud/es7-2026-10-19/results/C3U2/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min(1.0, ($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver.log; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
