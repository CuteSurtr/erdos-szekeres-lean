#!/bin/bash
# s3520-gate (22 Nov 2026): import-memory test. Writes ImpTest.lean importing every finished RS3519 chunk olean of
# res-slices-fv (listed now; finished oleans are not written any more; read-only) and every gate RS3520 chunk module
# with an olean, then compiles it under sampled.sh. No proofs; only the import cost is measured.
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate; C=$G/controls/rootmem; F=/home/jay/research/data/formalize-20261122/res-slices-fv
{ echo "-- s3520-gate import-memory test, listed $(date '+%F %T')"
  ls $F/olean/RS3519/ | grep '\.olean$' | sed 's/\.olean$//' | sort | sed 's/^/import RS3519./'
  ls $G/olean/RS3520/ | grep '^C.*\.olean$' | sed 's/\.olean$//' | sort | sed 's/^/import RS3520./'
  echo "open CompactChecker"; echo "#check @split_pm"; } > $C/ImpTest.lean
n19=$(grep -c '^import RS3519' $C/ImpTest.lean); n20=$(grep -c '^import RS3520' $C/ImpTest.lean)
b19=$(grep '^import RS3519' $C/ImpTest.lean | sed "s|import RS3519.|$F/olean/RS3519/|; s|$|.olean|" | xargs stat -c %s | awk '{s+=$1} END{print s}')
b20=$(grep '^import RS3520' $C/ImpTest.lean | sed "s|import RS3520.|$G/olean/RS3520/|; s|$|.olean|" | xargs stat -c %s | awk '{s+=$1} END{print s}')
echo "imports: RS3519 $n19 ($b19 olean bytes), RS3520 $n20 ($b20 olean bytes)"
$G/tools/sampled.sh $C/ImpTest.mem $G/tools/compile.sh $C/ImpTest.lean $C/olean/ImpTest.olean $C/ImpTest.log $C; echo "ImpTest rc=$? $(cut -d' ' -f1-3 $C/ImpTest.mem)"
grep -E "Elapsed|Maximum resident" $C/ImpTest.log
