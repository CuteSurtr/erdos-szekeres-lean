#!/bin/bash
# gate.sh (reviewer slot lrv2): exit 0 iff a new unit may start now.
[ -e /home/jay/research/data/agents-20261121/YIELD ] && { echo "YIELD present"; exit 1; }
T=$(sensors | awk '/Tctl/ {gsub(/[+°C]/,"",$2); print int($2)}')
[ -z "$T" ] && { echo "no Tctl reading"; exit 1; }
[ "$T" -ge 86 ] && { echo "Tctl $T"; exit 1; }
S=0; for f in /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice/esr-ag-*.service/memory.stat; do
  [ -f "$f" ] && S=$((S + $(awk '/^anon / {print $2}' "$f"))); done
[ $((S/1048576)) -ge 3500 ] && { echo "pool $((S/1048576)) MB"; exit 1; }
systemctl --user is-active --quiet 'esr-ag-lrv2-*' && { echo "lrv2 unit active"; exit 1; }
systemctl --user is-active --quiet 'esr-ag-lenc7-*' && { echo "worker lenc7 unit active (olean store may change)"; exit 1; }
echo "gate ok: Tctl $T, pool $((S/1048576)) MB"; exit 0
