#!/bin/bash
# Build the task-E tools.  usage: build.sh CADICAL_DIR OUT_BIN_DIR
# (CADICAL_DIR = a built CaDiCaL checkout with build/libcadical.a and src/cadical.hpp)
set -e
CAD="$1"; OUT="$2"
D="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT"
c++ -O2 -std=c++17 -o "$OUT/cnfeval" "$D/cnfeval.cpp"
cc -O2 -o "$OUT/geomcount" "$D/geomcount.c"
for f in ccworker assume_check; do
  if [ -f "$D/$f.cpp" ]; then
    c++ -O3 -std=c++17 -I"$CAD/src" -o "$OUT/$f" "$D/$f.cpp" "$CAD/build/libcadical.a"
  fi
done
ls -la "$OUT"
