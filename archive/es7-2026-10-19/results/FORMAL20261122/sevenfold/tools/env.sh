# Read-only LEAN_PATH over ENCBLEAN's olean stores plus this directory's own output (sourced by the build scripts).
R=/home/jay/research/lean/erdos-szekeres-lean/archive/es7-2026-10-19/results/ENCBLEAN
G=$R/geo
TC=/home/jay/.elan/toolchains/leanprover--lean4---v4.24.0
W=/home/jay/research/data/formalize-20261122/sevenfold
LEAN=$TC/bin/lean
# Std-only part (EncB + this package)
LP_STD="$TC/lib/lean:$W/olean"
# Mathlib part: geo's own Mathlib checkout (f897ebcf) and geo's build (ES8Geo + vendored ErdosSzekeres); never the repo's .lake
LP_GEO="$TC/lib/lean"
for p in aesop batteries importGraph LeanSearchClient mathlib plausible proofwidgets Qq; do LP_GEO="$LP_GEO:$G/.lake/packages/$p/.lake/build/lib/lean"; done
LP_GEO="$LP_GEO:$G/.lake/build/lib/lean:$R/.lake/build/lib/lean:$W/olean"
# Self-built geometric part: Mathlib from geo's checkout only; ES8Geo, the vendored ErdosSzekeres and EncB from this
# directory's own olean store (built from verbatim sources, logs/geo_vendor.sha256, logs/encb_vendor.sha256).
LP_SELF="$TC/lib/lean"
for p in aesop batteries importGraph LeanSearchClient mathlib plausible proofwidgets Qq; do LP_SELF="$LP_SELF:$G/.lake/packages/$p/.lake/build/lib/lean"; done
LP_SELF="$LP_SELF:$W/olean"
