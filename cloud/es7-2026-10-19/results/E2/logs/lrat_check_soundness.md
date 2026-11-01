# lrat-check soundness problem (found 2026-10-20, E2)

Checker: drat-trim/lrat-check, git 2e3b2dc (= upstream master on 2026-10-20; the same
commit task E used).

Reproduction (any satisfiable CNF):

    printf 'p cnf 1 1\n1 0\n' > triv.cnf      # satisfiable: x1
    echo "2 0 0" > triv.lrat                    # "clause 2 = empty clause, no hints"
    lrat-check triv.cnf triv.lrat               # prints "c VERIFIED", exit 0

Same result for n12k6m3.cnf (SAT, model checked) with the proof line "37828 0 0".

Cause (lrat-check.c, checkClause): a lemma whose RUP hints end without a conflict falls
through to the RAT branch; the line `if (res == SUCCESS) return FAILED;` is commented
out, and with no RAT hints the lemma is accepted when intro[pivot^1] == 0.  For the empty
clause the pivot is convertLit(0), for which intro[] is always 0, so the empty clause is
accepted with any non-conflicting hint list, including none.

Consequence: "c VERIFIED" from this lrat-check build does not certify UNSAT.  The task E
results "LRAT-checked (c VERIFIED)" (n33k7d3, n33k7m3refl, n33k7d3direct) were checked
with this build, so they are solver claims plus a check that would also have passed a
bogus proof whose final step is unjustified.  The proofs are probably fine (CaDiCaL wrote
them), but they need re-checking with a sound checker.  See lrat_recheck.log for E2's
re-checks with a patched lrat-check and with an independent checker.
