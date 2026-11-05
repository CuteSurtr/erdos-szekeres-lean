#!/bin/bash
# End-to-end composition test of the compact ES(8) <= 311 recheck on real subtrees
# (6 November 2026): every module below one node, then that export's Root, which combines
# the subtree roots over the skeleton by split_pm and states the exclusion at the node's own
# path (pmask (zerosF n) path). Same caps as run_trial_es311.sh.
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
E=$(cd "$D/.." && pwd)
T=$D/build/es311/trial
JOBS=${JOBS:-3}
BAL=(--side balanced --source "$E/omission-cover-certificates-2026-10-10/balanced-v2-source.json"
     --tree "$E"/omission-final311-2026-10-14/certificate/tree-63.json.xz.part-*)
RES=(--side residual --source "$E/omission-residual32-rank-global-2026-10-10/source-2650.json.gz"
     --tree "$E"/omission-final313-2026-10-11/certificate/tree-2650-32.json.xz.part-*)
X=(systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 nice -n 5 python3 "$D/export_es311.py" --cache "$D/build/es311")
mkdir -p "$T"
# balanced node 789369: 15,064 leaves, depth 6; residual node 487209: 4,600 leaves, depth 8
[ -d "$T/B-sub789369-L5000-B64" ] || "${X[@]}" "${BAL[@]}" --out "$T/B-sub789369-L5000-B64" \
  --export-root 789369 --chunk-leaves 5000 --block-leaves 64 > "$T/B-sub789369-L5000-B64.export.json"
[ -d "$T/R-sub487209-L1000-B64" ] || "${X[@]}" "${RES[@]}" --out "$T/R-sub487209-L1000-B64" \
  --export-root 487209 --chunk-leaves 1000 --block-leaves 64 > "$T/R-sub487209-L1000-B64.export.json"
for tag in R-sub487209-L1000-B64 B-sub789369-L5000-B64; do
  python3 "$D/drive_es311.py" "$T/$tag" --jobs "$JOBS" || echo "driver on $tag: some module not ok"
done
