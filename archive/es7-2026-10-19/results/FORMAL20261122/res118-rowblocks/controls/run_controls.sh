#!/bin/bash
# Lean negative controls: each file must be REJECTED by the compiler (rc != 0).
source /home/jay/research/data/formalize-20261122/res118-rowblocks/tools/env_geo.sh
cd $D/lean
ok=0
for f in BadSource BadFixed; do
  $TC/bin/lean -j1 -R . $D/controls/$f.lean > $D/controls/$f.out 2>&1
  rc=$?
  if [ $rc -ne 0 ]; then echo "$f: rejected as expected (rc=$rc): $(grep -m1 error $D/controls/$f.out)"; else echo "$f: ACCEPTED (control FAILED)"; ok=1; fi
done
exit $ok
