#!/bin/bash
# res118-lean: compile the Res118 modules with the bare Lean 4.24.0 binary (no lake), one after the other.
# Usage: tools/build.sh Module [Module ...]   e.g. tools/build.sh Rows LemmaA Glue Final Adapter
# Reads only existing olean stores (LEAN_PATH below); writes only under this work directory.
set -u
D=/home/jay/research/data/formalize-20261122/res118
LEAN=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean:$R/experiments/omission-compact-checker-2026-11-05/build/chain311/olean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$D/olean"
mkdir -p $D/olean/Res118 $D/logs
cd $D/lean
for a in "$@"; do
  # a module given as X means Res118/X; a path with a slash (or BalancedBudgetsZ) is relative to lean/
  case "$a" in */*|BalancedBudgetsZ) mp=$a ;; *) mp=Res118/$a ;; esac
  m=${mp//\//_}
  mkdir -p $(dirname $D/olean/$mp)
  echo "== $mp $(date -Is)"
  /usr/bin/time -v -o $D/logs/$m.time $LEAN -j1 -R $D/lean -o $D/olean/$mp.olean $D/lean/$mp.lean > $D/logs/$m.log 2>&1
  rc=$?
  echo "rc=$rc" >> $D/logs/$m.log
  echo "$mp rc=$rc $(grep -E 'Maximum resident|Elapsed' $D/logs/$m.time | tr -s ' ' | tr '\n' ' ')"
  if [ $rc -ne 0 ]; then echo "STOP at $m"; exit $rc; fi
done
echo "ALL OK $(date -Is)"
