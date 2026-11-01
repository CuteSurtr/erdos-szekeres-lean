#!/bin/bash
# Stream an archived (zstd) mirror CNF into evalbig, hashing the decompressed bytes on the way.
# usage: run_big.sh TAG ARCHIVE.zst CONF   -> big/TAG.eval.log, big/TAG.sha256
O=$(cd "$(dirname "$0")" && pwd)
tag=$1; arc=$2; conf=$3
cd $O
s=$(date +%s)
zstd -dc "$arc" | tee >(shasum -a 256 | cut -d' ' -f1 > big/$tag.sha256) | /usr/bin/time -l ./evalbig $conf 7 > big/$tag.eval.log 2> big/$tag.eval.err
echo "pipeline status ${PIPESTATUS[*]} wall $(( $(date +%s) - s )) s" >> big/$tag.eval.log
sleep 2
echo "decompressed sha256 $(cat big/$tag.sha256)" >> big/$tag.eval.log
cat big/$tag.eval.log
grep -E "conv vars|maximum resident|UNEXPLAINED" big/$tag.eval.err | head -25
