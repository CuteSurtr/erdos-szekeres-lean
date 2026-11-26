#!/bin/bash
# verify_zst.sh (26 Nov 2026): for every kept proof of the d1 queue and of n66-resolve-20261125, decompress the
# .lrat.zst and compare its SHA-256 with the lrat_sha256 that certify_cnf.sh recorded (certify.jsonl) before
# compressing. Read-only. Output: <set>/zst_roundtrip.tsv (id, expected, got, OK|BAD). 8 at a time.
set -u
one() { # $1 = certify.jsonl
  python3 -I -c '
import json,sys
d=[json.loads(x) for x in open(sys.argv[1]) if "\"s VERIFIED UNSAT\"" in x][-1]
print(sys.argv[1].split("/")[-2], d["lrat_sha256"], d["proof"])' "$1" | while read -r id want p; do
    got=$(zstd -dcq "$p" | sha256sum | cut -c1-64)
    [ "$got" = "$want" ] && s=OK || s=BAD
    printf '%s\t%s\t%s\t%s\n' "$id" "$want" "$got" "$s"
  done
}
export -f one
for S in /home/jay/research/data/resolve-queue-20261126/d1 /home/jay/research/data/n66-resolve-20261125; do
  ls $S/out/*/certify.jsonl | xargs -P 8 -I{} bash -c 'one {}' | sort > $S/zst_roundtrip.tsv
  echo "$(date '+%F %T') $S: $(grep -c OK$ $S/zst_roundtrip.tsv) OK, $(grep -c BAD$ $S/zst_roundtrip.tsv) BAD of $(ls $S/out/*/certify.jsonl | wc -l)"
done
