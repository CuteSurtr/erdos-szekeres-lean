#!/bin/bash
# Compile modules of this work dir with the bare lean, in order (inside a unit); stop at the first failure.
# usage: lc.sh [-c] Pkg/Mod ...   (-c also writes the IR C to build/ir, for the printer exes)
# Writes build/olean/<Pkg/Mod>.olean (+ .ilean), logs/lc/<Pkg_Mod>.log (time -v), one line per module in logs/lc.log.
set -u
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
source $D/tools/env.sh
OD=${OLEAN:-$D/build/olean}
C=0; [ "${1:-}" = "-c" ] && { C=1; shift; }
cd $D/lean
for m in "$@"; do
  mkdir -p $OD/$(dirname $m) $D/build/ir/$(dirname $m)
  log=$D/logs/lc/$(echo $m | tr / _).log
  extra=(); [ $C = 1 ] && extra=(-c $D/build/ir/$m.c)
  { echo "== $(date '+%F %T') lean $m"; /usr/bin/time -v $TC/bin/lean -j1 -R . -o $OD/$m.olean -i $OD/$m.ilean "${extra[@]}" $m.lean; echo "rc=$?"; } > $log 2>&1
  rc=$(tail -1 $log)
  echo "$(date '+%T') $m $rc $(grep Elapsed $log | awk '{print $NF}') $(grep 'Maximum resident' $log | awk '{print $NF}')" >> $D/logs/lc.log
  [ "$rc" = "rc=0" ] || { echo "FAIL $m"; exit 1; }
done
echo OK
