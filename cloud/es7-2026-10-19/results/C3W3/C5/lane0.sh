#!/bin/bash
# lane 0 of 1: roots at positions = 0 (mod 1) of roots.tsv
export PATH=/opt/bin:$PATH
K=0; LANES=1
END=$((1792557740 + 6*3600 - 900))
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | awk -v k=$K -v n=$LANES '(NR-1) % n == k' | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP"; break; fi
  S=$(python3 -c "print(round(min(2.0, ($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
