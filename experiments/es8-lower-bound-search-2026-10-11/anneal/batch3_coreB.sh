#!/bin/bash
# Third batch on the control core. Output: $OUT/batch3B.log
# Originally run with the third build of cgon.c ("cgon3", the retained source); see README.
. "$(dirname "$0")/common.sh"
L="$OUT/batch3B.log"
echo "== R64: N=64 K=8 random start (can SA find a 64-point octagon-free set from scratch?), log energy" >> "$L"
"$CGON" anneal 8 64 300000 0.5 0.005 91 random:1000000 "$OUT/r64_s91.txt" 0 0 0 2>"$OUT/r64_s91.err" >> "$L"
echo "== M65 plateau walk: from init_w8p_4, raw energy, T 0.6->0.2, 300k iters" >> "$L"
"$CGON" anneal 8 65 300000 0.6 0.2 81 init_w8p_4.txt "$OUT/m65w_plateau_s81.txt" 0 0 1 2>"$OUT/m65w_plateau_s81.err" >> "$L"
echo "== DONE" >> "$L"
