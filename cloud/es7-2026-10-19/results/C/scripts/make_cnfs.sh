#!/bin/bash
# Generate every CNF used in Task C with tools/etv/gen_etv.py, then the orbit-substituted
# versions with mirgen.py.  Usage: make_cnfs.sh <outdir>
set -e
OUT="$1"; HERE="$(cd "$(dirname "$0")" && pwd)"; G="$HERE/../../../tools/etv/gen_etv.py"
mkdir -p "$OUT"; cd "$OUT"
gen() { name="$1"; shift; python3 "$G" "$@" -o "$name.cnf" > "$name.json"; cat "$name.json"; }
# controls
gen m7k5   7 5 5 5 --mirror
gen hm7k5  7 5 5 5 --mirror --hull
gen m8k5   8 5 5 5 --mirror
gen hm8k5  8 5 5 5 --mirror --hull
gen m9k5   9 5 5 5 --mirror
gen hm9k5  9 5 5 5 --mirror --hull
gen m11k6 11 6 6 6 --mirror
gen hm11k6 11 6 6 6 --mirror --hull
gen m16k6 16 6 6 6 --mirror
gen hm16k6 16 6 6 6 --mirror --hull
gen m17k6 17 6 6 6 --mirror
gen hm17k6 17 6 6 6 --mirror --hull
gen m32k7 32 7 7 7 --mirror
gen hm32k7 32 7 7 7 --mirror --hull
# main instances
gen m33k7  33 7 7 7 --mirror
gen hm33k7 33 7 7 7 --mirror --hull
# orbit-substituted instances for the runs
python3 "$HERE/mirgen.py" hm33k7.cnf 33 --hull -o hm33k7.sub.cnf
python3 "$HERE/mirgen.py" m33k7.cnf 33 --interior --yflip-unit -o m33k7int.sub.cnf
python3 "$HERE/mirgen.py" m17k6.cnf 17 -o m17k6.sub.cnf
python3 "$HERE/mirgen.py" hm17k6.cnf 17 --hull -o hm17k6.sub.cnf
python3 "$HERE/mirgen.py" m9k5.cnf 9 -o m9k5.sub.cnf
python3 "$HERE/mirgen.py" m32k7.cnf 32 -o m32k7.sub.cnf
