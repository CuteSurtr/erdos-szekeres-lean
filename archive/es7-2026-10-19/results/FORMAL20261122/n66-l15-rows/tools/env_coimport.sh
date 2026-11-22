# LEAN_PATH for the co-import check only (read-only stores; no olean written): this dir + n66-level15 + n66enc +
# res118 + res118-rowblocks + comp-audit's composition oleans (its LemmaZ.olean is byte-identical to leanz's
# ef249ba1…, so leanz/olean is left off to keep one provider per module; tools/shadow.py checks this).
R=/home/jay/research/lean/erdos-szekeres-lean
P=$R/.lake/packages
ENCB=$R/archive/es7-2026-10-19/results/ENCBLEAN
F=/home/jay/research/data/formalize-20261122
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
export LEAN_PATH="$P/Cli/.lake/build/lib/lean:$P/batteries/.lake/build/lib/lean:$P/Qq/.lake/build/lib/lean:$P/aesop/.lake/build/lib/lean:$P/proofwidgets/.lake/build/lib/lean:$P/importGraph/.lake/build/lib/lean:$P/LeanSearchClient/.lake/build/lib/lean:$P/plausible/.lake/build/lib/lean:$P/mathlib/.lake/build/lib/lean:$R/.lake/build/lib/lean:$TC/lib/lean:$R/experiments/omission-compact-checker-2026-11-05/build/chain311/olean:$F/comp-audit/out/olean:$ENCB/.lake/build/lib/lean:$F/res118/olean:$F/res118-rowblocks/build/olean:$F/n66enc/build/olean:$F/n66-level15/build/olean:$F/n66-l15-rows/build/olean"
