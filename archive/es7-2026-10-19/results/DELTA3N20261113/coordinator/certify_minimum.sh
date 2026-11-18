#!/bin/bash
set -euo pipefail
ulimit -v 524288
cd /home/jay/research/data/delta3-codex-20261113/coordinator/minimized/counterexample
for tag in unconstrained_lower cap_free_same_size; do
  set +e
  /usr/bin/cadical --lrat=true --binary=false "$tag.cnf" "$tag.lrat" > "$tag.cadical.out" 2>&1
  rc=$?
  set -e
  test "$rc" -eq 20
  /home/jay/.local/bin/cake_lpr --CML_HEAP_SIZE=256 --CML_STACK_SIZE=32 "$tag.cnf" "$tag.lrat" > "$tag.cake.out" 2>&1
  grep -Fx 's VERIFIED UNSAT' "$tag.cake.out"
done
sha256sum *.cnf *.lrat *.cake.out witness.json independent_audit.json > SHA256SUMS
touch VERIFIED
