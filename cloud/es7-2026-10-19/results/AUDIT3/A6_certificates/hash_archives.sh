#!/bin/bash
# A6 audit, phase 1: for every manifest entry, check that the archive file exists, record its size and its SHA-256
# (shasum -a 256, one file at a time). Read-only on the archive.
# usage: hash_archives.sh MANIFEST_TSV ARCHIVE_ROOT OUT_TSV
set -u
M=$1; A=$2; OUT=$3
printf 'archive_rel\texists\tbytes\tsha256\tseconds\n' > "$OUT"
tail -n +2 "$M" | cut -f3 | while IFS= read -r rel; do
  f="$A/$rel"
  if [ -f "$f" ]; then
    t0=$(date +%s)
    b=$(stat -f %z "$f")
    h=$(shasum -a 256 "$f" | cut -d' ' -f1)
    printf '%s\tyes\t%s\t%s\t%s\n' "$rel" "$b" "$h" "$(( $(date +%s) - t0 ))" >> "$OUT"
  else
    printf '%s\tNO\t\t\t\n' "$rel" >> "$OUT"
  fi
done
echo "phase1 done $(date -u +%H:%M:%SZ)"
