#!/bin/sh
# Build and start 4 extend32 workers (seeds 1-4) that stop after $1 seconds.
cd "$(dirname "$0")"
mkdir -p out
gcc -O2 -march=native -Wall -o out/lbs lbs.c -lm
gcc -O2 -Wall -o out/vfy vfy.c
for s in 1 2 3 4; do
  setsid nohup out/lbs run $s "$1" out/w$s bases/base*.txt > out/w$s.stderr 2>&1 &
done
