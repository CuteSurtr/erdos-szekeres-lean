#!/bin/bash
export PATH=/opt/bin:$PATH
K=1
END=1792563909
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
awk -v k=$K '(NR-1)%3==k' /opt/work/roots.txt | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP (other lane)"; break; fi
  S=$(python3 -c "print(round(min(0.5,($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
