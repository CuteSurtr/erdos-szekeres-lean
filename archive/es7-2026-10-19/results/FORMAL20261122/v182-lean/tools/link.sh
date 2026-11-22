#!/bin/bash
# Compile the IR C files (V182Enc + the ENCBLEAN modules in the import closure) and link build/bin/v182print.
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/v182-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
mkdir -p $D/build/obj $D/build/bin
for m in Gen Dimacs Coded Cover Render; do
  /usr/bin/time -f "EncB.$m cc wall=%e s maxrss=%M KB" $TC/bin/leanc -c -O3 -DNDEBUG -o $D/build/obj/EncB_$m.o $ENCB/.lake/build/ir/EncB/$m.c
done
for m in Gen Main; do
  /usr/bin/time -f "$m cc wall=%e s maxrss=%M KB" $TC/bin/leanc -c -O3 -DNDEBUG -o $D/build/obj/V182Enc_$m.o $D/build/ir/V182Enc/$m.c
done
$TC/bin/leanc -o $D/build/bin/v182print $D/build/obj/*.o
sha256sum $D/build/bin/v182print
