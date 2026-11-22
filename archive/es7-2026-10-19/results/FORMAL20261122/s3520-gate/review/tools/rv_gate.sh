#!/bin/bash
# Reviewer's gate before starting a unit: YIELD absent, Tctl < 86 C, cpu_free esr >= 1, s20 track anon + EXP <= 85 % of 8000 MB.
# Usage: rv_gate.sh EXPECTED_MB   (exit 0 = may start)
exp=${1:-1000}
[ -e /home/jay/research/data/agents-20261121/YIELD ] && { echo "YIELD present"; exit 1; }
t=$(sensors | awk '/Tctl/ {gsub(/[+°C]/,"",$2); print int($2)}')
f=$(/home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/cpu_free.sh esr)
s=0
for u in $(systemctl --user list-units --no-legend --plain --state=active 'esr-s20-*' | awk '{print $1}'); do
  d=/sys/fs/cgroup/user.slice/user-1000.slice/user@1000.service/app.slice/$u
  a=$(awk '$1=="anon"||$1=="shmem"{s+=$2} END{printf "%d", s/1048576}' $d/memory.stat 2>/dev/null); s=$((s + ${a:-0}))
done
echo "$(date '+%T') Tctl=$t free=$f s20_anon=${s}MB exp=${exp}MB"
[ "$t" -lt 86 ] && [ "$f" -ge 1 ] && [ $((s + exp)) -le 6800 ]
