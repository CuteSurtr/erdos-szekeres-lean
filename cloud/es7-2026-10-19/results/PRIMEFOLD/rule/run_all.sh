#!/bin/sh
# The rotated-cluster rule: compute B(h), rebuild the four point files from the rule, and check the 253- and
# 991-point sets with the GMP verifier sym_cvx (plus a 120-digit decimal re-check of 200,000 sampled signs).
# usage: sh run_all.sh OUTDIR      (GMP needed; set CFLAGS/LDFLAGS if it is not on the default paths)
set -e
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1"; OUT=$(cd "$1" && pwd)
S=$D/../sets
${CC:-cc} -O2 ${CFLAGS:-} -o "$OUT/sym_cvx" "$D/sym_cvx.c" ${LDFLAGS:-} -lgmp -lm
python3 "$D/recdp.py" 6 > "$OUT/recdp.log"                     # B(h) for h = 1..6 (h = 7 needs about 2.3 GB)
: > "$OUT/rebuild.log"
for a in "2 0.1 0.1 9 $D/rule_p5.reps.pts" "3 0.03 0.05 13 $D/rule_p7.reps.pts" \
         "4 0.005 0.005 22 $S/k10/rule_p9_253pts.pts" "5 0.002 0.002 30 $S/k12/rule_p11_991pts.pts"; do
  set -- $a
  python3 "$D/gen_points.py" $1 $2 $3 $4 "$OUT/gen_h$1.pts" > /dev/null
  cmp "$OUT/gen_h$1.pts" "$5" && echo "h=$1: rule output identical to $(basename $5)" | tee -a "$OUT/rebuild.log"
done
cd "$D"
"$OUT/sym_cvx" rule_p5.reps.pts trig_p5.txt 6 > "$OUT/p5.log"
"$OUT/sym_cvx" rule_p7.reps.pts trig_p7.txt 8 > "$OUT/p7.log"
SUBSET_WINDOWS=1,2,3,0 SAMPLE_OUT="$OUT/p9_sample.txt" "$OUT/sym_cvx" "$S/k10/rule_p9_253pts.pts" trig_p9.txt 10 3 16 21 > "$OUT/p9.log"
SUBSET_WINDOWS=1,2,3,0 SAMPLE_OUT="$OUT/p11_sample.txt" SAMPLE_N=200000 "$OUT/sym_cvx" "$S/k12/rule_p11_991pts.pts" trig_p11.txt 12 6 18 21 > "$OUT/p11.log"
python3 "$D/indep_sample.py" "$S/k10/rule_p9_253pts.pts" "$OUT/p9_sample.txt" > "$OUT/p9_indep.log"
python3 "$D/indep_sample.py" "$S/k12/rule_p11_991pts.pts" "$OUT/p11_sample.txt" > "$OUT/p11_indep.log"
tail -1 "$OUT/p5.log" "$OUT/p7.log" "$OUT/p9.log" "$OUT/p11.log"; cat "$OUT/p9_indep.log" "$OUT/p11_indep.log"
