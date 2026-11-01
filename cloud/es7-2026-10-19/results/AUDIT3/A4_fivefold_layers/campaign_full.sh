#!/bin/bash
cd "$(dirname "$0")"
V=${PY:-python3}
/usr/bin/time -l $V test_full.py 5 35 L 3 41 big/c5_n35L.cnf big/c5_n35L.json > logs/full_c5_35L.log 2>&1
/usr/bin/time -l $V test_full.py 5 35 A 3 42 big/c5_n35.cnf big/c5_n35.json > logs/full_c5_35A.log 2>&1
/usr/bin/time -l $V test_full.py 4 32 L 3 43 big/c4_n32L.cnf big/c4_n32L.json > logs/full_c4_32L.log 2>&1
echo FULL DONE
