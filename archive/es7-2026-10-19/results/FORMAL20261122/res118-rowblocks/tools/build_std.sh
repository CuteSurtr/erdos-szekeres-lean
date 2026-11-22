#!/bin/bash
# Bare-lean build of the Std-only modules RowEnc.* (oleans, ileans and IR C under build/), the IR C of the
# hash-pinned Res118/Rows.lean (no olean), and the exe build/bin/rowprint (leanc).
set -euo pipefail
source /home/jay/research/data/formalize-20261122/res118-rowblocks/tools/env_std.sh
mkdir -p $D/build/olean/RowEnc $D/build/ir/RowEnc $D/build/ir/Res118 $D/build/obj $D/build/bin
MODS=${@:-StatesData States Enc Main}
cd $D/lean
for m in $MODS; do
  /usr/bin/time -v -o $D/logs/time_std_$m.txt $TC/bin/lean -j1 -R . \
    -o $D/build/olean/RowEnc/$m.olean -i $D/build/olean/RowEnc/$m.ilean -c $D/build/ir/RowEnc/$m.c RowEnc/$m.lean
  grep -E "Maximum resident|Elapsed" $D/logs/time_std_$m.txt | sed "s/^/$m: /"
done
echo "Rows.lean sha256: $(sha256sum $R118/lean/Res118/Rows.lean | cut -c1-64) (pinned d19bbdbd252441324d36e60bd34801a2d7f4b52025a831b802790b01a34e41a8)"
[ "$(sha256sum $R118/lean/Res118/Rows.lean | cut -c1-64)" = d19bbdbd252441324d36e60bd34801a2d7f4b52025a831b802790b01a34e41a8 ]
[ -f $D/build/ir/Res118/Rows.c ] || $TC/bin/lean -j1 -R $R118/lean -c $D/build/ir/Res118/Rows.c $R118/lean/Res118/Rows.lean
for m in Gen Dimacs Coded Cover Render; do
  $TC/bin/leanc -c -O3 -DNDEBUG -o $D/build/obj/EncB_$m.o $ENCB/.lake/build/ir/EncB/$m.c
done
$TC/bin/leanc -c -O3 -DNDEBUG -o $D/build/obj/Res118_Rows.o $D/build/ir/Res118/Rows.c
for m in StatesData States Enc Main; do
  $TC/bin/leanc -c -O3 -DNDEBUG -o $D/build/obj/RowEnc_$m.o $D/build/ir/RowEnc/$m.c
done
$TC/bin/leanc -o $D/build/bin/rowprint $D/build/obj/*.o
sha256sum $D/build/bin/rowprint
