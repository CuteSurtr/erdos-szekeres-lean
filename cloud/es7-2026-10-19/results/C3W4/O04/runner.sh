#!/bin/bash
# C3W4 O04 runner: W4_one.tsv rows = 4 (mod 16), slice 2.5 h, END = start + 5 h - 15 min
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
END=1792858570
LOG=/opt/work/driver.log
cd $TOOLS
for R in $(awk -F'\t' 'NR>1{print $2}' /opt/work/roots.tsv); do
  NOW=$(date +%s); LEFT=$((END-NOW))
  [ $LEFT -le 0 ] && { echo "=== END reached before ROOT $R $(date -u)" >> $LOG; break; }
  S=$(python3 -c "print(round(min(2.5, $LEFT/3600), 4))")
  echo "=== ROOT $R start $(date -u) hours=$S" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours $S >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u) rc=$?" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" $LOG; then echo "=== STOP on SAT/PROOF $(date -u)" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u)" >> $LOG
