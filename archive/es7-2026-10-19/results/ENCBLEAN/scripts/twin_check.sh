#!/usr/bin/env bash
# twin_check.sh [TSV] [EXTRA "m K t" ...]: encB = gen as Lean values, in compiled code, with no printing involved
# (`encb_dimacs twin-check`: same refusal, same nv, same clause list `encB m K t = (gen m K t).clauses.toList`).
# Runs every row of TSV (default ref/hashes.tsv) and then the extra instances given as arguments. A row with
# status FAIL:* must give BOTH-REFUSE; every other row must give EQUAL. Exit 0 iff all do.
# Run inside the memory-capped, nice'd scope described in ../README.md.
set -u -o pipefail
cd "$(dirname "$0")/.."
TSV=${1:-ref/hashes.tsv}; shift || true
EXE=.lake/build/bin/encb_dimacs
[ -x "$EXE" ] || { echo "build first: lake build"; exit 2; }
ok=0; bad=0; t_all=$(date +%s.%N)
check() {  # m K t expected(EQUAL|BOTH-REFUSE)
  local out t0; t0=$(date +%s.%N)
  out=$("$EXE" twin-check "$1" "$2" "$3" 2>/dev/null)
  if [[ "$out" == *" $4 "* ]] || [[ "$out" == *" $4" ]]; then ok=$((ok+1)); r=OK; else bad=$((bad+1)); r=FAIL; fi
  printf '%s\t%s\t%.2fs\n' "$r" "$out" "$(echo "$(date +%s.%N) - $t0" | bc)"
}
while IFS=$'\t' read -r m K t status rest; do
  case "$m" in \#*|'') continue;; esac
  if [ "$status" = OK ]; then check "$m" "$K" "$t" EQUAL; else check "$m" "$K" "$t" BOTH-REFUSE; fi
done < "$TSV"
for x in "$@"; do set -- $x; check "$1" "$2" "$3" EQUAL; done
printf 'SUMMARY twin-check ok=%d fail=%d total_seconds=%.1f\n' "$ok" "$bad" "$(echo "$(date +%s.%N) - $t_all" | bc)"
[ "$bad" -eq 0 ]
