#!/bin/sh
# Compare `lake exe etv_dimacs` with tools/etv/gen_etv.py byte for byte.
# Usage (from results/H, after `lake build`): scripts/compare_dimacs.sh [N A U K]...
# With no arguments a default grid of small instances is checked.
# Set XSB=1 to compare the `--xsb` variants.
set -eu
EXTRA=""
if [ "${XSB:-0}" = "1" ]; then EXTRA="--xsb"; fi
HERE=$(cd "$(dirname "$0")/.." && pwd)
GEN="$HERE/../../tools/etv/gen_etv.py"
EXE="$HERE/.lake/build/bin/etv_dimacs"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0
count=0
check() {
  python3 "$GEN" "$1" "$2" "$3" "$4" -o "$TMP/py.cnf" $EXTRA > /dev/null
  "$EXE" "$1" "$2" "$3" "$4" "$TMP/lean.cnf" $EXTRA
  if cmp -s "$TMP/py.cnf" "$TMP/lean.cnf"; then
    count=$((count + 1))
  else
    echo "MISMATCH N=$1 A=$2 U=$3 K=$4 $EXTRA"
    fail=1
  fi
}
if [ $# -ge 4 ]; then
  while [ $# -ge 4 ]; do
    check "$1" "$2" "$3" "$4"
    shift 4
  done
else
  for N in 0 1 2 3 4 5 6 7 9 12; do
    # gen_etv.py --xsb needs N >= 3 (it reads X[(1,2,3)]).
    if [ -n "$EXTRA" ] && [ "$N" -lt 3 ]; then continue; fi
    for A in 2 3 4 5 6 7; do
      for U in 2 3 4 5 6 7; do
        for K in 3 4 5 6 7 8; do
          check $N $A $U $K
        done
      done
    done
  done
fi
echo "identical: $count $EXTRA"
exit $fail
