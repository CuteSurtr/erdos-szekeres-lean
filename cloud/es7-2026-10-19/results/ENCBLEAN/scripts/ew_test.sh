#!/usr/bin/env bash
# ew_test.sh: the M3 early-warning test (docs/M3PLAN.md section 4, unit U6). Evidence only: EncB/EarlyWarning.lean
# is elaborated and its `main` interpreted by `lean --run` (never the kernel; no .olean is written, .lake is not
# touched; EncB.lean does not import the file).
#   usage: bash scripts/ew_test.sh [LOG]        (default LOG: logs/m3_early_warning.log, overwritten)
# The log gets a header (date, load, toolchain, HEAD, hashes of the inputs), the test's output and the exit code.
# Exit 0 iff `main` exits 0 and prints "EW SUMMARY: PASS".
# Runs under a 4G memory cap at nice 10; waits until the CPU temperature (sensors, Tctl) is below 88 C first.
set -u -o pipefail
cd "$(dirname "$0")/.."
LOG=${1:-logs/m3_early_warning.log}
if command -v sensors >/dev/null 2>&1; then
  while :; do
    T=$(sensors 2>/dev/null | grep Tctl | grep -oE '[0-9]+(\.[0-9]+)?' | head -1)
    [ -z "$T" ] && break
    awk -v t="$T" 'BEGIN { exit !(t < 88) }' && break
    echo "Tctl=$T C, waiting 30 s" >&2; sleep 30
  done
fi
{
  echo "# M3 early-warning test (scripts/ew_test.sh), $(date -Is)"
  echo "# load average: $(cut -d' ' -f1-3 /proc/loadavg)"
  echo "# toolchain: $(cat lean-toolchain); $(lake env lean --version)"
  echo "# git HEAD: $(git rev-parse HEAD 2>/dev/null || echo n/a)"
  sha256sum EncB/Gen.lean EncB/Dimacs.lean EncB/Coded.lean EncB/Model.lean EncB/EarlyWarning.lean | sed 's/^/# sha256 /'
  echo "# command: systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10 lake env lean --run EncB/EarlyWarning.lean"
} > "$LOG"
start=$(date +%s)
systemd-run --user --scope -q -p MemoryMax=4G -p MemorySwapMax=0 nice -n 10 \
  lake env lean --run EncB/EarlyWarning.lean 2>&1 | tee -a "$LOG"
rc=${PIPESTATUS[0]}
echo "# exit=$rc wall=$(( $(date +%s) - start ))s" | tee -a "$LOG"
if [ "$rc" -eq 0 ] && grep -q '^EW SUMMARY: PASS' "$LOG"; then echo "EW TEST PASS"; exit 0; fi
echo "EW TEST FAIL"; exit 1
