#!/bin/bash
# One review compile (slot lrv2): loads the worker's oleans read-only; no -o (writes no olean); output in review/.
set -uo pipefail
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
D=/home/jay/research/data/formalize-20261122/n66enc
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$ENCB/.lake/build/lib/lean:$D/build/olean"
cd $D/review
echo "LEAN_PATH=$LEAN_PATH"
sha256sum $D/build/olean/N66Geo/End.olean $D/build/olean/N66Enc/Full.olean $D/build/olean/N66Enc/Rows.olean /home/jay/research/data/bal186-20261119/zrow/leanz/olean/LemmaZ.olean
/usr/bin/time -v $TC/bin/lean -j1 ReviewN66.lean
echo "lean_rc=$?"
