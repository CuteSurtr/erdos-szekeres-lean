# C2C34: centrally symmetric sets of 34 points (partial results)

Local runs on an Apple M5 Pro, 2026-10-29 (UTC).

**The question.** Is there a set of 34 points in general position with no 7 points in convex position that is
symmetric under the half-turn about a centre c? The centre is not a point of such a set, so the set is 17 antipodal
pairs.
- Excluding 34 points would exclude every centrally symmetric set of 34 or more points, since antipodal pairs can be
  deleted.
- This is the only symmetric route to a counterexample to ES(7) = 33 that `results/WRITEUP/SYMMETRIC.md` leaves open.

**Status: open.** Certified so far:
1. **Coverage.** The hull case split below covers the problem. Its LRAT proof is accepted by lrat-check and cake_lpr.
2. **Hexagonal hulls.** All 120 hexagonal-hull cases are UNSAT. Each has a retained LRAT proof, archived with a verified
   round trip and accepted by both lrat-check and cake_lpr (`logs/hex_cases.tsv`).

Together these give the following theorem. It needs no relabelling argument.

> **Theorem (computer-assisted).** Every centrally symmetric set of 34 points in general position without a convex
> 7-gon has a parallelogram as its convex hull.

The parallelogram cases are not solved, so the question stays open.

## 1. Encoding

- **Encoder.** The centrally symmetric branch of `results/SYMZ/zcnf.py` (`rot`, m = 2). It encodes the chirotope of the
  34 points and the centre c:
  - zero triples exactly {c, p, −p};
  - the identity χ(c, p, q) = χ(−p, p, q), from v_c = (v_p + v_{−p})/2;
  - half-turn invariance;
  - Grassmann–Plücker and interiority clauses;
  - no convex 7-gon via the four-point criterion.
- **Angular normal form** (`--hull`). The first point is a vertex of the convex hull. The other pairs are represented by
  their point in the open half-plane left of c → (0,0), sorted by angle. Base CNF `c34h_final.cnf`:
  p cnf 838032 16653336, SHA-256 `b0061e908bff80e6a597f31a6fec1d91e8504aebc09b0bcf41c2ff21604d8ff1`.
- **Tests.** Real central sets (`results/SYMZ/val_real.log`) and two-way random tests (`results/SYMZ/rt_run_all.log`).
- **Independent review.** An adversarial review (§5) found the encoder sound.
- **What the model does not impose.** An abstract centre gives no metric midpoint condition, and a satisfying assignment
  need not be realizable. Only UNSAT answers are used.

## 2. Hull case split (`hullcubes.py`)

**The cases.** The hull of such a set is a centrally symmetric polygon with 4 or 6 vertices: 8 vertices would be a
convex 7-gon, and the set is not collinear. In the angular normal form it is determined by:
- one further pair a: a quadrilateral `P<a>`, 16 cases;
- or two further pairs a < b: a hexagon `H<a>-<b>`, 120 cases.

The cube of a case says that every point not on a hull edge lies strictly left of it (`cubes.txt`).

**Coverage (certified).** The formula plus the negation of all 136 cubes is UNSAT. Its LRAT proof is accepted by
lrat-check and cake_lpr (`results/WRITEUP/CERTIFICATES.md`, central34-cover).

**Canonical cases (an argument about real configurations).**
- The numbers of antipodal classes between consecutive hull vertices form a cyclic sequence summing to 17.
- Starting the labelling at another hull vertex rotates this sequence. Reflecting the configuration reverses it.
- So every real configuration falls into a case whose sequence is least under rotation and reversal: 8 quadrilaterals
  and 24 hexagons (`canonical.txt`).

Since all 120 hexagonal cases are now refuted directly (§3), the result does not depend on this argument; it is kept for the parallelogram cases.

## 3. Hexagonal hulls (with retained proofs)

**Method** (`hlane.sh`): base CNF plus the hull cube, then:
1. CaDiCaL 3.0.1 `--lrat` (limit 3,600 s);
2. lrat-check on the proof;
3. zstd compression into the local proof archive (outside Git), checking that decompression reproduces the proof;
4. cake_lpr on the archived proof, run separately (`hchecker.sh`, heap 16,000 MB).

**Per-case records** (`logs/hex_cases.tsv`): CNF SHA-256, proof size and SHA-256, archive SHA-256, round trip,
lrat-check and cake_lpr verdicts.

**Results.** All 120 cases are UNSAT, solved in 291 to 1,562 s each (median 687 s). The proofs total 524 GB before
compression. lrat-check and cake_lpr accepted all 120; cake_lpr took 171 to 1,001 s per proof (median 376 s). The
counts are in `logs/summary.txt`.

## 4. Quadrilateral hulls (open)

**Direct runs.** All 8 canonical quadrilateral cases ran 50 to 75 minutes without an answer, without proofs
(`logs/hull_probes_no_proofs.tsv`).

**Second-layer split.**
- The 30 inner points have a centrally symmetric quadrilateral or hexagon as hull, so `l2cubes.py` splits a case `P<a>`
  into C(15,2) + C(15,3) = 560 subcases.
- A sample of 10 subcases of P8, run without proofs with a 30-minute limit (`logs/p8_layer2_samples.tsv`):
  - every hexagonal second layer was UNSAT in 13 to 236 s;
  - quadrilateral second layers took 468 to 743 s, or gave no answer in 30 minutes (2 of 5).
- So nested parallelograms are the hard core. This fits the shape of the known extremal sets: the 32-point central set
  of `results/SYM2` has convex layers of 2, 3, 3, 3, 3 and 2 pairs.

**Layer normal form** (`zlayers.py`, `layer_lane.sh`).
- **The form.** Pairs are numbered layer by layer, with within-layer angular order and edge units. It has 86 possible
  layer profiles.
- **Checks.** It is sound and exhaustive by the review in §5, with real-set and random tests in `zlvalidate.py`.
- **Result.** The angular order across layers is left free, and profiles made mostly of quadrilaterals gave no answer in
  25 to 45 minutes (`logs/layer_profile_probes.tsv`).

**Estimated cost of completing the case.**
- Splitting every canonical quadrilateral case at the second layer gives about 8 × 560 = 4,480 subcases.
- The sample suggests several hundred core-hours, plus a deeper split of the nested-quadrilateral subcases.
- Retaining every proof (about 4 GB each before compression) would need a different archival plan, or check-and-discard
  with recorded verdicts.

## 5. Independent review

An adversarial review on 2026-10-29 checked two things: the `rot` encoder with m = 2 and `--no-sb`, and the layer
reduction of `zlayers.py`. It found both sound, and the reduction exhaustive.
- **Regeneration.** It regenerated the 34-point base byte-identically and checked that the lane scripts append exactly
  the layer units.
- **Independent checker.** Its own exact-arithmetic checker (`review/`) evaluated every clause on:
  - about 21,000 labelled random and stress sets;
  - the real 28- and 32-point sets;
  - all 86 profiles, with every choice of first point (5,016 labellings).
- **Findings.** No unit was false, and no clause failed other than genuine 7-gon clauses.
- **What it did not cover.** The hull cubes were not part of that review. Their coverage is certified by the SAT proof
  in §2, and each cube's soundness is the statement that the hull is that polygon.

## 6. Pilot on the parallelogram case P8 (2026-10-29)

**Split.** `l2cubes.py` splits P8 by the second convex layer into 560 subcases (105 quadrilateral, 455 hexagonal).

**Cover (certified).** `p8/cover.cnf` is the base, the P8 hull cube as units, and one clause per subcase saying that
some literal of its second-layer cube fails. It is UNSAT in 550 s. The LRAT proof (4.68 GB, SHA-256
`bb6ade84591f1ec441f834b01c6ea04ee815a154e25ad235c2b2d6718a88c1eb`) was accepted by lrat-check (37 s) and cake_lpr
(171 s, heap 8,000 MB) and then deleted.

**Orbits (an argument about real configurations, not yet independently reviewed).** Reflect a real configuration with
hull case P8 and restart the angular normal form at the other hull class. The base CNF imposes only that the first point
is a hull vertex and that the representatives are sorted by angle in the half-plane left of c → (0,0), so the result is
again a labelling in normal form with hull case P8. Class i becomes class (8 − i) mod 17, so subcase (P8, V) becomes
(P8, {(8 − i) mod 17 : i ∈ V}). Hence the 560 subcases fall into 287 orbits (56 quadrilateral, 231 hexagonal;
`p8/orbits.tsv`), and refuting one subcase per orbit refutes P8. The run order (`p8/units.txt`) takes one representative
per orbit first; the other members follow, so the case can also be closed without this argument.

**Method (check and delete).**
- Solver lanes (`p8/solver.sh`): CaDiCaL 3.0.1 `--lrat` with a 1,800 s cap, then lrat-check.
- One checker lane (`p8/checker.sh`): cake_lpr with an 8,000 MB heap, one process at a time.
- Each proof's size and SHA-256 and both verdicts are recorded (`logs/p8_units.tsv`); the proof is deleted only after
  both checkers accept it. A proof that fails a check would be kept.
- Resource limits: two solver lanes and one checker lane, and a memory guard (`p8/guard2.sh`) that pauses new claims
  above 30 GB in use.

**Results.** Counts (`logs/p8_summary.txt`; per-unit records in `logs/p8_units.tsv`):

```
cover: 1 run, 1 UNSAT (1 accepted by both checkers), 0 no answer within the cap, 0 SAT; solve time min 550 s, median 550 s, max 550 s
hexagonal: 53 run, 53 UNSAT (53 accepted by both checkers), 0 no answer within the cap, 0 SAT; solve time min 9 s, median 160 s, max 337 s
quadrilateral: 14 run, 11 UNSAT (11 accepted by both checkers), 3 no answer within the cap, 0 SAT; solve time min 391 s, median 565 s, max 1382 s
representatives closed by both checkers: 64 of 287 (11 of 56 quadrilateral, 53 of 231 hexagonal)
proofs deleted after both checks: 65; proofs kept (a check failed): 0
```

- **Hexagonal second layers.** Every one run was refuted:
  - solve time 9 to 337 s (median 160 s);
  - lrat-check median 31 s, cake_lpr median 124 s;
  - proofs of 0.21 to 3.70 GB.
- **Quadrilateral second layers.** 11 of 14 run were refuted within the cap (391 to 1,382 s, median 565 s).
  - P8_3-11, P8_2-11, P8_1-9 gave no answer in 1,800 s; these would need a deeper split.
- **Memory.** CaDiCaL used up to 11.6 GB (median 10.1 GB) per subcase.

**Status.** P8 is not closed. 64 of its 287 representatives are refuted, each with both checks.

**Estimate for the rest of P8.** Use the measured means of solve time plus both checks:
- 283 s for a hexagonal representative;
- 903 s for a quadrilateral one that is refuted within the cap.

The remaining 178 hexagonal and 45 quadrilateral representatives then need about 23 core-hours, at up to 12 GB per
solver process. On top of that come deeper splits for the quadrilateral ones that do not finish (here 3 of 14).

The other 7 canonical parallelogram cases have not been run. By the same reflection argument, their subcases also form
287 orbits each (the reflection fixes 14 of the 560).

A second, compact encoding of the whole parallelogram case is in `results/C2SGN`.

## Files

- **Case split.**
  - Scripts: `hullcubes.py`, `l2cubes.py`, `zlayers.py`, `zlvalidate.py`.
  - Data: `cubes.txt`, `canonical.txt`.
- **Lanes and checking.** `hlane.sh`, `hchecker.sh`, `layer_lane.sh` and `norm.py`. The scripts read `C2C`, `TOOLS` and
  `ARCHIVE` from the environment.
- **P8 pilot (§6).** `p8/`:
  - scripts: `mkunits.py`, `solver.sh`, `checker.sh`, `guard2.sh`, `summary.py`;
  - data: `orbits.tsv`, `units.txt`, and `P8_cubes.txt` (the output of `l2cubes.py` for P8);
  - the scripts read `WORK` from the environment.
- **Review.** `review/`, with the scripts of the independent reviewer.
- **Logs.** `logs/`: the summary tables and the per-case records.
