# rv5 review: LEAN_PATH = exactly the worker's roots (combined/tools/env.sh), all read-only. Source it.
FV304_LP=/home/jay/research/data/fv304-20261120/lean_path.txt   # 14 roots; sha256 65463fd5... (fv304-audit)
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN/.lake/build/lib/lean
RB=/home/jay/research/data/formalize-20261122/res118-rowblocks/build/olean
W=/home/jay/research/data/formalize-20261122/combined
export LEAN_PATH="$(cat $FV304_LP):$ENCB:$RB:$W/links:$W/out"
