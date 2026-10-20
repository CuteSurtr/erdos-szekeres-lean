#!/bin/sh
# Re-run only the (method, start) jobs of run_all.sh whose JSON is missing or empty.
cd "$(dirname "$0")/.."
BUDGET=${BUDGET:-600}
for f in starts/rnd_*.txt starts/nm_*.txt; do
  b=$(basename $f .txt)
  for m in tabu lns pen; do [ -s runs/$m/$b.json ] || echo "$m $f $b"; done
done | xargs -P 4 -L 1 sh -c 'mkdir -p runs/$0; ./bin_n2 $0 $1 '$BUDGET' 1 runs/$0/$2 > runs/$0/$2.json 2> runs/$0/$2.err'
