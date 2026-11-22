#!/bin/bash
# gate.sh: exit 0 iff a new unit may start now (no YIELD, Tctl < 86 C, esr-ag-* anon sum < 3500 MB, no lenc7 unit active).
[ -e /home/jay/research/data/agents-20261121/YIELD ] && { echo "YIELD present"; exit 1; }
T=$(sensors | awk '/Tctl/ {gsub(/[+°C]/,"",$2); print int($2)}')
[ "$T" -ge 86 ] && { echo "Tctl $T"; exit 1; }
S=0; for f in /sys/fs/cgroup/user.slice/user-$(id -u).slice/user@$(id -u).service/app.slice/esr-ag-*.service/memory.stat; do
  [ -f "$f" ] && S=$((S + $(awk '/^anon / {print $2}' "$f"))); done
[ $((S/1048576)) -ge 3500 ] && { echo "pool ${S}B"; exit 1; }
systemctl --user is-active --quiet 'esr-ag-lenc7-*' && { echo "lenc7 unit active"; exit 1; }
echo "gate ok: Tctl $T, pool $((S/1048576)) MB"; exit 0
