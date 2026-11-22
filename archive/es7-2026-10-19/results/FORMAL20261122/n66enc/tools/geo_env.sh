# LEAN_PATH for the Mathlib side (read-only olean stores; outputs only under build/)
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
D=/home/jay/research/data/formalize-20261122/n66enc
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0/lib/lean:/home/jay/research/data/bal186-20261119/zrow/leanz/olean:$ENCB/.lake/build/lib/lean:$D/build/olean"
