# Task C: the mirror-symmetric class at 33 points (in progress)

Part 1 (encoding validation) is complete; Parts 2 and 3 are running. This file will be
replaced by the final report at the end of the run.

- `logs/part1_validate_report.json`: 1,000 random exactly mirror-symmetric 33-point sets
  (all orientation-only clauses satisfied in both frames) and small-k equivalence tests.
- `logs/part1_controls.log`: k = 5 and k = 6 controls (LRAT-checked UNSAT) and the 32-point
  positive control.
- `scripts/`: encoder post-processor, validation, cube-and-conquer driver and worker,
  mirror annealer with exact axis scan.
