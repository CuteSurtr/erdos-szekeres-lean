#!/bin/bash
# per-root slice watchdog: close_tree checks --hours only between batches; stop a root's close_tree
# (and its solver/checker children) when its slice has run out, so the runner moves to the next root
LOG=/opt/work/driver.log
while pgrep -f runner.sh >/dev/null; do
  L=$(grep "=== ROOT .* start" $LOG | tail -1)
  R=$(echo $L | awk '{print $3}'); T0=$(date -d "$(echo $L | awk '{print $5}')" +%s); H=$(echo $L | awk '{print $7}')
  LIM=$(python3 -c "print(int($T0 + $H*3600))")
  if [ $(date +%s) -ge $LIM ] && ! grep -q "=== ROOT $R end" $LOG; then
    P=$(pgrep -of "close_tree.py .* $R ")
    if [ -n "$P" ]; then
      echo "=== SLICE over for $R $(date -u +%T), stopping close_tree" >> $LOG
      # kill the python main and workers first, so that no record is written for the killed nodes
      pkill -KILL -f "close_tree.py .* $R "; sleep 1
      pkill -KILL -x cadical; pkill -KILL -x cake_lpr; pkill -KILL -x lrat-check
    fi
  fi
  sleep 15
done
