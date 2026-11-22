#!/bin/bash
# Bare-lean build of the Mathlib-side modules V182Geo/* (this directory only). usage: build_geo.sh Mod1 Mod2 ...
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/v182-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
source $D/tools/geo_env.sh
mkdir -p $D/build/olean/V182Geo
cd $D/lean
for m in "$@"; do
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/V182Geo/$m.olean -i $D/build/olean/V182Geo/$m.ilean V182Geo/$m.lean
done
