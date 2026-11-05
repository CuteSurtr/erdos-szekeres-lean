#!/bin/bash
# Reproduce the lrat-check soundness defect (drat-trim 2e3b2dc) and the correct behaviour of cake_lpr.
cd "$(dirname "$0")"
echo "== lrat-check on a SATISFIABLE formula with a bogus proof (must be rejected):"
lrat-check sat_formula.cnf bogus_proof.lrat; echo "exit code $?"
echo "== cake_lpr on the same input:"
cake_lpr sat_formula.cnf bogus_proof.lrat; echo "exit code $? (cake_lpr exits 0 either way; only 's VERIFIED UNSAT' counts)"
echo "== cake_lpr on a genuine CaDiCaL proof of an UNSAT formula:"
cake_lpr unsat_formula.cnf genuine_proof.lrat
echo "== the grep pitfall: 'c NOT VERIFIED' matches a plain grep for VERIFIED:"
printf 'c NOT VERIFIED\n' | grep -o -m1 -E 'VERIFIED|FAILED'
