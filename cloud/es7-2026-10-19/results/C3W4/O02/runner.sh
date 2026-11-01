#!/bin/bash
# C3W4 O02 runner: one close_tree.py run per root, in order, until END
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
END=1792858587
SLICE=2.5
LOG=/opt/work/driver.log
cd $TOOLS
for R in $(awk -F'\t' 'NR>1{print $2}' /opt/work/roots.tsv); do
  LEFT=$((END - $(date +%s)))
  [ $LEFT -le 0 ] && { echo "=== END reached before ROOT $R $(date -u +%FT%TZ)" >> $LOG; break; }
  S=$(python3 -c "print(round(min($SLICE, $LEFT/3600), 4))")
  echo "=== ROOT $R start $(date -u +%FT%TZ) hours=$S" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours $S >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u +%FT%TZ) rc=$?" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" $LOG; then echo "=== STOP $(date -u +%FT%TZ)" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> $LOG
