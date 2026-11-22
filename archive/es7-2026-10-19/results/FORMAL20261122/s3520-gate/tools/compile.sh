#!/bin/bash
# s3520-gate: res-slices-fv/tools/compile.sh (a4965096...) with D = this directory. Compile one Lean file to an .olean
# with a read-only LEAN_PATH (no lake): the same stores as res-slices-fv (res-slices-fv/olean read-only for RS.Cat3520
# and the pinned CompactChecker oleans), plus this directory's olean/ LAST (the gate's RS3520.* chunk oleans).
# Usage: compile.sh SRC.lean OUT.olean LOG [ROOT]     (writes OUT only on rc 0; run inside an esr-s20-g-* unit)
set -u
G=/home/jay/research/data/formalize-20261122/s3520-gate
F=/home/jay/research/data/formalize-20261122/res-slices-fv
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
X=$R/experiments/omission-compact-checker-2026-11-05
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean:$X/build/chain311/olean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$F/olean:/home/jay/research/data/formalize-20261122/res118/olean:${GATE_OLEAN:-$G/olean}"
src=$1; out=$2; log=$3; root=${4:-$(pwd)}
case "$out" in "$G"/*) ;; *) echo "refusing to write outside $G: $out" >&2; exit 2 ;; esac
mkdir -p "$(dirname "$out")" "$(dirname "$log")"
/usr/bin/time -v /home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean -j1 -R "$root" -o "$out.tmp" "$src" > "$log" 2>&1; rc=$?
if [ $rc -eq 0 ]; then mv "$out.tmp" "$out"; else rm -f "$out.tmp"; fi
echo "lean_rc=$rc" >> "$log"
exit $rc
