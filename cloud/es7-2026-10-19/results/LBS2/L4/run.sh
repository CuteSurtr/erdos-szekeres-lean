#!/bin/sh
# Build and start 4 walk32 workers (epoch $2) that stop at unix time $1.
cd "$(dirname "$0")"
gcc -O2 -o sat ../../../tools/trackA/sat.c
gcc -O2 -march=native -o walk walk.c -lm
gcc -O2 -o vfy4 vfy4.c
mkdir -p live
for w in 1 2 3 4; do
  setsid nohup python3 driver.py $w "$1" "$2" > live/e$2_w$w.stderr 2>&1 &
done
