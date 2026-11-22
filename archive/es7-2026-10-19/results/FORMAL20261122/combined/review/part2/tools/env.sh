# rv5 part-2 review: LEAN_PATH = exactly the worker's 20 roots (combined/tools/env2.sh), all read-only. Source it.
# FV304's 14 roots (lean_path.txt, sha256 65463fd5..., checked by start.sh), ENCBLEAN, res118-rowblocks, the worker's
# links/ and out/, n66-level15 and n66-l15-rows build/olean.
FV304_LP=/home/jay/research/data/fv304-20261120/lean_path.txt
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN/.lake/build/lib/lean
RB=/home/jay/research/data/formalize-20261122/res118-rowblocks/build/olean
W=/home/jay/research/data/formalize-20261122/combined
L15=/home/jay/research/data/formalize-20261122/n66-level15/build/olean
L15R=/home/jay/research/data/formalize-20261122/n66-l15-rows/build/olean
export LEAN_PATH="$(cat $FV304_LP):$ENCB:$RB:$W/links:$W/out:$L15:$L15R"
