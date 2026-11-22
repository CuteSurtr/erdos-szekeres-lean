#!/bin/bash
# Start gates (task rule 3): no YIELD file, Tctl < 86 C, active esr-ag-* anon sum < 4500 MB (pool limit 8000 MB).
# Bounded wait: poll every 60 s, up to 60 min. Exit 0 = go, 1 = gave up.
for i in $(seq 1 61); do
  y=0; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=1
  t=$(sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  a=0
  for f in /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice/esr-ag-*.service/memory.stat; do
    [ -f "$f" ] && a=$((a + $(awk '/^anon /{print int($2/1048576)}' "$f")))
  done
  if [ $y -eq 0 ] && [ -n "$t" ] && [ "$t" -lt 86 ] && [ $a -lt 4500 ]; then
    echo "gate ok: tctl=$t anon_ag=${a}MB"; exit 0
  fi
  echo "gate wait $i: yield=$y tctl=$t anon_ag=${a}MB"
  [ $i -lt 61 ] && sleep 60
done
exit 1
