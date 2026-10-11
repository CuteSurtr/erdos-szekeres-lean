#!/bin/bash
# Fourth batch on the control core: continue the 64-point random-start run. Output: $OUT/batch4B.log
# RECONSTRUCTED: the original batch-4 driver was not retained. The anneal
# parameters are exactly those printed in out/batch4B.log; the starting set
# out/r64_s91.txt is inferred from out/r64_cont_s92.err, which starts at E=46,
# the final count of r64_s91. Originally run with build "cgon3" (the retained
# source); see README for the replay check of this command.
. "$(dirname "$0")/common.sh"
L="$OUT/batch4B.log"
"$CGON" anneal 8 64 200000 2.0 0.05 92 out/r64_s91.txt "$OUT/r64_cont_s92.txt" 0 0 1 2>"$OUT/r64_cont_s92.err" >> "$L"
echo "== DONE" >> "$L"
