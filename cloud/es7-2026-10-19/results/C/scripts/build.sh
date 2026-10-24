#!/bin/bash
# Build the Task C tools.  Usage: build.sh <cadical-dir> <bin-dir>
# (cadical-dir must contain build/libcadical.a and src/cadical.hpp)
set -e
CAD="$1"; BIN="$2"; HERE="$(cd "$(dirname "$0")" && pwd)"
TA="$HERE/../../../tools/trackA"
c++ -O2 -std=c++17 -I"$CAD/src" -o "$BIN/asolve" "$HERE/asolve.cpp" "$CAD/build/libcadical.a"
if [ -f "$HERE/cncw.cpp" ]; then
  c++ -O2 -std=c++17 -I"$CAD/src" -o "$BIN/cncw" "$HERE/cncw.cpp" "$CAD/build/libcadical.a"
fi
if [ -f "$HERE/mirann.c" ]; then
  cc -O3 -march=native -o "$BIN/mirann" "$HERE/mirann.c" -lm
fi
cc -O3 -o "$BIN/cgon" "$TA/cgon.c" -lm
echo built
