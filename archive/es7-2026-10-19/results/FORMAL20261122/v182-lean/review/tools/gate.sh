#!/bin/bash
# Start gates (task rule 3 + house thread cap): no YIELD file, Tctl < 86 C, active esr-ag-* anon sum < 4500 MB,
# no active esr-ag-lrv3-* unit (one unit of the slot at a time; the slot name is shared), cpu_free.sh >= 1.
# Bounded wait: poll every 60 s, up to 60 min. Exit 0 = go, 1 = gave up.
CF=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh
B=/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice
for i in $(seq 1 61); do
  y=0; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=1
  t=$(sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  a=0
  for f in $B/esr-ag-*.service/memory.stat; do
    [ -f "$f" ] && a=$((a + $(awk '/^anon /{print int($2/1048576)}' "$f")))
  done
  s=$(systemctl --user list-units 'esr-ag-lrv3-*' --type=service --state=active --plain --no-legend | wc -l)
  c=$(bash $CF esr)
  if [ $y -eq 0 ] && [ -n "$t" ] && [ "$t" -lt 86 ] && [ $a -lt 4500 ] && [ "$s" -eq 0 ] && [ "$c" -ge 1 ]; then
    echo "gate ok $(date '+%F %T'): tctl=$t anon_ag=${a}MB slot_units=$s cpu_free=$c"; exit 0
  fi
  echo "gate wait $i $(date '+%T'): yield=$y tctl=$t anon_ag=${a}MB slot_units=$s cpu_free=$c"
  [ $i -lt 61 ] && sleep 60
done
exit 1
