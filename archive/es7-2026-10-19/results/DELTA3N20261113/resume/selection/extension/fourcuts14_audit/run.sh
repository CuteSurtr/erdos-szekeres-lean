#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
r="$PWD/cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/fourcuts14_audit"
mkdir -p "$r/data"
.claude/skills/es-research/scripts/cpu_free.sh nov13c > "$r/data/cpu-free.txt"
test "$(cat "$r/data/cpu-free.txt")" -ge 1
/usr/bin/time -v -o "$r/data/time.txt" /usr/bin/timeout 20 /usr/bin/prlimit --as=314572800 --cpu=19 /usr/bin/taskset -c 5 /usr/bin/nice -n 10 /usr/bin/python3 -B "$r/tools/check.py" > "$r/data/stdout" 2> "$r/data/stderr"
