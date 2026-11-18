#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
/usr/bin/time -v -o cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/data/provenance.time timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/tools/provenance.py > cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/data/provenance.stdout 2> cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/low_split_audit/data/provenance.stderr
