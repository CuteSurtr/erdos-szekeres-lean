#!/bin/bash
# lane 0 of 1 (C3W3 B7): roots at positions = 0 (mod 1) of roots.tsv
export PATH=/opt/bin:$PATH
K=0; SLICE=0.9
END=1792567588   # start 04:41:28 UTC + 3 h - 15 min = 07:26:28 UTC
LOG=/opt/work/driver$K.log
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | awk -v k=$K -v n=1 '(NR-1)%n==k' | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  S=$(python3 -c "print(round(min($SLICE, ($END-$NOW)/3600), 3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out$K.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u +%T)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)" >> $LOG
