#!/bin/bash
# run_open_ext.sh CNF INDEX TIMEOUT WORKDIR -> one JSON line.  INDEX is the 1-based line of
# results/H3/logs/open_cubes_ii_interior.txt; builds G_o (open_ext.py), cadical --lrat, cake_lpr.
set -u
CNF=$1; I=$2; T=$3; W=$4; HERE="$(cd "$(dirname "$0")" && pwd)"; BIN=${BIN:-/tmp/claude-0/w/bin}
o=$(sed -n "${I}p" "$HERE/../../H3/logs/open_cubes_ii_interior.txt" | sed 's/ 0$//; s/ /,/g')
d="$W/oe_$I.$$"; mkdir -p "$d"
python3 "$HERE/open_ext.py" "$CNF" "$o" "$d/g.cnf"
sha=$(sha256sum "$d/g.cnf" | cut -d' ' -f1)
t0=$(date +%s.%N); "$BIN/cadical" --lrat --binary=false -q -t "$T" "$d/g.cnf" "$d/p.lrat" > "$d/out" 2>&1; rc=$?
st=$(printf "%.3f" "$(echo "$(date +%s.%N) - $t0" | bc)")
res=UNKNOWN; [ $rc = 20 ] && res=UNSAT; [ $rc = 10 ] && res=SAT
chk=null; ct=null; psz=null
if [ $res = UNSAT ]; then
  psz=$(stat -c %s "$d/p.lrat"); c0=$(date +%s.%N)
  "$BIN/cake_lpr" "$d/g.cnf" "$d/p.lrat" > "$d/chk" 2>&1
  ct=$(printf "%.3f" "$(echo "$(date +%s.%N) - $c0" | bc)"); chk="\"$(grep -m1 '^s ' "$d/chk" | tr -d '\n')\""
fi
[ $res = SAT ] && cp "$d/g.cnf" "$W/SAT_open_$I.cnf" && "$BIN/cadical" -q "$d/g.cnf" > "$W/SAT_open_$I.model"
echo "{\"open_index\":$I,\"open_cube\":[${o}],\"cnf_sha256\":\"$sha\",\"timeout\":$T,\"result\":\"$res\",\"solve_s\":$st,\"proof_bytes\":$psz,\"cake_lpr\":$chk,\"check_s\":$ct}"
rm -rf "$d"
