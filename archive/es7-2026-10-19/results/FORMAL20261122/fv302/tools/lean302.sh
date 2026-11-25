#!/bin/bash
# FV302: compile one Lean file to an .olean with the combined project's audited LEAN_PATH (env2.sh) plus the FV302 olean
# dir. Pinned v4.24.0 binary by path. Usage: lean302.sh SRC.lean OUT.olean LOG
set -u
. /home/jay/research/data/formalize-20261122/combined/tools/env2.sh
export LEAN_PATH="/home/jay/research/data/fv302-20261124/olean:$LEAN_PATH"
src=$1; out=$2; log=$3
mkdir -p "$(dirname "$out")"
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -o "$out.tmp" "$src" > "$log" 2>&1; rc=$?
if [ $rc -eq 0 ]; then mv "$out.tmp" "$out"; else rm -f "$out.tmp"; fi
echo "lean_rc=$rc" >> "$log"
exit $rc
