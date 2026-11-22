#!/bin/bash
# Final checks: R0 coverage by the printed trims; SHA-256 manifest of the final sources and data.
D=/home/jay/research/data/formalize-20261122/n66enc
echo "== R0 coverage (distinct R indices in desc/*.txt; R0 has 11884 rows)"
cat $D/desc/*.txt | awk '$1=="R"{print $2}' | sort -un > $D/logs/r0_used_indices.txt
n=$(wc -l < $D/logs/r0_used_indices.txt); mn=$(head -1 $D/logs/r0_used_indices.txt); mx=$(tail -1 $D/logs/r0_used_indices.txt)
echo "distinct=$n min=$mn max=$mx"
[ "$n" = 11884 ] && [ "$mn" = 0 ] && [ "$mx" = 11883 ] && echo "R0_FULLY_COVERED" || echo "R0_NOT_FULLY_COVERED"
echo "== source manifest"
cd $D && sha256sum lean/N66Enc/*.lean lean/N66Geo/*.lean lean/N66Enc/data/* tools/*.py tools/*.sh > $D/logs/final_source_manifest.sha256
wc -l < $D/logs/final_source_manifest.sha256
