#!/bin/bash
# A6 audit, phase 2: decompress every manifest entry to a pipe and hash it with shasum -a 256 (one file at a time,
# never written to disk); record the frame-header decompressed size and, for CNFs, the DIMACS header line.
# Read-only on the archive. Two processes at a time (zstd | shasum).
# usage: roundtrip.sh MANIFEST_TSV ARCHIVE_ROOT OUT_TSV
set -u
M=$1; A=$2; OUT=$3
printf 'archive_rel\tdecomp_bytes\tdecomp_sha256\tpline\tseconds\n' > "$OUT"
tail -n +2 "$M" | cut -f3 | while IFS= read -r rel; do
  f="$A/$rel"
  t0=$(date +%s)
  db=$(zstd -lv "$f" 2>/dev/null | sed -n 's/^Decompressed Size:.*(\([0-9]*\) B).*/\1/p' | head -1)
  pl=""
  case "$rel" in *.cnf.zst) zstd -dc "$f" 2>/dev/null | head -c 65536 > "$OUT.head"; pl=$(grep -a -m1 '^p cnf' "$OUT.head"); rm -f "$OUT.head";; esac
  h=$(zstd -dc "$f" | shasum -a 256 | cut -d' ' -f1)
  printf '%s\t%s\t%s\t%s\t%s\n' "$rel" "$db" "$h" "$pl" "$(( $(date +%s) - t0 ))" >> "$OUT"
done
echo "phase2 done $(date -u +%H:%M:%SZ)"
