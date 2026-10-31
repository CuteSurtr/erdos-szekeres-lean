#!/bin/bash
# usage: run_cad.sh tag timeout_s [cadical args...]
tag=$1; T=$2; shift 2; OUT=${OUTTAG:-$tag}
D="$(cd "$(dirname "$0")" && pwd)"
CAD="${CADICAL:-cadical}"
s=$(date +%s)
/usr/bin/time -p "$CAD" "$@" -t $T "$D/cnf/$tag.cnf" > "$D/runs/$OUT.out" 2> "$D/runs/$OUT.time"
ec=$?
e=$(date +%s)
echo "$OUT exit=$ec $(grep '^s ' "$D/runs/$OUT.out") wall=$((e-s))s $(grep -E '^(real|user)' "$D/runs/$OUT.time" | tr '\n' ' ') args=[$*]" >> "$D/runs/summary.txt"
