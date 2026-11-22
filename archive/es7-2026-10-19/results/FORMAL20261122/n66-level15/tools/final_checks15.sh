#!/bin/bash
# Final checks: R0_15 coverage by the printed trims; freeze check of the printer (exe + IR C + obj files as linked);
# SHA-256 manifest of the final sources and data.
D=/home/jay/research/data/formalize-20261122/n66-level15
cd $D
echo "== R0_15 coverage (distinct R indices in desc/*.txt; R0_15 has 10859 rows)"
cat desc/*.txt | awk '$1=="R"{print $2}' | sort -un > logs/r0_15_used_indices.txt
n=$(wc -l < logs/r0_15_used_indices.txt); mn=$(head -1 logs/r0_15_used_indices.txt); mx=$(tail -1 logs/r0_15_used_indices.txt)
echo "distinct=$n min=$mn max=$mx"
[ "$n" = 10859 ] && [ "$mn" = 0 ] && [ "$mx" = 10858 ] && echo "R0_15_FULLY_COVERED" || echo "R0_15_NOT_FULLY_COVERED"
echo "== freeze check (logs/freeze_manifest.sha256, written right after the M1 link)"
sha256sum -c logs/freeze_manifest.sha256 | grep -v ': OK$' || true
echo "freeze entries OK: $(sha256sum -c logs/freeze_manifest.sha256 2>/dev/null | grep -c ': OK$') of $(wc -l < logs/freeze_manifest.sha256)"
echo "== source manifest"
sha256sum lean/N66E15/*.lean lean/N66G15/*.lean lean/N66E15/data/* tools/*.py tools/*.sh tools/leaf_order15.txt \
  DESIGN.md ref/* > logs/final_source_manifest.sha256
wc -l < logs/final_source_manifest.sha256
