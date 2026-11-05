#!/bin/bash
# Scaling trial of the compact ES(8) <= 311 recheck on real 311 data (6 November 2026).
# Exports selected chunk modules of both certificate trees (export_es311.py --only) and
# compiles them with drive_es311.py --bench, under the caps of the 6 November ground rules
# (one lean -j1 process per module, MemoryMax=12G, CPUQuota=100%, nice 5; at most 3 at a time,
# so that with one other build at most 4 processes run). Results: build/es311/trial/*/run.tsv,
# summarised by summarize_trial_es311.py into logs/es311/trial-*.tsv.
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
E=$(cd "$D/.." && pwd)
T=$D/build/es311/trial
JOBS=${JOBS:-3}
RUNS=${RUNS:-2}
BAL=(--side balanced --source "$E/omission-cover-certificates-2026-10-10/balanced-v2-source.json"
     --tree "$E"/omission-final311-2026-10-14/certificate/tree-63.json.xz.part-*)
RES=(--side residual --source "$E/omission-residual32-rank-global-2026-10-10/source-2650.json.gz"
     --tree "$E"/omission-final313-2026-10-11/certificate/tree-2650-32.json.xz.part-*)
X=(systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 nice -n 5 python3 "$D/export_es311.py" --cache "$D/build/es311")

export1() {  # export1 TAG SIDE-ARRAY-NAME ARGS...
  local tag=$1 side=$2; shift 2
  local -n S=$side
  [ -f "$T/$tag/manifest-"*.json ] 2>/dev/null && return 0
  "${X[@]}" "${S[@]}" --out "$T/$tag" "$@" > "$T/$tag.export.json" || { echo "export $tag failed"; exit 1; }
}
mkdir -p "$T"
# modules: the first one, then the largest in the middle third and in the last third
export1 B-L1000-B64  BAL --chunk-leaves 1000 --block-leaves 64   --only 1,711,1087
export1 B-L5000-B64  BAL --chunk-leaves 5000 --block-leaves 64   --only 1,75,193
export1 R-L1000-B64  RES --chunk-leaves 1000 --block-leaves 64   --only 1,380,577
export1 R-L5000-B64  RES --chunk-leaves 5000 --block-leaves 64   --only 1,67,124
export1 B-L1000-B256 BAL --chunk-leaves 1000 --block-leaves 256  --only 711
export1 B-L1000-B1000 BAL --chunk-leaves 1000 --block-leaves 1000 --only 711
export1 R-L1000-B256 RES --chunk-leaves 1000 --block-leaves 256  --only 380
export1 R-L1000-B1000 RES --chunk-leaves 1000 --block-leaves 1000 --only 380
# rejection test: module 1 with one weight of its least-margin leaf changed (margin 1 -> -5)
export1 BX-L1000-B64 BAL --prefix E311BX --chunk-leaves 1000 --block-leaves 64 --only 1 --corrupt 1
# one larger module per side (the largest in the middle third at a 20,000-leaf limit), 1 run
export1 B-L20000-B64 BAL --chunk-leaves 20000 --block-leaves 64 --only 25
export1 R-L20000-B64 RES --chunk-leaves 20000 --block-leaves 64 --only 16
# (end-to-end Root tests on two real subtrees: run_e2e_es311.sh)
for tag in "$@"; do
  python3 "$D/drive_es311.py" "$T/$tag" --jobs "$JOBS" --bench "$RUNS" || echo "driver on $tag: some module not ok"
done
