#!/bin/bash
# Second batch on the main core: 65-point runs from randomised-offset construction variants,
# with a secondary pressure (mu) on the number of convex 7-gons. Output: $OUT/batch2A.log
# Originally run with builds "cgon2" (addpoint) and "cgon3" (anneal) of cgon.c; see README.
# The generated starting sets init_v8p_$v.txt are written to $OUT (committed copies: ./init_v8p_*.txt).
. "$(dirname "$0")/common.sh"
L="$OUT/batch2A.log"
for v in 1 2 3; do
  echo "== variant v8_$v: addpoint (4000 candidates) then anneal raw T 1.0->0.05 mu=0.05" >> "$L"
  "$CGON" addpoint 8 4000 5$v < v8_$v.txt | tee -a "$L" > "$OUT/addpoint_v8_$v.txt"
  P=$(sed -E 's/.*at \((-?[0-9]+),(-?[0-9]+)\).*/\1 \2/' "$OUT/addpoint_v8_$v.txt")
  (cat v8_$v.txt; echo "$P") > "$OUT/init_v8p_$v.txt"
  "$CGON" anneal 8 65 200000 1.0 0.05 6$v "$OUT/init_v8p_$v.txt" "$OUT/m65v_s$v.txt" 0 0.05 1 2>"$OUT/m65v_s$v.err" >> "$L"
done
echo "== M65w raw mu=0.2 from init_w8p_3, T 2.0->0.1" >> "$L"
"$CGON" anneal 8 65 200000 2.0 0.1 71 init_w8p_3.txt "$OUT/m65w_mu_s71.txt" 0 0.2 1 2>"$OUT/m65w_mu_s71.err" >> "$L"
echo "== DONE" >> "$L"
