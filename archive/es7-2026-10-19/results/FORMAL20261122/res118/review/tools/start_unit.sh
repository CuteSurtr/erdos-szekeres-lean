#!/bin/bash
# Start ONE unit of slot lrev after the gates: no YIELD file, Tctl < 86 C, no esr-ag-lrev-* unit active (the slot is
# shared with another reviewer). Polls every 60 s, at most <max_wait_minutes>.
# Usage: tools/start_unit.sh <job> <max_wait_minutes> <command...>
set -u
job=$1; maxw=$2; shift 2
V=/home/jay/research/data/formalize-20261122/res118/review
for ((k = 0; k <= maxw; k++)); do
  t=$(sensors | awk '/Tctl/ {gsub(/[^0-9.]/, "", $2); print $2}')
  if [ ! -e /home/jay/research/data/agents-20261121/YIELD ] && awk -v t="$t" 'BEGIN {exit !(t < 86)}'; then
    if systemctl --user list-units --no-legend --state=active,activating,deactivating 'esr-ag-lrev-*' | grep -q .; then
      echo "$(date -Is) an esr-ag-lrev unit is active; waiting"
    else
      echo "$(date -Is) gates open (Tctl $t); starting esr-ag-lrev-$job"
      exec systemd-run --user --unit=esr-ag-lrev-$job -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 \
        -p RuntimeMaxSec=7200 --nice=10 --working-directory=$V "$@"
    fi
  else
    echo "$(date -Is) gate closed (Tctl $t, YIELD $( [ -e /home/jay/research/data/agents-20261121/YIELD ] && echo yes || echo no))"
  fi
  [ $k -lt $maxw ] && sleep 60
done
echo "$(date -Is) gates did not open within $maxw min"; exit 3
