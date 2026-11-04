#!/bin/bash
# restart any cube worker that stopped (e.g. on an unresolved model) unless its cube is UNSAT; until the deadline
W="<run-dir>"; DL=$(cat "$W/deadline"); cd "$W"
while [ $(date +%s) -lt $((DL - 120)) ]; do
  while IFS=$'\t' read -r nm ord lits; do
    grep -q "^[0-9:]* $nm UNSAT" events.txt 2>/dev/null && continue
    ps -axww -o command | grep -q "[w]orker.py $nm " && continue
    n=$(grep -c "restart $nm" logs/supervisor.log 2>/dev/null); [ "${n:-0}" -ge 80 ] && continue
    echo "$(date +%H:%M:%S) restart $nm" >> logs/supervisor.log
    nohup ./satvenv/bin/python -I worker.py "$nm" "$lits" $DL >> "logs/$nm.out" 2>&1 &
  done < cubes.txt
  sleep 30
done
