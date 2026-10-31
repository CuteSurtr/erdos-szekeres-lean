#!/bin/sh
# Compare `lake exe trackb_dimacs` with tools/trackB/gen_cnf.py byte for byte.
# Usage (from results/H, after `lake build`):
#   scripts/compare_trackb.sh                      default grid, all option combinations
#   scripts/compare_trackb.sh N K [options...]     one instance
set -eu
HERE=$(cd "$(dirname "$0")/.." && pwd)
GEN="$HERE/../../tools/trackB/gen_cnf.py"
EXE="$HERE/.lake/build/bin/trackb_dimacs"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0
count=0
check() {
  n=$1
  k=$2
  shift 2
  python3 "$GEN" "$n" "$k" "$@" -o "$TMP/py.cnf" > /dev/null
  "$EXE" "$n" "$k" "$TMP/lean.cnf" "$@"
  if cmp -s "$TMP/py.cnf" "$TMP/lean.cnf"; then
    count=$((count + 1))
  else
    echo "MISMATCH N=$n K=$k $*"
    fail=1
  fi
}
if [ $# -ge 2 ]; then
  check "$@"
else
  for N in 3 4 5 6 7 8 9 12; do
    for K in 4 5 6 7 8; do
      check $N $K
      check $N $K --no-mono
      check $N $K --hull
      check $N $K --hull --mirror
      check $N $K --hull --mirror --no-mono
      check $N $K --flip
      check $N $K --flip --no-mono
    done
  done
fi
echo "identical: $count"
exit $fail
