#!/bin/bash
# res118-lean negative controls: each file must FAIL to compile (expected rc != 0). Writes controls/logs/*.
set -u
D=/home/jay/research/data/formalize-20261122/res118
LEAN=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean
source <(grep '^R=\|^P=\|^export LEAN_PATH' $D/tools/build.sh)
mkdir -p $D/controls/olean
for m in BadLo BadGlue; do
  $LEAN -j1 -R $D/controls/lean -o $D/controls/olean/$m.olean $D/controls/lean/Res118Ctl/$m.lean > $D/controls/logs/$m.log 2>&1
  rc=$?
  echo "rc=$rc" >> $D/controls/logs/$m.log
  if [ $rc -ne 0 ]; then echo "$m: rejected as expected (rc=$rc)"; else echo "$m: UNEXPECTEDLY ACCEPTED"; fi
done
