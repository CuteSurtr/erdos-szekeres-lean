#!/bin/bash
# Reviewer's single audit compile for res118-rowblocks (slot lrv3). Bare Lean 4.24.0, no lake, no -o (no olean
# written). LEAN_PATH = the worker's tools/env_geo.sh (read-only stores); writes only review/logs and review/data.
set -u
V=/home/jay/research/data/formalize-20261122/res118-rowblocks/review
source /home/jay/research/data/formalize-20261122/res118-rowblocks/tools/env_geo.sh
cd $V/lean
echo "start $(date -Is) sha256 $(sha256sum LrvReview.lean | cut -c1-64) LEAN_PATH=$LEAN_PATH" > $V/logs/audit.meta
/usr/bin/time -v -o $V/logs/audit.time $TC/bin/lean -j1 $V/lean/LrvReview.lean > $V/logs/audit.log 2>&1
rc=$?
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
{ echo "rc=$rc"; echo "end $(date -Is)"; echo "cgroup_memory_peak_bytes=$(cat $cg/memory.peak 2>/dev/null)"; } >> $V/logs/audit.meta
exit $rc
