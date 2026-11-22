#!/bin/bash
# Clean rebuild of every module (RowEnc.*, RowGeo.*) and of the exe into build2/ (LEAN_PATH with build2/olean in
# place of build/olean); then compare sha256 of every olean and of the exe with build/.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/res118-rowblocks
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
R118=/home/jay/research/data/formalize-20261122/res118
B=$D/build2
rm -rf $B; mkdir -p $B/olean/RowEnc $B/olean/RowGeo $B/ir/RowEnc $B/ir/Res118 $B/obj $B/bin
cd $D/lean
export LEAN_PATH="$ENCB/.lake/build/lib/lean:$R118/olean:$B/olean"
for m in StatesData States Enc Main; do
  $TC/bin/lean -j1 -R . -o $B/olean/RowEnc/$m.olean -i $B/olean/RowEnc/$m.ilean -c $B/ir/RowEnc/$m.c RowEnc/$m.lean
done
$TC/bin/lean -j1 -R $R118/lean -c $B/ir/Res118/Rows.c $R118/lean/Res118/Rows.lean
for m in Gen Dimacs Coded Cover Render; do $TC/bin/leanc -c -O3 -DNDEBUG -o $B/obj/EncB_$m.o $ENCB/.lake/build/ir/EncB/$m.c; done
$TC/bin/leanc -c -O3 -DNDEBUG -o $B/obj/Res118_Rows.o $B/ir/Res118/Rows.c
for m in StatesData States Enc Main; do $TC/bin/leanc -c -O3 -DNDEBUG -o $B/obj/RowEnc_$m.o $B/ir/RowEnc/$m.c; done
$TC/bin/leanc -o $B/bin/rowprint $B/obj/*.o
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:$R/experiments/omission-compact-checker-2026-11-05/build/chain311/olean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$ENCB/.lake/build/lib/lean:$R118/olean:$B/olean"
for m in Decode Members Bridge Geo Sound Text Blocks; do
  $TC/bin/lean -j1 -R . -o $B/olean/RowGeo/$m.olean -i $B/olean/RowGeo/$m.ilean RowGeo/$m.lean > $B/$m.out 2>&1
done
cat $B/Blocks.out
cd $D
bad=0
for f in $(cd build/olean && ls RowEnc/*.olean RowGeo/*.olean) ; do
  a=$(sha256sum build/olean/$f | cut -c1-64); b=$(sha256sum build2/olean/$f | cut -c1-64)
  [ "$a" = "$b" ] && echo "SAME $f $a" || { echo "DIFF $f $a $b"; bad=1; }
done
a=$(sha256sum build/bin/rowprint | cut -c1-64); b=$(sha256sum build2/bin/rowprint | cut -c1-64)
[ "$a" = "$b" ] && echo "SAME rowprint $a" || { echo "DIFF rowprint $a $b"; bad=1; }
CG=$(sed -n "s/^0:://p" /proc/self/cgroup); echo "cgroup memory.peak: $(cat /sys/fs/cgroup$CG/memory.peak 2>/dev/null)"
exit $bad
