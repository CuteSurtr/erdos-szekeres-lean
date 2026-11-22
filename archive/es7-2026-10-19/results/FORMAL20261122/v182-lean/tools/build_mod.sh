#!/bin/bash
# Bare-lean build of modules given as paths under lean/ (e.g. V182Chk/Walk V182Geo/Six); Mathlib LEAN_PATH.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/v182-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
source $D/tools/geo_env.sh
cd $D/lean
for m in "$@"; do
  mkdir -p $D/build/olean/$(dirname $m)
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/$m.olean -i $D/build/olean/$m.ilean $m.lean
done
