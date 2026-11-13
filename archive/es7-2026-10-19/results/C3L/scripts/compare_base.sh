#!/bin/sh
# Compare `c3_dimacs base m k` with `gen_case.py m k none` byte for byte.
# usage (from results/C3L, after `lake build`): scripts/compare_base.sh WORKDIR "m k" ["m k" ...]
set -e
W=$1; shift
for mk in "$@"; do
  set -- $mk
  python3 ../C3-S/tools/gen_case.py $1 $2 none -o "$W/py.cnf" > /dev/null
  .lake/build/bin/c3_dimacs base $1 $2 "$W/lean.cnf"
  if cmp -s "$W/py.cnf" "$W/lean.cnf"; then r=IDENTICAL; else r=DIFFERENT; fi
  echo "m=$1 k=$2 $(head -1 "$W/lean.cnf") $r $(sha256sum < "$W/lean.cnf" | cut -c1-64)"
  rm -f "$W/py.cnf" "$W/lean.cnf"
done
