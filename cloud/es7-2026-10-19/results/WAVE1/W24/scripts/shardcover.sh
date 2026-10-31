#!/bin/bash
# Cover check of one case-shard with results/Mii-S/scripts/covercheck.py.
#   1. top.icnf alone must be COVERED (march_cu -d 7 gives a full partition of the case);
#   2. leaves.icnf plus the top cubes of the other shards (lines i with i mod k != s) must be
#      COVERED; since every leaf extends one of this shard's top cubes, this holds exactly when
#      the verified leaves cover this shard's part.
# Usage: shardcover.sh DIR s k
set -e
DIR="$1"; S="$2"; K="$3"; HERE="$(cd "$(dirname "$0")" && pwd)"
CC="$HERE/../../../Mii-S/scripts/covercheck.py"
echo "top.icnf: $(python3 "$CC" "$DIR/top.icnf")"
T=$(mktemp); awk -v s="$S" -v k="$K" '/^a/{ if ((n % k) != s) print; n++ }' "$DIR/top.icnf" > "$T"
echo "other-shard top cubes: $(wc -l < "$T")"
echo "leaves.icnf + other shards: $(python3 "$CC" "$DIR/leaves.icnf" "$T")"
rm -f "$T"
