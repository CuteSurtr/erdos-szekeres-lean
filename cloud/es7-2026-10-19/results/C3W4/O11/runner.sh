#!/bin/bash
# C3W4 O11 runner: one close_tree.py per root, in order, slice min(2.5, hours left before END)
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
END=$(cat /opt/work/END)
LOG=/opt/work/driver.log
cd $TOOLS
for R in $(awk -F'\t' 'NR>1 {print $2}' /opt/work/roots.tsv); do
  LEFT=$((END - $(date +%s)))
  [ $LEFT -le 0 ] && { echo "=== END reached before ROOT $R" >> $LOG; break; }
  S=$(python3 -c "print(min(2.5, $LEFT/3600))")
  echo "=== ROOT $R start $(date -u +%FT%TZ) hours $S" >> $LOG
  python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours $S >> $LOG 2>&1; RC=$?
  echo "=== ROOT $R end $(date -u +%FT%TZ) rc $RC" >> $LOG
  if grep -qE 'SAT FOUND|PROOF NOT ACCEPTED' $LOG; then echo "=== STOP" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> $LOG
