#!/bin/bash
# Bare-lean build of the Std-only modules V182Enc/* (this directory only). usage: build.sh [modules...]
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/v182-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
export LEAN_PATH="$ENCB/.lake/build/lib/lean:$TC/lib/lean:$D/build/olean"
mkdir -p $D/build/olean/V182Enc $D/build/ir/V182Enc
MODS=${@:-Gen Main}
cd $D/lean
for m in $MODS; do
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/V182Enc/$m.olean -i $D/build/olean/V182Enc/$m.ilean -c $D/build/ir/V182Enc/$m.c V182Enc/$m.lean
done
