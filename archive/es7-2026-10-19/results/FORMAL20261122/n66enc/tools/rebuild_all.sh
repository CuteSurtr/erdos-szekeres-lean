#!/bin/bash
# Clean rebuild of every module (Std-only N66Enc, then Mathlib-side N66Geo) into build/olean, in dependency order,
# then the source audit. Exit nonzero on the first failure.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66enc
rm -rf $D/build/olean
$D/tools/build.sh States Atoms Clauses Alloc Cover Rows Full Print Main DecodeA DecodeB Bridge
$D/tools/build_geo.sh Model Tail Assembly Facts Owners Small Final Families Sem Triple Quad Final3 Pos Final4 Pair \
  Final5 MirrorA MirrorB Final6 CapCup End
echo "== audit (forbidden tokens in lean/; comments included)"
grep -rnE '\bsorry\b|\badmit\b|native_decide|implemented_by|@\[extern|\bunsafe\b|^axiom |^opaque |ofReduceBool' $D/lean --include=*.lean || echo "audit: none found"
