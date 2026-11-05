#!/bin/bash
# Sequential single-core compiles for gate G2 (LEAN_NUM_THREADS=1).
cd /home/jay/research/lean/erdos-szekeres-lean
D=experiments/omission-compact-checker-2026-11-05
export LEAN_NUM_THREADS=1 OMP_NUM_THREADS=1
for m in "$@"; do
  echo "== $m $(date +%T)"
  lake env bash -c "LEAN_PATH=\$LEAN_PATH:$PWD/$D/build /usr/bin/time -f '%e s %M KB' lean -R $D -o $D/build/CompactChecker/$m.olean $D/CompactChecker/$m.lean" > $D/logs/$m.log 2>&1
  echo "exit=$? $(tail -1 $D/logs/$m.log) olean=$(stat -c %s $D/build/CompactChecker/$m.olean 2>/dev/null)"
done
echo "== done $(date +%T)"
