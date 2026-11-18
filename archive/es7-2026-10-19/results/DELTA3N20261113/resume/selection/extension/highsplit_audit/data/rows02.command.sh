#!/bin/bash
set -eu
cd /home/jay/research/lean/erdos-szekeres-lean
/usr/bin/time -v -o cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/data/rows02.time timeout -k 1 20s prlimit --as=314572800 --cpu=19 taskset -c 5 nice -n 10 python3 -B cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/tools/check_rows.py rows-run02 > cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/data/rows02.stdout 2> cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/extension/highsplit_audit/data/rows02.stderr
