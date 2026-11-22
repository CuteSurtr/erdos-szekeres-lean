#!/bin/bash
# launch.sh -- reviewer rv4: wait (at most 45 min, poll 30 s) until a thread is free under the 28-thread cap, YIELD is
# absent and Tctl < 86 C; then start the driver as unit $1 (1 thread, MemoryMax 3000M, no swap, 3 h deadline).
V=/home/jay/research/data/formalize-20261122/n66enc-recheck/verify
U=${1:-esr-ag-rv4-n66v1}
CF=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh
end=$(( $(date +%s) + 2700 ))
ready() {
  local t; t=$(sensors 2>/dev/null | awk '/^Tctl/{print $2; exit}' | tr -cd '0-9.')
  [ "$(bash "$CF")" -ge 1 ] && [ ! -e /home/jay/research/data/agents-20261121/YIELD ] && [ -n "$t" ] &&
    awk -v t="$t" 'BEGIN{exit !(t < 86)}'
}
until ready; do
  [ "$(date +%s)" -ge "$end" ] && { echo "launch: gave up at $(date '+%F %T')"; exit 1; }
  sleep 30
done
systemd-run --user --unit="$U" -p CPUQuota=100% -p MemoryMax=3000M -p MemorySwapMax=0 -p RuntimeMaxSec=10800 \
  --nice=10 --working-directory="$V" /bin/bash "$V/tools/driver.sh"
echo "launched $U at $(date '+%F %T'); cpu_free after: $(bash "$CF")"
