#!/bin/bash
# Bare-lean build of the Std-only package N66Enc (this directory only) and of the printer exe.
# usage: build.sh [modules...]   (default: all, in dependency order); then links build/bin/n66print.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66enc
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
export LEAN_PATH="$ENCB/.lake/build/lib/lean:$D/build/olean"
mkdir -p $D/build/olean/N66Enc $D/build/ir/N66Enc $D/build/obj $D/build/bin $D/logs
MODS=${@:-States Atoms Clauses Alloc Cover Rows Full Print Main DecodeA DecodeB Bridge}
cd $D/lean
for m in $MODS; do
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/N66Enc/$m.olean -i $D/build/olean/N66Enc/$m.ilean -c $D/build/ir/N66Enc/$m.c N66Enc/$m.lean
done
