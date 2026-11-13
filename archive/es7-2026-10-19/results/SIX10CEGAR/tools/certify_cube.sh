#!/bin/bash
# certify_cube.sh CUBE : CLI CaDiCaL 3.0.1 + LRAT on current.cnf + all shared cuts (snapshot) + the cube units;
# then lrat-check and cake_lpr (one at a time, lock); proof compressed with zstd, hashes recorded.
set -u
W="<run-dir>"; BIN="<bin>"
BASE="<proof-archives>/es8-rot-refine-2026-11-04/m6/current.cnf"
n=$1; C="$W/cert/$n"; mkdir -p "$C"; lits=$(grep "^$n"$'\t' "$W/cubes.txt" | cut -f3)
cp "$W/cuts.clauses" "$C/cuts_snapshot.clauses"; nc=$(wc -l < "$C/cuts_snapshot.clauses" | tr -d ' ')
nv=$(head -1 "$BASE" | awk '{print $3}'); nb=$(head -1 "$BASE" | awk '{print $4}'); nu=$(echo $lits | wc -w | tr -d ' ')
{ echo "p cnf $nv $((nb + nc + nu))"; tail -n +2 "$BASE"; cat "$C/cuts_snapshot.clauses"; for l in $lits; do echo "$l 0"; done; } > "$C/cube.cnf"
echo "cnf $(shasum -a 256 "$C/cube.cnf" | cut -c1-64) cuts $nc units $lits" > "$C/record.txt"
f="$C/p.fifo"; rm -f "$f"; mkfifo "$f"; (zstd -q -1 -f -o "$C/proof.lrat.zst" < "$f") &
"$BIN/cadical" -t 3000 --lrat --binary=false "$C/cube.cnf" "$f" > "$C/cadical.log" 2>&1; ec=$?; wait; rm -f "$f"
echo "cadical exit $ec" >> "$C/record.txt"
if [ $ec -eq 20 ]; then
  g="$C/q.fifo"; mkfifo "$g"; (zstd -dc "$C/proof.lrat.zst" > "$g") &
  echo "lrat-check: $("$BIN/lrat-check" "$C/cube.cnf" "$g" 2>&1 | grep -m1 -E 'VERIFIED|FAIL')" >> "$C/record.txt"; wait; rm -f "$g"
  h="$C/r.fifo"; mkfifo "$h"; (zstd -dc "$C/proof.lrat.zst" > "$h") &
  echo "cake_lpr: $(/usr/bin/lockf "$W/cake.lock" "$BIN/cake_lpr" --CML_HEAP_SIZE=8000 --CML_STACK_SIZE=4000 "$C/cube.cnf" "$h" 2>&1 | grep -m1 -E 's VERIFIED|FAIL|rror')" >> "$C/record.txt"; wait; rm -f "$h"
  echo "proof zst sha256 $(shasum -a 256 "$C/proof.lrat.zst" | cut -c1-64)" >> "$C/record.txt"
else
  rm -f "$C/proof.lrat.zst"
fi
rm -f "$C/cube.cnf"
