#!/bin/bash
# Enforces the per-root slice S of lane0.sh: close_tree.py only checks --hours between whole
# frontier waves, so a root whose (presplit) frontier is large overruns its slice.
# When the current root has run S hours (+30 s), kill its close_tree.py process tree; lane0.sh
# then moves on to the next root (records already written to out0.jsonl are kept).
LOG=/opt/work/driver0.log
killtree() { for c in $(pgrep -P $1); do killtree $c; done; kill -TERM $1 2>/dev/null; }
while ! grep -q "RUNNER DONE" $LOG; do
  L=$(grep "=== ROOT .* start" $LOG | tail -1)
  R=$(echo "$L" | awk '{print $3}'); T=$(echo "$L" | awk '{print $5}'); S=$(echo "$L" | awk '{print $7}')
  if [ -n "$R" ] && ! grep -q "=== ROOT $R end" $LOG; then
    T0=$(date -u -d "today $T" +%s)
    LIM=$(python3 -c "print(int($T0 + $S*3600 + 30))")
    if [ $(date +%s) -ge $LIM ]; then
      P=$(pgrep -f "close_tree.py /opt/work/base.cnf /opt/work/out0.jsonl $R " | head -1)
      [ -n "$P" ] && { echo "=== WATCHDOG kill $R pid $P at $(date -u +%T) (slice $S h used)" >> $LOG; killtree $P; }
    fi
  fi
  sleep 15
done
