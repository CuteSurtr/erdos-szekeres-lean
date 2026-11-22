#!/bin/bash
# s3520-gate (22 Nov 2026): Root-memory calibration. Compiles (1) the import baseline Base3520 (RS.Cat3520 +
# CompactChecker.Path, the imports of every chunk module) and (2) the unit sub-root RS3520.U2080 (57 chunk imports,
# 320,422 leaves, 61 split_pm joins), each under sampled.sh (anon + shmem of this unit, every 0.5 s). ImpTest: imptest.sh.
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate; C=$G/controls/rootmem
$G/tools/sampled.sh $C/Base3520.mem $G/tools/compile.sh $C/Base3520.lean $C/olean/Base3520.olean $C/Base3520.log $C; echo "base rc=$? $(cut -d' ' -f1-3 $C/Base3520.mem)"
$G/tools/sampled.sh $G/logs/RS3520_U2080.mem $G/tools/compile.sh $G/export/3520/src/RS3520/U2080.lean $G/olean/RS3520/U2080.olean $G/logs/RS3520_U2080.log $G/export/3520/src; echo "U2080 rc=$? $(cut -d' ' -f1-3 $G/logs/RS3520_U2080.mem)"
grep -E "Elapsed|Maximum resident" $C/Base3520.log $G/logs/RS3520_U2080.log
grep "depends on axioms" $G/logs/RS3520_U2080.log
