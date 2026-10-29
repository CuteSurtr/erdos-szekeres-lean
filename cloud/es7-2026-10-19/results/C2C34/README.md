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

## Files

- **Case split.**
  - Scripts: `hullcubes.py`, `l2cubes.py`, `zlayers.py`, `zlvalidate.py`.
  - Data: `cubes.txt`, `canonical.txt`.
- **Lanes and checking.** `hlane.sh`, `hchecker.sh`, `layer_lane.sh` and `norm.py`. The scripts read `C2C`, `TOOLS` and
  `ARCHIVE` from the environment.
- **Review.** `review/`, with the scripts of the independent reviewer.
- **Logs.** `logs/`: the summary tables and the per-case records.
