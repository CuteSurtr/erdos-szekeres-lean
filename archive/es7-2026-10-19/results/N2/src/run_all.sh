#!/bin/sh
# Paired campaign: every start x every method, same seed, BUDGET CPU-s each, 4 in parallel.
cd "$(dirname "$0")/.."
BUDGET=${BUDGET:-600}
for f in starts/nm_*.txt starts/rnd_*.txt; do
  b=$(basename $f .txt)
  for m in tabu lns pen; do echo "$m $f $b"; done
done | xargs -P 4 -L 1 sh -c 'mkdir -p runs/$0; ./bin_n2 $0 $1 '$BUDGET' 1 runs/$0/$2 > runs/$0/$2.json 2> runs/$0/$2.err'
