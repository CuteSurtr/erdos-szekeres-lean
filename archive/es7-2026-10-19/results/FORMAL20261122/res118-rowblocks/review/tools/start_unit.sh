#!/bin/bash
# Start ONE unit of slot lrv3 after the gates (task rule 3): no YIELD file; Tctl < 86 C; no esr-ag-lrv3-* unit active
# (the slot is shared with another reviewer); sum of anon over active esr-ag-* units < 4500 MB. Polls every 60 s, at
# most <max_wait_minutes>. Usage: tools/start_unit.sh <job> <max_wait_minutes> <command...>
set -u
job=$1; maxw=$2; shift 2
V=/home/jay/research/data/formalize-20261122/res118-rowblocks/review
U=$(id -u); APP=/sys/fs/cgroup/user.slice/user-$U.slice/user@$U.service/app.slice
for ((k = 0; k <= maxw; k++)); do
  t=$(sensors 2>/dev/null | awk '/Tctl/ {gsub(/[^0-9.]/, "", $2); print $2}')
  a=0
  for f in $APP/esr-ag-*.service/memory.stat; do
    [ -f "$f" ] && a=$((a + $(awk '/^anon /{print int($2/1048576)}' "$f")))
  done
  slot=$(systemctl --user list-units --no-legend --state=active,activating,deactivating 'esr-ag-lrv3-*' | wc -l)
  y=no; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=yes
  if [ "$y" = no ] && [ -n "$t" ] && awk -v t="$t" 'BEGIN {exit !(t < 86)}' && [ "$a" -lt 4500 ] && [ "$slot" -eq 0 ]; then
    echo "$(date -Is) gates open (Tctl $t, pool anon ${a} MB); starting esr-ag-lrv3-rbx-$job"
    exec systemd-run --user --unit=esr-ag-lrv3-rbx-$job -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 \
      -p RuntimeMaxSec=7200 --nice=10 --working-directory=$V "$@"
  fi
  echo "$(date -Is) waiting: YIELD $y, Tctl $t, pool anon ${a} MB, active lrv3 units $slot"
  [ $k -lt $maxw ] && sleep 60
done
echo "$(date -Is) gates did not open within $maxw min"; exit 3
