#!/bin/bash
# run_review.sh: the reviewer's ONE compile (unit esr-ag-lrv2-ax). Reads the worker's oleans; writes only here.
set -u
V=/home/jay/research/data/formalize-20261122/sevenfold/review
W=/home/jay/research/data/formalize-20261122/sevenfold
G=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN/geo
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
LP="$TC/lib/lean"
for p in aesop batteries importGraph LeanSearchClient mathlib plausible proofwidgets Qq; do LP="$LP:$G/.lake/packages/$p/.lake/build/lib/lean"; done
export LEAN_PATH="$LP:$W/olean"
cd "$V"
(cd "$W/olean" && find . -name '*.olean' | sort | xargs sha256sum) > "$V/oleans_before.sha256"
sha256sum "$V/ReviewSevenfold.lean" > "$V/review_source.sha256"
echo "# $(date -Is) LEAN_PATH=$LEAN_PATH" > "$V/review_compile.log"
/usr/bin/time -v -o "$V/review_compile.time" timeout 1800 "$TC/bin/lean" -j1 -R "$V" "$V/ReviewSevenfold.lean" >> "$V/review_compile.log" 2>&1
rc=$?
echo "rc=$rc $(date -Is)" >> "$V/review_compile.log"
(cd "$W/olean" && find . -name '*.olean' | sort | xargs sha256sum) > "$V/oleans_after.sha256"
if cmp -s "$V/oleans_before.sha256" "$V/oleans_after.sha256"; then echo "olean store unchanged during the compile" >> "$V/review_compile.log"; else echo "OLEAN STORE CHANGED during the compile" >> "$V/review_compile.log"; fi
exit $rc
