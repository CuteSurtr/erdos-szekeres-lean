#!/bin/bash
# run_cover.sh CNF OBLIGATION TIMEOUT WORKDIR [lrat]   -> one JSON line (see cover.py)
# With "lrat", an UNSAT answer is
# checked with cake_lpr and the proof is deleted afterwards.
set -u
CNF=$1; OB=$2; T=$3; W=$4; MODE=${5:-}
HERE="$(cd "$(dirname "$0")" && pwd)"; BIN=${BIN:-/tmp/claude-0/w/bin}
name=$(echo "$OB" | tr ":," "_-"); d="$W/$name.$$"; mkdir -p "$d"
python3 "$HERE/cover.py" cnf "$CNF" "$OB" "$d/case.cnf"
sha=$(sha256sum "$d/case.cnf" | cut -d' ' -f1)
t0=$(date +%s.%N)
if [ "$MODE" = lrat ]; then
  "$BIN/cadical" --lrat --binary=false -t "$T" "$d/case.cnf" "$d/p.lrat" > "$d/out" 2>&1; rc=$?
else
  "$BIN/cadical" -t "$T" "$d/case.cnf" > "$d/out" 2>&1; rc=$?
fi
t1=$(date +%s.%N); st=$(printf "%.3f" "$(echo "$t1 - $t0" | bc)")
res=UNKNOWN; [ $rc = 20 ] && res=UNSAT; [ $rc = 10 ] && res=SAT
chk=null; ct=null; psz=null
if [ "$MODE" = lrat ] && [ $res = UNSAT ]; then
  psz=$(stat -c %s "$d/p.lrat")
  c0=$(date +%s.%N)
  "$BIN/cake_lpr" "$d/case.cnf" "$d/p.lrat" > "$d/chk" 2>&1
  c1=$(date +%s.%N); ct=$(printf "%.3f" "$(echo "$c1 - $c0" | bc)")
  chk="\"$(grep -m1 '^s ' "$d/chk" | tr -d '\n')\""
fi
[ $res = SAT ] && cp "$d/out" "$W/SAT_$name.out"
echo "{\"case\":\"$name\",\"obligation\":\"$OB\",\"cnf_sha256\":\"$sha\",\"timeout\":$T,\"result\":\"$res\",\"solve_s\":$st,\"proof_bytes\":$psz,\"cake_lpr\":$chk,\"check_s\":$ct}"
rm -rf "$d"
