#!/bin/sh
# All nodes of results/C3-S/manifest_depth2.tsv, in batches of 10 (base generated once per batch).
# usage (from results/C3L): scripts/compare_all_nodes.sh WORKDIR > logs/compare_all_nodes.log
W=$1
awk -F'\t' 'NR > 1 {print $2, $4}' ../C3-S/manifest_depth2.tsv > "$W/all.txt"
cut -d' ' -f1 "$W/all.txt" | xargs -n 10 | while read names; do
  .lake/build/bin/c3_dimacs node 11 7 "$W" $names
  for nd in $names; do
    exp=$(awk -v n="$nd" '$1 == n {print $2}' "$W/all.txt")
    got=$(sha256sum < "$W/$nd.cnf" | cut -c1-64)
    if [ "$got" = "$exp" ]; then r=MATCH; else r=MISMATCH; fi
    echo "$nd $got $r"
    rm -f "$W/$nd.cnf"
  done
done
