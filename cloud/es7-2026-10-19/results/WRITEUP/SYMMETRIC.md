# Symmetric point sets and the Erdős–Szekeres problem for heptagons

Revised 1 November 2026 (UTC), after the audit of the same day (`AUDIT3`), the composition check of the central 34-point
search (`C2FINAL`) and the Lean check of the reduction (`SYMLEAN`). Paths are relative to `cloud/es7-2026-10-19/results`.

**Setting.** ES(7) is the least n such that every n points in general position (no three on a line) contain 7 points in
convex position. The Erdős–Szekeres conjecture says ES(7) = 33, and 32-point sets without a convex 7-gon are classical.
A "k-gon" below means k points in convex position. A *symmetry* of a finite set S is an isometry or an affine bijection
of the plane, other than the identity, that maps S into itself.

**Scope.** Nothing here settles ES(7) or improves its unrestricted upper bound. The results exclude symmetric
counterexamples. "No matching prior result was found" means only that none was found in the sources listed in §5; it is
not a claim of priority.

## 0. Main theorem

**Theorem A (computer-assisted).** Every set of at least 33 points in general position that has a symmetry contains a
convex 7-gon.

- **Sharpness.** There are 32-point sets without a convex 7-gon with a half-turn (`SYM2/sym7_32points.txt`) and with a
  reflection (`SYMMAX/mirror_32points.txt`).
- **The case theorems.** The minimal set is: the half-turn at 34 points (Theorem 4), threefold rotations at 33 points
  (Theorem 1), fivefold rotations at 35 or more points (Theorem 5) and reflections (Theorem 2). Every rotation has a
  power that is the half-turn or has prime order, and for a prime p ≥ 7 every orbit other than the centre is a regular
  p-gon. A set of exactly 33 points needs only Theorems 1 and 2.
- **The reduction is Lean-checked** (`SYMLEAN`). `heptagon_of_nontrivial_isometry` and
  `heptagon_of_nontrivial_affineEquiv` derive Theorem A, for isometries and for affine bijections, from five case classes
  stated as Lean propositions: `HalfTurn34`, `Threefold33`, `Fivefold35`, `MirrorOneAxis33` and `MirrorNoAxis34`.
  Axioms: `propext`, `Classical.choice`, `Quot.sound`.
- **The mirror classes are Lean-checked theorems** (`SYMLEAN/mirror/ReductionThreeClasses.lean`, SHA-256
  `0cc83994…`). The file proves `MirrorOneAxis33` and `MirrorNoAxis34` from Baek's theorem (Theorem 2 below), with no
  SAT input. Its theorems `heptagon_of_nontrivial_isometry_3` and `heptagon_of_nontrivial_affineEquiv_3` assume only
  `HalfTurn34`, `Threefold33` and `Fivefold35`; axioms as above. An independent check recompiled it and listed the
  hypotheses of both theorems.
- **Not Lean-checked.** No step from a CNF to a Lean class. Each of `HalfTurn34`, `Threefold33` and `Fivefold35` rests on
  a written soundness proof of its encoder, on certificates and, for Theorems 1 and 4, on recorded verdicts of deleted
  proofs (§3).
- **Credit.** No matching prior result was found in the sources inspected (§5) for Theorem A, Theorem 1 or Theorem 4.
  The mirror case is implied by Baek's theorem through the mirror reduction (Theorem 2). The fivefold case also follows
  from a computation reported by B. C. Dumitru (Theorem 5). The fourfold case, which Theorem A does not need, was
  reported by Subercaseaux, Mackey, Qian and Heule (§2). For k = 7 the results bear on their suspicion that symmetric
  constructions exist for all k ≥ 7 (arXiv:2506.00224, §7): 32-point examples exist with a half-turn or a reflection,
  while every set of 32 or more points with a rotation of order at least 3 contains a convex 7-gon (for fourfold
  32-point sets this uses `C4CUT`).

**Corollary 3 (the variant without Theorem 4).** Assume Theorems 1, 2 and 5 and the fourfold 32-point exclusion
(`C4CUT`). Then every symmetry of a 7-gon-free set of at least 33 points in general position is a half-turn about a point
outside the set, and the set has an even number of points, at least 34. Lean-checked for isometries
(`halfTurn_of_symmetric_counterexample` in `SYMLEAN`, with the class `Fourfold32`). Theorem 4 excludes this last case.

## 1. The case theorems

**Theorem 1 (threefold rotation).** Every set of 33 points in general position that is invariant under a rotation of
order 3 contains a convex 7-gon. The largest threefold-symmetric set without a convex 7-gon has exactly 31 points.
- **Reduction.** A threefold set has 3m or 3m + 1 points (only the centre is fixed). One with at least 33 points
  contains 11 whole non-central orbits. A set of 32 points is not possible.
- **Lower example.** `SYMMAX/c3_31points.txt`: 31 points, centre included, exact coordinates, checked independently.
- **Proof.** A projective normal form (`C3-S/soundness.md`, written proof, audited) and the chain encoding of `C3a`,
  cross-checked on smaller cases against `../tools/symmetric/symcnf.py` and the encoding of `C3b`. A generic centre comes
  from the perturbation lemma (written proof in `C2ENC`, `perturbation.md`,
  refereed with it). The case is split into 116,883 certified pieces. Two composers (`C3FINAL`) re-derive every piece's
  CNF hash from the base formula and cover all 910 depth-2 roots. That the 73,567 leaves of one explicit cut cover the
  910 roots is Lean-checked (`C3LEAN`).
- **Trust.** Each piece was accepted by both checkers when solved, and its proof was then deleted (recorded verdicts).
  2,120 pieces were re-solved (`C3SPOT`, a stratified random draw). That draw excluded the records in σ-cube format. A
  run on 1 November re-solved the 204 such pieces that the cover cannot do without, on hash-checked CNFs with both
  checkers and archived proofs: 204 of 204 certified, 200 of them with the recorded proof size (σ-cube records keep no
  proof hash) (`C3PIECES`; local archive `es7-c3-indispensable-2026-11-01`).
- **Credit.** No matching prior result was found in the sources inspected. The closest results concern other
  parameters: for 16 points without a convex hexagon the threefold formula is unsatisfiable (arXiv:2506.00224, §6.1;
  Mackey's thesis, §3.2.4), and a 7-gon-free set of 32 points can only have 1-, 2- or 4-fold rotational symmetry
  (arXiv:2506.00224, §6.2). Dumitru (arXiv:2512.24061, Table 1) reports UNSAT runs for two convex-layer templates
  compatible with threefold symmetry (3^11 and 6,6,6,3,6,6). A threefold 33-point counterexample may have any of 144
  layer profiles, so these runs do not imply Theorem 1.

**Theorem 2 (reflection).** Every set of at least 33 points in general position that is symmetric under a reflection
contains a convex 7-gon. The largest mirror-symmetric set without a convex 7-gon has exactly 32 points.
- **It follows from Baek's theorem.** Baek (arXiv:2206.04260, Thm 1.6 in the arXiv numbering; Eur. J. Combin. 124
  (2025) 104085) proved the case a = 4 of the Erdős–Tuza–Valtr conjecture: every C(n−1, 2) + 2 points in general
  position with distinct x-coordinates contain a 4-cap or a convex n-gon. For n = 7, a set with neither has at most 16
  points.
- **The mirror reduction** (written proof: the note `WRITEUP/note`, `prop:mirrorred`; also `MIRRORETV`). Put the mirror on the x-axis. Let R be the points strictly above it and A the points on it; |A| ≤ 2. Points
  of R ∪ {a}, a ∈ A, have distinct x-coordinates, by general position. A cap of R ∪ A together with its mirror image is
  in convex position (the mirror lemma, §2). So R has no 4-cap (it would give 8 points in convex position), and
  R ∪ {a} has none either: a 4-cap through a has a as an endpoint, and with its mirror image it gives 2·4 − 1 = 7
  points in convex position. Baek's theorem gives |R| ≤ 16, and |R| ≤ 15 when A is not empty. Hence the size is
  2|R| + |A| ≤ 32.
- **Lean-checked** (`SYMLEAN/mirror`). `MirrorOdd.mirror_seven_line` proves |S| ≤ 32 for a reflection in any line,
  with no SAT input; `mirrorOneAxis33_proved` and `mirrorNoAxis34_proved` derive the two mirror classes from it. It
  uses the repository's vendored formalization of Baek's theorem (`ErdosSzekeres/Vendor/ETV` at the repository root,
  adapted from Baek's Lean 4 code) and bridge lemmas adapted from M. Schroeder's archive (`docs/THIRD_PARTY.md` at the
  repository root). Axioms: `propext`, `Classical.choice`, `Quot.sound`. Reviews recompiled it and re-sent the 497
  repository constants of the mirror development to the kernel.
- **Independent confirmations by SAT.** Deleting pairs reduces Theorem 2 to two cases. With no axis point the size is
  even, at least 34, and 17 pairs remain. With one or two axis points, 16 pairs and one axis point remain.
  - *Theorem 2a (33 points, exactly one on the axis).* A single CNF of the encoding `SYMZ/zcnf.py` (the reflection's
    point at infinity as an element) is UNSAT. Its LRAT proof is retained and accepted by both checkers (`mirror33`).
    The Lean chain of 21 October (`WRITEUP/MIRROR.md`) is a further proof, conditional on about 75,000 CNF facts
    whose cake_lpr verdicts were recorded and whose proofs were not retained.
  - *Theorem 2b (34 points, none on the axis).* A single CNF of the same encoding is UNSAT, solved in 443 s. Its LRAT
    proof is retained and accepted by both checkers (`mirror34`).
  - The case n = 7 of Baek's theorem has its own 17-point certificate (no 4-cap, no 7-gon), accepted by lrat-check
    only (`MIRRORETV`); Balko and Valtr (ENDM 49, 2015) had reported this case from a SAT run over pseudolinear
    colourings.
- **Lower example.** `SYMMAX/mirror_32points.txt`: 16 mirror pairs, no point on the axis, found by search. A 32-point
  mirror set also follows from the classical construction in Lovász's form (Morris–Soltan 2000, Thm 2.6): choose the
  cluster at angle −θ as the mirror image of the cluster at θ. For k = 7 no cluster lies on the axis.
- **Credit.** Theorem 2, including the statements of Theorems 2a and 2b, is implied by Baek's theorem through the
  elementary mirror reduction; the lower bound follows from the classical construction. The SAT proofs are independent
  confirmations. No matching prior result was found in the sources inspected for the mirror reduction itself or for its
  combination with Baek's theorem. The only reflection-symmetric Erdős–Szekeres-type statement found concerns empty
  hexagons (Koshelev–Koshka, arXiv:2604.20120, §9.1.2), a different problem.

**Theorem 4 (half-turn).** Every centrally symmetric set of 34 points in general position contains a convex 7-gon.
Pairs can be deleted, so the same holds for every larger centrally symmetric set, and N(C2) = 32: the 32-point example
`SYM2/sym7_32points.txt` is a case of Valtr's construction as described by Baek and Balko (§2).
- **Encoding.** `SYMZ/zcnf.py rot 17 7 --m 2 --hull`: base CNF `b0061e90…`, 838,032 variables and 16,653,336 clauses.
  The centre is an element, the zero triples are exactly {c, p, −p}, and the first point is a hull vertex. Soundness:
  written proof (`C2ENC`), refereed on 1 November: sound, with minor documentation gaps and no blocking or major finding.
- **Split.** The convex hull is a centrally symmetric hexagon or parallelogram (136 cases, cover certified). All 120
  hexagonal cases are UNSAT with retained proofs (`C2C34`). The 16 parallelogram cases reduce to P1..P8 (reduction A).
  Each is split at its second convex layer into 560 subcases, with a cover relative to the hull cube, and a reflection
  (reduction B) pairs the subcases into 287 orbits. Reductions A and B: written proof, reviewed (`C2P/review`), and
  checked at the CNF level by `AUDIT3` (A5).
- **Closure** (`C2FINAL`). 2,492 records: 2,385 UNSAT, 107 no answer within the cap, 0 SAT. Every orbit of every case
  has a member closed by a record with both verdicts. All 2,589 recorded CNF hashes rebuild from the base. The orbit
  bookkeeping is Lean-checked (`C2FINAL/Central34Orbits.lean`).
- **Re-solves.** Seven pilot units without a hash were re-solved. A sample of 24 cloud units, drawn before any result,
  gave 24 of 24 certified: 23 reproduce the recorded proof byte for byte, and `P8_1-10` gave a different proof that both
  checkers accept. A second draw of 8 units: 8 of 8 reproduced.
- **Re-checks started on 1 November** (`C2RECHECK`). The 120 hexagonal proofs with both checkers on hash-checked files:
  120 of 120, each with the rebuilt CNF, the archive and the decompressed proof equal to the recorded SHA-256. The 58 P8
  pilot orbits: 58 of 58 certified, all reproducing the recorded proof. The 60 orbit representatives and 5 covers that
  rest only on records of the local Mac lanes: 44 of 65 by 1 November 2026, 19:43 UTC, all certified and reproducing the
  recorded proof (still running). A lane-stratified spot check, one unit from each of the 242 lanes not already
  reached by a re-solve: 81 of 242 by the same time, all certified and reproducing the recorded proof (still running). The replay of retained certificates (§3). Before them
  about 98% of the 2,304 orbit and cover facts rested on recorded verdicts of deleted proofs; by 1 November 2026, 19:43 UTC,
  224 of the 2,304 (9.7%) had a re-solve on a hash-checked CNF with both checkers and an archived proof (`C2FINAL` §9).
- **Credit.** No matching prior result was found in the sources inspected. Subercaseaux et al. examined only fourfold
  symmetry at 32 points (§6.2) and listed a twofold 32-point realization as open (§7). Krapivin, Przybocki and Heule
  found no realization among 200,000 abstract 32-point solutions, with no symmetry imposed (arXiv:2607.02958, §6).

**Theorem 5 (fivefold rotation).** Every set of at least 35 points in general position with a rotation of order 5
contains a convex 7-gon. The largest such set without a convex 7-gon has exactly 31 points (`SYMMAX/c5_31points.txt`,
centre included; 32 to 34 are impossible sizes).
- **Proof** (`SYM5`). Two normal forms of one encoder, the angle form (proof P1) and the layer form (proof L1). Each
  LRAT proof is retained and accepted by both checkers. A generic centre comes from the perturbation lemma.
- **Layer lemma.** A rotation of order m ≥ 4 about a point outside S, with no K-gon in S for some K ≤ 2m, makes every
  convex layer a single orbit. So a 35-point set would be seven nested regular pentagons. arXiv:2506.00224, §3.2, states
  a special case (16 points, fourfold, no hexagon: four layers of four points). The lemma, including strict nesting, is
  Lean-checked in `LAYERLEAN` (4 November).
- **Credit.** The bound also follows from an earlier reported computation, which has priority (30 December 2025).
  Dumitru (arXiv:2512.24061, §7, Table 1, row 5^6 (H = 30), baseline) reports an unsatisfiable Kissat run for 33 points
  whose first six convex layers are pentagons, with the remaining three points inside them. His public generator
  (github.com/bogdan27182/esc-paper, `es_sat_gen.py`), with zero offsets, adds to the base encoding only within-layer
  convexity and nesting units. Deleting two points of the innermost pentagon of a 35-point fivefold set gives such a
  configuration. No proof files or logs for that run are public, so it is a prior reported claim, not an independently
  verified theorem. His homepage announces a second version; on 1 November 2026 (UTC) arXiv listed only v1.

## 2. Sizes and constructions

| symmetry | largest size without a convex 7-gon | lower example | upper bound and credit |
|---|---|---|---|
| half-turn (C2) | **32** | `SYM2/sym7_32points.txt` | Theorem 4 |
| 3-fold rotation | **31** | `SYMMAX/c3_31points.txt` | Theorem 1 |
| 4-fold rotation | **28** | `SYMMAX/c4_28points.txt` | sizes are multiples of 4; 32 points: stated by Subercaseaux, Mackey, Qian and Heule (arXiv:2506.00224, §6.2; the arXiv version gives no method for its last step, that the six inner 12-point patterns are not realizable); certified in `C4CUT` (six realizability cuts by exact computation; certificate accepted by both checkers; encoder: written proof, refereed) |
| 5-fold rotation | **31** | `SYMMAX/c5_31points.txt` | Theorem 5 |
| 6-fold rotation | **30** | `SYMMAX/c6_30points.txt` | 36 points contain a threefold 33-point set (Theorem 1) |
| mirror | **32** | `SYMMAX/mirror_32points.txt` | Theorem 2 |

A rotation of order 7 or more has only regular orbits with at least 7 vertices, apart from the centre. Theorem A does not
need `C4CUT`: a fourfold set of at least 33 points has at least 36 points and contains 17 antipodal pairs.

**Central symmetry, odd k.** For every odd k there is a centrally symmetric set of 2^(k−2) points in general position
with no convex k-gon (`SYM2`; for k = 7, 32 points). This follows from Valtr's construction as described by Baek and
Balko (SoCG 2025, Definition 13, Lemma 14 and §6.1), with a centrally symmetric base and each cluster paired with its
negative. The cubic construction of `SYM2` is a special case after a quarter-turn. What `SYM2` adds is the explicit
specialization, a short direct proof and exact integer coordinates, answering the realization task of arXiv:2506.00224,
§7 (a twofold symmetric 32-point set).

**Central symmetry, even k.** For k = 6 the fourfold 16-point sets of arXiv:2506.00224 (App. C, Table 1) and of
Mackey's thesis (Fig. 3.28) are centrally symmetric. For every even k ≥ 8, a centrally symmetric 2^(k−2)-point set
without a convex k-gon is implied by Baek–Balko, Lemma 14, applied to either set with a half-turn-symmetric labelling
and half-turn-paired clusters. Neither paper states this, and the SoCG version omits the proof of Lemma 14. Exact
instances from this route with 64 points (k = 8) and 256 points (k = 10) are in `SYMEVEN/lit`. `SYMEVEN` also has a self-contained proof that does not use Lemma 14, a cubic construction with a much
narrower middle cluster (written proof, refereed), with exact instances for k = 6, 8 and 10. The section "Even k" of
`SYM2` predates this.

**Hexagons (k = 6; `SYMMAX`, section "Hexagons").** The largest symmetric hexagon-free sets have 16 points for 4- and
5-fold rotations (the examples are in arXiv:2506.00224) and for the half-turn (a fourfold set is twofold), 13 for
threefold rotations (15 and 16 points are UNSAT with retained LRAT proofs; 16 agrees with arXiv:2506.00224), and 12 for
a reflection (the mirror lemma below).

**Mirror lemma.** Take as coordinates the projection to the mirror and the signed distance to it. A cap of points of S
on or above the mirror (its interior points are then strictly above), together with the mirror images, is in convex
position; an endpoint on the mirror counts once. The polygon through the cap and back through the images is x-monotone,
hence simple, and all its turns have one sign; so it is convex. With the cups–caps theorem the lemma bounds
mirror-symmetric octagon-free sets by 58 points. With Baek's theorem for n = 8 (at most 22 points) the bound is
2·22 + 2 = 46, a corollary of Baek's theorem (Lean-checked as `MirrorOdd.mirror_eight_line` in `SYMLEAN/mirror`); a
46-point example is in `MIRRORETV` (exact computation).

## 3. Trust base

**Lean-checked.**
- The reduction from the case classes to Theorem A, for isometries and affine bijections (`SYMLEAN`).
- Bookkeeping: the cover of the 910 threefold roots by 73,567 leaves (`C3LEAN`, `C3Cover.lean` `4b64293d…`, core Lean,
  `decide +kernel`), and the closure of the 8 × 287 central orbits (`C2FINAL/Central34Orbits.lean`). Lean does not know
  which records are certified; that every leaf or orbit member names a certified record with a matching CNF hash is an
  exact computation in Python.
- The mirror chain of 21 October for Theorem 2a, conditional on its CNF facts (`WRITEUP/MIRROR.md` §6).
- The mirror bound |S| ≤ 32 from the repository's formalization of Baek's theorem, and with it the two mirror classes
  (`SYMLEAN/mirror`, §0).

**Written proofs, refereed or audited (not Lean-checked).**
- Encoder soundness. Threefold: `C3-S/soundness.md` and the C3a encoding (audits `C3AUDIT`–`C3AUDIT4` and `AUDIT3` A2,
  which found two documentation gaps, A2-F3 and A2-F4). Fivefold and fourfold: `symcnf.py`, `SYM5/symcnf_layers.py`
  (`AUDIT3` A4; `C4CUT/review`). Mirror: `SYMZ/zcnf.py` (`SYMZ/README.md`; two audits of 29 October; `AUDIT3` A3).
  Central: `C2ENC`, refereed; its finding R1 adds that each second-layer cover is a cover relative to a hull cube, a
  one-line consequence of the base theorem (`C2FINAL` §1).
- The perturbation lemma for odd orders (`C2ENC`), reductions A and B, Lemma 5 and Lemma H6M of the
  threefold split, and the mirror reduction (also Lean-checked in `SYMLEAN/mirror`).
- Every case except Theorem 2 rests on one encoder; Theorem 5 uses two normal forms of one encoder.
- Baek's theorem itself is a refereed published theorem; the repository uses an adapted Lean formalization of it.

**Certificates accepted by both checkers, proofs retained** (`WRITEUP/CERTIFICATES.md`): `mirror33`, `mirror34`, the
fivefold P1 and L1, the central hull cover, the 120 hexagonal hulls (cake_lpr first ran on an unhashed rebuilt CNF; the
re-check on hash-checked files is under Theorem 4), the C4CUT final proof, 7 pilot and 34 sample re-solves of central
units, and the re-solves of 1 November: the 58 P8 pilot orbits, 44 of the 65 local-record units and 81 lane spot-check
units by 19:43 UTC (`C2RECHECK`), and the 204 indispensable threefold σ-cube pieces (`C3PIECES`). The checkers lrat-check (2e3b2dc with the E2 patch) and cake_lpr
(a36874a8, verified in CakeML, built locally for arm8) are trusted; CaDiCaL c6073042 (3.0.1), which produced the
proofs, is not.

**Certificates accepted by lrat-check only.** The second fivefold proof L2, in the hash-bound replay of 1 November
(`AUDIT3` §5 row 1), and the 17-point case n = 7 of Baek's theorem (`MIRRORETV`).

**Recorded verdicts (proofs deleted).**
- Threefold: all 116,883 pieces, each accepted by both checkers at solve time; 26,436 records carry the proof's
  SHA-256, which identifies a proof but cannot recreate it.
- Central parallelograms: the 2,385 UNSAT records, each accepted by both checkers at solve time and carrying the proof's
  SHA-256, apart from the units since re-solved with both checkers.
- Mirror chain of 21 October: about 75,000 CNF facts with recorded cake_lpr verdicts (that chain trusts only
  cake_lpr).

**Exact computations.** The compositions (`C3FINAL`; `C2FINAL` recount and hash matching), the verification of the six
C4CUT cuts, and the lower-bound examples (two independent exact methods per file, `AUDIT3` A7).

**Computational evidence.** Random, real-set and mutation tests of every encoder, and the random re-solve samples
(`C3SPOT`, `C2FINAL` §5) as evidence about the records that were not re-solved.

**Replays of retained certificates** (the re-solves are listed under Theorems 1 and 4). A replay kit hash-checked 191
retained certificates (archive, proof and CNF SHA-256 equal the records) and replayed lrat-check with hash-bound logs on
the 18 proofs under 2 GB, all `c VERIFIED`, among them L1, L2 and the C4CUT proof (`AUDIT3` §5 row 1). A full replay
with both checkers and hash-bound logs (`REPLAY`, 1 November, 17:59–18:02 UTC) accepted L1, the C4CUT proof and the
two c3hex proofs. By 1 November 2026, 19:43 UTC, it had not been run on `mirror33`, `mirror34`, P1, L2 or the hull
cover (cake_lpr heaps 8,000 to 30,000 MiB): lrat-check has no hash-bound replay on `mirror33`, `mirror34`, P1 or the
cover, and cake_lpr none on these or on L2. (After that time the hull cover was replayed as well, at 20:10 UTC: both checkers accepted it on files with the recorded hashes; see `REPLAY` §6.)
The retained proofs are archived outside Git, compressed with zstd, with decompression round trips
(`WRITEUP/CERTIFICATES.md`, also for the regeneration plans).

## 4. What remains open

- **ES(7).** Still open; no unrestricted bound is improved.
- **Recorded verdicts.** Most threefold pieces and most central parallelogram pieces can be re-checked only by
  re-solving them. A full regeneration needs compute comparable to the original campaigns.
- **Lean.** No step from a CNF to a Lean class is formalized, and the encoder soundness proofs are written proofs.
- **Further checks named by `AUDIT3`.** A CNF-level check of Lemma 5 and Lemma H6M, not run. The lane-stratified spot
  check of the central records was started on 1 November: 81 of 242 units by 1 November 2026, 19:43 UTC (Theorem 4).
- **Limits of abstract models.** A satisfying assignment is not a counterexample until it is realized with exact
  coordinates. The fourfold 32-point formula of the layered encoder is satisfiable although no real set exists; only
  UNSAT answers, with sound encodings and certified covers, are used.

## 5. Literature consulted

- Subercaseaux–Mackey–Qian–Heule, arXiv:2506.00224v1 (full text) and its public code; the CICM 2025 chapter (Springer,
  pages 29–47): metadata only, its text was not accessible.
- E. Mackey, CMU-CS-25-108 (thesis): abstract, contents, §3.1, §3.2.4, chapter 4 and a full-text search.
- B. C. Dumitru, arXiv:2512.24061v1 (full text, Table 1 as rendered), the generator `bogdan27182/esc-paper` at commit
  9520ceac17, and his homepage.
- J. Baek, Eur. J. Combin. 124 (2025) 104085 (arXiv:2206.04260), and its Lean 4 formalization.
- Baek–Balko, SoCG 2025 (Definition 13, Lemma 14, §6.1 and a text search); the JCTA version: abstract only.
- Balko–Valtr, ENDM 49 (2015); Morris–Soltan, Bull. AMS 37 (2000), Thm 2.6; Erdős–Szekeres 1935 and 1960/61.
- Krapivin–Przybocki–Heule, arXiv:2607.02958v1 (full text).
- Zeng–Liu–Ratnavelu–Ong, SSRN 7334758 (August 2026), read through a cached copy (SSRN returned 403): a SAT encoding for
  33 points. It reports that the reduced five-point family of Dumitru's generator admits a Boolean model at the known
  (17, 6) threshold, so that model is a weak relaxation, not an unsound one.
- M. Schroeder, Zenodo 22842891 (September 2026; text search): claims ES(7) ≤ 81 and ES(8) ≤ 319, unreviewed; no
  symmetric results.
- Georgiev–Gómez-Serrano–Tao–Wagner (AlphaEvolve), arXiv:2511.02864, Problem 6.58: constructions with 2^(k−2) points
  for k ≤ 8, no symmetry stated.
- Koshelev–Koshka, arXiv:2604.20120v1 (§9.1.2 and a text search).
- Heule–Scheucher arXiv:2403.00737 (in part); Scheucher arXiv:2105.08406 and arXiv:1807.10848; Subercaseaux et al.
  arXiv:2403.17370 and arXiv:2311.03645 (text search).
- Index searches: OpenAlex, Semantic Scholar (citations of arXiv:2506.00224 and of Dumitru), the arXiv API, zbMATH
  Open, OEIS, erdosproblems.com #107 and its forum thread, MathOverflow, and the 2025–2026 publication files of M. Heule;
  for the even-k question also Google Scholar (queries and cited-by lists, until it showed a robot check).
- **Not inspected:** the text of the CICM 2025 chapter, Dumitru's announced second version, Erdős–Tuza–Valtr 1996, the
  journal versions of Balko–Valtr and Baek–Balko, and DBLP. Priority
  statements stay provisional until these are checked.
