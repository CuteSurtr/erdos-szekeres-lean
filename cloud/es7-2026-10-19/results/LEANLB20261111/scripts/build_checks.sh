#!/usr/bin/env bash
# Build the kernel-check modules one at a time (at most 2 threads, 12 GB), logging wall time and peak RSS.
set -u
cd "$(dirname "$0")/.."
mkdir -p logs
for m in "$@"; do
  echo "== $m $(date '+%F %T %Z')" | tee -a logs/build_checks.log
  LEAN_NUM_THREADS=2 systemd-run --user --scope -q -p CPUQuota=200% -p MemoryMax=12G nice -n 10 \
    /usr/bin/time -v lake build "LeanLB.Check.$m" > "logs/build_$m.log" 2>&1
  echo "exit $?" | tee -a logs/build_checks.log
  grep -E "Built LeanLB.Check|error|Elapsed|Maximum resident" "logs/build_$m.log" | tee -a logs/build_checks.log
done
