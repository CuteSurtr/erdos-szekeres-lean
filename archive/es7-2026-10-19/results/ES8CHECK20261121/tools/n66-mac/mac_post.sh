#!/bin/bash
# mac_post.sh <certdir>: the level-15 disk policy of cubes20261120/README.md section 2 (c15_post.sh, which is not in git,
# re-implemented from that description): trim.lrat and cert.cnf -> zstd; an original is removed only after the SHA-256 of
# the decompressed stream equals the value in cert.json (trim_lrat_sha256, full_cnf_sha256). trim.cnf stays uncompressed.
set -u
d=$1
for pair in "trim.lrat:trim_lrat_sha256" "cert.cnf:full_cnf_sha256"; do
  f=${pair%%:*}; k=${pair##*:}
  [ -f "$d/$f" ] || continue
  want=$(python3 -c "import json,sys;print(json.load(open(sys.argv[1]))[sys.argv[2]])" "$d/cert.json" "$k")
  [ -f "$d/$f.zst" ] || zstd -q -3 -T1 "$d/$f" -o "$d/$f.zst" || { echo "post $d: zstd $f failed"; continue; }
  got=$(zstd -dc "$d/$f.zst" | shasum -a 256 | cut -c1-64)
  if [ "$got" = "$want" ]; then rm -f "$d/$f"; echo "post $d: $f.zst ok ($got), original removed"
  else echo "post $d: $f.zst hash $got != cert.json $want; original KEPT"; fi
done
