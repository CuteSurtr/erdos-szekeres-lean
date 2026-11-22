#!/bin/bash
# Compile the IR C files and link the two printer exes (runs inside a unit). Read-only inputs: ENCBLEAN's Lake IR
# of EncB.{Gen,Dimacs,Coded,Cover,Render} and n66-level15's IR of N66E15.{States,Atoms,Clauses,Alloc,Cover} (freeze
# manifest verified before use); this dir's IR of N66R15Enc.*. Objects only under build/obj.
#   build/bin/n66r15print  cube printer: EncB + N66E15 (no Rows/Full/Print) + RowsD* + RowList + Print + Main
#   build/bin/r15rowprint  certificate printer: EncB + N66E15.States + Gen + DataT* + DataC* + RowMain
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
L15=/home/jay/research/data/formalize-20261122/n66-level15
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
O=$D/build/obj
mkdir -p $O $D/build/bin
rm -f $O/*.o
cc() { /usr/bin/time -f "$2 cc wall=%e s maxrss=%M KB" $TC/bin/leanc -c -O1 -DNDEBUG -o $O/$2.o $1; }
for m in Gen Dimacs Coded Cover Render; do cc $ENCB/.lake/build/ir/EncB/$m.c EncB_$m; done
for m in States Atoms Clauses Alloc Cover; do cc $L15/build/ir/N66E15/$m.c N66E15_$m; done
RD=$(cd $D/build/ir/N66R15Enc && ls RowsD*.c | sed 's/\.c$//')
for m in $RD RowList Print Main Gen DataT0 DataT1 DataT2 DataT3 DataT DataC0 DataC1 DataC2 DataC3 DataC RowMain; do
  cc $D/build/ir/N66R15Enc/$m.c N66R15Enc_$m
done
CUBE="$O/EncB_*.o $O/N66E15_*.o $O/N66R15Enc_RowsD*.o $O/N66R15Enc_RowList.o $O/N66R15Enc_Print.o $O/N66R15Enc_Main.o"
ROW="$O/EncB_*.o $O/N66E15_States.o $O/N66R15Enc_Gen.o $O/N66R15Enc_Data*.o $O/N66R15Enc_RowMain.o"
$TC/bin/leanc -o $D/build/bin/n66r15print $CUBE
$TC/bin/leanc -o $D/build/bin/r15rowprint $ROW
echo "cube link: $(echo $CUBE | tr ' ' '\n' | xargs -n1 basename | tr '\n' ' ')"
echo "row link:  $(echo $ROW | tr ' ' '\n' | xargs -n1 basename | tr '\n' ' ')"
sha256sum $D/build/bin/n66r15print $D/build/bin/r15rowprint
