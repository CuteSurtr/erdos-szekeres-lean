# Final report: chord-lemma threshold cubes (generated 2026-11-05 16:00:59 KST by supervisor.py v2)

This report is generated automatically. It claims no bound. Verdicts come from cake_lpr; lrat-check is not used.

## 5-fold (24 phase-order cubes)

- phase-order cubes UNSAT, proof accepted by cake_lpr: 0 of 24
- transitivity-violating patterns UNSAT, proof accepted by cake_lpr (imp2_results.tsv): 40 of 40
- cover complete with every proof accepted by cake_lpr: NO

| cube | status |
|---|---|
| cubes5/o1234.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o1243.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o1324.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o1342.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o1423.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o1432.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o2134.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o2143.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o2314.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o2341.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o2413.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o2431.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o3124.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o3142.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o3214.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o3241.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o3412.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o3421.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o4123.cnf | UNRESOLVED-AT-CUTOFF |
| cubes5/o4132.cnf | NEVER-STARTED |
| cubes5/o4213.cnf | NEVER-STARTED |
| cubes5/o4231.cnf | NEVER-STARTED |
| cubes5/o4312.cnf | NEVER-STARTED |
| cubes5/o4321.cnf | NEVER-STARTED |

## 4-fold (12 phase-order cubes)

- phase-order cubes UNSAT, proof accepted by cake_lpr: 0 of 12
- transitivity-violating patterns UNSAT, proof accepted by cake_lpr (imp2_results.tsv): 20 of 20
- cover complete with every proof accepted by cake_lpr: NO

| cube | status |
|---|---|
| cubes4/o1234.cnf | LOST-WRAPPER-KILL |
| cubes4/o1243.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o1324.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o1342.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o1423.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o1432.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o3124.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o3142.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o3412.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o4123.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o4132.cnf | UNRESOLVED-AT-CUTOFF |
| cubes4/o4312.cnf | UNRESOLVED-AT-CUTOFF |

## Remaining obligations before any theorem can be stated

- Every phase-order cube and every transitivity pattern UNSAT, with each proof accepted by cake_lpr (table above).
- Soundness of encoder A for (m, K) = (5, 8) and (4, 8): written proof, reviewed in ROT456 section 2, not Lean-checked.
- Soundness of the reflection unit (H(1) for odd m, Y(1,2) for even m): written, C7UPPER / C6UPPER section 2.
- The chord lemma: written proof; every added clause is proved by an independent exact verifier (CHORD20261105 section 6).
- Unresolved cubes need longer runs or a finer split, for example by the position of layer 5. Their partial LRAT files are
  unfinished and unverified; this script deletes one only when that is needed to keep 400 GB of disk free.

Health at report time: Tctl 44.75 C, MemAvailable 55.5 GiB, swap used 1.4 GiB, disk free 518 GB.
