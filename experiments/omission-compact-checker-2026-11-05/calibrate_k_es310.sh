#!/bin/bash
# Calibration E5 of the per-word k for the ES(8) <= 310 compact check (6 Nov 2026). ES(8) <= 310 is NOT proved.
#   calibrate_k_es310.sh ROUNDS        (log: logs/es310/calibrate_k_es310-<time>.log)
# Needs build/es310/test-calib-k{4,8,16}-{a,b}: the same ctx-2407 export (export_es310.py --ctx 2407
# --chunk-leaves 12000 --per-word k --prefix E310BT, merge --partial) twice per k. Two lanes run side by side,
# each compiling E310BT.C240701 once per k per round through drive_es310.py --only ... --bench 1:
#   lane a: k = 4, 8, 16, 4, 8, 16, ...   on the -a copies
#   lane b: k = 8, 16, 4, 8, 16, 4, ...   on the -b copies
# so at most 2 Lean jobs run, the k values are interleaved in time, and no export is driven by two drivers.
# Each start waits until fewer than 2 lean processes run on the machine and Tctl < 85 C (the driver's own
# gate is --max-tctl 80). Every compile is a drive_es310.py scope: MemoryMax 12G, MemorySwapMax 0, nice 10.
# Results: the run.tsv of each copy (kernel_s, wall_s, olean_bytes, ...).
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
R=${1:-3}
T=$D/build/es310
LOG=$D/logs/es310/calibrate_k_es310-$(date +%Y%m%d-%H%M%S).log
mkdir -p "$D/logs/es310"
exec > >(tee "$LOG") 2>&1
for k in 4 8 16; do for l in a b; do
  [ -f "$T/test-calib-k$k-$l/manifest-E310BT.json" ] || { echo "missing $T/test-calib-k$k-$l"; exit 2; }
done; done
tctl() { sensors 2>/dev/null | awk '/^Tctl:/{gsub(/[+°C]/,"",$2); print int($2); exit}'; }
wait_slot() {
  while :; do
    n=$(pgrep -xc lean); t=$(tctl)
    if [ "${n:-0}" -lt 2 ] && [ -n "$t" ] && [ "$t" -lt 85 ]; then return; fi
    sleep 3
  done
}
lane() {
  local l=$1; shift
  local ks=("$@")
  for r in $(seq 1 "$R"); do
    for k in "${ks[@]}"; do
      wait_slot
      echo "$(date -u +%FT%TZ) lane $l round $r k=$k start (Tctl $(tctl), lean procs $(pgrep -xc lean))"
      python3 "$D/drive_es310.py" "$T/test-calib-k$k-$l" --only E310BT.C240701 --bench 1 --jobs 1 --nice 10 \
          --no-final > "$T/test-calib-k$k-$l/drive-r$r.out" 2> "$T/test-calib-k$k-$l/drive-r$r.err"
      echo "$(date -u +%FT%TZ) lane $l round $r k=$k exit $? $(tail -n 2 "$T/test-calib-k$k-$l/drive-r$r.out" | head -n 1)"
    done
  done
}
lane a 4 8 16 &
PA=$!
sleep 2
lane b 8 16 4 &
PB=$!
wait $PA $PB
echo "== summary (median over runs; verdict ok only)"
python3 - "$T" <<'EOF'
import csv, statistics, sys
T = sys.argv[1]
for k in (4, 8, 16):
    rows = []
    for l in "ab":
        rows += [r for r in csv.DictReader(open(f"{T}/test-calib-k{k}-{l}/run.tsv"), delimiter="\t")]
    ok = [r for r in rows if r["verdict"] == "ok"]
    ks = sorted(float(r["kernel_s"]) for r in ok)
    ws = sorted(float(r["wall_s"]) for r in ok)
    us = sorted(float(r["user_s"]) for r in ok)
    ob = sorted({int(r["olean_bytes"]) for r in ok})
    print(f"k={k:2d} runs={len(rows)} ok={len(ok)} olean_bytes={ob} kernel_s={ks} median={statistics.median(ks):.2f} "
          f"wall median={statistics.median(ws):.2f} user median={statistics.median(us):.2f} "
          f"rss max={max(int(r['peak_rss_kb']) for r in ok)} cg max={max(int(r['cg_peak_kb']) for r in ok)}")
EOF
