#!/bin/bash
# Reviewer rv5 start gate (task rule 3). usage: gate.sh <expected peak MB>
# YIELD absent; Tctl < 86 C; cpu_free.sh esr >= 1; sum of anon+shmem over active esr-ag-* units + expected peak
# <= 6800 MB (85 % of the ag budget 8000 MB); no other esr-ag-rv5-* unit active. Poll 60 s, up to 90 min.
PEAK=${1:?peak MB}
B=/sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice
CF=/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh
for i in $(seq 1 91); do
  y=0; [ -e /home/jay/research/data/agents-20261121/YIELD ] && y=1
  t=$(sensors 2>/dev/null | awk '/Tctl/{gsub(/[+°C]/,"",$2); print int($2)}')
  c=$($CF esr)
  a=0
  for f in $B/esr-ag-*.service/memory.stat; do
    [ -f "$f" ] && a=$((a + $(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s/1048576}' "$f")))
  done
  own=$(systemctl --user list-units 'esr-ag-rv5-*' --type=service --state=active --plain --no-legend | wc -l)
  if [ $y -eq 0 ] && [ -n "$t" ] && [ "$t" -lt 86 ] && [ "$c" -ge 1 ] && [ $((a + PEAK)) -le 6800 ] && [ "$own" -eq 0 ]; then
    echo "$(date '+%F %T') gate ok: tctl=$t cpu_free=$c anon_ag=${a}MB peak=${PEAK}MB"; exit 0
  fi
  echo "$(date '+%F %T') gate wait $i: yield=$y tctl=$t cpu_free=$c anon_ag=${a}MB peak=${PEAK}MB own=$own"
  [ $i -lt 91 ] && sleep 60
done
exit 1
