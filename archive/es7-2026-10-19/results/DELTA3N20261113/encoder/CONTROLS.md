# Encoder controls, completed 13 November 2026

**COMPUTED:** 501,024 individual Delta-failure comparisons, zero mismatches.
**CERTIFIED:** six small new-encoding UNSAT instances accepted by cake_lpr.
**COMPUTED:** three recorded cap-side obstructions returned SAT and were
independently verified; none is a weak/cup-side obstruction.

Full parameters, artifact paths, exact hashes, logs' verdict lines, times,
sizes and counts are retained in [control_report.json](control_report.json).
CNFs and LRAT files remain in the assigned scratch directory. No proof was
deleted. These controls reproduce known cases and do not extend the
universal frontier.

## Individual-clause semantics

`semantic_controls.py` independently enumerates all signotopes on 4, 5,
and 6 labelled points: 8, 62, 908. For each case below, direct semantics
checks all triples for caps and all 4-subsets for convexity, partitions
each convex target by chord sign, and evaluates every subset Delta.

It compares that answer with three SAT formulations:

1. the compiled bounded-deletion lattice;
2. the compiled encoder's flat pool, retaining the compact seeds;
3. the original `eager_cert.Enc` or `upper_exact.build` imported read-only.

For each CNF it separates the final all-Delta pool from the definitions,
guards each individual failure clause with a distinct selector, fixes
every orientation variable, and asks whether that selected clause can be
satisfied. Thus the test checks both directions of each existential
witness encoding, rather than accepting a vacuous whole-formula UNSAT.
It also checks base satisfiability for every enumerated signotope,
including invalid configurations.

| m | n | mode | signotopes | valid | individual comparisons | mismatches |
|---:|---:|---|---:|---:|---:|---:|
| 4 | 5 | cup | 8 | 8 | 384 | 0 |
| 5 | 5 | weak | 62 | 54 | 5,184 | 0 |
| 5 | 5 | cup | 62 | 54 | 5,184 | 0 |
| 5 | 5 | cap | 62 | 54 | 5,184 | 0 |
| 5 | 8 | cup | 62 | 61 | 5,856 | 0 |
| 6 | 6 | cup | 908 | 832 | 159,744 | 0 |
| 6 | 6 | cap | 908 | 832 | 159,744 | 0 |
| 6 | 6 | weak | 908 | 832 | 159,744 | 0 |

The m5,n8 row explicitly exercises absent target seeds/children: no
7-gon fits in the ground set. No nonexistent witness is allowed to make a
failure clause true. The m4 row exercises the smallest cap leaves and
empty clauses. All 501,024 queries completed in 1.14 s wall time, peak
RSS 38,484 KiB, with a 350 MiB address-space limit and an 18-second timeout.

## Whole-instance proof controls

All use `--sym none`, `--pool lattice`, AS 340 MiB, CaDiCaL limit 3 s,
cake heap 96 and stack 16, checker limit 3 s. The outer batches were
bounded by 18 s and completed in under one second each. A valid solver
status is not treated as a certificate: each row below has the exact
line `s VERIFIED UNSAT` in its retained `cake.log`.

| instance | fixed signs? | retained directory | LRAT bytes |
|---|---|---|---:|
| cup (5,6), m10 | no | control-cup-n6-m10 | 514,370 |
| cup (5,7), m9 | no | control-cup-n7-m9 | 6,099 |
| cup (5,8), m10 | no | control-cup-n8-m10 | 12,963 |
| cup (5,6), m11 | recorded cap-side fixture | control-cup-same-fixture | 78,117 |
| cup (5,7), m12 | recorded cap-side fixture | control-cup-fixture-n7 | 120,005 |
| cup (5,8), m13 | recorded cap-side fixture | control-cup-fixture-n8 | 232,643 |

The fixed-sign rows certify only those configurations. They do not prove
the statement for every configuration of that size. The universal rows
are already inside the recorded frontier.

## Negative controls: cap side really is false

Fixtures are the old record's
`DELTA2N20261113/data/cex/upperchain_weak_a5_n{n}_m{m}.json`, read-only.
The compiled cap-side CNF was pinned to the fixture's orientation signs.
Each returned SAT. The separate checker then reconstructed targets using
the 4-subset convexity definition, checked no 5-cap/no n-gon, and counted
all working Delta subsets. For the two real fixtures it also recomputed
every orientation determinant from the supplied integer coordinates.

| n,m | realization | 4-caps | weak Delta | cup-side Delta | cap-side Delta |
|---|---|---:|---:|---:|---:|
| 6,11 | exact integer points | 5 | 861 | 684 | **0** |
| 7,12 | abstract only | 9 | 2,541 | 2,433 | **0** |
| 8,13 | exact integer points | 5 | 5,746 | 5,746 | **0** |

These rows test the opposite sign convention and long complementary cup
witnesses, as well as sensitivity of the whole exists-forall formula to a
real counterexample. The abstract m12 fixture has `P: null`; the checker
correctly treats that as no coordinate realization, not as a point set.
The cup-side CNFs on the same signs were independently cake-checked UNSAT
as listed above.

Finally, the m10 cup proof was copied with its final three lines removed.
cake_lpr rejected that owned copy with

    c empty clause not derived at end of proof

and did not emit `s VERIFIED UNSAT`. The original proof remains intact.
Both the truncated copy and rejection log are retained. This guards
against accidentally treating a process exit code as certification.

## Resource scope and outstanding work

Only compilation, generation, fixed small controls and exhaustive m<=6
comparisons were run by this encoder track. None exceeded 20 seconds.
No systemd unit or frontier solve was launched here. The parent separately
scheduled cup n6 m14/m15 and n7 m14; n8 m14 is next when its budget permits.
The n6m15 run subsequently returned an abstract cup-side counterexample;
DESIGN.md and `frontier_n6m15.json` record that separate COMPUTED result.
Its Euclidean realizability is unresolved in this record. The other outcomes
are not inferred from these control results.

The generator's memory advantage is measured. A solver speed advantage is
not established: sharing introduces auxiliary variables and changes
propagation, so compact CNFs can still be slower to refute. The exact flat
variant and safe cube option remain available for parent-scheduled
comparisons if needed.
