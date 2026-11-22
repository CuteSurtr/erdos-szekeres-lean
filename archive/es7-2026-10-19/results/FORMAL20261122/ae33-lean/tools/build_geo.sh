#!/bin/bash
# Bare-lean build of the Mathlib-side modules AE33Geo/* (outputs only under build/).
set -euo pipefail
D=/home/jay/research/data/formalize-20261122/ae33-lean
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
source $D/tools/geo_env.sh
mkdir -p $D/build/olean/AE33Geo
cd $D/lean
for m in "$@"; do
  /usr/bin/time -f "$m lean wall=%e s maxrss=%M KB" $TC/bin/lean -j1 -R . \
    -o $D/build/olean/AE33Geo/$m.olean -i $D/build/olean/AE33Geo/$m.ilean AE33Geo/$m.lean
done
CG=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
echo "cgroup memory.peak=$(( $(cat $CG/memory.peak 2>/dev/null || echo 0) / 1048576 )) MB"
