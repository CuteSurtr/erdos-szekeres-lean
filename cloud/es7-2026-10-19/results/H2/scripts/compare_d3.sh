#!/usr/bin/env bash
# Byte-for-byte comparison of `lake exe d3_dimacs N K` with `results/E/tools/d3cnf.py N K`.
# usage: scripts/compare_d3.sh [N K]...   (default grid below); run after `lake build`.
set -euo pipefail
here="$(cd "$(dirname "$0")/.." && pwd)"
py="$here/../E/tools/d3cnf.py"
exe="$here/.lake/build/bin/d3_dimacs"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
if [ $# -eq 0 ]; then set -- 3 5 9 5 9 6 15 5 15 6 21 6 21 7 27 7; fi
fail=0
while [ $# -ge 2 ]; do
  n=$1; k=$2; shift 2
  python3 "$py" "$n" "$k" -o "$tmp/py.cnf" > /dev/null
  "$exe" "$n" "$k" "$tmp/lean.cnf"
  if cmp -s "$tmp/py.cnf" "$tmp/lean.cnf"; then
    echo "N=$n K=$k identical $(sha256sum < "$tmp/lean.cnf" | cut -c1-16)"
  else
    echo "N=$n K=$k DIFFERENT"; fail=1
  fi
done
exit $fail
