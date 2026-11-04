# FIVEIDENT: pentagon identity clauses on the fivefold threshold instance (4 November 2026)

**Question.** Do the exact pentagon identities found on the review branch make m5K8t13 + H(1) cubes tractable? These are
four families of linear identities over Q(√5), turned into clauses (`proof-archives/es8-rot-refine-2026-11-04/m5/`).

**Answer.** No (evidence only). All 9 runs of 7–12 minutes were UNKNOWN, with or without the identities.

**Soundness of the identity clauses.** Written proof (reviewed, not refereed), with exact computation for the identities
and their tests on the certified 56-point set. The arguments are quoted in the agent's report.

**Root effect (exact computation, two unit-propagation implementations agree).**
- **linear00.** The 1,560-clause 3-term family forces 1,939 extra variables at the root, 89 of them orientation
  variables.
- **The other families.** The 7-, 5- and 8-term families force none.

**Matched runs (evidence only; one seed).**
- **Search counts.** The augmented formula gets 19–30% fewer conflicts and 16–38% fewer decisions in the same time.
- **Fixed variables.** The fixed-variable gap stays at about the root gap of 1,939.
- **Throughput.** The loss comes from the 350k long clauses.
- **Data.** Per-run figures are in `results.tsv`.

**Verdict.** linear00 is cheap and adds root information. linear01–03 cost about 20% throughput and add nothing at the
root. Nothing suggests these identities make m5K8t13 tractable.

**Files.**
- **Scripts.** `build.py` assembles the formulas and checks the family hashes and exact-test metadata against the
  review's assembly. `up.py` is the unit-propagation check; `stats.py` and `launch.sh` drive the runs.
- **CNFs.** About 800 MB, rebuildable in about 10 s; their hashes are in `*.assembly.json`.
- **Certificates.** None, since no run was UNSAT.
