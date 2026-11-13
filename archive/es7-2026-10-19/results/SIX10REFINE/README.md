# SIX10REFINE: exclusion of the 60-point sixfold model `model0090` (4 November 2026)

**Context.** At 10 layers (60 points) the GP-refined sixfold encoding still had the abstract model `model0090` (review
archive `es8-rot-refine-2026-11-04/m6/models/model0090.json`, SHA-256 `62b5c1d0…`). It passes all GP sign relations,
has an acyclic product graph, and admits a strictly feasible linear lift.

**Exact computation plus written proof (not refereed).** `model0090` has no realization with the prescribed Euclidean
sixfold rotation.
- **Certificate.** There are 36 signed orientation triples with positive integer weights. Their weighted sum is a
  negative semidefinite quadratic form on the 20 real seed coordinates.
- **Kernel.** The form vanishes exactly on a 4-dimensional face W: layers 1–8 collapse onto one orbit and layer 9 onto
  the centre.
- **Off the kernel.** Minus the form is positive definite on the complement, with 16 positive rational LDL pivots.
- **Contradiction.** A realization would make the weighted sum strictly positive, which is impossible.
- **Files.** The witness is `face_sparse0090/face_witness.json` (`6747891d…`). Two exact checkers accept it: `face_cert.py`,
  and the independent stdlib `check_cert.py`, which the coordinator re-ran with result `ok: true`.
- **Why earlier attempts missed it.** The earlier search looked for a strictly negative-definite form, but the PSD
  relaxation's optimum sits exactly at margin 0 on W. So only a semidefinite certificate on that face exists.

**Loop (exact computation per round).** The 36-literal cut (`cut_model0090_sparse.clauses`) was added, and the
refinement repeated for 55 rounds.
- **Every round SAT.** Each round was SAT, and every model passed full GP.
- **Models 1–54.** Each was excluded on the same face W, with 25–35 terms each and both checkers passing.
- **Model 55.** It leaves the face. It was excluded by a 55-term negative-definite certificate on layers 0–8, checked by
  `check_def.py`, but its cut was not added before the deadline.
- **Result.** No UNSAT, and no near-realization was found. The sixfold maximum stays **54 or 60**.

**Open issues.**
- **Cut strength.** Each cut is a single clause. Relabelings that keep W cut none of the loop models.
- **Review.** The certificates have had no second-person review.

**Files.** The full working directory, with all 55 rounds, witnesses and logs, is archived in
`proof-archives/final-2026-11-04-six` (zstd, round trip verified). `REPORT.md` is the agent's full report.
