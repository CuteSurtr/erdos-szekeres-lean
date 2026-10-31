#!/bin/bash
# Solve a whole CNF from scratch with an LRAT proof and check it with lrat-check.
# usage: lrat_full.sh CNF PROOF CADICAL LRATCHECK LOG [cadical options...]
CNF="$1"; PRF="$2"; CAD="$3"; CHK="$4"; LOG="$5"; shift 5
{
  echo "cnf $CNF"
  echo "sha256 $(shasum -a 256 "$CNF" | cut -d' ' -f1)"
  echo "solver_options $*"
  date
  /usr/bin/time -l "$CAD" -q --lrat=1 --binary=0 "$@" "$CNF" "$PRF" 2>&1 | grep -E '^s |real|maximum resident'
  echo "proof_bytes $(stat -f %z "$PRF")"
  date
  /usr/bin/time -l "$CHK" "$CNF" "$PRF" 2>&1 | grep -E 'VERIFIED|FAILED|WARNING|parsed|time|real|maximum resident'
  echo "lrat_check_exit ${PIPESTATUS[0]}"
  date
} > "$LOG" 2>&1
