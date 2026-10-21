#!/bin/bash
# C3WAVE2 K01 runner: one fixed slice per root; run as: setsid nohup runner.sh >> /opt/work/driver.log 2>&1
export PATH=/opt/bin:$PATH
START=1792542147                      # 2026-10-21 00:22:27 UTC
END=$((START + 5400 - 900))           # start + 1.5 h - 15 min
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min(0.17, ($END-$NOW)/3600),3))")
  L0=$(wc -l < /opt/work/driver.log)
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if tail -n +$((L0+1)) /opt/work/driver.log | grep -q "SAT FOUND\|PROOF NOT ACCEPTED"; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
