#!/bin/bash
# Std-only compile with C output (for the printer exe). usage: lcc.sh <Pkg/Mod>...   (runs inside a unit)
set -u
D=/home/jay/research/data/formalize-20261122/n66-rowsvalid
source $D/tools/env.sh
mkdir -p $D/logs
cd $D/lean
for m in "$@"; do
  mkdir -p $D/build/olean/$(dirname $m) $D/build/ir/$(dirname $m)
  log=$D/logs/$(echo $m | tr / _).log
  { echo "== $(date '+%F %T') lean -c $m"; /usr/bin/time -v $TC/bin/lean -j1 -R . -o $D/build/olean/$m.olean -i $D/build/olean/$m.ilean -c $D/build/ir/$m.c $m.lean; echo "rc=$?"; } > $log 2>&1
  tail -1 $log | grep -q "rc=0" || { echo "FAIL $m"; exit 1; }
done
echo OK
