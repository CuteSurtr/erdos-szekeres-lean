#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
record="$PWD/cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/replay"
.claude/skills/es-research/scripts/cpu_free.sh nov13c > "$record/data/cpu-free-before-low14.txt"
systemctl --user show memguard5-20261113.service -p ActiveState > "$record/data/memguard-before-low14.txt"
test "$(cat "$record/data/memguard-before-low14.txt")" = ActiveState=active
test "$(cat "$record/data/cpu-free-before-low14.txt")" -ge 1
systemd-run --user --unit=nov13c-vfy-delta6-low14-independent \
  -p CPUQuota=100% -p MemoryMax=1000M -p MemorySwapMax=0 -p RuntimeMaxSec=480 \
  -p "StandardOutput=append:$record/data/unit.stdout" \
  -p "StandardError=append:$record/data/unit.stderr" \
  --nice=10 --working-directory="$PWD" \
  /usr/bin/prlimit --as=734003200 --cpu=450 \
  /usr/bin/taskset -c 5 /usr/bin/python3 -B "$record/tools/replay.py" 14
