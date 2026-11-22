#!/bin/bash
# Reviewer job (slot lrv3), run as one unit: (1) rebuild the worker's theorem modules from the snapshot review/src into
# review/olean (own kernel check of the sources read); (2) compile review/src/Fidelity.lean against them (axioms,
# statements, definitions, restatements); (3) compare the rebuilt oleans with the worker's build/olean; (4) sample the
# exe against L18's kept CNFs (byte comparison). Writes only under review/. Read-only on everything else.
set -u
D=/home/jay/research/data/formalize-20261122/ae33-lean
V=$D/review
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
L18=/home/jay/research/data/roadmap-20261115/pm1115/l1118/e72
X=$D/build/bin/ae33print
O=$V/olean
rm -rf $O; mkdir -p $O/AE33Enc $O/AE33Geo $V/logs
LP_STD="$TC/lib/lean:$ENCB/.lake/build/lib/lean:$O"
LP_GEO="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:$ENCB/.lake/build/lib/lean:$O"
echo "LP_GEO=$LP_GEO"
cd $V/src
rc=0
for m in Basic Clause Gen Data Bridge; do
  /usr/bin/time -f "AE33Enc.$m wall=%e s maxrss=%M KB" env LEAN_PATH=$LP_STD $TC/bin/lean -j1 -R . \
    -o $O/AE33Enc/$m.olean AE33Enc/$m.lean > $V/logs/build_Enc_$m.log 2>&1
  r=$?; echo "AE33Enc.$m rc=$r errors=$(grep -c 'error' $V/logs/build_Enc_$m.log) $(tail -1 $V/logs/build_Enc_$m.log)"
  [ $r -eq 0 ] || rc=1
done
for m in Slot Sem Sound Pair Radius1; do
  /usr/bin/time -f "AE33Geo.$m wall=%e s maxrss=%M KB" env LEAN_PATH=$LP_GEO $TC/bin/lean -j1 -R . \
    -o $O/AE33Geo/$m.olean AE33Geo/$m.lean > $V/logs/build_Geo_$m.log 2>&1
  r=$?; echo "AE33Geo.$m rc=$r errors=$(grep -c 'error' $V/logs/build_Geo_$m.log) $(tail -1 $V/logs/build_Geo_$m.log)"
  [ $r -eq 0 ] || rc=1
done
echo "rebuild rc=$rc"
/usr/bin/time -f "Fidelity wall=%e s maxrss=%M KB" env LEAN_PATH=$LP_GEO $TC/bin/lean -j1 -R . Fidelity.lean \
  > $V/logs/fidelity.out 2>&1
echo "fidelity rc=$?"
for f in AE33Enc/Basic AE33Enc/Clause AE33Enc/Gen AE33Enc/Data AE33Enc/Bridge AE33Geo/Slot AE33Geo/Sem AE33Geo/Sound \
         AE33Geo/Pair AE33Geo/Radius1; do
  a=$(sha256sum $O/$f.olean | cut -c1-64); b=$(sha256sum $D/build/olean/$f.olean | cut -c1-64)
  [ "$a" = "$b" ] && echo "olean same $f $a" || echo "olean DIFF $f mine=$a worker=$b"
done
echo "exe sha256 start $(sha256sum $X | cut -c1-64)"
T=$V/tmp; mkdir -p $T
for i in 109 110 202; do
  nm=$($X name $i)
  /usr/bin/time -f "exe cnf $i wall=%e s maxrss=%M KB" $X cnf $i > $T/exe.cnf
  zstd -q -dc $L18/cnf/$nm.cnf.zst > $T/kept.cnf
  cmp -s $T/exe.cnf $T/kept.cnf && same=1 || same=0
  echo "sample $i $nm exe_sha=$(sha256sum < $T/exe.cnf | cut -c1-64) kept_sha=$(sha256sum < $T/kept.cnf | cut -c1-64) cmp_same=$same bytes=$(stat -c %s $T/exe.cnf) header=$(head -1 $T/exe.cnf)"
  rm -f $T/exe.cnf $T/kept.cnf
done
rmdir $T
echo "exe sha256 end $(sha256sum $X | cut -c1-64)"
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "cgroup memory.peak=$(( $(cat $CG/memory.peak 2>/dev/null || echo 0) / 1048576 )) MB"
exit $rc
