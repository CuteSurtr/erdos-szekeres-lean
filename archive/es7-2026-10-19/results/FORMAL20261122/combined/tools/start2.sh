#!/bin/bash
# combined part 2 (copy of start.sh: env2.sh, slot lcb2, gates2.log): gated start of one unit esr-ag-lcb2-JOB (task rule 3). Gates: no YIELD file; Tctl < 86 C; cpu_free.sh esr
# >= 1; no other esr-ag-lcb2-* unit active; ag track anon (active esr-ag-* units) + 1500 MB <= 6800 MB (85 % of 8000).
# Bounded wait: poll 60 s, up to 90 min, then exit 1. Unit stdout/stderr go to logs/JOB.out.
# Usage: start.sh JOB MEM_MB RUNTIME_S WAIT(0|1) command...
set -u
. /home/jay/research/data/formalize-20261122/combined/tools/env2.sh
job=$1 mem=$2 secs=$3 wait=$4; shift 4
U=$(id -u); APP=/sys/fs/cgroup/user.slice/user-$U.slice/user@$U.service/app.slice
CPUF=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh
for i in $(seq 1 91); do
  y=0; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=1
  t=$(sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  f=$($CPUF esr)
  a=0
  for s in $APP/esr-ag-*.service/memory.stat; do
    [ -f "$s" ] && a=$((a + $(awk '/^anon /{print int($2/1048576)}' "$s")))
  done
  mine=$(systemctl --user list-units --state=active --no-legend --plain 'esr-ag-lcb2-*' 2>/dev/null | wc -l)
  if [ $y -eq 0 ] && [ -n "$t" ] && [ "$t" -lt 86 ] && [ "$f" -ge 1 ] && [ $((a + 1500)) -le 6800 ] && [ "$mine" -eq 0 ]; then
    echo "$(date '+%F %T') gate ok for esr-ag-lcb2-$job: tctl=$t free=$f ag_anon=${a}MB" | tee -a $W/logs/gates2.log
    w=(); [ "$wait" = 1 ] && w=(--wait)
    systemd-run --user --unit=esr-ag-lcb2-$job --collect "${w[@]}" -p CPUQuota=100% -p MemoryMax=${mem}M \
      -p MemorySwapMax=0 -p RuntimeMaxSec=$secs --nice=10 --working-directory=$W -E LEAN_PATH="$LEAN_PATH" \
      -p StandardOutput=file:$W/logs/$job.out -p StandardError=file:$W/logs/$job.out "$@"
    exit $?
  fi
  echo "$(date '+%F %T') gate wait $i for $job: yield=$y tctl=$t free=$f ag_anon=${a}MB mine=$mine" | tee -a $W/logs/gates2.log
  [ $i -lt 91 ] && sleep 60
done
echo "gave up after 90 min" | tee -a $W/logs/gates2.log
exit 1
