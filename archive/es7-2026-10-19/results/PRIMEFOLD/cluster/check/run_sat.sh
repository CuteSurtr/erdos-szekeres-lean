#!/bin/bash
# usage: run_sat.sh CNF   -> runs CaDiCaL 3.0.1 (ASCII LRAT proof) and lrat-check, appends a line to sat_results.log
# Set CADICAL and LRATCHECK to the two executables (defaults: found on PATH).
D=$(cd "$(dirname "$0")" && pwd)
CAD=${CADICAL:-cadical}
CHK=${LRATCHECK:-lrat-check}
cnf=$1
base=${cnf%.cnf}
proof=$base.lrat
start=$(date +%s)
$CAD -q -t 840 --lrat --no-binary "$cnf" "$proof" > "$base.out" 2>&1
end=$(date +%s)
res=$(grep '^s ' "$base.out")
line="$(basename $cnf): ${res:-'(no result)'} solve_s=$((end-start))"
if [ "$res" = "s UNSATISFIABLE" ]; then
  chk=$($CHK "$cnf" "$proof" 2>&1 | grep -E 'VERIFIED|FAILED|ERROR|error' | head -2 | tr '\n' ' ')
  line="$line lrat-check: $chk proof_bytes=$(stat -f %z "$proof") cnf_sha=$(shasum -a 256 "$cnf" | cut -c1-16) lrat_sha=$(shasum -a 256 "$proof" | cut -c1-16)"
else
  rm -f "$proof"
fi
echo "$line" | tee -a $D/sat_results.log
