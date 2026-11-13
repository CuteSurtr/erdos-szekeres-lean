#!/bin/sh
# Compare existing gen_cnf.py outputs named nNkK[h][m].cnf (h = --hull, m = --mirror)
# in DIR with `lake exe trackb_dimacs`, byte for byte.
# Usage (from results/H, after `lake build`): scripts/compare_trackb_dir.sh DIR
set -eu
HERE=$(cd "$(dirname "$0")/.." && pwd)
EXE="$HERE/.lake/build/bin/trackb_dimacs"
DIR=$1
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
fail=0
for f in "$DIR"/n*k*.cnf; do
  b=$(basename "$f" .cnf)
  rest=${b#n}
  N=${rest%%k*}
  t=${rest#*k}
  K=$(echo "$t" | tr -d 'hm')
  opts=""
  case "$t" in *h*) opts="$opts --hull";; esac
  case "$t" in *m*) opts="$opts --mirror";; esac
  "$EXE" "$N" "$K" "$TMP/lean.cnf" $opts
  if cmp -s "$TMP/lean.cnf" "$f"; then
    echo "identical $b"
  else
    echo "DIFFERENT $b"
    fail=1
  fi
done
exit $fail
