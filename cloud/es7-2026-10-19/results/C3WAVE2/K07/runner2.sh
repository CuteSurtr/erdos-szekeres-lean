#!/bin/bash
# C3WAVE2 K07 runner: 10-minute slice per root (TASK.md step 3)
export PATH=/opt/bin:$PATH
START=1792542191                 # 2026-10-21 00:23:11 UTC
END=$((START + 5400 - 900))      # start + 1.5 h - 15 min
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +${FROM:-2} /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min(0.17, ($END-$NOW)/3600), 3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver.log; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
