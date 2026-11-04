# Sixfold mathematical separation summary

**Final exact-computation record.** 39 verified families comprise 38 positive zero-identity families and 1 family based on negative-definite quadratic combinations. Their clause counts sum to 5,385,408; this sum does not deduplicate across families.

**Written proof + exact computation.** Every retained source has positive integer weights, exact direct seed-polynomial verification, model-hash binding and exact certified-set regression tests. Large linear and quadratic sources additionally invoke the independent checker before queueing. Small linear sources receive the separately retained batch independent checks. Numerical LP/SDP statuses only guide searches.

There are 101,316,696 source certified-set tests and 1,284,096 additional emitted-clause tests. Sources on at most four orbits use exhaustive linear tests; larger linear and quadratic sources use explicitly finite samples plus original/mirrored tests of every emitted canonical clause. The largest retained source uses 7 orbits. `math_catalog.json` states each scope and hash.

**Method boundary.** Model0033 has an independently checked rational lift satisfying all 5,710 strict orientation inequalities and decreasing positive radii, and the main campaign finds its full product graph acyclic. A 16-row negative-definite certificate on five orbits nevertheless excludes its prescribed geometric rotation. This is a concrete separation between these tested methods, not a completeness or general dominance assertion. Model0046 shows why full linear search is needed after small restrictions: a 39-row zero identity on seven orbits excludes it after every two-/three-/four-orbit linear restriction survives.

**Limits.** These are obstructions to the specified Euclidean rotational realization, not claims that the underlying abstract order type has no other realization. A feasible lift would not prove rank-one realizability. The mathematical lane alone does not settle the 60-point case or change the bound 54 ≤ maximum ≤ 60.

**Evidence only (resources).** The largest recorded math process peak RSS is 392.3 MB. Numerical searches and family checks run serially with one compute core. The written proofs are in `math.md` and `math_sdp.md`; compact certificate records are in `math_witnesses/`.

**Final unresolved boundary.** Model0090 has an independently checked rational linear lift with minimum strict margin `2/3491`. The particular lift is indefinite, while PSD feasibility and geometric realizability remain unresolved. Ten nine-orbit SDP probes and 1,218 rounded integer semidefinite-dual attempts produced no exact certificate. No cut was queued for this model; numerical near-zero margins were not accepted as proof. Details and the model hash are in `math_sdp.md`.

**Archive verification.** Every retained math artifact was compressed with one worker and checked by decompression against its raw SHA-256. `math_summary.json` records archive totals and the manifest hash. The watcher stopped and its managed child process group was reaped; no mathematical search remains running.
