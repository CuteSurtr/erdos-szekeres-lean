#!/bin/bash
# C3W4 H16 runner: one close_tree.py run per root, in order, until END
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
END=$(cat /opt/work/end_epoch)
LOG=/opt/work/driver.log
tail -n +2 /opt/work/roots.tsv | cut -f2 | while read R; do
  NOW=$(date +%s); LEFT=$((END-NOW))
  [ $LEFT -le 0 ] && { echo "=== END reached before $R" >> $LOG; break; }
  S=$(python3 -c "print(round(min(2.0, $LEFT/3600), 4))")
  echo "=== ROOT $R start $(date -u +%FT%TZ) hours=$S" >> $LOG
  (cd $TOOLS && python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours $S) >> $LOG 2>&1
  echo "=== ROOT $R end $(date -u +%FT%TZ) rc=$?" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" $LOG; then echo "=== STOP" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> $LOG
