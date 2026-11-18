#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/n6
.claude/skills/es-research/scripts/cpu_free.sh nov13c > "$record/data/cpu-free.txt"
for m in 10 11; do
 /usr/bin/time -v -o "$record/data/left$m-wrapper.time" timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 python3 -B "$record/tools/audit.py" "$m" > "$record/data/left$m-wrapper.stdout" 2> "$record/data/left$m-wrapper.stderr"
done
