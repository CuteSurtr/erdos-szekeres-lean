#!/bin/bash
# rv5: gated start of ONE unit esr-ag-rv5-JOB with --wait (task rule 3). Gates: no YIELD; Tctl < 86 C;
# cpu_free.sh esr >= 1; no other esr-ag-rv5-* unit active; ag-track anon (active esr-ag-* units) + EXP_MB <= 6800 MB
# (85 % of 8000); fv304 lean_path.txt hash unchanged. Bounded wait: poll 60 s, up to 90 min.
# Usage: start.sh JOB MEM_MB RUNTIME_S EXP_MB command...
set -u
R=/home/jay/research/data/formalize-20261122/combined/review
. $R/tools/env.sh
job=$1 mem=$2 secs=$3 exp=$4; shift 4
U=$(id -u); APP=/sys/fs/cgroup/user.slice/user-$U.slice/user@$U.service/app.slice
CPUF=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh
[ "$(sha256sum /home/jay/research/data/fv304-20261120/lean_path.txt | cut -c1-64)" = 65463fd5680b9f1ccadb2e7ea0bb9a2820d5d4d5ae445d61318834d477f4a2cf ] || { echo "lean_path.txt changed"; exit 1; }
for i in $(seq 1 91); do
  y=0; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=1
  t=$(sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  f=$($CPUF esr)
  a=0
  for s in $APP/esr-ag-*.service/memory.stat; do [ -f "$s" ] && a=$((a + $(awk '/^anon /{print int($2/1048576)}' "$s"))); done
  mine=$(systemctl --user list-units --state=active --no-legend --plain 'esr-ag-rv5-*' 2>/dev/null | wc -l)
  if [ $y -eq 0 ] && [ -n "$t" ] && [ "$t" -lt 86 ] && [ "$f" -ge 1 ] && [ $((a + exp)) -le 6800 ] && [ "$mine" -eq 0 ]; then
    echo "$(date '+%F %T') gate ok esr-ag-rv5-$job: tctl=$t free=$f ag_anon=${a}MB" | tee -a $R/logs/gates.log
    systemd-run --user --unit=esr-ag-rv5-$job --collect --wait -p CPUQuota=100% -p MemoryMax=${mem}M \
      -p MemorySwapMax=0 -p RuntimeMaxSec=$secs --nice=10 --working-directory=$R -E LEAN_PATH="$LEAN_PATH" \
      -p StandardOutput=file:$R/logs/$job.out -p StandardError=file:$R/logs/$job.out "$@"
    rc=$?; echo "$(date '+%F %T') unit esr-ag-rv5-$job ended rc=$rc" | tee -a $R/logs/gates.log; exit $rc
  fi
  echo "$(date '+%F %T') wait $i $job: yield=$y tctl=$t free=$f ag_anon=${a}MB mine=$mine" >> $R/logs/gates.log
  [ $i -lt 91 ] && sleep 60
done
echo "$(date '+%F %T') gave up after 90 min" | tee -a $R/logs/gates.log; exit 1
