#!/usr/bin/env bash
# compare_b.sh [TSV]: for every row of ref/hashes.tsv (made by ref/make_ref.py from gen_b2.py), emit the base CNF
# with the Lean exe and compare the SHA-256 of its bytes with the recorded one. A row with status FAIL:* (gen_b2.py
# raised) must make the exe refuse (exit 1, no output). Prints one line per instance and a summary; exit 0 iff all agree.
# Run from anywhere; run inside the memory-capped, nice'd scope described in ../README.md.
set -u -o pipefail
cd "$(dirname "$0")/.."
TSV=${1:-ref/hashes.tsv}
EXE=.lake/build/bin/encb_dimacs
[ -x "$EXE" ] || { echo "build first: lake build"; exit 2; }
ok=0; bad=0; t_all=$(date +%s.%N)
while IFS=$'\t' read -r m K t status sha rest; do
  case "$m" in \#*|'') continue;; esac
  t0=$(date +%s.%N)
  if [ "$status" = OK ]; then
    got=$("$EXE" base "$m" "$K" "$t" 2>/dev/null | sha256sum | cut -c1-64); rc=$?
    if [ $rc -eq 0 ] && [ "$got" = "$sha" ]; then r=MATCH; ok=$((ok+1)); else r="MISMATCH rc=$rc lean=$got python=$sha"; bad=$((bad+1)); fi
  else
    out=$("$EXE" base "$m" "$K" "$t" 2>/dev/null | wc -c); rc=$?
    "$EXE" stats "$m" "$K" "$t" >/dev/null 2>&1; rc=$?
    if [ $rc -eq 1 ] && [ "$out" -eq 0 ]; then r="REFUSED (python $status)"; ok=$((ok+1)); else r="NOT-REFUSED rc=$rc bytes=$out (python $status)"; bad=$((bad+1)); fi
  fi
  printf '%s\t%s\t%s\t%s\t%.2fs\n' "$m" "$K" "$t" "$r" "$(echo "$(date +%s.%N) - $t0" | bc)"
done < "$TSV"
printf 'SUMMARY agree=%d disagree=%d total_seconds=%.1f\n' "$ok" "$bad" "$(echo "$(date +%s.%N) - $t_all" | bc)"
[ "$bad" -eq 0 ]
