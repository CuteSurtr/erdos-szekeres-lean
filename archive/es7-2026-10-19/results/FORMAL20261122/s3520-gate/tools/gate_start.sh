#!/bin/bash
# s3520-gate (22 Nov 2026): start one unit esr-s20-g-<job> after the gates: no YIELD file, Tctl < 86 C, at least one
# free thread under the 28-thread cap (cpu_free.sh esr), fewer than 2 active esr-s20-* units, and track room (anon +
# shmem of the active esr-s20-* units + the expected peak <= 85 % of the 8,000 MB track budget). Polls every 60 s.
# Usage: tools/gate_start.sh <job> <MemoryMax MB> <RuntimeMaxSec> <expected peak MB> <max_wait_min> <command...>
set -u
job=$1; mem=$2; rt=$3; est=$4; maxw=$5; shift 5
G=/home/jay/research/data/formalize-20261122/s3520-gate
CG=/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice
for ((k = 0; k <= maxw; k++)); do
  t=$(sensors | awk '/Tctl/ {gsub(/[^0-9.]/, "", $2); print $2}')
  f=$(/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh esr)
  n=$(systemctl --user list-units --no-legend --plain --state=active,activating 'esr-s20-*' | grep -c .)
  used=0
  for d in "$CG"/esr-s20-*.service; do
    [ -d "$d" ] && used=$((used + $(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s/1048576}' "$d/memory.stat")))
  done
  if [ ! -e /home/jay/research/data/agents-20261121/YIELD ] && awk -v t="$t" 'BEGIN {exit !(t < 86)}' && [ "$f" -ge 1 ] \
     && [ "$n" -lt 2 ] && [ $((used + est)) -le 6800 ]; then
    echo "$(date -Is) start esr-s20-g-$job (Tctl $t, free threads $f, s20 units $n, s20 anon $used MB + est $est MB)"
    exec systemd-run --user --unit=esr-s20-g-$job --collect -p CPUQuota=100% -p MemoryMax=${mem}M -p MemorySwapMax=0 \
      -p RuntimeMaxSec=$rt --nice=10 --working-directory=$G "$@"
  fi
  echo "$(date -Is) gate closed (Tctl $t, free threads $f, s20 units $n, s20 anon $used MB, YIELD $([ -e /home/jay/research/data/agents-20261121/YIELD ] && echo yes || echo no))"
  [ $k -lt $maxw ] && sleep 60
done
echo "$(date -Is) gates did not open within $maxw min"; exit 3
