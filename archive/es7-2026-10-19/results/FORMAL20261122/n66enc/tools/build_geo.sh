#!/bin/bash
# Bare-lean build of the Mathlib-side modules N66Geo/* (this directory only).
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66enc
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
source $D/tools/geo_env.sh
mkdir -p $D/build/olean/N66Geo
cd $D/lean
for m in "$@"; do
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/N66Geo/$m.olean -i $D/build/olean/N66Geo/$m.ilean N66Geo/$m.lean
done
