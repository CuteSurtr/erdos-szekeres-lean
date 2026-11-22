# LEAN_PATH (read-only olean stores; outputs only under this work dir's build/). No n66enc, n66-rowsvalid or
# res118-rowblocks store: N66R15* are renamed copies; N66E15/N66G15 come from n66-level15 (manifests verified).
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
L15=/home/jay/research/data/formalize-20261122/n66-level15
D=/home/jay/research/data/formalize-20261122/n66-l15-rows
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$ENCB/.lake/build/lib/lean:$L15/build/olean:${OLEAN:-$D/build/olean}"
