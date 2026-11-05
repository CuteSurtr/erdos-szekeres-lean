#!/bin/bash
# implane2.sh CUBE.cnf : solve a transitivity-violating pattern, check with cake_lpr, keep all artifacts and hashes.
f=$1; b=${f%.cnf}
timeout 900 cadical --lrat --binary=false -q $f $b.lrat > $b.out 2>&1
res=$(grep -m1 -E '^s ' $b.out | cut -c3-)
cake_lpr --CML_HEAP_SIZE=8000 $f $b.lrat > $b.cake.log 2>&1
if grep -q '^s VERIFIED UNSAT' $b.cake.log; then v=VERIFIED; elif grep -q 'Checking failed' $b.cake.log; then v=REJECTED; else v=INTERRUPTED; fi
sha256sum $f $b.lrat $b.out $b.cake.log > $b.hashes.txt
printf "%s\t%s\t%s\n" "$f" "$res" "$v" >> imp2_results.tsv
