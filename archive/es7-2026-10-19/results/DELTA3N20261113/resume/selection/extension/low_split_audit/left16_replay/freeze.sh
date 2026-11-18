#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
/usr/bin/timeout 20 /usr/bin/prlimit --as=157286400 --cpu=19 /usr/bin/taskset -c 5 /usr/bin/nice -n 10 /usr/bin/python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/left16_replay/tools/freeze.py
