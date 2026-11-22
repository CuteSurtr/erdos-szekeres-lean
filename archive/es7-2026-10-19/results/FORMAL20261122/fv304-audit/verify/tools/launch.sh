#!/bin/bash
# rv4: gated launch of one unit. Gates (poll 60 s, up to 45 min): no YIELD file, Tctl < 86 C, cpu_free.sh esr,esv >= 1,
# ag-track anon+shmem + NEED_MB <= 8000 - 1000. Usage: launch.sh UNIT NEED_MB RUNTIME_S CMD...
unit=$1 need=$2 rt=$3; shift 3
V=/home/jay/research/data/formalize-20261122/fv304-audit/verify
S=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts
CG=/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice
for i in $(seq 1 45); do
  t=$(sensors | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  f=$(bash $S/cpu_free.sh esr,esv 2>/dev/null | tail -1)
  ag=$(cat $CG/esr-ag-*.service/memory.stat 2>/dev/null | awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s/1048576}')
  echo "$(date '+%F %T') gate $unit: yield=$([ -e /home/jay/research/data/agents-20261121/YIELD ] && echo 1 || echo 0) tctl=$t free=$f ag_mb=$ag" >> $V/logs/launch.log
  if [ ! -e /home/jay/research/data/agents-20261121/YIELD ] && [ "${t:-99}" -lt 86 ] && [ "${f:-0}" -ge 1 ] && [ $((ag + need)) -le 7000 ]; then
    systemd-run --user --unit=$unit -p CPUQuota=100% -p MemoryMax=4000M -p MemorySwapMax=0 -p RuntimeMaxSec=$rt \
      --nice=10 --working-directory=$V "$@" >> $V/logs/launch.log 2>&1
    echo "$(date '+%F %T') launched $unit rc=$?" >> $V/logs/launch.log
    exit 0
  fi
  sleep 60
done
echo "$(date '+%F %T') refused $unit: gates not met in 45 min" >> $V/logs/launch.log
exit 1
