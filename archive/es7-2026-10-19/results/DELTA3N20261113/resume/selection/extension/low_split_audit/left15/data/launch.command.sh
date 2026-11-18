#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
record="$PWD/cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/left15"
.claude/skills/es-research/scripts/cpu_free.sh nov13c > "$record/data/cpu-free-before-replay.txt"
systemctl --user show memguard5-20261113.service -p ActiveState > "$record/data/memguard-before.txt"
test "$(cat "$record/data/memguard-before.txt")" = ActiveState=active
test "$(cat "$record/data/cpu-free-before-replay.txt")" -ge 1
systemd-run --user --unit=nov13c-vfy-delta6-low15-independent \
 -p CPUQuota=100% -p MemoryMax=2200M -p MemorySwapMax=0 -p RuntimeMaxSec=780 \
 -p "StandardOutput=append:$record/data/unit.stdout" -p "StandardError=append:$record/data/unit.stderr" \
 --nice=10 --working-directory="$PWD" \
 /usr/bin/prlimit --as=1730150400 --cpu=720 /usr/bin/taskset -c 5 \
 /usr/bin/python3 -B "$record/tools/replay.py"
