#!/bin/bash
# s3520-gate (22 Nov 2026): import-memory noise and slope. Base3520 twice, Imp2080 (the 57 chunk modules of unit 2080,
# import only) twice, then imptest.sh (all finished RS3519 oleans of res-slices-fv + the gate's RS3520 oleans).
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate; C=$G/controls/rootmem
for r in 1 2; do
  $G/tools/sampled.sh $C/Base3520_r$r.mem $G/tools/compile.sh $C/Base3520.lean $C/olean/Base3520.olean $C/Base3520_r$r.log $C; echo "base r$r rc=$? $(cut -d' ' -f1-3 $C/Base3520_r$r.mem)"
  $G/tools/sampled.sh $C/Imp2080_r$r.mem $G/tools/compile.sh $C/Imp2080.lean $C/olean/Imp2080.olean $C/Imp2080_r$r.log $C; echo "Imp2080 r$r rc=$? $(cut -d' ' -f1-3 $C/Imp2080_r$r.mem) $(grep -E 'Elapsed' $C/Imp2080_r$r.log | tr -s ' ')"
done
$C/imptest.sh
