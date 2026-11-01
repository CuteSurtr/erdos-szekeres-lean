#!/bin/sh
# Re-run (same seed, same budget) the jobs whose result files were clobbered by a git checkout.
cd "$(dirname "$0")/.."
BUDGET=${BUDGET:-600}
xargs -P 4 -L 1 sh -c 'mkdir -p runs/$0; ./bin_n2 $0 $1 '$BUDGET' 1 runs/$0/$2 > runs/$0/$2.json 2> runs/$0/$2.err' < "$1"
