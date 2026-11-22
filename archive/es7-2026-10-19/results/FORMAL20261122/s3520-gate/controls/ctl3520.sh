#!/bin/bash
# s3520-gate control (22 Nov 2026): s35_20 units exported by the reference (slice_export_w13fix.py, json.loads of whole
# contexts) into controls/ref3520 and by slice_export_v3.py into the gate export export/3520 (same pre-pass, same cut,
# driver parameters); chunk sources and manifests must be byte-identical. Usage: ctl3520.sh UNIT [UNIT ...]
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate; C=$G/controls
PY=/home/jay/research/data/six10-linux-20261105/venv.disk/bin/python
S=/home/jay/research/data/es308-20261114
A=(3520 --budget 35 --master $S/runs/b35s20/bb-s1/master.json --ctxdir $S/runs/b35s20/bb-s1 --extra $S/inputs/b35s20-v169/extra.json
   --unit-leaves 40000 --chunk-leaves 8000)
mkdir -p $C/ref3520
cp -p $G/export/3520/prepass.json $C/ref3520/prepass.json           # the reference reuses the v3 pre-pass (same format)
for u in "$@"; do
  $G/tools/sampled.sh $C/ref3520_u$u.mem /usr/bin/time -v $PY -I -B $G/tools/slice_export_w13fix.py "${A[@]}" --out $C/ref3520 --units $u:$((u + 1)) > $C/ref3520_u$u.out 2> $C/ref3520_u$u.time; echo "ref unit $u rc=$? $(cat $C/ref3520_u$u.mem | cut -d' ' -f1-3)"
  $G/tools/sampled.sh $C/v3-3520_u$u.mem /usr/bin/time -v $PY -I -B $G/tools/slice_export_v3.py "${A[@]}" --out $G/export/3520 --units $u:$((u + 1)) > $C/v3-3520_u$u.out 2> $C/v3-3520_u$u.time; echo "v3 unit $u rc=$? $(cat $C/v3-3520_u$u.mem | cut -d' ' -f1-3)"
done
$PY -I -B $G/tools/cmp_export.py $C/ref3520 $G/export/3520 3520 "$@"; echo "cmp rc=$?"
