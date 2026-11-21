#!/bin/bash
# Remaining steps to compile the four chain-dependent target files on this Mac (lean-rebuild, 21 Nov 2026).
# Skips any .olean already built. One compile at a time.
# MEMORY: BalancedCoverCutsV2 needs about 19 GB (Linux chain311 record: 1106.6 s wall, max RSS 19,434,208 KB);
#         each Geometry module needs 6.7-8.5 GB (Linux record).
set -euo pipefail
A=SCRATCH/agents/lean-rebuild
TC=HOME_DIR/.elan/toolchains/leanprover--lean4---v4.24.0
LEAN=$TC/bin/lean
PK=$A/esb/.lake/packages
OUT=$A/olean
SRC=$A/chain/src
RES=$A/esb/archive/es7-2026-10-19/results
LP=""
for p in Cli batteries Qq aesop proofwidgets importGraph LeanSearchClient plausible mathlib; do LP="$LP$PK/$p/.lake/build/lib/lean:"; done
export LEAN_PATH="$LP$TC/lib/lean:$OUT"
mkdir -p $A/logs/remaining
run() { # log-name dir args...
  local n=$1 d=$2; shift 2
  local rc=0
  (cd "$d" && nice -n 10 /usr/bin/time -l "$LEAN" -j1 "$@") > $A/logs/remaining/$n.log 2>&1 || rc=$?
  echo "$n rc=$rc $(grep -E 'real|maximum resident' $A/logs/remaining/$n.log | tr -s ' ' | tr '\n' ' ')"
  return $rc
}
# 1. Geometry modules not yet built (84 in all)
for f in "$SRC"/Geometry*.lean; do
  m=$(basename "$f" .lean)
  [ -f "$OUT/$m.olean" ] || run "$m" "$SRC" -s 32768 -R . -o "$OUT/$m.olean" -i "$OUT/$m.ilean" "$m.lean"
done
# 2. BalancedRows
[ -f "$OUT/BalancedRows.olean" ] || run BalancedRows "$SRC" -s 32768 -R . -o "$OUT/BalancedRows.olean" -i "$OUT/BalancedRows.ilean" BalancedRows.lean
[ "${STOP_AFTER_ROWS:-0}" = 1 ] && { echo "stopped after BalancedRows (STOP_AFTER_ROWS=1)"; python3 $A/cmp_chain.py; exit 0; }
# 3. BalancedCoverCutsV2 (about 19 GB)
[ -f "$OUT/BalancedCoverCutsV2.olean" ] || run BalancedCoverCutsV2 "$SRC" -s 32768 -R . -o "$OUT/BalancedCoverCutsV2.olean" -i "$OUT/BalancedCoverCutsV2.ilean" BalancedCoverCutsV2.lean
# 4. The four target files (flags as in tools/build.sh, build_fixed.sh, build_zs.sh, build_zsn.sh)
run BalancedBudgetsZ   "$RES/ES305N20261119" -R . BalancedBudgetsZ.lean
run FixedStatesZ       "$RES/ES305N20261119" -R . -o "$OUT/FixedStatesZ.olean" -i "$OUT/FixedStatesZ.ilean" FixedStatesZ.lean
run BalancedBudgetsZZs "$RES/ES303N20261120" -R . -o "$OUT/BalancedBudgetsZZs.olean" -i "$OUT/BalancedBudgetsZZs.ilean" BalancedBudgetsZZs.lean
run BalancedBudgetsZZsN "$RES/ES303N20261120" -R . BalancedBudgetsZZsN.lean
# 5. #print axioms the files do not print themselves (zero_mem_occupied, one_mem_occupied, composition_303_zzsf, ...)
run ExtraAxioms "$A/axioms" -R . ExtraAxioms.lean
grep -h "depends on axioms" $A/logs/remaining/*.log
# 6. Compare the chain .olean files with the recorded Linux chain311 hashes
python3 $A/cmp_chain.py
