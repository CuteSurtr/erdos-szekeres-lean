#!/bin/bash
# Clean full rebuild (run inside one unit): every module from source into build_clean/, the printer exe relinked,
# its SHA-256 compared with the M9 exe; End's #guard_msgs axiom guards must pass. Log: logs/rebuild_all.log
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/v182-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
C=$D/build_clean
rm -rf $C; mkdir -p $C/olean $C/ir/V182Enc $C/obj $C/bin
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$TC/lib/lean:$ENCB/.lake/build/lib/lean:$C/olean"
cd $D/lean
fail=0
for m in V182Enc/Gen V182Enc/Main V182Geo/Defs V182Geo/Masks V182Geo/Sound V182Geo/Cover V182Geo/Norm V182Geo/SixData \
         V182Chk/WalkDefs V182Ctl/WalkMut V182Chk/WalkA V182Chk/WalkB V182Chk/Walk V182Geo/Six V182Geo/End; do
  mkdir -p $C/olean/$(dirname $m)
  extra=""
  case $m in V182Enc/*) extra="-c $C/ir/$m.c";; esac
  if ! /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . -o $C/olean/$m.olean -i $C/olean/$m.ilean $extra $m.lean; then
    echo "FAIL $m"; fail=1; break
  fi
done
if [ $fail -eq 0 ]; then
  for m in Gen Dimacs Coded Cover Render; do $TC/bin/leanc -c -O3 -DNDEBUG -o $C/obj/EncB_$m.o $ENCB/.lake/build/ir/EncB/$m.c; done
  for m in Gen Main; do $TC/bin/leanc -c -O3 -DNDEBUG -o $C/obj/V182Enc_$m.o $C/ir/V182Enc/$m.c; done
  $TC/bin/leanc -o $C/bin/v182print $C/obj/*.o
  echo "exe $(sha256sum $C/bin/v182print | cut -c1-64) (M9 exe b0b270cb5840bb92151900b77eb76ff8be1b71efd3dee93dbfe198ed6a531c5d)"
  cmp $C/bin/v182print $D/build/bin/v182print && echo "EXE_IDENTICAL"
  cmp $C/ir/V182Enc/Gen.c $D/build/ir/V182Enc/Gen.c && echo "GEN_IR_IDENTICAL"
  $C/bin/v182print base | sha256sum
fi
echo "REBUILD_EXIT $fail"
