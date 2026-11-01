# ES7SPLIT: splits of heptagon-free sets and the Erdős–Tuza–Valtr case (7,5,7)

Written proofs, an independent review and local checks on an Apple M5 Pro, 1 November 2026 (UTC).

**Statement.** Let S be a set of at least 33 points in general position with no 7 points in convex position. Every
z-split S = A ∪ B with |A|, |B| ≥ 2 is unbalanced: one part is a convex chain of at most 6 points, and the other part
has at least 27 points and no z-5-cap (or no z-5-cup). Such a split exists for some 33-point set if and only if
N(7,5,7) ≥ 27, that is, if and only if the Erdős–Tuza–Valtr conjecture fails in the case (7,5,7).

**Status.**
- Theorems 5 and 6, Corollary 7, Proposition 8 and the hexagon chord lemma are written proofs (`proofs/`). Each was
  checked by an independent review, which found no error (§8, `review/`).
- Theorems 5 and 6 and Corollary 7 use one published theorem as a black box: Baek's case a = 4 of the
  Erdős–Tuza–Valtr conjecture. Its abstract form at n = 7 is Lean-checked; the step to real point sets is not (§2).
  Nothing else here is Lean-checked. Proposition 8 uses no outside result except the classical cups–caps theorem,
  and the chord lemma is elementary.
- The 27-point witness (§4) and the split counts of the known example sets (§6) are exact computations, checked by
  the review.
- That splits are rare among 32-point heptagon-free sets is computational evidence from a biased sample (§6).
- No hexagonal hull at 33 points, at least 7 convex layers at 33 points, and N(7,5,7) = 26 are conjectures (§7).

## 1. Definitions

- S is a finite set of points in the plane in general position (no three on a line). gon(X) is the largest number of
  points of X in convex position. "Heptagon-free" means gon ≤ 6.
- A *point outside S* is either a point z ∉ conv(S) or a direction, read as a point at infinity.
- A partition S = A ∪ B into nonempty parts is a *z-split* (A the upper part, B the lower part) if
  - (S1) every b ∈ B lies strictly on z's side of every line through two points of A, and
  - (S2) every a ∈ A lies strictly on the side of every line through two points of B that does not contain z.

  For z the downward direction, B lies below every line spanned by A and A lies above every line spanned by B.
  Baek and Balko (SoCG 2025) call this "B deep below A" when in addition every point of B is lower than every point of
  A. That extra condition is not used here. A split is *nontrivial* if |A|, |B| ≥ 2. A set is *split-free* if it has
  no nontrivial z-split for any z.
- Points are ordered by angle as seen from z. A sequence in this order is a *z-cup* if every middle point lies on z's
  side of the chord through two points around it, and a *z-cap* if it lies on the other side. For the downward
  direction these are the usual cups and caps. cap_z(X) and cup_z(X) are the largest sizes.
- N(7, a, b) is the largest size of a set in general position with distinct x-coordinates, no a-cap, no b-cup and
  gon ≤ 6. Known: N(7,3,7) ≤ 6 (with no 3-cap the set is a cup, hence convex); N(7,4,7) ≤ 16 (Baek);
  26 ≤ N(7,5,7) ≤ 56 (the Erdős–Tuza–Valtr construction, and the cups–caps bound C(8,3)). The Erdős–Tuza–Valtr
  conjecture says N(7,5,7) = 26. It is open according to the repository's survey `docs/RELATED_WORK_2026-10-14.md`,
  which cites Baek–Balko (SoCG 2025).

## 2. The split theorem (Theorem 5)

**Statement.** Let S be in general position with gon(S) ≤ 6 and |S| ≥ 33, and let S = A ∪ B be a z-split with
|A|, |B| ≥ 2. Put c = cap_z(A) and d = cup_z(B). Then (c, d) is (4, 2) or (2, 4).
- In case (4, 2), B is a z-cap of 2 to 6 points, so it is in convex position, and A has at least |S| − 6 ≥ 27 points
  and no z-5-cap.
- Case (2, 4) is the mirror image: A is a z-cup of 2 to 6 points, and B has at least 27 points and no z-5-cup.
- If N(7,5,7) = 26, no such split exists.

**Proof outline** (`proofs/split_theorem.md`).
- A projective map sends z to the downward direction. It keeps orientation signs and convex position, and it turns
  the z-order into the x-order and z-caps and z-cups into caps and cups (Lemma 0; z may first be moved off all lines
  through two points, Lemma 0′).
- A subset in convex position that meets both parts meets A in a z-cap and B in a z-cup (Lemma 2, a wedge argument).
  A z-cap of A together with a z-cup of B is always in convex position (Lemma 3, by comparison with points on a
  circle). Hence
  gon(S) = max(gon(A), gon(B), cap_z(A) + cup_z(B)) (Corollary 4).
- So c, d ≥ 2 and c + d ≤ 6. With N(7,3,7) ≤ 6 and Baek's N(7,4,7) ≤ 16:

| (c, d) | bound on \|A\| + \|B\| |
|---|---|
| (2, 2) | 6 + 6 = 12 |
| (2, 3), (3, 2) | 6 + 16 = 22 |
| (3, 3) | 16 + 16 = 32 |

  All are below 33. Only (4, 2) and (2, 4) remain.

**Rigor.** Written proof (reviewed). The black box is Baek's theorem: C(n−1, 2) + 2 points in general position with
distinct x-coordinates contain a 4-cap or n points in convex position (J. Baek, Eur. J. Combin. 124 (2025) 104085,
arXiv:2206.04260).
- The repository's port of its Lean formalization (`docs/THIRD_PARTY.md`, `ErdosSzekeres/Vendor/ETV/Main/Main.lean`)
  states the theorem for abstract configurations.
- Its instantiation at n = 7 (17 points) is Lean-checked: `review/equivalence/BaekSeven.lean`, axioms `propext`,
  `Classical.choice`, `Quot.sound`.
- The step from the abstract form to real point sets is not Lean-checked for n = 7; the repository's bridge covers the
  octagon case only. Here that step rests on the published paper.

**At 32 points** the same table leaves (3, 3) with two parts of 16 points, and (4, 2) or (2, 4) with one part of at
most 6 points. The classical set realizes all three (§6). With a single hull vertex as B, Corollary 4 gives the
Tóth–Valtr reduction ES(7) ≤ N(7,6,7) + 2.

## 3. Equivalence with ETV(7,5,7), and general k

**Theorem 6.** The following are equivalent:
1. some set of 33 points in general position with gon ≤ 6 has a z-split with |A|, |B| ≥ 2;
2. N(7,5,7) ≥ 27: some 27 points in general position with distinct x-coordinates contain no 5-cap and no 7 points in
   convex position.

- 1 ⇒ 2 is Theorem 5. 2 ⇒ 1 is the classical Erdős–Tuza–Valtr gluing: put a 6-point cap far below the 27 points. It
  is also recorded in `cloud/es7-2026-10-19/plan/es7_structure.md`, lead L1.
- So a 33-point counterexample to ES(7) = 33 with a nontrivial split exists exactly when ETV(7,5,7) fails. If
  ETV(7,5,7) holds, every 33-point heptagon-free set is split-free.
- **Rigor.** Written proof (reviewed). The review ran the gluing recipe on the 26 leftmost points of the classical set,
  since no 27-point set is known: at M = 3000, 10⁴, 10⁵ and 10⁶ it gives 32 points in general position with gon 6;
  at M = 10, 100 and 1000 the split fails (`review/equivalence/gluing_check.txt`).

**Corollary 7 (general k).** Let k ≥ 5, and let S be in general position with more than 2^(k−2) points and no k points
in convex position. If the Erdős–Tuza–Valtr values N(k, a, k) = Σ_{i=0}^{a−2} C(k−2, i) hold for all 5 ≤ a ≤ k − 2,
then S has no z-split with |A|, |B| ≥ 2.
- The cases needed beyond Baek's theorem are a = 5 for k = 7, and a = 5, 6 for k = 8. They are open according to
  `docs/RELATED_WORK_2026-10-14.md`; this was not checked further. The case a = 3 is trivial and a = 4 is Baek's
  theorem. For k ≤ 6 the statement is vacuous (ES(5) = 9, ES(6) = 17).
- **Rigor.** Written proof (reviewed); the written proof is a short sketch that refers back to Theorem 5. The
  arithmetic (the two bounds add up to at most 2^(k−2), with equality exactly when c + d = k − 1) is an exact
  computation for k ≤ 120 (`review/general_k/arith_check.out`).
- General position is needed: two parallel rows of 5 points form a z-split of 10 > 8 points with no 5 points in
  strictly convex position (`review/general_k/nongp_example.out`).

## 4. Hull vertices and convex hexagons (Proposition 8)

Let N* = N(7,5,7), so 26 ≤ N* ≤ 56.
- (a) Let S be in general position with gon(S) ≤ 6, v a vertex of conv(S), and T ⊆ S ∖ {v} with |T| ≥ N* + 1. Then
  T ∪ {v} contains a convex hexagon with v as a vertex. So every hull vertex of a heptagon-free set of at least
  N* + 2 points lies on a convex hexagon.
- (b) Some heptagon-free set of N* + 1 points has a hull vertex on no convex hexagon.
- Consequence: "every hull vertex of a 33-point counterexample lies on a convex hexagon" follows from N(7,5,7) ≤ 31.
- The key step is the Tóth–Valtr frame: seen from the hull vertex v, Y ∪ {v} is in convex position exactly when Y is
  a v-cap. So a convex hexagon through v is the same as a v-5-cap.
- **Rigor.** Written proof (reviewed).

**The 27-point witness** (`data/prop8b_witness27.txt`, SHA-256 `a888c6b2…`). Exact computation, checked by the
review with three convexity tests (`review/witness27/`, `review/hull_vertex_hexagon/`).
- It is the upper part A (26 points) of a (26, 6) z-split of the classical set with cap_z(A) = 4, followed by the
  first point b = (0, 0) of the lower part. The split was checked exactly with z = (−290/3141, 1000290/3141).
- General position. 0 of the 888,030 7-subsets are convex; there are 9,632 convex hexagons.
- b is a vertex of the 5-point hull. 0 of the 65,780 6-subsets through b are convex; the largest convex set through b
  has 5 points.
- Layer profile (5, 6, 5, 6, 4, 1).

So the property fails at 27 points. That is N* + 1 only if N(7,5,7) = 26; the threshold N* + 2 is at least 28. In
the full classical set, b lies on 10,006 convex hexagons; removing the other 5 points of the lower part removes all of
them. In all 216 sampled 32-point sets (§6), every hull vertex lies on a convex hexagon (computational evidence).

## 5. The hexagon chord lemma

**Statement** (`proofs/hexagon_chord_lemma.md`). Let S be in general position with gon(S) ≤ 6, and let
H = h_0 … h_5 be a convex hexagon with vertices in S, counter-clockwise. For m ∈ {1, 2, 3} let a = h_i and
b = h_{i+m+1}; the chord ab cuts off the m vertices h_{i+1}, …, h_{i+m}. Let R(i, m) be the open region beyond ab, on
the side of the cut-off vertices, and strictly inside the two edge lines of H at a and b on the kept side.
- **Lemma.** No m + 1 points of S ∩ R(i, m) are in convex position together with a and b.
- **Corollary (m = 1).** For every vertex h_j, the points of S in R(j − 1, 1) form a chain totally ordered by nesting
  with respect to the chord h_{j−1}h_{j+1}. The chain consists of h_j, the points inside the ear triangle
  h_{j−1}h_jh_{j+1}, and the points outside H that see exactly the two edges at h_j. If the hull is a hexagon, the
  points in each ear triangle are nested. If H is a 6-hole, the outside points that see exactly the two edges at h_j
  form, with h_j, a nested chain.

**Rigor.** Written proof (reviewed). It is elementary and of folklore type; no novelty is claimed. It gives exact
local constraints around every convex hexagon, for example around a hexagonal hull, or around the 6-holes that a
33-point counterexample must contain (Heule–Scheucher, as recorded in `LIT/RELATED.md`: every 24 points contain a
6-hole or 7 points in convex position).

**Checks** (exact computation, by the review). Every convex hexagon of the classical, mirror and central sets (39,648,
23,184 and 27,055 hexagons), of the 3-fold 27-, 30- and 31-point, 4-fold 28-point and 6-fold 30-point sets, of the
witness, and of all 216 sampled order types (3,545,557 hexagons), with every i and m: the largest subset of
S ∩ R(i, m) in convex position together with a and b has exactly m points. The ear triangles of the classical hull
contain 4, 4, 4, 9, 9 and 4 points, so nesting does not force ears to be small.

## 6. Splits in known sets: rare, so little pruning power

**Example sets** (exact computation, reproduced by the review).

| set | file (copy of) | SHA-256 | points | nontrivial z-splits |
|---|---|---|---|---|
| classical (Erdős–Szekeres construction) | `data/classical32.txt` (output of `scripts/es_lower_bound_witness.py 7`) | `7b3f97bb…` | 32 | 6 |
| mirror | `data/mirror32.txt` (`SYMMAX/mirror_32points.txt`) | `255e2390…` | 32 | 0 |
| central | `data/central32.txt` (`SYM2/sym7_32points.txt`) | `7246a30a…` | 32 | 0 |
| 3-fold | `data/c3_31points.txt` (`SYMMAX/`) | `f0220193…` | 31 | 0 |
| 3-fold | `data/c3_30points.txt` (`SYMMAX/`) | `c57cc567…` | 30 | 0 |
| 6-fold | `data/c6_30points.txt` (`SYMMAX/`) | `40745fe6…` | 30 | 0 |
| 4-fold | `data/c4_28points.txt` (`SYMMAX/`) | `86d4e0bf…` | 28 | 0 |
| 3-fold | `data/c3_27points.txt` (`SYMMAX/`) | `4fa6a01a…` | 27 | 0 |
| 5-fold | `data/c5_31points.txt` (`SYMMAX/`) | `4f1e2e63…` | 31 | 0 (review only) |
| 5-fold | `data/c5_30points.txt` (`SYMMAX/`) | `f709fb90…` | 30 | 0 (review only) |

- The 6 splits of the classical set are 3 partitions (its first 6 | last 26, first 16 | last 16 and first 26 | last 6
  points in x-order), each with both choices of upper part. Their types (|A|, |B|, cap_z A, cup_z B) are
  (6, 26, 2, 4) ×2, (26, 6, 4, 2) ×2 and (16, 16, 3, 3) ×2, all with c + d = 6, as §2 predicts at 32 points. The
  16-point parts sit at Baek's bound. The 26-point parts sit at the ETV construction value 26, the conjectured
  N(7,5,7), which is not a proven bound.
- **Completeness.** Every nontrivial z-split is induced by a line through two points (Lemma 4′ in
  `proofs/split_theorem.md`, written proof, reviewed). `tools/splits.py` tests every such partition. On the split-free
  sets every partition already fails the exact one-sidedness test, so the LP decides nothing
  (`logs/split_exactness.txt`). The review enumerated all one-sided partitions again by two methods that do not use
  Lemma 4′.
- The 3-fold and 6-fold files are in Eisenstein coordinates (`SYMMAX/README.md`). The map to the plane is linear with
  positive determinant, so orientation signs, and with them all results here, are unchanged. The 5-fold files are in
  cyclotomic coordinates; only `review/example_set_splits/fivefold_check.py` reads them, with exact arithmetic in
  Q(√5).

**Walk sample** (computational evidence).
- 216 distinct order types (up to reflection) of heptagon-free 32-point sets. They come from random walks through
  heptagon-free sets started at the classical, mirror and central sets (3 seeds each) and at 3 annealed random sets,
  run with the repository generator `cloud/es7-2026-10-19/tools/trackA/gen.c` (byte-identical, with `gen_core.h`, to
  the copy in `experiments/es7-search-2026-10-13/saturation/src/` that was compiled; `data/walks/`,
  `logs/walks.out`). Every set was re-verified exactly: general position, largest convex subset 6.
- Only the classical start has a nontrivial split: 215 of the 216 are split-free. The walks from the classical set
  emit a state every 1,000 accepted moves, and already the first state after the start has none
  (`logs/split_exactness.txt` counts 18 splits in all 222 emitted sets: the 6 of the start, once per seed). In a
  separate walk from the classical set that moves one point per step (40 visited sets), only the start has splits
  (`review/split_theorem/log_k7_walk.txt`).
- Hull sizes: 3: 40, 4: 127, 5: 45, 6: 4. Numbers of convex layers: 6: 14, 7: 168, 8: 34. The profile
  (6, 6, 6, 6, 6, 2) occurs twice: the mirror set and one set from the walks with random starts.
- Every hull vertex has a 5-cap and a 6-cup in its own frame, so it lies on a convex hexagon.
- The 4 hexagonal-hull sets have nested ears, with up to 9 points per ear.
- The sample comes from a biased local search. It is evidence about the sets such walks reach, not about all
  heptagon-free 32-point sets. The split counts of the sample were not re-checked by the review. The chord-lemma
  check re-ran all 216 order types with its own code (heptagon-freeness, hull sizes, ears).
- One of the ten walks (classical start, seed 1) was regenerated with a fresh build of the generator; its 21 lines
  matched byte for byte (`logs/walk_regen.txt`).

**Consequence** (computational evidence, not a proof). In this sample every set away from the classical start is
split-free. This suggests that a counterexample, if one exists, would be split-free anyway, so the split theorem
prunes little.

## 7. Conjectures

Conjectures 1 and 2 are statements about 33-point heptagon-free sets, that is about objects that do not exist if
ES(7) = 33, so they cannot be refuted without refuting ES(7) = 33. Their use would be as case splits or as partial
results. Conjecture 3 is about 27-point sets: a 27-point example would refute it without refuting ES(7) = 33.

1. **Conjecture (no hexagonal hull).** No set of 33 points in general position with no 7 points in convex position
   has a hexagonal convex hull. The 32-point analogue fails: the classical and mirror sets and two more sampled sets
   have hexagonal hulls.
2. **Conjecture (at least 7 layers).** Every such 33-point set has at least 7 convex layers. A special case, also
   open: five nested convex hexagons as layers plus 3 interior points always contain 7 points in convex position, so
   the layer profile (6, 6, 6, 6, 6, 3) does not occur. The 32-point analogue fails: 14 sampled sets have exactly 6
   layers, among them the classical (6, 6, 6, 5, 6, 3), central (4, 6, 6, 6, 6, 4) and mirror (6, 6, 6, 6, 6, 2)
   sets. Five nested hexagons occur at 30, 31 and 32 points: the 3-fold and 6-fold 30-point sets (6, 6, 6, 6, 6), the
   3-fold 31-point set (6, 6, 6, 6, 6, 1) and the mirror set (exact computation, `tools/geom.py`).
3. **Conjecture (Erdős–Tuza–Valtr, case (7,5,7)).** N(7,5,7) = 26: every 27 points in general position with distinct
   x-coordinates contain a 5-cap or 7 points in convex position. With Theorem 6 and Proposition 8 it would make every
   33-point heptagon-free set split-free and put every hull vertex on a convex hexagon; for the latter N(7,5,7) ≤ 31
   suffices.

**Cost** (computational evidence, `calib/`). The project's estimate for ETV(7,5,7) at 27 points is 10⁵ to 10⁶
core-hours (`B3/README.md`; the earlier probes of `B2/README.md` gave 10⁴ to 10⁶ or more). Plain CaDiCaL 3.0.1 runs
here, with wall-clock or user times on a shared, loaded machine:
- **Hexagonal hull, k = 7** (`calib/gen_hull.py`: the repository's hull normal form plus an exact hull-size
  constraint). 33 points with the repository's reflection lex-leader: no answer after 900 s (user 890 s). 32 points:
  SAT in 2.6 s (user time). That model is an abstract signotope with 6 extreme points and largest convex subset 6,
  used only to validate the encoding; it is not claimed realizable.
- **The k = 6 analogue at 17 points.** Pentagonal hull 24.8 s, quadrilateral 128.4 s, triangular 105.1 s (user time),
  against 123 s wall-clock for the instance without a hull constraint. The (k−1)-gon case is the cheapest piece, but
  splitting by hull size does not reduce the total.
- **ETV encoder** (`calib/gen_etv.py`, signotope model). Controls: (6,4,6) SAT at 11 and UNSAT at 12; (6,5,6) SAT at 15
  and UNSAT at 16 (62 s); (7,4,7) SAT at 16 and UNSAT at 17 (0.6 s); (6,6,6), the ES(6) instance, SAT at 16 and no
  answer at 17 within 120 s; (7,5,7) SAT at 20, 23 and 26. The case (6,5,6) is UNSAT at 17, 18 and 20 points in 86,
  125 and 235 s. So adding points makes plain CDCL slower here. By extrapolation from this k = 6 case, weakening
  ETV(7,5,7) to N(7,5,7) ≤ 31 is not expected to be cheaper with this encoding; this was not tested at k = 7.
- **Validation.** Every SAT model was re-checked by a separate decoder (`calib/check_model.py`,
  `calib/check_hull_model.py`), which recomputes the properties from the model, not from the clauses
  (`calib/logs/model_checks.txt`). The decoders come from the same work as the encoders and were not reviewed. The
  hull-size constraint gives SAT for hulls 3 and 4 and UNSAT for hull 5 at 8 points without a convex pentagon, and SAT
  for hulls 3, 4, 5 and UNSAT for hull 6 at 16 points without a convex hexagon; every model has the prescribed number
  of extreme points. A first version used the wrong hull side, and the decoder caught it.
- The UNSAT answers here carry no proofs and are not certificates.

## 8. Independent review (1 November 2026)

Seven independent checks, one per claim, each run separately from the work and from each other, with their own
exact-arithmetic code (`review/README.md`). **No claim was refuted and no mathematical error was found.**

| claim | label after the check |
|---|---|
| Theorem 5 (split theorem) | written proof (reviewed) |
| Theorem 6 (equivalence) | written proof (reviewed) |
| Corollary 7 (general k) | written proof (reviewed) |
| Proposition 8 | written proof (reviewed) |
| the 27-point witness | exact computation |
| hexagon chord lemma | written proof (reviewed) |
| z-splits of the example sets | exact computation |

Remarks taken into this directory:
- Every statement needs general position; the review gave a two-row example for Corollary 7 without it.
- "Lean-formalized" applies to the abstract form of Baek's theorem only (§2).
- The dynamic program used first for the witness re-typed the repository's own, so the review replaced it by
  exhaustive enumeration. The code that wrote the witness had been run inline and not saved; it is now
  `tools/make_witness27.py`, and a re-run reproduces the file byte for byte.
- In `tools/test_chord_lemma.py` the control "reaches m + 2" because that is the cap of the search loop; the proof file
  now says so.
- The scripts that wrote `logs/split_exactness.txt`, `logs/classical_split_bruteforce.txt` and
  `logs/walks_summary.txt` had been run inline. They are now saved in `tools/`, and re-runs reproduce the logs
  exactly.

## 9. Literature (1 November 2026)

For Theorem 5 and the direction 1 ⇒ 2 of Theorem 6, no matching prior result was found in the sources inspected:
- Baek–Balko, "The Erdős–Szekeres conjecture revisited", SoCG 2025 (LIPIcs, HTML version), read when the proof was
  written and again by the review: definitions of "deep below" and of decomposable sets, and Theorem 8 on recursively
  decomposable sets (proof omitted there). It contains no statement about a single split with arbitrary parts.
- Baek, "On the Erdős–Tuza–Valtr conjecture", arXiv:2206.04260 (Eur. J. Combin. 124 (2025) 104085): abstract and main
  theorem.
- The repository's surveys: `docs/RELATED_WORK_2026-10-14.md`, `cloud/es7-2026-10-19/plan/es7_structure.md` (lead L1
  records the direction 2 ⇒ 1), `LIT/RELATED.md` and `WRITEUP/SYMMETRIC.md`.
- Not inspected: the Erdős–Tuza–Valtr paper of 1996 and the journal version of Baek–Balko. Either could contain a
  matching statement.

The argument for 1 ⇒ 2 is a short combination of the classical cap–cup mechanism with Baek's theorem, so it may well
be known. Priority is not claimed. The chord lemma is of folklore type, and no novelty is claimed for it.

## 10. What is not checked

- None of the written proofs is formalized in Lean. Baek's theorem for real point sets at n = 7 is used as published.
- Novelty beyond the sources of §9.
- The split counts, layer counts and hull-vertex statistics of the walk sample come from `tools/` only; the review
  re-checked heptagon-freeness, hull sizes and ears of all 216 order types. The sample is not a census.
- No statement about 33-point sets is decided by computation here; the one 33-point run (§7) gave no answer. The
  conditional statements (the last sentence of Theorem 5, the consequence of Proposition 8, Corollary 7) depend on
  Erdős–Tuza–Valtr cases that are open.
- The Heule–Scheucher result (§5) is cited from `LIT/RELATED.md`, and the open status of the Erdős–Tuza–Valtr cases
  from `docs/RELATED_WORK_2026-10-14.md`. Neither was checked against the original papers here.
- The encoders in `calib/`, and the repository encoder `experiments/es7-search-2026-10-13/encoding/gen_cnf.py` that
  `gen_hull.py` calls, were checked by controls and model decoding only, not by a review. Their UNSAT answers have no
  proofs. The timings come from a shared machine.
- `review/split_theorem/log_k6_walk_seed1.txt` was written by an earlier version of `test_k6_walk.py` with narrower
  move scales.

## 11. Files

Paths in this README are relative to this directory (`proofs/`, `data/`, `tools/`, `logs/`, `calib/`, `review/`) or to
`cloud/es7-2026-10-19/results` (`SYMMAX/`, `SYM2/`, `B2/`, `B3/`, `LIT/`, `WRITEUP/`). Paths beginning with `docs/`,
`scripts/`, `experiments/`, `ErdosSzekeres/` or `cloud/` are from the repository root.

- `proofs/`: `split_theorem.md` (Lemmas 0–4′, Theorems 5–6, Corollary 7, Proposition 8) and
  `hexagon_chord_lemma.md`.
- `data/`: the example sets of §6, the witness `prop8b_witness27.txt` (last line = the hull vertex b), and `walks/`
  (generator output, one line per set: tag, number of 7-gons (0), two order-type signatures, n, coordinates).
- `tools/`: `geom.py` (exact predicates, layers, z-caps and z-cups), `splits.py` (all nontrivial z-splits),
  `split_exactness.py`, `classical_split_bruteforce.py`, `make_witness27.py`, `test_split_lemma.py`, `test_lemma0.py`,
  `test_chord_lemma.py`, `hullstats.py`, `analyze_walks.py`, `walks_summary.py`.
- `logs/`: outputs of the tools, and `walk_regen.txt` (one walk regenerated with a fresh build of the generator).
  Machine-specific path prefixes were removed from the logs.
- `calib/`: the ETV and hull-size encoders, their model decoders and run scripts, and `logs/` (solver outputs with the
  SAT models, run summaries `batch1.txt`, `batch2.txt`, `hull_calib_k6.txt`, `pilots.txt`, and `model_checks.txt`).
  No CNF is included; all are regenerable.
- `review/`: the independent review, its scripts and logs.

## Reproduction

From `cloud/es7-2026-10-19/results`. Python 3; `splits.py` and the scripts that import it need numpy and scipy.

```sh
E=ES7SPLIT
python3 $E/tools/geom.py $E/data/classical32.txt          # points, general position, gon, layer sizes
python3 $E/tools/splits.py $E/data/classical32.txt        # the 6 nontrivial z-splits with exact z
python3 $E/tools/split_exactness.py                       # = logs/split_exactness.txt
python3 $E/tools/classical_split_bruteforce.py            # = logs/classical_split_bruteforce.txt
python3 $E/tools/make_witness27.py w27.txt && cmp w27.txt $E/data/prop8b_witness27.txt
for s in 2 3 4 5; do python3 $E/tools/test_split_lemma.py $s 150; done      # = logs/test_split_lemma.txt
python3 $E/tools/test_lemma0.py                                             # = logs/test_lemma0.txt
python3 $E/tools/test_chord_lemma.py $E/data/classical32.txt $E/data/mirror32.txt \
  $E/data/central32.txt                                                     # = logs/test_chord_lemma.txt
# walk sample: build the repository generator (output files are appended to)
cc -O2 -o gen ../tools/trackA/gen.c -lm
for s in classical32 mirror32 central32; do for seed in 1 2 3; do
  ./gen walk 7 32 $seed 1 $E/data/$s.txt 1000 1 0.01 20000 1000 walk_$s.txt; done; done
./gen walk 7 32 77 3 random:200000 400000 1.0 0.01 20000 2000 walk_random.txt
python3 $E/tools/analyze_walks.py $E/data/walks/walk_classical32.txt $E/data/walks/walk_mirror32.txt \
  $E/data/walks/walk_central32.txt $E/data/walks/walk_random.txt walks_analysis.jsonl
python3 $E/tools/walks_summary.py walks_analysis.jsonl                      # = logs/walks_summary.txt
```

Calibration (`CADICAL` names the solver binary, `PY` the Python interpreter; outputs go to `etv_work/` and
`hull_work/`):

```sh
C=ES7SPLIT/calib
for spec in "11 6 4 6" "12 6 4 6" "15 6 5 6" "16 6 5 6" "16 6 6 6" "17 6 6 6" "16 7 4 7" "17 7 4 7"; do
  bash -c "$C/run_etv.sh $spec 120"; done                                      # logs/batch1.txt
for spec in "17 6 5 6 300" "18 6 5 6 300" "20 6 5 6 300" "20 7 5 7 120" "23 7 5 7 300" "26 7 5 7 300"; do
  bash -c "$C/run_etv.sh $spec" | cut -c1-80; done                            # logs/batch2.txt
mkdir -p hull_work/cnf
for h in 5 4 3; do python3 $C/gen_hull.py 17 6 $h -o hull_work/cnf/hull_N17_K6_h$h.cnf; done
python3 $C/gen_hull.py 32 7 6 -o hull_work/cnf/hull_N32_K7_h6.cnf
python3 $C/gen_hull.py 33 7 6 --mirror -o hull_work/cnf/hull_N33_K7_h6_m.cnf
WORK=hull_work bash $C/run_pilots.sh                                          # logs/pilots.txt
python3 ../../../experiments/es7-search-2026-10-13/encoding/gen_cnf.py 17 6 --hull -o plain.cnf
cadical -q -t 400 plain.cnf                                                    # logs/plain_N17_K6.out
python3 $C/check_hull_model.py 32 $C/logs/pilot_k7_N32_h6.out                  # one line of logs/model_checks.txt
```

The hull-size validation used `gen_hull.py 8 5 h` (h = 3, 4, 5) and `gen_hull.py 16 6 h` (h = 3, …, 6), each solved
with `cadical -q` and decoded with `check_hull_model.py`. The review's commands are in `review/README.md`.
