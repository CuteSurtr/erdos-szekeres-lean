#!/usr/bin/env bash
# Build the package one module group at a time (Lake 5.0 has no job limit; the kernel-check modules need
# 5-8 GB each, so they must not run in parallel). Every step runs in a scope of 2 CPUs and 12 GB at nice 10.
# Usage: scripts/build_all.sh [--clean]   (--clean removes this package's .lake/build only, not .lake/packages)
# Log: logs/build_final.log (lake output, per-module times, GNU time per step).
set -u
cd "$(dirname "$0")/.."
LOG=logs/build_final.log
mkdir -p logs
[ "${1:-}" = "--clean" ] && rm -rf .lake/build
: > "$LOG"
CAP="systemd-run --user --scope -q -p CPUQuota=200% -p MemoryMax=12G nice -n 10"
export LEAN_NUM_THREADS=2
step() {
  echo "== lake build $* ($(date '+%F %T %Z'))" >> "$LOG"
  $CAP /usr/bin/time -f "   step wall %e s, peak RSS %M KB, exit %x" lake build "$@" >> "$LOG" 2>&1
  local rc=$?
  [ $rc = 0 ] || { echo "FAILED: lake build $*" | tee -a "$LOG"; exit $rc; }
}
T0=$(date +%s)
step ErdosSzekeres
for m in LeanLB.Checker LeanLB.CheckerSound LeanLB.Statement LeanLB.Bridge LeanLB.Geometry \
         LeanLB.G.Sound LeanLB.G.Bridge LeanLB.G.Approx LeanLB.G.Cyclo LeanLB.G.Five LeanLB.G.Seven \
         LeanLB.Check.Rows; do
  step "$m"
done
for m in MirN46 C4N52 C6N60 C2N64 C3N61 C5N56 C7N64; do
  step "LeanLB.Check.$m"
done
step LeanLB
T1=$(date +%s)
echo "== total wall $((T1 - T0)) s ($(date '+%F %T %Z'))" | tee -a "$LOG"
grep -E "Built LeanLB|step wall" "$LOG" | tail -40
