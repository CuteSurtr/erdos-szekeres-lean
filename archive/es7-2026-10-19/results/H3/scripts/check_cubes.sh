#!/bin/bash
# Per-cube certification with a verified checker.
# Usage: check_cubes.sh CNF CUBEFILE OUT.jsonl [--timed] [FIRST [COUNT]]
#   For each cube c (lines `l1 … 0`, or `time l1 … 0` with --timed) write
#   cubeCnf F c = F ++ [[l] | l ∈ c]  (Mir.cubeCnf: header count + |c|, units appended),
#   run CaDiCaL with a textual LRAT proof and check it with cake_lpr.
#   Env: CADICAL, CAKE_LPR (binaries), TMPD (scratch dir), SOLVE_TIMEOUT (seconds, 0 = none).
#   CNF/proof files are deleted.
set -u
CNF="$1"; CUBES="$2"; OUT="$3"; shift 3
TIMED=0; if [ "${1:-}" = "--timed" ]; then TIMED=1; shift; fi
FIRST="${1:-1}"; COUNT="${2:-1000000000}"
: "${CADICAL:?}"; : "${CAKE_LPR:?}"; TMPD="${TMPD:-/tmp}"
read -r _ _ NV NC < <(head -1 "$CNF")
n=0
while read -r line; do
  n=$((n+1)); [ $n -lt $FIRST ] && continue; [ $n -ge $((FIRST+COUNT)) ] && break
  set -- $line; [ $TIMED = 1 ] && shift; [ "${1:-}" = "a" ] && shift
  lits=(); for t in "$@"; do [ "$t" = 0 ] && break; lits+=("$t"); done
  f="$TMPD/cube$n.cnf"; p="$TMPD/cube$n.lrat"
  { echo "p cnf $NV $((NC + ${#lits[@]}))"; tail -n +2 "$CNF"; for l in "${lits[@]}"; do echo "$l 0"; done; } > "$f"
  t0=$(date +%s.%N)
  timeout "${SOLVE_TIMEOUT:-0}" "$CADICAL" -q --elim=0 --lrat --binary=false "$f" "$p" > /dev/null; st=$?
  t1=$(date +%s.%N)
  if [ $st = 20 ]; then
    v=$("$CAKE_LPR" "$f" "$p" 2>&1 | tr '\n' ' '); pb=$(stat -c %s "$p")
  else v="solver exit $st"; pb=0; fi
  t2=$(date +%s.%N)
  printf '{"n": %d, "cube": [%s], "solver_exit": %d, "solve_s": %.2f, "proof_bytes": %d, "cake_lpr": "%s", "check_s": %.2f}\n' \
    $n "$(IFS=,; echo "${lits[*]}")" $st "$(echo "$t1 - $t0" | bc)" $pb "${v% }" "$(echo "$t2 - $t1" | bc)" >> "$OUT"
  rm -f "$f" "$p"
done < "$CUBES"
