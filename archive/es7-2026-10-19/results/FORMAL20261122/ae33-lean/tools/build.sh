#!/bin/bash
# Bare-lean build of the Std-only modules AE33Enc/* (outputs only under build/).
# usage: build.sh [modules...]   (default: all, in dependency order)
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/ae33-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
export LEAN_PATH="$TC/lib/lean:$ENCB/.lake/build/lib/lean:$D/build/olean"
mkdir -p $D/build/olean/AE33Enc $D/build/ir/AE33Enc
MODS=${@:-Basic Clause Gen Data Main Bridge}
cd $D/lean
for m in $MODS; do
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/AE33Enc/$m.olean -i $D/build/olean/AE33Enc/$m.ilean -c $D/build/ir/AE33Enc/$m.c AE33Enc/$m.lean
done
