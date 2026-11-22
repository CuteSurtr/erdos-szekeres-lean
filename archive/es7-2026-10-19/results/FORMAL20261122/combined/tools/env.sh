# combined: LEAN_PATH (read-only roots; this build writes only $W/out). Source it: . tools/env.sh
W=/home/jay/research/data/formalize-20261122/combined
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
FV304_LP=/home/jay/research/data/fv304-20261120/lean_path.txt   # 14 roots, sha256 65463fd5... (fv304-audit)
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN/.lake/build/lib/lean
RB=/home/jay/research/data/formalize-20261122/res118-rowblocks/build/olean
export LEAN_PATH="$(cat $FV304_LP):$ENCB:$RB:$W/links:$W/out"
