#!/bin/bash
# Bare-lean build of the Std-only package N66E15 (this directory only). usage: build.sh [modules...]
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66-level15
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
export LEAN_PATH="$ENCB/.lake/build/lib/lean:$D/build/olean"
mkdir -p $D/build/olean/N66E15 $D/build/ir/N66E15 $D/build/obj $D/build/bin $D/logs
MODS=${@:-States Atoms Clauses Alloc Cover Rows Full Print Main DecodeA DecodeB Bridge}
cd $D/lean
for m in $MODS; do
  if [ "${TIMEFMT:-}" = "-v" ]; then T=(-v); else T=(-f "$m lean wall=%e s maxrss=%M KB"); fi
  /usr/bin/time "${T[@]}" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/N66E15/$m.olean -i $D/build/olean/N66E15/$m.ilean -c $D/build/ir/N66E15/$m.c N66E15/$m.lean
done
