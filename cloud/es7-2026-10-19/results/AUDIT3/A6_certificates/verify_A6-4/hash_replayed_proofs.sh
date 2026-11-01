#!/bin/bash
# verify_A6-4: stream-decompress the archived L1 and mirror34 proofs (read-only) and hash them, to tie the untracked
# 2026-10-29 replay records (which name the proof by SHA-256) to the archived proofs. Nothing is written to disk.
# Expected: L1.lrat 8625b321d58ed231924ffd22ffd730fde91314c898b835ea182848c9100d39f4 (1,812,130,098 bytes)
#           mr34_def.lrat 98e4d02a8f1e1e301603b9672dfe2c4e61e6659f14c2b5edc9e74bd31d4c6537 (4,373,364,691 bytes)
set -u
A="${PROOF_ARCHIVES:?set PROOF_ARCHIVES to the local proof-archive directory}/es7-symmetry"
for f in c5/L1.lrat.zst mirror34/mr34_def.lrat.zst; do
  s=$(date +%s)
  out=$(zstd -dc --long=31 "$A/$f" | tee >(wc -c | tr -d ' ' > /dev/stderr) | shasum -a 256 | cut -d' ' -f1)
  echo "$f decompressed sha256 $out  ($(( $(date +%s) - s )) s)"
done
