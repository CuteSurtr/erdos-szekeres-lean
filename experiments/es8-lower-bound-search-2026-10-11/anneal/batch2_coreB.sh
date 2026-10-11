#!/bin/bash
# Second batch on the control core (sequential, single process at a time). Output: $OUT/batch2B.log
# Originally run with the second build of cgon.c ("cgon2"); see README.
# The generated starting set init_w7p.txt is written to $OUT (committed copy: ./init_w7p.txt).
. "$(dirname "$0")/common.sh"
L="$OUT/batch2B.log"
echo "== addpoint on witness(7) (32 pts), K=7" >> "$L"
"$CGON" addpoint 7 40000 21 < w7.txt | tee -a "$L" > "$OUT/addpoint_w7.txt"
P=$(sed -E 's/.*at \((-?[0-9]+),(-?[0-9]+)\).*/\1 \2/' "$OUT/addpoint_w7.txt")
(cat w7.txt; echo "$P") > "$OUT/init_w7p.txt"
echo "== addpoint on witness(8) (64 pts), K=8, 20000 candidates" >> "$L"
"$CGON" addpoint 8 20000 22 < w8.txt >> "$L"
echo "== scan: single-point-move neighbourhoods of witness(8)+1 configurations" >> "$L"
for i in 1 2; do "$CGON" scan 8 1000 3$i "$OUT/scan_w8p_${i}_ZERO.txt" < init_w8p_$i.txt >> "$L"; done
echo "== scan: witness(7)+1 (33 pts) and witness(6)+1 (17 pts)" >> "$L"
"$CGON" scan 7 3000 41 "$OUT/scan_w7p_ZERO.txt" < "$OUT/init_w7p.txt" >> "$L"
"$CGON" scan 6 3000 42 "$OUT/scan_w6p_ZERO.txt" < init_w6p.txt >> "$L"
echo "== R65: N=65 K=8 random start control (log energy)" >> "$L"
"$CGON" anneal 8 65 100000 0.5 0.01 7 random:1000000 "$OUT/r65_s7.txt" 0 0 0 2>"$OUT/r65_s7.err" >> "$L"
echo "== C33w: N=33 K=7 from witness(7)+1, raw energy" >> "$L"
for s in 1 2 3; do "$CGON" anneal 7 33 400000 1.5 0.05 $s "$OUT/init_w7p.txt" "$OUT/c33w_s$s.txt" 0 0 1 2>/dev/null >> "$L"; done
echo "== DONE" >> "$L"
