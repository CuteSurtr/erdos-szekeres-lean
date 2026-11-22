#!/bin/bash
# Bare-lean build of the Mathlib-side modules RowGeo.* (this directory only), one after the other; stops at the
# first failure. usage: build_geo.sh Mod [Mod ...]
set -u
source /home/jay/research/data/formalize-20261122/res118-rowblocks/tools/env_geo.sh
mkdir -p $D/build/olean/RowGeo
cd $D/lean
for m in "$@"; do
  echo "== RowGeo.$m $(date -Is)"
  /usr/bin/time -v -o $D/logs/time_geo_$m.txt $TC/bin/lean -j1 -R . -o $D/build/olean/RowGeo/$m.olean \
    -i $D/build/olean/RowGeo/$m.ilean RowGeo/$m.lean > $D/logs/geo_$m.log 2>&1
  rc=$?
  echo "rc=$rc" >> $D/logs/geo_$m.log
  echo "RowGeo.$m rc=$rc $(grep -E 'Maximum resident|Elapsed' $D/logs/time_geo_$m.txt | tr -s ' ' | tr '\n' ' ')"
  if [ $rc -ne 0 ]; then CG=$(sed -n "s/^0:://p" /proc/self/cgroup); echo "cgroup memory.peak: $(cat /sys/fs/cgroup$CG/memory.peak 2>/dev/null)"; echo "STOP at $m"; cat $D/logs/geo_$m.log | head -60; exit $rc; fi
done
CG=$(sed -n "s/^0:://p" /proc/self/cgroup)
echo "cgroup memory.peak: $(cat /sys/fs/cgroup$CG/memory.peak 2>/dev/null) bytes"
echo "ALL OK $(date -Is)"
