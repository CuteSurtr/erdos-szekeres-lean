#!/bin/bash
# Full export of both ES(8) <= 311 certificate trees for the compact recheck (6 November 2026),
# then the independent coverage check of both manifests. This writes sources only; compiling
# them is the full run (drive_es311.py build/es311/full --jobs N), which is NOT started here.
#   export_full_es311.sh [CHUNK_LEAVES] [BLOCK_LEAVES]     (defaults 5000 and 64)
set -u -o pipefail
D=$(cd "$(dirname "$0")" && pwd)
E=$(cd "$D/.." && pwd)
L=${1:-5000}
B=${2:-64}
OUT=$D/build/es311/full
LOG=$D/logs/es311
mkdir -p "$OUT" "$LOG"
CAP=(systemd-run --user --scope --quiet -p MemoryMax=12G -p MemorySwapMax=0 nice -n 5)
"${CAP[@]}" python3 "$D/export_es311.py" --cache "$D/build/es311" --out "$OUT" \
  --side balanced --source "$E/omission-cover-certificates-2026-10-10/balanced-v2-source.json" \
  --tree "$E"/omission-final311-2026-10-14/certificate/tree-63.json.xz.part-* \
  --chunk-leaves "$L" --block-leaves "$B" > "$LOG/full-export-E311B.json" &
"${CAP[@]}" python3 "$D/export_es311.py" --cache "$D/build/es311" --out "$OUT" \
  --side residual --source "$E/omission-residual32-rank-global-2026-10-10/source-2650.json.gz" \
  --tree "$E"/omission-final313-2026-10-11/certificate/tree-2650-32.json.xz.part-* \
  --chunk-leaves "$L" --block-leaves "$B" > "$LOG/full-export-E311R.json" &
wait
"${CAP[@]}" python3 "$D/coverage_es311.py" "$OUT/manifest-E311B.json" --expect-leaves 782437 \
  > "$LOG/full-coverage-E311B.json"; echo "coverage E311B exit $?"
"${CAP[@]}" python3 "$D/coverage_es311.py" "$OUT/manifest-E311R.json" --expect-leaves 437579 \
  > "$LOG/full-coverage-E311R.json"; echo "coverage E311R exit $?"
du -sb "$OUT/src" | tee "$LOG/full-export-du.txt"
