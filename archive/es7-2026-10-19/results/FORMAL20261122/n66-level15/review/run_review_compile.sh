#!/bin/bash
# The one review compile (slot lrv3): bare lean against the worker's oleans, read-only LEAN_PATH (copied from the
# worker's tools/geo_env.sh), no -o (writes no olean); all output goes to review/.
set -uo pipefail
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
D=/home/jay/research/data/formalize-20261122/n66-level15
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$ENCB/.lake/build/lib/lean:$D/build/olean"
cd $D/review
echo "== start $(date '+%F %T')"
echo "LEAN_PATH=$LEAN_PATH"
echo "== olean hashes"
sha256sum $D/build/olean/N66G15/End.olean $D/build/olean/N66G15/Assembly.olean $D/build/olean/N66E15/Full.olean \
  $D/build/olean/N66E15/Rows.olean $D/build/olean/N66E15/Cover.olean $D/build/olean/N66E15/Bridge.olean \
  /home/jay/research/data/bal186-20261119/zrow/leanz/olean/LemmaZ.olean \
  $ENCB/.lake/build/lib/lean/EncB/Render.olean $ENCB/.lake/build/lib/lean/EncB/Dimacs.olean ReviewL15.lean
echo "== shadow check: LemmaZ / N66E15 / N66G15 / EncB on the LEAN_PATH (each should appear once)"
IFS=: read -ra DIRS <<< "$LEAN_PATH"
for d in "${DIRS[@]}"; do
  find "$d" -maxdepth 2 \( -name 'LemmaZ.olean' -o -name 'N66E15' -o -name 'N66G15' -o -name 'EncB' \
    -o -name 'N66E15.olean' -o -name 'N66G15.olean' -o -name 'EncB.olean' -o -name 'N66Enc' -o -name 'N66Geo' \) 2>/dev/null
done
echo "== compile"
/usr/bin/time -v $TC/bin/lean -j1 ReviewL15.lean
echo "lean_rc=$?"
echo "== end $(date '+%F %T')"
