#!/bin/bash
# Compile the IR C of RowEnc and link build/bin/rowprint with n66enc's objects of EncB.{Gen,Dimacs,Coded,Cover,Render}
# and N66Enc.States (read-only). Runs inside a unit.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
N66=/home/jay/research/data/formalize-20261122/n66enc
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
mkdir -p $D/build/obj $D/build/bin
for m in Gen DataT0 DataT1 DataT2 DataT3 DataT DataC0 DataC1 DataC2 DataC3 DataC Main; do
  /usr/bin/time -f "RowEnc.$m cc wall=%e s maxrss=%M KB" $TC/bin/leanc -c -O1 -DNDEBUG -o $D/build/obj/RowEnc_$m.o $D/build/ir/RowEnc/$m.c
done
$TC/bin/leanc -o $D/build/bin/rowprint $D/build/obj/RowEnc_*.o $N66/build/obj/EncB_*.o $N66/build/obj/N66Enc_States.o
sha256sum $D/build/bin/rowprint
