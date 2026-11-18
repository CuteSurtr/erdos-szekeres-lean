#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/left15
.claude/skills/es-research/scripts/cpu_free.sh nov13c > "$record/data/cpu-free-before-instance.txt"
/usr/bin/time -v -o "$record/data/instance.time" timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 python3 -B "$record/tools/instance.py" > "$record/data/instance.stdout" 2> "$record/data/instance.stderr"
