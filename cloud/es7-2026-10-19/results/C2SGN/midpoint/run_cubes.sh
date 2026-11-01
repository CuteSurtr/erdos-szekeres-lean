#!/bin/bash
# Exploratory cube runs (no proofs): one CaDiCaL run per named cube of a "name lits..." file, cube literals as units.
# usage: run_cubes.sh CNF CUBES OUTDIR CAP_S NAME...   (appends {"cube", "exit", "wall_s"} lines to OUTDIR/res.jsonl)
F=$1; C=$2; O=$3; T=$4; shift 4
B=$(cd "$(dirname "$0")/../../local/bin" && pwd)     # results/local/bin, as for closesgn.py
mkdir -p "$O"
for nm in "$@"; do
  lits=$(awk -v n="$nm" '$1 == n {for (i = 2; i <= NF; i++) printf "%s ", $i}' "$C")
  k=$(echo $lits | wc -w | tr -d ' ')
  key=${nm//\//_}; G="$O/cube_$key.cnf"
  awk -v k="$k" '/^p cnf/ {print $1, $2, $3, $4 + k; next} {print}' "$F" > "$G"
  for l in $lits; do echo "$l 0" >> "$G"; done
  t0=$(date +%s)
  nice -n 5 "$B/cadical" -t "$T" -q "$G" > "$O/$key.out" 2>&1; ec=$?
  t1=$(date +%s)
  echo "{\"cube\": \"$nm\", \"exit\": $ec, \"wall_s\": $((t1 - t0))}" >> "$O/res.jsonl"
  rm -f "$G"
done
