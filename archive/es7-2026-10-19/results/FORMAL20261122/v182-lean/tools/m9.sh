#!/bin/bash
# M9 driver (run inside a unit): hash binding of the 4,404 printed pieces.
D=/home/jay/research/data/formalize-20261122/v182-lean
cd $D
/usr/bin/time -v python3 -I -B tools/hash_binding.py logs/m9_hash_binding.tsv $D/tmp_m9 > logs/m9.log 2> logs/m9.time
echo "EXIT $?" >> logs/m9.log
