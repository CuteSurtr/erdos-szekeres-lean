#!/bin/bash
# lane 0 of C3W3 C6: roots at positions = 0 (mod 1) of roots.tsv, in order
export PATH=/opt/bin:$PATH
END=1792578457
LOG=/opt/work/driver0.log
cd /opt/c3s/cloud/es7-2026-10-19/results/C3-S/tools
tail -n +2 /opt/work/roots.tsv | cut -f2 | awk 'NR % 1 == 0 % 1' | while read R; do
  NOW=$(date +%s); [ $NOW -ge $END ] && break
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log 2>/dev/null; then echo "=== STOP" >> $LOG; break; fi
  S=$(python3 -c "print(round(min(2.0, ($END-$NOW)/3600), 3))")
  echo "=== ROOT $R start $(date -u +%T) hours $S" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl $R --jobs 3 --caps 300,300,600 --cadopts=--sat --split-singles --hours $S >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u +%T)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" /opt/work/driver*.log; then echo "=== STOP" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u +%T)" >> $LOG
