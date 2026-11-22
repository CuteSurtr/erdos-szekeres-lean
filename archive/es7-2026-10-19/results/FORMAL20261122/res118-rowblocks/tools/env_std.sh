# LEAN_PATH for the Std-only modules RowEnc.* (read-only stores; outputs only under build/)
ENCB=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
R118=/home/jay/research/data/formalize-20261122/res118
D=/home/jay/research/data/formalize-20261122/res118-rowblocks
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
export LEAN_PATH="$ENCB/.lake/build/lib/lean:$R118/olean:$D/build/olean"
