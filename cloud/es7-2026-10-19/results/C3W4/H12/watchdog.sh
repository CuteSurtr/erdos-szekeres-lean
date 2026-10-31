#!/bin/bash
# kills a close_tree.py run (and its workers) once its --hours slice has elapsed;
# close_tree only checks its deadline between frontier waves
killtree() { for c in $(pgrep -P $1); do killtree $c; done; kill -9 $1 2>/dev/null; }
while pgrep -x -f "bash /opt/work/runner.sh" >/dev/null; do
  for P in $(pgrep -x python3); do
    grep -qa close_tree.py /proc/$P/cmdline 2>/dev/null || continue
    PP=$(ps -o comm= -p $(ps -o ppid= -p $P | tr -d ' ') | tr -d ' ')
    [ "$PP" = bash ] || continue
    H=$(tr '\0' ' ' < /proc/$P/cmdline | sed 's/.*--hours \([0-9.]*\).*/\1/')
    E=$(ps -o etimes= -p $P | tr -d ' ')
    if [ -n "$E" ] && python3 -c "import sys; sys.exit(0 if $E > $H*3600 else 1)"; then
      echo "=== WATCHDOG kill close_tree pid $P after ${E}s (slice ${H} h) $(date -u +%T)" >> /opt/work/watchdog.log
      killtree $P
    fi
  done
  sleep 20
done
