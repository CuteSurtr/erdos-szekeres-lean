#!/bin/sh
# usage: [HEAP=MB] check.sh CUBEDIR   (cake_lpr on cube.cnf + proof.lrat; records hashes + verdict; on success zstd the
# proof and drop the cnf, which BASE0 + cube.units rebuilds with the recorded hash). Heap exhaustion -> file heapfail.
d=$1; HEAP=${HEAP:-8500}
[ -f $d/noproof ] && { echo "noproof probe (statistics only): $(cat $d/solved)" > $d/result.txt; exit 0; }
grep -q "exit 20" $d/solved || { echo "not UNSAT: $(cat $d/solved)" > $d/result.txt; exit 0; }
[ -f $d/proof.sha256 ] || sha256sum $d/proof.lrat > $d/proof.sha256
sha256sum -c $d/cnf.sha256 > $d/cnf.recheck 2>&1
t0=$(date +%s)
/usr/bin/time -v ~/.local/bin/cake_lpr --CML_HEAP_SIZE=$HEAP --CML_STACK_SIZE=1000 $d/cube.cnf $d/proof.lrat > $d/cake.out 2> $d/cake.err
if grep -qi "heap space exhausted" $d/cake.out $d/cake.err; then echo "heap $HEAP exhausted $(date +%T)" >> $d/heapfail; exit 0; fi
v=$(grep -c "^s VERIFIED UNSAT" $d/cake.out)
{ echo "cube $(basename $d): $(cat $d/cube.desc)"; echo "units: $(tr '\n' ' ' < $d/cube.units)"; cat $d/cnf.sha256 $d/proof.sha256 $d/cnf.recheck $d/solved;
  grep -E "^c conflicts:|total process time|maximum resident" $d/cadical.out;
  echo "proof bytes $(stat -c %s $d/proof.lrat)"; echo "cake_lpr seconds $(( $(date +%s) - t0 )) heap $HEAP";
  echo "cake_lpr binary sha256 $(sha256sum ~/.local/bin/cake_lpr | cut -c1-64)";
  echo "cake_lpr stdout: $(head -c 300 $d/cake.out | tr '\n' ' ')"; grep -E "Maximum resident|Elapsed" $d/cake.err;
  echo "VERIFIED_LINES $v"; } > $d/result.txt
if [ "$v" = 1 ]; then
  zstd -q -3 -T1 --rm $d/proof.lrat -o $d/proof.lrat.zst && sha256sum $d/proof.lrat.zst >> $d/result.txt && rm -f $d/cube.cnf
fi
