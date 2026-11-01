#!/bin/bash
# batch of exact real-set tests on both solved CNFs (sequential, one process at a time)
V=$(cd "$(dirname "$0")" && pwd); cd $V
for s in 2 3 4; do python3 -B realtest.py big/c5_n35L.cnf big/c5_n35L.json layer $s; done
for s in 1 2 3; do for o0 in 0 3 6; do python3 -B realtest.py big/c5_n35.cnf big/c5_n35.json angle $s $o0; done; done
python3 -B realtest.py big/c5_n35.cnf big/c5_n35.json angle 5 2 --mutate
python3 -B realtest.py big/c5_n35L.cnf big/c5_n35L.json layer 5 --mutate
