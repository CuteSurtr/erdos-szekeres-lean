# C2C34: centrally symmetric sets of 34 points: encoding, hull split and hexagonal hulls

Local runs on an Apple M5 Pro, 2026-10-29 (UTC). README revised 1 November 2026 (UTC). Paths are relative to
`cloud/es7-2026-10-19/results`.

**The question.** Is there a set of 34 points in general position with no 7 points in convex position that is
symmetric under the half-turn about a centre c? The centre is not a point of such a set, so the set is 17 antipodal
pairs.
- Excluding 34 points excludes every centrally symmetric set of 34 or more points, since antipodal pairs can be
  deleted.
- It was the last symmetric case of the main theorem of `WRITEUP/SYMMETRIC.md`.

**Status (revised 1 November).** Settled. This directory holds the encoding, the hull split, the 120 hexagonal hulls and
the P8 pilot. The parallelogram cases were closed later (`C2P`–`C2P5`), and `C2FINAL` checks the composition and claims
the theorem: every centrally symmetric set of 34 points in general position contains a convex 7-gon. Certified here:
1. **Coverage.** The hull case split below covers the problem. Its LRAT proof is accepted by lrat-check and cake_lpr.
2. **Hexagonal hulls.** All 120 hexagonal-hull cases are UNSAT. Each has a retained LRAT proof, archived with a verified
   round trip and accepted by both lrat-check and cake_lpr (`logs/hex_cases.tsv`).

Together these give the following step. It needs no relabelling argument.

> **Theorem (computer-assisted).** Every centrally symmetric set of 34 points in general position without a convex
> 7-gon has a parallelogram as its convex hull.

## 1. Encoding

- **Encoder.** The centrally symmetric branch of `SYMZ/zcnf.py` (`rot`, m = 2). It encodes the chirotope of the
  34 points and the centre c:
  - zero triples exactly {c, p, −p};
  - the identity χ(c, p, q) = χ(−p, p, q), from v_c = (v_p + v_{−p})/2;
  - half-turn invariance;
  - Grassmann–Plücker and interiority clauses;
  - no convex 7-gon via the four-point criterion.
- **Angular normal form** (`--hull`). The first point is a vertex of the convex hull. The other pairs are represented by
  their point in the open half-plane left of c → (0,0), sorted by angle. Base CNF `c34h_final.cnf`:
  p cnf 838032 16653336, SHA-256 `b0061e908bff80e6a597f31a6fec1d91e8504aebc09b0bcf41c2ff21604d8ff1`.
- **Tests.** Real central sets (`SYMZ/val_real.log`) and two-way random tests (`SYMZ/rt_run_all.log`).
- **Soundness (revised 1 November).** A complete written proof for `rot 17 7 --m 2 --hull` covers every clause family of
  the base CNF: every real configuration, labelled in the normal form from any hull vertex, satisfies every clause
  (`C2ENC`). It was refereed on 1 November: sound, with minor
  documentation gaps, no blocking or major finding. Before that, the encoder rested on a docstring sketch and on the
  review of §5, which covered the variant `--no-sb` and kept its scripts but not its run logs.
- **What the model does not impose.** An abstract centre gives no metric midpoint condition, and a satisfying assignment
  need not be realizable. Only UNSAT answers are used.

## 2. Hull case split (`hullcubes.py`)

**The cases.** The hull of such a set is a centrally symmetric polygon with 4 or 6 vertices: 8 vertices would be a
convex 7-gon, and the set is not collinear. In the angular normal form it is determined by:
- one further pair a: a quadrilateral `P<a>`, 16 cases;
- or two further pairs a < b: a hexagon `H<a>-<b>`, 120 cases.

The cube of a case says that every point not on a hull edge lies strictly left of it (`cubes.txt`).

**Coverage (certified).** The formula plus the negation of all 136 cubes is UNSAT. Its LRAT proof is accepted by
lrat-check and cake_lpr (`WRITEUP/CERTIFICATES.md`, central34-cover).

**Canonical cases (an argument about real configurations).**
- The index gaps between consecutive hull classes form a cyclic sequence summing to 17: (a, 17 − a) for a
  parallelogram, (a, b − a, 17 − b) for a hexagon. (Corrected 1 November: an earlier version spoke of the numbers of
  classes between hull vertices, which sum to 15 or 14; `AUDIT3`, A5-3.)
- Starting the labelling at another hull vertex rotates this sequence. Reflecting the configuration reverses it.
- So every real configuration falls into a case whose sequence is least under rotation and reversal: 8 quadrilaterals
  and 24 hexagons (`canonical.txt`).

Since all 120 hexagonal cases are refuted directly (§3), the result does not depend on this argument; it is kept for the
parallelogram cases (reduction A of `C2P`).

## 3. Hexagonal hulls (with retained proofs)

**Method** (`hlane.sh`): base CNF plus the hull cube, then:
1. CaDiCaL 3.0.1 `--lrat` (limit 3,600 s);
2. lrat-check on the proof;
3. zstd compression into the local proof archive (outside Git), checking that decompression reproduces the proof;
4. cake_lpr on the archived proof, run separately (`hchecker.sh`, heap 16,000 MB), on a CNF rebuilt by the same command
   but not hashed.

**Per-case records** (`logs/hex_cases.tsv`): CNF SHA-256, proof size and SHA-256, archive SHA-256, round trip,
lrat-check and cake_lpr verdicts.

**Results.** All 120 cases are UNSAT, solved in 291 to 1,562 s each (median 687 s). The proofs total 524 GB before
compression. lrat-check and cake_lpr accepted all 120; cake_lpr took 171 to 1,001 s per proof (median 376 s). The
counts are in `logs/summary.txt`.

**Re-check on hash-checked files (started 1 November).** Each case CNF was rebuilt and required to have the recorded
SHA-256, each archive and decompressed proof required to have the recorded SHA-256, and both checkers were run on
exactly these files (`WRITEUP/CERTIFICATES.md`, central34-hull). Result: 120 of 120 with all hashes equal and both
verdicts (finished 1 November, 17:59 UTC; `C2RECHECK`).

## 4. Quadrilateral hulls (closed later in `C2P`–`C2P5`)

**Direct runs.** All 8 canonical quadrilateral cases ran 50 to 75 minutes without an answer, without proofs
(`logs/hull_probes_no_proofs.tsv`).

**Second-layer split.**
- The 30 inner points have a centrally symmetric quadrilateral or hexagon as hull, so `l2cubes.py` splits a case `P<a>`
  into C(15,2) + C(15,3) = 560 subcases.
- A sample of 10 subcases of P8, run without proofs with a 30-minute limit (`logs/p8_layer2_samples.tsv`):
  - every hexagonal second layer was UNSAT in 13 to 236 s;
  - quadrilateral second layers took 468 to 743 s, or gave no answer in 30 minutes (2 of 5).
- So nested parallelograms are the hard core. This fits the shape of the known extremal sets: the 32-point central set
  of `SYM2` has convex layers of 2, 3, 3, 3, 3 and 2 pairs.

**Layer normal form** (`zlayers.py`, `layer_lane.sh`).
- **The form.** Pairs are numbered layer by layer, with within-layer angular order and edge units. It has 86 possible
  layer profiles.
- **Checks.** It is sound and exhaustive by the review in §5, with real-set and random tests in `zlvalidate.py`.
- **Result.** The angular order across layers is left free, and profiles made mostly of quadrilaterals gave no answer in
  25 to 45 minutes (`logs/layer_profile_probes.tsv`). The case split that closed the parallelograms (`C2P`) used the
  second-layer cubes of `l2cubes.py` instead.

## 5. Independent review (29 October)

An adversarial review on 2026-10-29 checked two things: the `rot` encoder with m = 2 and `--no-sb`, and the layer
reduction of `zlayers.py`. It found both sound, and the reduction exhaustive.
- **Regeneration.** It regenerated the 34-point base byte-identically and checked that the lane scripts append exactly
  the layer units.
- **Independent checker.** Its own exact-arithmetic checker (`review/`) evaluated every clause on:
  - about 21,000 labelled random and stress sets;
  - the real 28- and 32-point sets;
  - all 86 profiles, with every choice of first point (5,016 labellings).
- **Findings.** No unit was false, and no clause failed other than genuine 7-gon clauses.
- **What it did not cover.** The hull cubes and the `--hull` units were not part of that review. The written proof of
  §1 covers the `--hull` units, and by its corollaries the certified cover of §2 places every real configuration in
  the class of some cube, while an UNSAT cube has an empty class; so the hull cubes need no further soundness argument.
  The geometric meaning of the parallelogram cubes, which reductions A and B use, was checked by `AUDIT3` (A5).

## 6. Pilot on the parallelogram case P8 (2026-10-29)

**Split.** `l2cubes.py` splits P8 by the second convex layer into 560 subcases (105 quadrilateral, 455 hexagonal).

**Cover (certified).** `p8/cover.cnf` is the base, the P8 hull cube as units, and one clause per subcase saying that
some literal of its second-layer cube fails. It is UNSAT in 550 s. The LRAT proof (4.68 GB, SHA-256
`bb6ade84591f1ec441f834b01c6ea04ee815a154e25ad235c2b2d6718a88c1eb`) was accepted by lrat-check (37 s) and cake_lpr
(171 s, heap 8,000 MB) and then deleted. It is a cover relative to the hull cube; the encoder proof of §1 justifies
this use (`C2FINAL` §1). The cover was re-solved on 1 November with an archived proof (`C2FINAL` §4).

**Orbits.** Reflect a real configuration with hull case P8 and restart the angular normal form at the other hull class.
The base CNF imposes only that the first point is a hull vertex and that the representatives are sorted by angle in the
half-plane left of c → (0,0), so the result is again a labelling in normal form with hull case P8. Class i becomes
class (8 − i) mod 17, so subcase (P8, V) becomes (P8, {(8 − i) mod 17 : i ∈ V}). Hence the 560 subcases fall into 287
orbits (56 quadrilateral, 231 hexagonal; `p8/orbits.tsv`), and refuting one subcase per orbit refutes P8. (Revised
1 November: this is reduction B, reviewed in `C2P/review` and checked at the CNF level by `AUDIT3`, A5.)

**Method (check and delete).**
- Solver lanes (`p8/solver.sh`): CaDiCaL 3.0.1 `--lrat` with a 1,800 s cap, then lrat-check.
- One checker lane (`p8/checker.sh`): cake_lpr with an 8,000 MB heap, one process at a time, on a CNF rebuilt by the
  same command but not hashed.
- Each proof's size and SHA-256 and both verdicts are recorded (`logs/p8_units.tsv`); the proof is deleted only after
  both checkers accept it. A proof that fails a check would be kept.
- Resource limits: two solver lanes and one checker lane, and a memory guard (`p8/guard2.sh`) that pauses further claims
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
  - P8_3-11, P8_2-11, P8_1-9 gave no answer in 1,800 s in the pilot.
- **Memory.** CaDiCaL used up to 11.6 GB (median 10.1 GB) per subcase.

**Later status (revised 1 November).** P8 and the other seven canonical parallelogram cases were closed in
`C2P`–`C2P5`; `C2FINAL` checks the composition. Seven pilot records without a CNF hash were re-solved with archived
proofs (`C2FINAL` §4). The 58 other pilot orbits, whose cake_lpr check had run on an unhashed CNF, were re-solved on
hash-checked CNFs with both checkers: 58 of 58 certified, all reproducing the recorded proof (`C2RECHECK`). A second, compact encoding of the whole parallelogram case is
in `C2SGN`.

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
