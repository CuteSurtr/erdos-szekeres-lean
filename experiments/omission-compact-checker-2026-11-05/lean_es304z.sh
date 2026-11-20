#!/bin/bash
# FV304 (20 Nov 2026): compile one Lean file to an .olean with the FV304 LEAN_PATH (lake roots, build/chain311/olean,
# zrow/leanz/olean, the experiment's build/ for CompactChecker.*, and the FV304 olean dir). Run it inside an esv-*
# unit (memory guard esv). The v4.24.0 binary is called by path: elan resolves a bare `lean` outside the repo to its
# default toolchain (it auto-installed v4.36.0 on 20 Nov 18:39). Usage: lean_es304z.sh SRC.lean OUT.olean LOG
set -u
O=/home/jay/research/data/fv304-20261120
export LEAN_PATH=$(cat $O/lean_path.txt)
src=$1; out=$2; log=$3
mkdir -p "$(dirname "$out")"
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -o "$out.tmp" "$src" > "$log" 2>&1; rc=$?
if [ $rc -eq 0 ]; then mv "$out.tmp" "$out"; else rm -f "$out.tmp"; fi
echo "lean_rc=$rc" >> "$log"
exit $rc
