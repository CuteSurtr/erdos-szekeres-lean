#!/bin/sh
# CATALAN20261110: rerun every check.  usage: sh run_all.sh OUTDIR   (GMP needed for sym_cvx)
# Writes OUTDIR/run_all.log (timings, sym_cvx exit codes, byte comparison with the committed sets/).
set -e
D=$(cd "$(dirname "$0")" && pwd); P=$D/../../PRIMEFOLD/rule; SETS=$D/../sets
mkdir -p "$1"; OUT=$(cd "$1" && pwd); LOG=$OUT/run_all.log; : > "$LOG"
t0=$(date +%s)
python3 -I "$D/count_check.py" > "$OUT/count_check.log"
python3 -I "$D/profile_check.py" 7 > "$OUT/profile_check.log"
echo "count_check + profile_check: $(( $(date +%s) - t0 )) s; $(tail -n 1 "$OUT/count_check.log"), $(tail -n 1 "$OUT/profile_check.log")" >> "$LOG"
${CC:-cc} -O2 ${CFLAGS:-} -o "$OUT/sym_cvx" "$P/sym_cvx.c" ${LDFLAGS:-} -lgmp -lm 2> /dev/null
for a in "2 0.1 0.1 9 5 6" "3 0.03 0.05 13 7 8" "4 0.005 0.005 22 9 10" "5 0.002 0.002 30 11 12"; do
  set -- $a
  python3 -I "$D/gen_ftree.py" $1 $2 $3 $4 "$OUT/ftree_h$1.pts" > /dev/null
  if [ -f "$SETS/ftree_h$1.pts" ]; then
    if cmp -s "$OUT/ftree_h$1.pts" "$SETS/ftree_h$1.pts"; then echo "h=$1: generated file identical to sets/ftree_h$1.pts" >> "$LOG"
    else echo "h=$1: generated file DIFFERS from sets/ftree_h$1.pts" >> "$LOG"; fi
  fi
  t0=$(date +%s)
  if [ $1 -le 3 ]; then
    "$OUT/sym_cvx" "$OUT/ftree_h$1.pts" "$P/trig_p$5.txt" $6 > "$OUT/sym_cvx_h$1.log"
  else   # as PRIMEFOLD/rule/run_all.sh for its 253- and 991-point sets: subset second method + sample for indep_sample.py
    SUBSET_WINDOWS=1,2,3,0 SAMPLE_OUT="$OUT/sample_h$1.txt" SAMPLE_N=200000 \
      "$OUT/sym_cvx" "$OUT/ftree_h$1.pts" "$P/trig_p$5.txt" $6 6 18 21 > "$OUT/sym_cvx_h$1.log"
    python3 -I "$P/indep_sample.py" "$OUT/ftree_h$1.pts" "$OUT/sample_h$1.txt" > "$OUT/indep_sample_h$1.log"
  fi
  echo "h=$1: sym_cvx exit 0, $(( $(date +%s) - t0 )) s: $(grep 'largest convex subset =' "$OUT/sym_cvx_h$1.log" | head -n 1); $(tail -n 1 "$OUT/sym_cvx_h$1.log")" >> "$LOG"
  [ -f "$OUT/indep_sample_h$1.log" ] && echo "h=$1: $(tail -n 2 "$OUT/indep_sample_h$1.log" | tr '\n' ' ')" >> "$LOG"
done
cat "$LOG"
