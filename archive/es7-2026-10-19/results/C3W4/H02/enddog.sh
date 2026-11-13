#!/bin/bash
# at END - 40 s: kill close_tree python processes first, then solvers/checkers, so no record is written for killed nodes
END=1792858567
while [ $(date +%s) -lt $((END-40)) ]; do sleep 5; done
if pgrep -f "close_tree.py" >/dev/null; then
  echo "=== END-40s $(date -u +%T): stopping close_tree" >> /opt/work/driver.log
  pkill -KILL -f "close_tree.py"; sleep 1; pkill -KILL -x cadical; pkill -KILL -x cake_lpr; pkill -KILL -x lrat-check
fi
