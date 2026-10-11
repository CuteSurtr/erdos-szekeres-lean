#!/bin/bash
# Main 65-point runs (single core, sequential). Output: $OUT/main65.log
# Originally run with the first build of cgon.c ("cgon"); the first run was
# interrupted after iteration 49,152 (see out/m65w_s1.err and README).
. "$(dirname "$0")/common.sh"
L="$OUT/main65.log"
for s in 1 2 3 4; do
  echo "== M65w: N=65 K=8 from witness(8)+point init $s, mu=0" >> "$L"
  "$CGON" anneal 8 65 220000 0.3 0.005 $s init_w8p_$s.txt "$OUT/m65w_s$s.txt" 0 0 2>"$OUT/m65w_s$s.err" >> "$L"
done
echo "== DONE" >> "$L"
