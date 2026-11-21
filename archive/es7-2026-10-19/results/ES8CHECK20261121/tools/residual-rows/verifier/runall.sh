#!/bin/sh
# single-threaded, sequential; outputs one JSON line per batch
date
for m in unif para mix; do
  python3 -B check_c1.py random 101 200 18 45 $m
done
for m in mix para unif; do
  python3 -B grow.py 201 25 1500 $m
done
date
