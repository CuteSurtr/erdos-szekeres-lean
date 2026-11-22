#!/bin/bash
# s3520-gate control (22 Nov 2026): --stop-after. Slice 3318 with v3 into a fresh directory with --stop-after 0 must
# print "stopped_before_unit", exit 0 and write no manifest; the rerun without the flag must give the same chunk as
# controls/v3-3318 (byte-identical).
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate; C=$G/controls; O=$C/stop3318
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
L=/home/jay/research/data/lo33-20261113/bb_66_55_leanrows
XTRA=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/data/cert_66_55_leanrows/extra_66_55_leanrows.json
A=(3318 --budget 33 --master $L/master.json --ctxdir $L --extra $XTRA --unit-leaves 40000 --chunk-leaves 8000 --out $O)
rm -rf $O
$PY -I -B $G/tools/slice_export_v3.py "${A[@]}" --stop-after 0; rc=$?
echo "stop-after 0: rc=$rc manifests=$(ls $O/ctx | wc -l) sources=$(ls $O/src/RS3318 | wc -l)"
$PY -I -B $G/tools/slice_export_v3.py "${A[@]}"; rc=$?
echo "rerun: rc=$rc manifests=$(ls $O/ctx | wc -l)"
cmp $O/src/RS3318/C000001.lean $C/v3-3318/src/RS3318/C000001.lean && echo "rerun chunk = controls/v3-3318 chunk (byte-identical)"
$PY -I -B $G/tools/cmp_export.py $C/v3-3318 $O 3318; echo "cmp rc=$?"
