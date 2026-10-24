#!/bin/bash
# C3W4 H16 runner, version 2 (from 13:45 UTC): as runner.sh, but close_tree checks its deadline only
# between rounds, so each root run is killed at the end of its slice S (and at END): the close_tree
# processes first (so no partial record is written), then any solver or checker left.
export PATH=/opt/bin:$PATH
TOOLS=/opt/c3u/cloud/es7-2026-10-19/results/C3U/tools
END=$(cat /opt/work/end_epoch)
LOG=/opt/work/driver.log
killall_ct() { pkill -f close_tree.py; sleep 2; pkill -x cadical; pkill -x cake_lpr; pkill -x lrat-check; }
tail -n +2 /opt/work/roots.tsv | cut -f2 | sed -n "${FIRST:-1},\$p" | while read R; do
  NOW=$(date +%s); LEFT=$((END-NOW))
  [ $LEFT -le 0 ] && { echo "=== END reached before $R" >> $LOG; break; }
  SEC=$(( LEFT < 7200 ? LEFT : 7200 ))
  S=$(python3 -c "print(round($SEC/3600, 4))")
  echo "=== ROOT $R start $(date -u +%FT%TZ) hours=$S" >> $LOG
  (cd $TOOLS && exec python3 close_tree.py /opt/work/base.cnf /opt/work/out.jsonl $R --jobs 3 --sigma-split 3 --sigma-levels 2 --caps 1,1,300,600 --cadopts=--sat --hours $S) >> $LOG 2>&1 &
  P=$!; T=$(( $(date +%s) + SEC ))
  while kill -0 $P 2>/dev/null && [ $(date +%s) -lt $T ]; do sleep 10; done
  if kill -0 $P 2>/dev/null; then echo "=== ROOT $R slice over $(date -u +%T), killing the running round" >> $LOG; killall_ct; fi
  wait $P
  echo "=== ROOT $R end $(date -u +%FT%TZ)" >> $LOG
  if grep -q "SAT FOUND\|PROOF NOT ACCEPTED" $LOG; then echo "=== STOP" >> $LOG; break; fi
done
echo "=== RUNNER DONE $(date -u +%FT%TZ)" >> $LOG
