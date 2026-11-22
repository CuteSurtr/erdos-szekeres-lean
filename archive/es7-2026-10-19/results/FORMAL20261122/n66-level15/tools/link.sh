#!/bin/bash
# Compile the IR C files (N66E15 exe closure + the ENCBLEAN modules the printer executes) and link build/bin/n66print15.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/n66-level15
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
mkdir -p $D/build/obj $D/build/bin
rm -f $D/build/obj/*.o
for m in Gen Dimacs Coded Cover Render; do
  /usr/bin/time -f "EncB.$m cc wall=%e s maxrss=%M KB" $TC/bin/leanc -c -O3 -DNDEBUG -o $D/build/obj/EncB_$m.o $ENCB/.lake/build/ir/EncB/$m.c
done
for m in States Atoms Clauses Alloc Cover Rows Full Print Main; do
  /usr/bin/time -f "$m cc wall=%e s maxrss=%M KB" $TC/bin/leanc -c -O3 -DNDEBUG -o $D/build/obj/N66E15_$m.o $D/build/ir/N66E15/$m.c
done
$TC/bin/leanc -o $D/build/bin/n66print15 $D/build/obj/*.o
sha256sum $D/build/bin/n66print15
