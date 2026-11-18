# COMPUTED failure candidate — parent notice

Historical notice. The final frozen result is an 18-point witness; see
`README.md`, `PROOF.md` and `PARENT_READY.md`. The parent has independently
checked the geometry and freshly certified the 108-clause core. The weaker
envelope criterion holds for all rightward X on the final witness.

The terminal-rank selection finder returns **UNSAT_UNCERTIFIED** on the
23-point real fixture at line 76 (zero-based index 75) of
`/home/jay/research/data/etvthy-20261113/pool_hept.jsonl`, parameter n=7.
The ordinary weak-Delta formula has a satisfying exact Boolean model.

Scratch prefix:
`/home/jay/research/data/delta3-codex-20261113/selection/terminal/hept-0075-n7`.
Files `.input.json`, `.points`, `.geometry.json`, `.terminal.cnf`,
`.terminal.finder.log`, `.weak.cnf`, `.weak.finder.log`, `.result.json`
retain coordinates, provenance, actual polygons/triples, clauses and models.
The encoder reports max cap=4, max convex polygon=6, 409 four-caps,
533 rank-three terminal triples and 1930 target hexagons.

This is a finder result, not a certificate or yet an independent geometric
audit. Minimization and a separate checker are in progress. The parent
should wait for the minimized ready packet before a fresh certificate.
No old manifest or other track was changed.
