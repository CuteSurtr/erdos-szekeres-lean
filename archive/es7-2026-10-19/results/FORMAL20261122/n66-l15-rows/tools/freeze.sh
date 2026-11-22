#!/bin/bash
# Freeze manifest of the two printer exes (run right after the link, before any E1/M9 print): the exes, the Lean
# sources of their closures, the IR C and objects as linked, and the read-only IR C inputs (ENCBLEAN, n66-level15).
# usage: freeze.sh write | check
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
L15=/home/jay/research/data/formalize-20261122/n66-level15
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
M=$D/logs/freeze_manifest.sha256
if [ "${1:-}" = write ]; then
  sha256sum $D/build/bin/n66r15print $D/build/bin/r15rowprint $D/lean/N66R15Enc/*.lean $D/build/ir/N66R15Enc/*.c \
    $D/build/obj/*.o $ENCB/.lake/build/ir/EncB/{Gen,Dimacs,Coded,Cover,Render}.c \
    $L15/build/ir/N66E15/{States,Atoms,Clauses,Alloc,Cover}.c > $M
  echo "wrote $(wc -l < $M) entries"
else
  bad=$(sha256sum -c $M 2>/dev/null | grep -v ': OK$' | wc -l)
  echo "freeze check: $(sha256sum -c $M 2>/dev/null | grep -c ': OK$') OK, $bad not OK"
  [ "$bad" = 0 ]
fi
