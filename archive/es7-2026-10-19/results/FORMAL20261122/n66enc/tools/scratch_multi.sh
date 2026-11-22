#!/bin/bash
D=/home/jay/research/data/formalize-20261122/n66enc
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
export LEAN_PATH="$ENCB/.lake/build/lib/lean:$D/build/olean"
cd $D/scratch
for f in "$@"; do
  /usr/bin/time -f "$f wall=%e s maxrss=%M KB exit=%x" timeout 4 $TC/bin/lean -j1 $f 2>&1 | head -5
done
