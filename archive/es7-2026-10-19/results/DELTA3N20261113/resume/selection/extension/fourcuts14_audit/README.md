# Four-family n7/m14 cut augmentation — PASS

Independent streamed reconstruction of all48 unique clauses and52 provenance
entries, unchanged audited exact base, Boolean truth controls and exact real
positive controls. The all-cap proof is reviewed independently; the three
older families inherit the frozen allcuts14 audit. No solver or proof replay
is run here. Limits AS300MiB, one CPU, wall20/CPU19. Earlier packets remain
frozen. This formula excludes real terminal counterexamples only under its
explicit geometric and prior-size dependencies; it is not abstract formula
equivalence. No UNSAT or finite14 conclusion is claimed without certification.

**COMPUTED:** all48 rows,52 provenance entries,10608 literals and every
original base byte match. Eleven distinct rows are new relative to the
frozen three-family formula. The output has32086 variables,231661 clauses,
633848 literals and SHA256
`3c6c1f83e2cf426ca13eb2e9ba7e363a1da42f1138cc3b9503c57601678e5788`.

**PROVED (written):** the appended rows preserve the canonical assignment
of every real n7/m14 terminal counterexample under the explicit dependencies
in [VERIFY_FOURCUTS14.md](VERIFY_FOURCUTS14.md). Exact controls:52 real sets,
185 selectors,104 real cut comparisons,52 canonical Boolean assignments,
10920 mixed flips,8008 pure flips and16576 exhaustive small comparisons.
The successful check took0.504s; all input hashes remain stable.

AttemptA reached its19s CPU cap when the reused optional thinning helper
was applied to m4,n7, outside that helper's nonnegative size-bound domain.
Its source and empty logs/time report are preserved in data/attemptA.
The final driver validates the actual selected sets and ambient witnesses
directly, without irrelevant thinning. No geometric row failed, no memory
limit was approached, and no frozen checker was edited. The successful
run stays within the original AS300/oneCPU/20s allowance.

Files: tools/check.py is the independent audit, run.sh the exact command,
data/result.json the row/hash receipt, data/controls.json the coordinates
and witnesses, and SHA256SUMS the frozen manifest. The producer and written
notes are retained as source snapshots. ROOTED_LEMMA is contextual only;
this audit makes no new independent rooted-lemma claim. Resume by reading
the frozen result; reruns need a fresh exclusive output record.

At08:23 the parent reports the fourcuts14 search finished UNKNOWN and its
archive roundtrip passed. There is no certificate and no new finite14
terminal theorem from this run. No new search is launched or requested.
