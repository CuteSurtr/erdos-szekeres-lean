#!/bin/bash
# res118-lean: start one systemd user unit of slot lres after the gates (no YIELD file, Tctl < 86 C).
# Usage: tools/start_unit.sh <job> <max_wait_minutes> <command...>
set -u
job=$1; maxw=$2; shift 2
D=/home/jay/research/data/formalize-20261122/res118
for ((k = 0; k <= maxw; k++)); do
  t=$(sensors | awk '/Tctl/ {gsub(/[^0-9.]/, "", $2); print $2}')
  if [ ! -e /home/jay/research/data/agents-20261121/YIELD ] && awk -v t="$t" 'BEGIN {exit !(t < 86)}'; then
    if systemctl --user list-units --no-legend --state=active,activating,deactivating 'esr-ag-lres-*' | grep -q .; then
      echo "$(date -Is) another lres unit is active; waiting"
    else
      echo "$(date -Is) gates open (Tctl $t); starting esr-ag-lres-$job"
      exec systemd-run --user --unit=esr-ag-lres-$job -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 \
        -p RuntimeMaxSec=7200 --nice=10 --working-directory=$D "$@"
    fi
  else
    echo "$(date -Is) gate closed (Tctl $t, YIELD $( [ -e /home/jay/research/data/agents-20261121/YIELD ] && echo yes || echo no))"
  fi
  [ $k -lt $maxw ] && sleep 60
done
echo "$(date -Is) gates did not open within $maxw min"; exit 3
