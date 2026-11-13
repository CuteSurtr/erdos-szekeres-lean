#!/bin/sh
# Cube-and-conquer of the monotone cube (S8.cnf: encoder A (8,9,16) + chord + cone + thr2 + cell rules B=2 +
# bin-order + all Y(i,j) units) over the 16 decision-list cubes on Z_i = Z(i,1) = [psi_i < 22.5 deg]:
#   c_r (r = 0..14): Z_1 .. Z_r true, Z_{r+1} false;   c_15: Z_1 .. Z_15 true.
# Every assignment of Z lies in exactly one cube (r + 1 = index of the first false Z).
# usage: cubes_mono.sh solve R...   |   cubes_mono.sh check R...
# solve: builds C/c_R/c_R.cnf (= S8.cnf + unit clauses), runs CaDiCaL with text LRAT, writes c_R/solved.
# check: waits for c_R/solved, runs cake_lpr, records hashes and verdicts in c_R/result.txt, compresses the proof.
set -u
W=${W:-<lb-k9oct-work-dir>}   # set W to the work directory
BASE=$W/sat/S8/S8.cnf
C=$W/sat/cubes
NV0=497697
HEAP=${HEAP:-11000}
mode=$1; shift
mkdir -p $C
for r in "$@"; do
  d=$C/c_$r; mkdir -p $d
  if [ "$mode" = solve ]; then
    [ -f $d/solved ] && continue
    : > $d/cube.units
    i=1; while [ $i -le $r ]; do echo "$((NV0 + i)) 0" >> $d/cube.units; i=$((i + 1)); done
    [ $r -lt 15 ] && echo "-$((NV0 + r + 1)) 0" >> $d/cube.units
    $W/tools/withunits.sh $BASE $d/cube.units $d/c_$r.cnf
    sha256sum $d/c_$r.cnf > $d/cnf.sha256
    t0=$(date +%s)
    cadical --lrat --binary=false $d/c_$r.cnf $d/proof.lrat > $d/cadical.out 2>&1; ec=$?
    echo "cadical exit $ec seconds $(( $(date +%s) - t0 ))" > $d/solved
  else
    while [ ! -f $d/solved ]; do sleep 20; done
    if ! grep -q "exit 20" $d/solved; then echo "c_$r: not UNSAT ($(cat $d/solved))" > $d/result.txt; continue; fi
    sha256sum $d/proof.lrat > $d/proof.sha256
    t0=$(date +%s)
    cake_lpr --CML_HEAP_SIZE=$HEAP --CML_STACK_SIZE=1000 $d/c_$r.cnf $d/proof.lrat > $d/cake.out 2> $d/cake.err
    v=$(grep -c "^s VERIFIED UNSAT" $d/cake.out)
    { echo "cube c_$r units: $(tr '\n' ' ' < $d/cube.units)"; cat $d/cnf.sha256 $d/proof.sha256; cat $d/solved;
      grep -E "conflicts:|total process time" $d/cadical.out | head -2;
      echo "proof bytes $(stat -c %s $d/proof.lrat)"; echo "cake_lpr seconds $(( $(date +%s) - t0 ))";
      echo "cake_lpr stdout: $(head -c 200 $d/cake.out | tr '\n' ' ')"; echo "cake_lpr stderr: $(head -c 200 $d/cake.err | tr '\n' ' ')";
      echo "VERIFIED_LINES $v"; } > $d/result.txt
    if [ "$v" = 1 ]; then
      zstd -q -3 -T1 --rm $d/proof.lrat -o $d/proof.lrat.zst && sha256sum $d/proof.lrat.zst >> $d/result.txt
      rm -f $d/c_$r.cnf
    fi
  fi
done
