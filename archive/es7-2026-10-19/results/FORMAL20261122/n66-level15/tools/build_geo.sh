#!/bin/bash
# Bare-lean build of the Mathlib-side modules N66G15/* (this directory only).
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66-level15
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
source $D/tools/geo_env.sh
mkdir -p $D/build/olean/N66G15
cd $D/lean
for m in "$@"; do
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/N66G15/$m.olean -i $D/build/olean/N66G15/$m.ilean N66G15/$m.lean
done
