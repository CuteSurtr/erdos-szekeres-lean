#!/bin/bash
# lane 0 of C3W3 B5: roots at positions = 0 (mod 1) of roots.tsv
export PATH=/opt/bin:$PATH
END=1792567596   # start 04:41:36 + 3 h - 15 min
LOG=/opt/work/driver0.log
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /home/user/erdos-szekeres-lean/cloud/es7-2026-10-19/results/C3W3/B5/roots.tsv | cut -f2 | awk 'NR%1==0' | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min(0.9,($END-$NOW)/3600),3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S"
  python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S 2>&1
  echo "=== ROOT $R end $(date -u +%T)"
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP"; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)"
