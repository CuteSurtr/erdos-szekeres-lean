#!/bin/bash
# Exe-to-theorem freeze: regenerate the IR C of the linked modules from the current sources and compare byte for
# byte with build/ir (what link.sh compiled into the exe); check the exe is newer than every linked .c; write the
# final manifest (sources, IR, ENCBLEAN IR, exe, tools, ref).
D=/home/jay/research/data/formalize-20261122/ae33-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
F=$D/build/freeze; rm -rf $F; mkdir -p $F/olean/AE33Enc $F/ir
cd $D/lean
ok=1
for m in Basic Clause Gen Data Main; do
  LEAN_PATH="$TC/lib/lean:$ENCB/.lake/build/lib/lean:$F/olean" $TC/bin/lean -j1 -R . -o $F/olean/AE33Enc/$m.olean \
    -c $F/ir/$m.c AE33Enc/$m.lean > /dev/null 2>&1 || { echo "compile FAIL $m"; ok=0; }
  if cmp -s $F/ir/$m.c $D/build/ir/AE33Enc/$m.c; then echo "ir same $m"; else echo "ir DIFF $m"; ok=0; fi
done
exe_m=$(stat -c %Y $D/build/bin/ae33print)
for c in $D/build/ir/AE33Enc/{Basic,Clause,Gen,Data,Main}.c; do
  [ $(stat -c %Y $c) -le $exe_m ] || { echo "linked .c newer than exe: $c"; ok=0; }
done
echo "exe sha256 $(sha256sum $D/build/bin/ae33print | cut -c1-64) (link2.log: $(tail -1 $D/logs/link2.log | cut -c1-64))"
echo "FREEZE $([ $ok = 1 ] && echo PASS || echo FAIL)"
cd $D
{ sha256sum lean/AE33Enc/*.lean lean/AE33Geo/*.lean build/ir/AE33Enc/{Basic,Clause,Gen,Data,Main}.c build/bin/ae33print \
    tools/*.sh tools/*.py ref/l2enc.cpp ref/ae33.txt ref/hashes_203.tsv DESIGN.md
  for m in Gen Dimacs Coded Cover Render; do sha256sum $ENCB/.lake/build/ir/EncB/$m.c; done; } > logs/final_manifest.sha256
echo "manifest lines $(wc -l < logs/final_manifest.sha256)"
rm -rf $F
