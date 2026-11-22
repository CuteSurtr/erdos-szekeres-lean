#!/bin/bash
# Reviewer's single audit compile for res118-lean (slot lrev). Bare Lean 4.24.0, no lake, no -o (no olean written).
# Reads only existing olean stores (same LEAN_PATH as the worker's tools/build.sh); writes only review/logs/.
set -u
V=/home/jay/research/data/formalize-20261122/res118/review
D=/home/jay/research/data/formalize-20261122/res118
LEAN=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/bin/lean
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean:$R/experiments/omission-compact-checker-2026-11-05/build/chain311/olean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$D/olean"
cd $V/lean
echo "start $(date -Is) sha256 $(sha256sum Res118Review.lean | cut -c1-64)" > $V/logs/audit.meta
/usr/bin/time -v -o $V/logs/audit.time $LEAN -j1 $V/lean/Res118Review.lean > $V/logs/audit.log 2>&1
rc=$?
cg=/sys/fs/cgroup$(cut -d: -f3 /proc/self/cgroup)
{ echo "rc=$rc"; echo "end $(date -Is)"; echo "cgroup_memory_peak_bytes=$(cat $cg/memory.peak 2>/dev/null)"; } >> $V/logs/audit.meta
exit $rc
