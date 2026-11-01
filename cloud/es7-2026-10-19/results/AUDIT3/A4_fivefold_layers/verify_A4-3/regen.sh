#!/bin/bash
# Regenerate the two solved fivefold CNFs (P1 angle form, L1 layer form) from copies of the repository encoders.
# usage: regen.sh  (writes into big/, logs RSS via /usr/bin/time -l)
V=$(cd "$(dirname "$0")" && pwd)
cd $V/big
/usr/bin/time -l python3 -B $V/enc/symcnf.py 35 7 5 -o c5_n35.cnf --map c5_n35.json > gen_P1.log 2> time_P1.log &
/usr/bin/time -l python3 -B $V/enc/symcnf_layers.py 35 7 5 -o c5_n35L.cnf --map c5_n35L.json > gen_L1.log 2> time_L1.log &
wait
shasum -a 256 c5_n35.cnf c5_n35L.cnf > sha.txt
