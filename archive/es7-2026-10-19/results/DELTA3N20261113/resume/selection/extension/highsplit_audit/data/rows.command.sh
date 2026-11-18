#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
.claude/skills/es-research/scripts/cpu_free.sh nov13c > cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/data/cpu-free-before-rows.txt
/usr/bin/time -v -o cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/data/rows.time timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/tools/check_rows.py > cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/data/rows.stdout 2> cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/data/rows.stderr
