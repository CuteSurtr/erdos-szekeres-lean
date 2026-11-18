# Frozen: one-old-blue repair fails even at a rightmost point

**COMPUTED real witnesses, independently confirmed by the parent; CERTIFIED
full coloring obstructions; PROVED small-size positive lemma.** There are
rightmost-point obstructions for n7 on 14 points and n8 on 16 points. Their
exact minimum number of newly selected old-blue points is **two**. Both
ordinary full weak Deltas and full weak Deltas selecting r exist.

## 1. Statement

For a weak Delta A of S minus {r}, repair cost means
`|B minus (A union {r})|`, where B is a full four-cap-free transversal of
the convex (n-1)-gons in S. Arbitrary deletions from A and either color of r
are allowed. The one-old-blue repair rule fails in both real, five-cap-free,
convex-n-gon-free fixtures below. Indices are zero-based in increasing x.

| Parameter | m | Rightmost r | Old Delta A | Minimum cost | Ordinary full Delta B | Full Delta selecting r |
|---|---:|---:|---|---:|---|---|
| n=7 | 14 | 13 | {5,11,12} | 2 | {1,5,9} | {1,5,9,13} |
| n=8 | 16 | 15 | {7,13,14} | 2 | {2,3} | {2,3,15} |

The n7 positives select old-blue points {1,9}; the n8 positives select {2,3}.
There are respectively **2,669 / 15,356** ordinary full Deltas, of which
**1,091 / 6,164** select r. These are obstructions to repair of a specified
old A, not counterexamples to weak Delta existence or to a favorable-choice
induction.

The earlier interior-root example remains separately frozen in
`data/reduced-n7.json`: n7/m14, r=1, A={5,6,7}, cost 2. Its properties are
not used to infer the rightmost claims.

## 2. Model and written soundness

[THEORY.md](THEORY.md) proves the exact deletion/addition criterion, the
O(m 2^m) min-plus transform, the coloring-CNF correspondence, and:

> If n>=5, S has no five-cap and |S|<=n+2, every old weak Delta admits a
> repair costing at most one old-blue selection. No rightmost-point or
> convex-n-gon-free assumption is needed. If |S|<=n+1, cost zero suffices.

The proof at n+2 uses a noncap four-subset of the five points A union {r,p};
such a subset exists because S has no five-cap, and its complement is too
small to contain a target. The theorem does not promise that r is selected.
The old n7/m9 and n8/m10 deletion-only obstructions require cost one, so
the allowance cannot be reduced to zero at n+2.

The lower bound two also has a direct written proof using private polygons:
a full Delta must omit a vertex t of the four-cap T=A union {r}; private
polygons for t have old-blue supports with empty intersection, so a single
old-blue point cannot hit them all. [PRIVATE_POLYGONS.md](PRIVATE_POLYGONS.md)
lists 12 hexagons for n7 and 13 heptagons for n8 that suffice. Their integer
geometry predicates are COMPUTED. No result here is Lean-checked or refereed.

## 3. Method

`repair.cpp` enumerates exact integer geometry and full Deltas, then applies
one min-plus transform to obtain minimum cost for every old Delta at every
root. Four-caps use consecutive negative turns; convex polygons use monotone
hulls. Intermediates use signed 128-bit integers with an explicit coordinate
bound. There is no pairwise 2^m-by-2^m subset enumeration.

`verify.py` independently implements geometry in Python arbitrary-precision
integers: every triple must be negative for a cap, and supporting edges test
convexity. It scans every full B once for the specified A, checking old-Delta
validity, all forbidden geometries and exact minimum cost. `controls.py`
uses a distinct 0-1 BFS transform and confirms all C++ histograms at every
root, covering 32,293 + 166,896 old-Delta/root pairs in the frozen fixtures.

The parent independently implemented a third coordinate/CNF-family audit
in `../check_obstructions.py`, recording the two cases as independently
confirmed in `../data/parent_obstructions.json`.

## 4. Results and finite search scope

| Bounded probe | Scope and result |
|---|---|
| Initial real-fixture batch | 17 fixtures, m<=16; found an n7/m16 obstruction at internal roots |
| Induced reduction of that fixture | Minimum m14 among checked induced grounds containing the fixed four points; no global minimality claim |
| Rational projections of the m14 fixture | 196 sampled order/reflection cases, 23 valid; a rightmost obstruction found |
| Simple integer projections | 368 tested, 13 valid; projection x'=-x-5y, y'=5x-y supplies a smaller-coordinate rightmost construction |
| ETV42 subset controls for n8 | 400 seeded m16 samples; every valid old Delta repaired with cost zero on these samples |
| Two old-blue near-duplicates | 2,205 n8/m16 candidates, 466 valid; 11 valid candidates had rightmost maximum cost two |

All rejected candidates and outcomes remain in the track's scratch directory.
The frozen n8 case clones two blue points of the simple projection, with
scale 1,000,000 and integer perturbations. Both acceptance and obstruction
were checked exactly, not inferred from numerical proximity.

Before searches were stopped, the rightmost examples were checked under
every induced ground containing their fixed four-point T (using the
small-size theorem below n+3). Every proper such ground had rightmost
maximum cost at most one. Thus the displayed examples are minimal under
those deletions while T is retained. They are not claimed globally smallest.
No further broad probe was run after the parent's freeze request.

## 5. Controls and certificates

- Exact full-Delta positive assignments are recorded separately for either
  color of r and for r selected, in `data/controls.json` and `*.model` files.
- `*-two.cnf` replaces the one-blue pair clauses with two-blue triple clauses;
  both kinds of positive assignments satisfy every clause.
- `positive-n7-one.cnf` and `positive-n8-one.cnf` have the genuine one-blue
  solution {0} on the old deletion-only fixtures.
- An intentionally invalid five-cap is detected. Process failures, rejected
  geometries and unsuccessful finite probes are preserved in
  `data/FAILED_ATTEMPTS.md` and scratch.
- The core CNFs are checked literal subformulas of the full formulas.

The parent ran fresh CaDiCaL 2.1.3 proofs and cake_lpr in
`nov13c-vfy-delta4-obstructions`. Both full formulas have the literal line
`s VERIFIED UNSAT`. This track read those logs and matched CNF, proof and
compressed-proof hashes; it did not independently replay cake. The parent's
compressed round-trip checks passed, and both plain and compressed proofs
remain retained.

| Full one-blue formula | Variables / clauses | CNF SHA-256 | LRAT SHA-256 |
|---|---|---|---|
| n7 | 14 / 213 | `ef26f775f629af551be837b84e9f106948b4163e674018e9980fd225b5df0edd` | `aa502ff4a7bee4a01aef7c9e15b2dd4f60838c8dda63222607953d110258b1ac` |
| n8 | 16 / 277 | `6517d49858bbaf2ae7cd743fb1d4597f62f8320ad05642a9952ea8ae65950f74` | `4eb33137aa612a3aeb077cbdc1b03f51df6d328a08c85095dc197b0bb324d194` |

Proofs are at
`/home/jay/research/data/delta3-codex-20261113/selection/certificates/repair7/`
and `repair8/`. `data/PARENT_CERTIFICATES.json` pins the parent audit entries,
certificate sources and matching hashes. The original frozen `*-audit.json`
files still describe the pre-certification snapshot; this certificate index
supersedes their historical UNSOLVED status. No finder-only UNSAT claim is used.

## 6. Files and hashes

- Frozen rightmost coordinates: `data/rotation-best.json` (n7) and
  `data/two-clones-n8-best.json` (n8).
- Complete coordinate audits and geometric families: `data/rightmost-n7-audit.json`
  and `data/rightmost-n8-audit.json`.
- Full formulas: `data/rightmost-n7-one.cnf`, `data/rightmost-n8-one.cnf`.
- Written proofs: `THEORY.md`, `PRIVATE_POLYGONS.md`; local verification report:
  `VERIFY_REPAIR.md`.
- Concise frozen output: `RESULT.json`; scoped hashes: `MANIFEST.json`.
- Retained scratch:
  `/home/jay/research/data/delta3-codex-20261113/selection/repair/`.

All new repository files are confined to this repair directory. No old
manifest, other track, git state or installation was changed. Each local
probe used one pinned CPU, at most 19 seconds plus a one-second kill grace,
CPU limit 18 seconds and AS 400 MiB; compilation used AS 500 MiB. The parent
alone scheduled certification. This track launched no long unit and has
no remaining job.

## 7. What remains

Weak D(5,7) and D(5,8), favorable old-Delta selection, and general rooted
existence remain outside the conclusions. The written positive theorem is
not Lean-formalized. Global minimality of the repair obstructions and a
universal two-old-blue repair theorem are not asserted. This track is frozen;
no further search is proposed here.

## 8. Reproduction without modifying frozen inputs

Copy this entire track into a new replay directory under its scratch path
before rerunning scripts that write outputs. For example, from the repository
root, with that replay directory not already present:

```sh
REPAIR_RECORD=cloud/es7-2026-10-19/results/DELTA3N20261113/resume/selection/repair
REPAIR_REPLAY=/home/jay/research/data/delta3-codex-20261113/selection/repair/replay-record
cp -a "$REPAIR_RECORD" "$REPAIR_REPLAY"
timeout --kill-after=1 19 taskset -c 30 prlimit --as=419430400 --cpu=18 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$REPAIR_REPLAY/verify.py" "$REPAIR_RECORD/data/rotation-best.json" replay-n7
timeout --kill-after=1 19 taskset -c 30 prlimit --as=419430400 --cpu=18 \
  /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B \
  "$REPAIR_REPLAY/verify.py" "$REPAIR_RECORD/data/two-clones-n8-best.json" replay-n8
```

Check the shared thread budget before any reproduction. Any longer job or
fresh certification remains for the parent to schedule.
