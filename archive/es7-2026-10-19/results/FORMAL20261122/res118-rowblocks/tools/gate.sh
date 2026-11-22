#!/bin/bash
# Start gates (task rule 3): no YIELD file, Tctl < 86 C, active esr-ag-* anon sum < 4500 MB, no other esr-ag-lrb-* unit.
# Bounded wait: poll every 60 s, up to 60 min. Exit 0 = go, 1 = gave up.
U=$(id -u); APP=/sys/fs/cgroup/user.slice/user-$U.slice/user@$U.service/app.slice
for i in $(seq 1 61); do
  y=0; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=1
  t=$(sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  a=0
  for f in $APP/esr-ag-*.service/memory.stat; do
    [ -f "$f" ] && a=$((a + $(awk '/^anon /{print int($2/1048576)}' "$f")))
  done
  mine=$(systemctl --user list-units --state=active --no-legend 'esr-ag-lrb-*' 2>/dev/null | wc -l)
  if [ $y -eq 0 ] && [ -n "$t" ] && [ "$t" -lt 86 ] && [ $a -lt 4500 ] && [ "$mine" -eq 0 ]; then
    echo "gate ok: tctl=$t anon_ag=${a}MB"; exit 0
  fi
  echo "gate wait $i: yield=$y tctl=$t anon_ag=${a}MB mine=$mine"
  [ $i -lt 61 ] && sleep 60
done
exit 1
