# A sufficient small-transversal route to weak D(5,8)

**PROVED conditional lemma.** Suppose S has no five-cap and there is a set
A of at most five points such that S minus A has no convex hexagon. Then S
has a weak Delta for n=8, without needing an octagon-free assumption.

Every convex heptagon meets A in at least two points: otherwise its six old
vertices would form a hexagon. Choose a four-cap-free subset R of A omitting
at most one point. For |A|≤3 take A; for |A|=4 take any three points. For
|A|=5 some four-subset is not a cap, since otherwise every triple of A would
be negative and A would itself be a forbidden five-cap. Such an R meets
every heptagon and proves the claim. This is the lift track's insertion
lemma applied to an unspecified hexagon-free remainder.

**COMPUTED: the sufficient condition fails for abstract signotopes at m=16.**
A SAT witness has no five-cap or octagon, 671 hexagons and 121 heptagons.
Every one of its 4,368 five-point deletions leaves a hexagon. Its minimum
hexagon-transversal size is exactly six; one example is {0,2,3,4,5,9}.
However, it has 16,794 working weak Deltas, including {0,3,4}.
This refutes only the proposed abstract sufficient condition.

Real realizability is unresolved. Three hundred numerical starts found no
exact realization; this failure is not evidence of nonrealizability. The
corresponding sufficient condition for real sets remains open here.

`transversal_cnf.cpp` searches for failure of that condition. It includes
the compact encoder's audited geometric base unchanged, including exact
convexity flags through size seven. For six-subsets J aliases exact
convexity. At larger sizes through m−5, J implies the OR of seven selected
one-vertex-deletion children. Any six-set avoids one of those seven vertices,
so the intended containment values give a canonical assignment, and every
true J descends to an actual hexagon. A unit J(C) for every (m−5)-subset C
therefore says every complement of a five-point deletion still has a hexagon.
Smaller deletions cannot do better. No symmetry or particular transversal
is selected. SAT is only a failed sufficient condition; UNSAT needs a fresh
LRAT certificate before supporting the weak-Delta consequence.

## Independent-from-encoder check and artifacts

`check_transversal.py` imports neither encoder. It checks every four-point
packet, all five-cap and octagon exclusions, and all possible deletion masks
with an unrestricted subset transform. It also verifies every emitted clause
under both the solver's full assignment and a reconstructed canonical
assignment. All 241,748 clauses, 935,246 literals and 74,322 variables pass.
The original and mapped regenerated CNFs have the same SHA-256:
`043d8b6f7b5446d8fdb48a6f4a786c79d2660ffa33f856ea6a4eb628ac667d7f`.

Small evidence is in `data/transversal/`, especially `geometry.json`,
`exact_audit.json`, `probe.out`, and the unsuccessful `realization.log`.
Large CNFs, variable map, binaries and the partial SAT trace remain at
`/home/jay/research/data/delta3-codex-20261113/resume/pool/transversal/`;
their hashes are in `../data/archive_manifest.json`. The SAT trace is not
an UNSAT certificate. This late parent experiment was not part of the
separate agent audit of the compact and embedding encoders.

The probe used a 10-second solver allowance. Realization used one numerical
thread, AS500MiB and an 18-second internal limit; the exact checker used
AS400MiB and a 25-second external deadline, completing in under one second.
To repeat the exact check from the repository root:

```sh
timeout --kill-after=2 25 prlimit --as=419430400 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  cloud/es7-2026-10-19/results/DELTA3N20261113/resume/pool/check_transversal.py \
  --dir /home/jay/research/data/delta3-codex-20261113/resume/pool/transversal
```
