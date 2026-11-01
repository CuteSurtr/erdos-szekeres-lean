#!/bin/bash
# C3W3 C15 lane 0: roots at positions = 0 (mod 1) of roots.tsv, in order
export PATH=/opt/bin:$PATH
K=0
END=$(( 1792557823 + 6*3600 - 15*60 ))   # start 2026-10-21 04:43:43 UTC + 6 h - 15 min
LOG=/opt/work/driver$K.log
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
cut -f2 /opt/work/roots$K.tsv | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min(2.0, ($END-$NOW)/3600), 3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u +%T)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)" >> $LOG
