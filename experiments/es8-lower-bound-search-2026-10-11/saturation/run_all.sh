#!/bin/sh
# Reproduce the saturation test (single-threaded, sequential).
#
#   sh experiments/es8-lower-bound-search-2026-10-11/saturation/run_all.sh
#
# Binaries, temporary files and fresh outputs go to $BUILD_DIR, by default the
# git-ignored .cache/es8-lower-bound-search-2026-10-11/saturation/ under the
# repository root. The committed ./out/ is only read: the last step compares
# the fresh outputs with it (timing fields and progress times excluded).
# Override the compiler with CC / CFLAGS. On a macOS host whose default SDK
# cannot link, export SDKROOT to an installed SDK.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
REPO=$(cd "$HERE/../../.." && pwd)
BUILD_DIR=${BUILD_DIR:-"$REPO/.cache/es8-lower-bound-search-2026-10-11/saturation"}
mkdir -p "$BUILD_DIR/out"
BUILD_DIR=$(cd "$BUILD_DIR" && pwd)
export BUILD_DIR PYTHONDONTWRITEBYTECODE=1
OUT="$BUILD_DIR/out"
CC=${CC:-cc}
CFLAGS=${CFLAGS:-"-O2 -Wall -Wextra"}
$CC $CFLAGS -o "$BUILD_DIR/sat" "$HERE/sat.c"
$CC $CFLAGS -o "$BUILD_DIR/verify" "$HERE/verify.c"
# The committed witnesses must equal the output of scripts/es_lower_bound_witness.py.
python3 - "$REPO/scripts" "$BUILD_DIR" <<'EOF'
import sys
sys.path.insert(0, sys.argv[1])
from es_lower_bound_witness import witness
for n in (5, 6, 7, 8):
    open(f"{sys.argv[2]}/witness{n}.txt", "w").write("".join(f"{x} {y}\n" for x, y in witness(n)))
EOF
for n in 5 6 7 8; do cmp "$BUILD_DIR/witness$n.txt" "$HERE/witness$n.txt"; done
cd "$HERE"
python3 brute_test.py 1 80         > "$OUT/brute_test.txt";             cat "$OUT/brute_test.txt"
python3 random_crosscheck.py 7 40  > "$OUT/random_crosscheck_seed7.txt"; cat "$OUT/random_crosscheck_seed7.txt"
python3 random_crosscheck.py 11 40 > "$OUT/random_crosscheck_seed11.txt"; cat "$OUT/random_crosscheck_seed11.txt"
for n in 5 6 7 8; do
  "$BUILD_DIR/sat" sat witness$n.txt $n "$OUT/bad$n.txt" "$OUT/cert$n.txt" > "$OUT/sat$n.json" 2> "$OUT/sat$n.log"
  "$BUILD_DIR/verify" witness$n.txt $n "$OUT/cert$n.txt" "$OUT/unc$n.txt" > "$OUT/verify$n.json" 2> "$OUT/verify$n.log"
  cat "$OUT/sat$n.json" "$OUT/verify$n.json"
done
python3 independent.py witness5.txt 5 "$OUT/bad5.txt" > "$OUT/independent5.json"; cat "$OUT/independent5.json"
python3 independent.py witness6.txt 6 "$OUT/bad6.txt" > "$OUT/independent6.json"; cat "$OUT/independent6.json"
python3 spotcheck.py 6 100 1 > "$OUT/spot6.json"; cat "$OUT/spot6.json"
python3 spotcheck.py 7 300 3 > "$OUT/spot7.json"; cat "$OUT/spot7.json"
python3 spotcheck.py 8 40 4  > "$OUT/spot8.json"; cat "$OUT/spot8.json"
# Compare with the committed outputs.
python3 - "$HERE/out" "$OUT" <<'EOF'
import json, os, re, sys
old, new = sys.argv[1], sys.argv[2]
timing = {"cpu_seconds", "seconds"}
def norm(path):
    text = open(path).read()
    if path.endswith(".json"):
        return {k: v for k, v in json.loads(text).items() if k not in timing}
    return re.sub(r"t=[0-9.]+s", "t=", text)
names = sorted(f for f in os.listdir(old) if os.path.isfile(os.path.join(old, f)))
diff = [f for f in names if norm(os.path.join(old, f)) != norm(os.path.join(new, f))]
print(json.dumps({"files_compared_with_committed_out": len(names), "differences": diff}))
sys.exit(1 if diff else 0)
EOF
