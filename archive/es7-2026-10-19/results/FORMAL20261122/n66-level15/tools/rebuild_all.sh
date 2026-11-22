#!/bin/bash
# Clean rebuild of every module (Std-only N66E15, link of the printer, its stats, then Mathlib-side N66G15), in
# dependency order, then the source audit. Exit nonzero on the first failure.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66-level15
rm -rf $D/build/olean $D/build/ir
echo "== start $(date '+%F %T')"
TIMEFMT='-v' $D/tools/build.sh States
$D/tools/build.sh Atoms Clauses Alloc Cover Rows Full Print Main DecodeA DecodeB Bridge
echo "== link $(date '+%F %T')"
$D/tools/link.sh
echo "== stats"
/usr/bin/time -f "stats wall=%e s maxrss=%M KB" $D/build/bin/n66print15 stats
echo "== geo $(date '+%F %T')"
$D/tools/build_geo.sh Model Tail Assembly Facts Owners Small Final Families Sem Triple Quad Final3 Pos Final4 Pair \
  Final5 MirrorA MirrorB Final6 CapCup End
echo "== audit (forbidden tokens in lean/; comments included)"
grep -rnE '\bsorry\b|\badmit\b|native_decide|implemented_by|@\[extern|\bunsafe\b|^axiom |^opaque |ofReduceBool|debug.skipKernelTC|#eval|run_cmd' $D/lean --include=*.lean || echo "audit: none found"
echo "== leftover level-14 identifiers"
grep -rnE 'N66Enc|N66Geo|tree14|leaves132|CubesUnsat132|\bR0\b[^_]' $D/lean --include=*.lean || echo "none found"
echo "== done $(date '+%F %T')"
