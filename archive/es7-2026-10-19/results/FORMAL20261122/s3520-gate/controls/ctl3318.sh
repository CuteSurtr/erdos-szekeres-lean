#!/bin/bash
# s3520-gate control (22 Nov 2026): slice 3318 (LO33, 111 contexts, 1,907 leaves) exported by the reference
# (slice_export_w13fix.py) and by slice_export_v3.py with the driver's parameters; both must be byte-identical, and the
# chunk source must equal res-slices-fv's w13 control export (controls/w13/3318-C, made by slice_export_w13.py 20:01).
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate; C=$G/controls
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
L=/home/jay/research/data/lo33-20261113/bb_66_55_leanrows
XTRA=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/LO33N20261113/data/cert_66_55_leanrows/extra_66_55_leanrows.json
A=(3318 --budget 33 --master $L/master.json --ctxdir $L --extra $XTRA --unit-leaves 40000 --chunk-leaves 8000)
$G/tools/sampled.sh $C/ref3318.mem $PY -I -B $G/tools/slice_export_w13fix.py "${A[@]}" --out $C/ref3318 > $C/ref3318.out; echo "ref rc=$?"
$G/tools/sampled.sh $C/v3-3318.mem $PY -I -B $G/tools/slice_export_v3.py "${A[@]}" --out $C/v3-3318 > $C/v3-3318.out; echo "v3 rc=$?"
$PY -I -B $G/tools/cmp_export.py $C/ref3318 $C/v3-3318 3318; echo "cmp rc=$?"
cmp $C/v3-3318/src/RS3318/C000001.lean /home/jay/research/data/formalize-20261122/res-slices-fv/controls/w13/3318-C/src/RS3318/C000001.lean \
  && echo "v3 chunk = res-slices-fv w13 control chunk (byte-identical)" || echo "v3 chunk DIFFERS from the res-slices-fv w13 control chunk"
