#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
record=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/left16_replay
/usr/bin/time -v -o "$record/data/recover.time" timeout -k 1 20s prlimit --as=157286400 --cpu=19 taskset -c 5 nice -n 10 python3 -B "$record/tools/recover.py" > "$record/data/recover.stdout" 2> "$record/data/recover.stderr"
