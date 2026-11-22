#!/bin/bash
# s3520-gate negative control (22 Nov 2026): unit 2080 (ctx-4274) exported by slice_export_v3.py with --corrupt 2080:21
# (module 21, the unit's smallest: one weight of its minimum-margin leaf changed until the exact full-load margin is
# <= 0; the exporter's own leaf test must then fail on that leaf only) into a SEPARATE directory controls/neg2080, and
# only that module compiled, into controls/olean-neg. Accepted as a negative control only if Lean rejects it: rc != 0,
# the log has "decide proved that the proposition", and no olean exists.
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate; C=$G/controls
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
S=/home/jay/research/data/es308-20261114
mkdir -p $C/neg2080
cp -p $G/export/3520/prepass.json $C/neg2080/prepass.json
$G/tools/sampled.sh $C/neg2080_exp.mem $PY -I -B $G/tools/slice_export_v3.py 3520 --budget 35 --master $S/runs/b35s20/bb-s1/master.json \
  --ctxdir $S/runs/b35s20/bb-s1 --extra $S/inputs/b35s20-v169/extra.json --out $C/neg2080 --unit-leaves 40000 \
  --chunk-leaves 8000 --corrupt 2080:21 > $C/neg2080_exp.out; echo "export rc=$? $(tail -1 $C/neg2080_exp.out)"
cmp -s $C/neg2080/src/RS3520/C208021.lean $G/export/3520/src/RS3520/C208021.lean && echo "ALERT: corrupted module equals the good one"
for mm in 01 20 22; do cmp -s $C/neg2080/src/RS3520/C2080$mm.lean $G/export/3520/src/RS3520/C2080$mm.lean \
  && echo "module $mm unchanged by the corruption (as expected)" || echo "module $mm DIFFERS (unexpected)"; done
$G/tools/sampled.sh $C/neg2080_lean.mem $G/tools/compile.sh $C/neg2080/src/RS3520/C208021.lean $C/olean-neg/RS3520/C208021.olean \
  $C/neg2080_lean.log $C/neg2080/src; rc=$?
if [ $rc -ne 0 ] && grep -q "proved that the proposition" $C/neg2080_lean.log && [ ! -e $C/olean-neg/RS3520/C208021.olean ]; then
  echo "NEGATIVE CONTROL: corrupted C208021 REJECTED by Lean as expected (rc=$rc)"
else
  echo "NEGATIVE CONTROL FAILED: rc=$rc -- ALERT"
fi
grep -n "proved that the proposition" $C/neg2080_lean.log | head -3 | cut -c1-300
