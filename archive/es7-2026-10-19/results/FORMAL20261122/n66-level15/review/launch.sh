#!/bin/bash
# Bounded launcher (slot lrv3). Waits (poll 60 s, at most 60 min) until: no YIELD file, Tctl < 86 C, agent-pool anon
# (sum over active esr-ag-* units) < 4500 MB, cpu_free.sh >= 1 free thread (house cap 28), and no other esr-ag-lrv3-*
# unit active. Then starts the unit. usage: launch.sh <job> <command...>
job=$1; shift
U=esr-ag-lrv3-$job
RV=/home/jay/research/data/formalize-20261122/n66-level15/review
for i in $(seq 1 61); do
  y=0; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=1
  t=$(sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  a=0
  for f in /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice/esr-ag-*.service/memory.stat; do
    [ -f "$f" ] && a=$((a + $(awk '/^anon /{print int($2/1048576)}' "$f")))
  done
  free=$(bash /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh)
  mine=$(systemctl --user list-units 'esr-ag-lrv3-*' --type=service --state=active --plain --no-legend | wc -l)
  if [ $y -eq 0 ] && [ -n "$t" ] && [ "$t" -lt 86 ] && [ "$a" -lt 4500 ] && [ "$free" -ge 1 ] && [ "$mine" -eq 0 ]; then
    echo "$(date '+%F %T') gate ok: tctl=$t anon_ag=${a}MB free=$free -> start $U"
    systemd-run --user --unit=$U -p CPUQuota=100% -p MemoryMax=3500M -p MemorySwapMax=0 -p RuntimeMaxSec=7200 \
      --nice=10 --working-directory=$RV "$@"
    exit $?
  fi
  echo "$(date '+%F %T') gate wait $i: yield=$y tctl=$t anon_ag=${a}MB free=$free mine=$mine"
  [ $i -lt 61 ] && sleep 60
done
echo "$(date '+%F %T') gave up after 60 min"; exit 1
