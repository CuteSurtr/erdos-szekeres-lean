#!/bin/bash
# Behavioural controls for every lrat-check build found on this machine (tiny inputs only; never runs cake_lpr).
# usage: checker_controls.sh OUTDIR BIN1 [BIN2 ...]
set -u
D=$1; shift; mkdir -p "$D/ctl"; cd "$D/ctl"
printf 'p cnf 1 1\n1 0\n' > sat1.cnf                  # satisfiable
printf '2 0 0\n' > forged_nohint.lrat                  # empty clause, no hints
printf '2 0 1 0\n' > forged_hint.lrat                  # empty clause, a non-conflicting hint
printf 'p cnf 1 2\n1 0\n-1 0\n' > unsat2.cnf           # unsatisfiable
printf '3 0 1 2 0\n' > genuine.lrat                    # genuine RUP proof of the empty clause
printf '3 0 1 0\n' > unsat_badhint.lrat                # UNSAT CNF but hint does not reach a conflict
for b in "$@"; do
  h=$(shasum -a 256 "$b" | cut -c1-16)
  for t in "sat1.cnf forged_nohint.lrat reject" "sat1.cnf forged_hint.lrat reject" "unsat2.cnf genuine.lrat accept" "unsat2.cnf unsat_badhint.lrat reject"; do
    set -- $t
    out=$("$b" "$1" "$2" 2>&1); rc=$?
    v=$(printf '%s\n' "$out" | grep -m1 -E 'VERIFIED|FAIL|rror' || true)
    printf '%s\t%s\t%s\texpect=%s\trc=%s\t%s\n' "$h" "$1" "$2" "$3" "$rc" "$v"
  done
done
