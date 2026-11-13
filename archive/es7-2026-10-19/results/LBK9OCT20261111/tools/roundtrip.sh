#!/bin/sh
# zstd round trip of the recorded cube proofs: decompressed SHA-256 must equal the raw proof hash in result.txt
# usage: roundtrip.sh CUBEDIR
for d in $1/c_*; do
  raw=$(grep "proof.lrat$" $d/result.txt | head -1 | cut -d' ' -f1)
  got=$(zstd -dc $d/proof.lrat.zst | sha256sum | cut -d' ' -f1)
  [ "$raw" = "$got" ] && echo "$(basename $d) round trip OK $got" || echo "$(basename $d) ROUND TRIP MISMATCH raw=$raw got=$got"
done
