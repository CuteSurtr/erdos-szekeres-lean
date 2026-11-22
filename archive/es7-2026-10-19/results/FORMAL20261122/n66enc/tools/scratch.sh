#!/bin/bash
# compile one scratch file (no olean output) against build/olean
D=/home/jay/research/data/formalize-20261122/n66enc
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
export LEAN_PATH="$ENCB/.lake/build/lib/lean:$D/build/olean"
cd $D/scratch && /usr/bin/time -f "$1 wall=%e s maxrss=%M KB" $TC/bin/lean -j1 $1
