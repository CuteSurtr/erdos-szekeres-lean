#!/bin/bash
# Pilot M1: pts hash, names, stats, and cnf SHA-256 for the given pair indices.
D=/home/jay/research/data/formalize-20261122/ae33-lean
X=$D/build/bin/ae33print
echo "pts $($X pts | sha256sum | cut -c1-64)"
for i in "$@"; do
  nm=$($X name $i)
  echo "name $i $nm"
  echo "stats $i $($X stats $i)"
  /usr/bin/time -f "cnf $i wall=%e s maxrss=%M KB" $X cnf $i | sha256sum | sed "s/^/sha $i /"
done
