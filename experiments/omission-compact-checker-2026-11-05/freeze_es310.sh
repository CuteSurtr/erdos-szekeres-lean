#!/bin/bash
# Freeze the ES(8) <= 310 pipeline (written 6 November 2026; ES(8) <= 310 is NOT proved). Run ONCE, by the
# operator, after the review and before the first real export (design G.3; operations review 9; soundness
# review item 6). It fills the four empty pins of assemble_final310.sh with the current sha256 of
#   export_es310.py -> EXPORTER_SHA256      merge_es310.py -> MERGE_SHA256
#   drive_es310.py  -> DRIVER_SHA256        coverage_es310.py -> COVERAGE_SHA256
# and writes a record of every pipeline file's sha256 and the chosen per-word k. Nothing else is changed;
# it compiles nothing and touches no build directory.
#
#   freeze_es310.sh K [--target FILE] [--record FILE]
#     K       the per-word k of the real export (calibration E5 recommends 16; it is recorded, and every later
#             export_es310.py command must use --per-word K)
#     --target the assembly script to fill (default: assemble_final310.sh next to this file; tests use a copy)
#     --record the record to write (default: logs/es310/frozen-shas.txt; refused if it exists)
#
# Refused (exit 1, nothing written) if any of the four pins is already set, if a file is missing, or if the
# record exists. After it: the sha256 of assemble_final310.sh has changed, so bash test_assemble_final310.sh
# must run again (gate 6), and none of the four scripts may be edited until the assembly is done.
set -euo pipefail
HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
K=${1:-}
[[ "$K" =~ ^[1-9][0-9]*$ ]] || { echo "usage: $0 K [--target FILE] [--record FILE]" >&2; exit 2; }
shift
TARGET=$HERE/assemble_final310.sh RECORD=$HERE/logs/es310/frozen-shas.txt
while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET=$2; shift 2 ;;
    --record) RECORD=$2; shift 2 ;;
    *) echo "unknown option $1" >&2; exit 2 ;;
  esac
done
[ -f "$TARGET" ] || { echo "freeze_es310: refused: no $TARGET" >&2; exit 1; }
[ ! -e "$RECORD" ] || { echo "freeze_es310: refused: $RECORD exists (already frozen?)" >&2; exit 1; }
for f in export_es310.py merge_es310.py drive_es310.py coverage_es310.py export_es311.py shapes_es311.py \
         assembly/Final310Compact.lean; do
  [ -f "$HERE/$f" ] || { echo "freeze_es310: refused: $HERE/$f is missing" >&2; exit 1; }
done
python3 -I - "$HERE" "$TARGET" <<'PY'
import hashlib, re, sys
from pathlib import Path
here, target = Path(sys.argv[1]), Path(sys.argv[2])
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
pins = {"EXPORTER_SHA256": "export_es310.py", "MERGE_SHA256": "merge_es310.py",
        "DRIVER_SHA256": "drive_es310.py", "COVERAGE_SHA256": "coverage_es310.py"}
t = target.read_text()
for var in pins:
    if t.count(f'\n{var}=""\n') != 1:
        sys.exit(f"freeze_es310: refused: {var} is not exactly one empty line '{var}=\"\"' in {target} "
                 "(already frozen?)")
for var, f in pins.items():
    t = t.replace(f'\n{var}=""\n', f"\n{var}={sha(here / f)}\n")
target.write_text(t)
print("filled:", ", ".join(f"{v}={sha(here / f)[:12]} ({f})" for v, f in pins.items()))
PY
mkdir -p "$(dirname "$RECORD")"
{ echo "# ES(8) <= 310 pipeline frozen $(date '+%F %T %Z') by freeze_es310.sh; per-word k = $K"
  echo "# every export_es310.py command from now on: --per-word $K --chunk-leaves 12000 --block-leaves 64"
  (cd "$HERE" && sha256sum export_es310.py merge_es310.py drive_es310.py coverage_es310.py export_es311.py \
     shapes_es311.py assembly/Final310Compact.lean freeze_es310.sh)
  echo "$(sha256sum < "$TARGET" | cut -c1-64)  $(basename "$TARGET") (after filling the pins)"
} > "$RECORD"
cat "$RECORD"
echo "next: bash test_assemble_final310.sh (the assembly script's sha256 changed); do not edit the frozen scripts"
