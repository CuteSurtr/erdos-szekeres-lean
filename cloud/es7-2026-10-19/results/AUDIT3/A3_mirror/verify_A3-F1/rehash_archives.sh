#!/bin/bash
# Stream-decompress the archived mirror33/mirror34 CNFs and LRAT proofs (zstd window 4 MiB, low memory)
# and compare SHA-256 and byte counts with the values recorded in CERTIFICATES.md / archive_hashes.tsv.
# Read-only on the archive. Usage: rehash_archives.sh > log
A="${PROOF_ARCHIVES:?set PROOF_ARCHIVES to the local proof-archive directory}/es7-symmetry"
T=$(cd "$(dirname "$0")" && pwd)
check() { # relpath expected_sha expected_bytes expected_archive_sha
  local f="$A/$1"
  local asha=$(shasum -a 256 "$f" | cut -d' ' -f1)
  local out=$(zstd -q -d -c "$f" | tee >(wc -c | tr -d ' ' > $T/.nb_$$) | shasum -a 256 | cut -d' ' -f1)
  sleep 1; local nb=$(cat $T/.nb_$$ 2>/dev/null); rm -f $T/.nb_$$
  local ok=MISMATCH; [ "$out" = "$2" ] && [ "$nb" = "$3" ] && [ "$asha" = "$4" ] && ok=OK
  printf '%s\tdecompressed_sha=%s\tbytes=%s\tarchive_sha=%s\t%s\n' "$1" "$out" "$nb" "$asha" "$ok"
}
date -u +%FT%TZ
check mirror33/m33_def.lrat.zst e1b2689d071a0b218f2c9be13a813f48bd3ea0fcd1e2fc1476a2549523ede1e4 4120793950 01f477fb1bcc9b160475da71749a04235ba03e920c086b3a2bb5cd15b54aa64a
check mirror33/m_t16k7a1.cnf.zst e45464edd52e06a31de4bbb664f444789540bad19039989679d76f7173739d02 518452724 8298fabacd7489ec746971396d2d50ec33b09de909c095845d8af3218dc0787f
check mirror34/mr34_def.lrat.zst 98e4d02a8f1e1e301603b9672dfe2c4e61e6659f14c2b5edc9e74bd31d4c6537 4373364691 39e93b6e2909efb3950bfdc32489864a37dd1b6f9fc48d0580c950cf0a85ac04
check mirror34/m_t17k7.cnf.zst b175eac0e7c000f533506ea6931774f4969a0e0415011ba0c4fb47e7f09a6c5b 620842936 33e5f6be15198ac65f01522f0595ade524a2a4a068e4a5fe21002172d0c6f06e
date -u +%FT%TZ
