#!/bin/bash
# regenerate the two fivefold 35-point CNFs with unmodified encoder copies and hash them (audit A4)
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")"
/usr/bin/time -l python3 ../enc/symcnf.py 35 7 5 -o c5_n35.cnf --map c5_n35.json > gen_c5_35A.log 2>&1
/usr/bin/time -l python3 ../enc/symcnf_layers.py 35 7 5 -o c5_n35L.cnf --map c5_n35L.json > gen_c5_35L.log 2>&1
shasum -a 256 c5_n35.cnf c5_n35L.cnf c5_n35.json c5_n35L.json > sha_c5_35.txt
head -3 c5_n35.cnf c5_n35L.cnf >> sha_c5_35.txt
