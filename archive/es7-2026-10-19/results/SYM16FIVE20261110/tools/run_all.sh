#!/bin/sh
# SYM16FIVE20261110: rerun every check.  usage: sh run_all.sh OUTDIR   (GMP needed for sym_cvx)
set -e
D=$(cd "$(dirname "$0")" && pwd); RES=$D/../..; F=$RES/F/data/sym16; P=$RES/PRIMEFOLD/rule
mkdir -p "$1/sets"; OUT=$(cd "$1" && pwd)
python3 -I "$D/ordertypes.py" "$F/m4" "$F/m5" > "$OUT/ordertypes.log"
python3 -I "$D/sym5_exact.py" "$F/m5" 1 > "$OUT/sym5_exact.log"
python3 -I "$D/make_sym5.py" "$F/m5" "$OUT/sets"
${CC:-cc} -O2 ${CFLAGS:-} -o "$OUT/sym_cvx" "$P/sym_cvx.c" ${LDFLAGS:-} -lgmp -lm
: > "$OUT/sym_cvx.log"
for f in "$OUT"/sets/model*.pts; do
  echo "== $(basename "$f")" >> "$OUT/sym_cvx.log"
  "$OUT/sym_cvx" "$f" "$P/trig_p5.txt" 6 >> "$OUT/sym_cvx.log"
done
echo "sym_cvx: $(grep -c '^PASS (K=6)' "$OUT/sym_cvx.log") PASS of $(ls "$OUT"/sets/model*.pts | wc -l)"
cat "$OUT/ordertypes.log" "$OUT/sym5_exact.log"
