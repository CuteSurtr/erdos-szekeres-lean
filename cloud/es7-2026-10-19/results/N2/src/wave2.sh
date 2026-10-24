#!/bin/sh
# Wave 2: fresh starts (starts2/), seed 2, BUDGET CPU-s per (method, start), 4 in parallel.
cd "$(dirname "$0")/.."
BUDGET=${BUDGET:-300}
for f in starts2/rnd_*.txt starts2/nm_*.txt; do
  b=$(basename $f .txt)
  for m in tabu lns pen; do [ -s runs2/$m/$b.json ] || echo "$m $f $b"; done
done | xargs -P 4 -L 1 sh -c 'mkdir -p runs2/$0; ./bin_n2 $0 $1 '$BUDGET' 2 runs2/$0/$2 > runs2/$0/$2.json 2> runs2/$0/$2.err'
