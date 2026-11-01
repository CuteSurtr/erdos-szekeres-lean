#!/bin/bash
export PATH=/opt/bin:$PATH
K=2
END=1792563909
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | awk -v k=$K '(NR-1)%3==k' | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver[0-9].log; then echo "=== STOP (flag in a driver log)"; break; fi
  H=$(python3 -c "print(round(min(0.5,($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $H"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 1 --caps 300,300,600 --cadopts=--sat --split-singles --hours $H 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
done
echo "=== RUNNER DONE $(date -u +%T)"
