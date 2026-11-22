#!/bin/bash
# Clean rebuild of every module into build/clean (fresh olean store), then compare with build/olean and print the
# axiom lines. Outputs only under build/clean and logs/.
set -uo pipefail
D=/home/jay/research/data/formalize-20261122/ae33-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
C=$D/build/clean
rm -rf $C; mkdir -p $C/AE33Enc $C/AE33Geo
LP_STD="$TC/lib/lean:$ENCB/.lake/build/lib/lean:$C"
LP_GEO="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:$ENCB/.lake/build/lib/lean:$C"
cd $D/lean
rc=0
for m in Basic Clause Gen Data Main Bridge; do
  /usr/bin/time -f "AE33Enc.$m wall=%e s maxrss=%M KB" env LEAN_PATH=$LP_STD $TC/bin/lean -j1 -R . -o $C/AE33Enc/$m.olean AE33Enc/$m.lean || rc=1
done
for m in Slot Sem Sound Pair Radius1 Audit; do
  [ -f AE33Geo/$m.lean ] || continue
  /usr/bin/time -f "AE33Geo.$m wall=%e s maxrss=%M KB" env LEAN_PATH=$LP_GEO $TC/bin/lean -j1 -R . -o $C/AE33Geo/$m.olean AE33Geo/$m.lean || rc=1
done
echo "rebuild rc=$rc"
for f in $(cd $C && find . -name '*.olean' | sort); do
  a=$(sha256sum $C/$f | cut -c1-64); b=$(sha256sum $D/build/olean/$f 2>/dev/null | cut -c1-64)
  [ "$a" = "$b" ] && echo "olean same $f" || echo "olean DIFF $f"
done
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "cgroup memory.peak=$(( $(cat $CG/memory.peak 2>/dev/null || echo 0) / 1048576 )) MB"
exit $rc
