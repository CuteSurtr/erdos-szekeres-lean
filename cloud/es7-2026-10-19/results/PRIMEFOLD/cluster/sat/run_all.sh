#!/bin/bash
# Theorem E: regenerate the CNFs, check their SHA-256 against SHA256SUMS.txt, solve with CaDiCaL (LRAT) and check the
# proofs with lrat-check.  usage: bash run_all.sh OUTDIR   (set CADICAL and LRATCHECK to the executables)
# The largest instance (m = 8, n = 15, clsat.py) has an 8.8 MB CNF and a 25 MB proof; all solve in seconds.
set -e
D=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$1"; OUT=$(cd "$1" && pwd); cd "$OUT"
CAD=${CADICAL:-cadical}; CHK=${LRATCHECK:-lrat-check}
for mn in "4 3" "5 4" "6 6" "7 10" "8 15"; do set -- $mn; python3 "$D/../clsat.py" $1 $2 m$1_n$2.cnf > /dev/null; done
python3 "$D/../clsat2.py" 7 10 0 dp_m7_n10.cnf > /dev/null
python3 "$D/../clsat2.py" 8 15 0 dp_m8_n15.cnf > /dev/null
for f in m4_n3 m5_n4 m6_n6 m7_n10 m8_n15 dp_m7_n10 dp_m8_n15; do
  want=$(grep " $f.cnf\$" "$D/SHA256SUMS.txt" | cut -d' ' -f1)
  have=$(shasum -a 256 $f.cnf | cut -d' ' -f1)
  [ "$want" = "$have" ] && h=same || h=DIFFERENT
  res=$($CAD -q --lrat --no-binary $f.cnf $f.lrat | grep '^s ' || true)
  chk=$($CHK $f.cnf $f.lrat 2>&1 | grep -E 'VERIFIED|FAILED|ERROR' | head -1)
  echo "$f: cnf sha256 ${have:0:16} ($h as recorded); $res; lrat-check: $chk; proof $(stat -f %z $f.lrat) bytes"
  rm -f $f.lrat
done
