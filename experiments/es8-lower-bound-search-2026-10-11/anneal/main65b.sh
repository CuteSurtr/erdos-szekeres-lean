#!/bin/bash
# Main 65-point runs, raw-count Metropolis energy (single core, sequential). Output: $OUT/main65b.log
# Originally run with the second build of cgon.c ("cgon2"); see README.
. "$(dirname "$0")/common.sh"
L="$OUT/main65b.log"
for s in 1 2 3 4; do
  echo "== M65w raw: N=65 K=8 from witness(8)+point init $s, T 1.5->0.05, mu=0" >> "$L"
  "$CGON" anneal 8 65 200000 1.5 0.05 $s init_w8p_$s.txt "$OUT/m65w_raw_s$s.txt" 0 0 1 2>"$OUT/m65w_raw_s$s.err" >> "$L"
done
echo "== DONE" >> "$L"
