#!/bin/bash
# Control runs (single core, sequential). Output: $OUT/controls.log
# Originally run with the first build of cgon.c ("cgon"); see README.
. "$(dirname "$0")/common.sh"
L="$OUT/controls.log"
echo "== C16: N=16 K=6 random starts" >> "$L"
for s in $(seq 1 20); do /usr/bin/time -p "$CGON" anneal 6 16 300000 0.5 0.01 $s random:1000000 "$OUT/c16_s$s.txt" 2>/dev/null >> "$L"; done
echo "== C17: N=17 K=6 random starts" >> "$L"
for s in $(seq 1 20); do "$CGON" anneal 6 17 300000 0.5 0.01 $s random:1000000 "$OUT/c17_s$s.txt" 2>/dev/null >> "$L"; done
echo "== C17w: N=17 K=6 from witness(6)+1 point" >> "$L"
for s in $(seq 1 10); do "$CGON" anneal 6 17 300000 0.2 0.005 $s init_w6p.txt "$OUT/c17w_s$s.txt" 2>/dev/null >> "$L"; done
echo "== C32: N=32 K=7 random starts" >> "$L"
for s in $(seq 1 6); do "$CGON" anneal 7 32 600000 0.5 0.005 $s random:1000000 "$OUT/c32_s$s.txt" 2>/dev/null >> "$L"; done
echo "== C33: N=33 K=7 random starts" >> "$L"
for s in $(seq 1 3); do "$CGON" anneal 7 33 600000 0.5 0.005 $s random:1000000 "$OUT/c33_s$s.txt" 2>/dev/null >> "$L"; done
echo "== DONE" >> "$L"
