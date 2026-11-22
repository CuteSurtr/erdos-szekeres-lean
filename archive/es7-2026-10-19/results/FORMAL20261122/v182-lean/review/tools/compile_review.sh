#!/bin/bash
# R2 (run inside ONE unit): rebuild everything behind the v182-lean theorems from source copies into review/build,
# then the audit files; relink the printer from own IR C and compare it with the frozen exe; compare own oleans with
# the worker's build_clean/ and ENCBLEAN's .lake. Writes only under review/. Log: review/logs/compile_review.log
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/v182-lean
RV=$D/review
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
B=$RV/build
FROZEN=b0b270cb5840bb92151900b77eb76ff8be1b71efd3dee93dbfe198ed6a531c5d
rm -rf $B $RV/src $RV/encb_src
mkdir -p $B/olean $B/ir/V182Enc $B/obj $B/bin $B/encb/olean/EncB $B/encb/ir/EncB $RV/src $RV/encb_src/EncB

# 1. source copies: the worker's lean/ tree (checked against its manifest) and ENCBLEAN's five modules
cp -r $D/lean/. $RV/src/
n=$(find $RV/src -name '*.lean' | wc -l)
( cd $RV && grep '  lean/' $D/logs/final_manifest.sha256 | sed 's#  lean/#  src/#' | sha256sum -c --strict --quiet ) \
  && echo "SRC_OK $n files = manifest" || { echo "SRC_MISMATCH"; exit 2; }
for m in Gen Dimacs Coded Cover Render; do
  cp $ENCB/EncB/$m.lean $RV/encb_src/EncB/
  g=$(git -C $R show HEAD:archive/es7-2026-10-19/results/ENCBLEAN/EncB/$m.lean | sha256sum | cut -c1-64)
  c=$(sha256sum $RV/encb_src/EncB/$m.lean | cut -c1-64)
  [ "$g" = "$c" ] && echo "ENCB_SRC_EQ_GIT_HEAD $m $c" || { echo "ENCB_SRC_NE_GIT_HEAD $m"; exit 2; }
done

# 2. ENCBLEAN's five modules from source (Init only)
cd $RV/encb_src
export LEAN_PATH="$TC/lib/lean:$B/encb/olean"
for m in Gen Dimacs Coded Cover Render; do
  /usr/bin/time -f "EncB.$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . -o $B/encb/olean/EncB/$m.olean \
    -i $B/encb/olean/EncB/$m.ilean -c $B/encb/ir/EncB/$m.c EncB/$m.lean || { echo "FAIL EncB.$m"; exit 3; }
  cmp -s $B/encb/olean/EncB/$m.olean $ENCB/.lake/build/lib/lean/EncB/$m.olean && echo "ENCB_OLEAN_SAME $m" || echo "ENCB_OLEAN_DIFF $m"
  cmp -s $B/encb/ir/EncB/$m.c $ENCB/.lake/build/ir/EncB/$m.c && echo "ENCB_IR_SAME $m" || echo "ENCB_IR_DIFF $m"
done

# 3. the v182 modules (Mathlib oleans read-only; EncB from step 2)
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$TC/lib/lean:$B/encb/olean:$B/olean"
cd $RV/src
fail=0
for m in V182Enc/Gen V182Enc/Main V182Geo/Defs V182Geo/Masks V182Geo/Sound V182Geo/Cover V182Geo/Norm V182Geo/SixData \
         V182Chk/WalkDefs V182Ctl/WalkMut V182Chk/WalkA V182Chk/WalkB V182Chk/Walk V182Geo/Six V182Geo/End; do
  mkdir -p $B/olean/$(dirname $m)
  extra=""
  case $m in V182Enc/*) extra="-c $B/ir/$m.c";; esac
  if ! /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . -o $B/olean/$m.olean -i $B/olean/$m.ilean $extra $m.lean; then
    echo "FAIL $m"; fail=1; break
  fi
  cmp -s $B/olean/$m.olean $D/build_clean/olean/$m.olean && echo "OLEAN_SAME_AS_WORKER $m" || echo "OLEAN_DIFF_FROM_WORKER $m"
done
echo "MODULES_EXIT $fail"

# 4. audit files (statements, axioms; non-vacuity checks)
cd $RV
if [ $fail -eq 0 ]; then
  /usr/bin/time -f "Audit lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 Audit.lean; echo "AUDIT_EXIT $?"
  /usr/bin/time -f "Sanity lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 Sanity.lean; echo "SANITY_EXIT $?"
fi

# 5. relink the printer from own IR C only; compare with the frozen exe
if [ $fail -eq 0 ]; then
  for m in Gen Dimacs Coded Cover Render; do $TC/bin/leanc -c -O3 -DNDEBUG -o $B/obj/EncB_$m.o $B/encb/ir/EncB/$m.c; done
  for m in Gen Main; do $TC/bin/leanc -c -O3 -DNDEBUG -o $B/obj/V182Enc_$m.o $B/ir/V182Enc/$m.c; done
  $TC/bin/leanc -o $B/bin/v182print $B/obj/*.o
  h=$(sha256sum $B/bin/v182print | cut -c1-64)
  echo "MY_EXE $h"
  [ "$h" = "$FROZEN" ] && echo "EXE_REPRODUCES_FROZEN" || echo "EXE_DIFFERS_FROM_FROZEN"
  cmp -s $B/bin/v182print $D/build/bin/v182print && echo "EXE_SAME_AS_M9_FILE" || echo "EXE_DIFF_FROM_M9_FILE"
  cmp -s $B/ir/V182Enc/Gen.c $D/build/ir/V182Enc/Gen.c && echo "GEN_IR_SAME_AS_M9" || echo "GEN_IR_DIFF_FROM_M9"
  cmp -s $B/ir/V182Enc/Main.c $D/build/ir/V182Enc/Main.c && echo "MAIN_IR_SAME_AS_M9" || echo "MAIN_IR_DIFF_FROM_M9"
fi
echo "COMPILE_REVIEW_DONE"
