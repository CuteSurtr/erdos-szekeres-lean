#!/bin/bash
set -euo pipefail
ulimit -v 524288
cd /home/jay/research/data/delta3-codex-20261113/coordinator/cup15
/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B /home/jay/research/lean/erdos-szekeres-lean/cloud/es7-2026-10-19/results/DELTA3N20261113/coordinator/audit_cup15.py > independent_geometry.log
set +e
/usr/bin/cadical --lrat=true --binary=false cup15_coloring.cnf cup15_coloring.lrat > cup15_coloring.cadical.out 2>&1
rc=$?
set -e
test "$rc" -eq 20
/home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=128 --CML_STACK_SIZE=32 cup15_coloring.cnf cup15_coloring.lrat > cup15_coloring.cake.out 2>&1
grep -Fx 's VERIFIED UNSAT' cup15_coloring.cake.out
sha256sum realized.json independent_geometry.json cup15_coloring.cnf cup15_coloring.lrat cup15_coloring.cake.out > SHA256SUMS
touch VERIFIED
