#!/bin/sh
# Extract the Lean row sources that some review scripts read as text (nothing in them is executed).
# All files come from tarballs committed under experiments/; the extracted copies are not kept in Git.
# Run from cloud/es7-2026-10-19/results:  sh ES8SLACK/review/extract_sources.sh
set -e
X=../../../experiments
R=ES8SLACK/review
for d in C1_certificates/extract_balanced_rows C1_certificates/extract_residual_cycles \
         C4_balanced/extract_rows C5_ceiling/extract_balbase; do
  mkdir -p "$R/$d"
done
tar -xzf "$X/omission-global-assembly-2026-10-10/balanced-rows-sources.tar.gz" -C "$R/C1_certificates/extract_balanced_rows"
tar -xzf "$X/omission-residual-geometry-2026-10-09/cycles-sources.tar.gz" -C "$R/C1_certificates/extract_residual_cycles"
tar -xzf "$X/omission-global-assembly-2026-10-10/balanced-rows-sources.tar.gz" -C "$R/C4_balanced/extract_rows"
tar -xzf "$X/omission-balanced-lean-2026-10-09/sources.tar.gz" -C "$R/C5_ceiling/extract_balbase" Catalog.lean
echo "extracted: 85 + 39 + 85 + 1 files"
