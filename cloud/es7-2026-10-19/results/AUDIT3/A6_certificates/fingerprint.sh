#!/bin/bash
# A6 audit, phase 3: streaming fingerprint of the archived LRAT proofs of CERTIFICATES.md and C4CUT (additions,
# empty clauses, deletion lines, deleted IDs, max ID), to compare with the counts printed in the CaDiCaL and
# lrat-check logs. Two processes at a time (zstd | lratcount). Read-only on the archive.
# usage: fingerprint.sh ARCHIVE_ROOT LRATCOUNT OUT_TSV
set -u
A=$1; LC=$2; OUT=$3
printf 'archive_rel\tbytes\tlines\tadditions\tempty_additions\tfirst_empty_id\tlast_line\tdeletion_lines\tdeleted_ids\tmax_id\tcomments\tmalformed\n' > "$OUT"
for rel in es7-symmetry/mirror34/mr34_def.lrat.zst es7-symmetry/mirror33/m33_def.lrat.zst es7-symmetry/c5/P1.lrat.zst \
           es7-symmetry/c5/L1.lrat.zst es7-symmetry/c5/L2.lrat.zst es7-symmetry/c3hex/c3_n15k6.lrat.zst \
           es7-symmetry/c3hex/c3_n16k6c.lrat.zst es7-symmetry/central34/hc34_coverL.lrat.zst \
           es7-c4-32-cuts-2026-11-01/c4cuts.lrat.zst; do
  r=$(zstd -dc "$A/$rel" | "$LC")
  printf '%s\t%s\n' "$rel" "$(echo $r | tr ' ' '\t')" >> "$OUT"
done
echo "phase3 done $(date -u +%H:%M:%SZ)"
