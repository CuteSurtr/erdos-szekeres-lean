#!/bin/sh
# Check `c3_dimacs node 11 7` against results/C3-S/manifest_depth2.tsv (column cnf_sha256).
# usage (from results/C3L, after `lake build`): scripts/compare_nodes.sh WORKDIR NODE...
# Prints: node units(header delta) expected_sha lean_sha MATCH|MISMATCH. Node CNFs are deleted.
W=$1; shift
for nd in "$@"; do
  exp=$(awk -F'\t' -v n="$nd" '$2 == n {print $4}' ../C3-S/manifest_depth2.tsv)
  eu=$(awk -F'\t' -v n="$nd" '$2 == n {print $3}' ../C3-S/manifest_depth2.tsv)
  .lake/build/bin/c3_dimacs node 11 7 "$W" "$nd"
  got=$(sha256sum < "$W/$nd.cnf" | cut -c1-64)
  nc=$(head -1 "$W/$nd.cnf" | cut -d' ' -f4)
  if [ "$got" = "$exp" ]; then r=MATCH; else r=MISMATCH; fi
  echo "$nd units=$((nc - 4154921)) manifest_units=$eu $exp $got $r"
  rm -f "$W/$nd.cnf"
done
