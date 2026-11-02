# PRIMEFOLD: (k−1)-fold symmetric sets of 2^(k−2) points without a convex k-gon

Local runs on an Apple M5 Pro, 1–2 November 2026 (UTC).

**Question.** For which k ≥ 3 is there a set of 2^(k−2) points in general position, invariant under a rotation of
order m = k−1, with no k points in convex position? If ES(k) = 2^(k−2) + 1 (the Erdős–Szekeres conjecture), such a set
has the largest possible size.

**Status.**
- The size 2^(k−2) fits an m-fold rotation exactly when m is an odd prime, an odd base-2 Fermat pseudoprime, or a
  power of 2 (§1; core Lean-checked). The rule is elementary: orbit counting plus Fermat's little theorem.
- Such sets exist for k = 3, 4, 5, 6, 8 (§2, §3). k = 3 and 4 are trivial; sets for k = 5 and 6 were already in print.
- k = 9 and k = 12 are open. The best sets found have 120 of 128 points (8-fold) and 991 of 1024 (11-fold) (§5).
- One orbit of rotated tiny generic clusters cannot give k = 9 (§4; certificate accepted by lrat-check only, on top
  of written proofs, not refereed).
- The general statement is a conjecture (§7), a specific form of a suspicion of Subercaseaux–Mackey–Qian–Heule
  (SMQH, arXiv:2506.00224v1).

Rigor labels: Lean-checked / certificate accepted by both checkers / certificate accepted by lrat-check only / exact
computation / written proof (not refereed) / computational evidence / conjecture / refuted.

## 1. Size compatibility (`compat/`)

**Statement.** A rotation by 2π/m (m ≥ 2) fixes only its centre O, so a finite invariant set S has mt + [O ∈ S]
points. Hence 2^(m−1) points are possible iff 2^(m−1) ≡ 0 or 1 (mod m).
- Even m: the residue must be 0, so m is a power of 2 (k = 3, 5, 9, 17, …), and O ∉ S.
- Odd m: the residue must be 1, so m is an odd prime or an odd base-2 Fermat pseudoprime, and O ∈ S.
- Compatible k: 3, 4, 5, 6, 8, 9, 12, 14, 17, 18, 20, …, and also 342, 562, 646 (m = 341 = 11·31, 561, 645).
- Antecedents: the prime case is Fermat's little theorem. SMQH §6.2 applies the same orbit count to 32 points
  (s ∈ {1, 2, 4}), and the 16-point layer formations (3,3,3,3,3,1), (4,4,4,4), (5,5,5,1) of Mackey (CMU-CS-25-108)
  are the same count for 16 points.

**Lean-checked** (`compat/lean/`; Lean 4.24.0, Mathlib `f897ebcf`; axioms `propext`, `Classical.choice`,
`Quot.sound` only).
- `PCompatCore.lean` (SHA-256 `ebc6aace…`): the orbit lemma in any commutative group with zero, for ζ of exact order
  m; its converse, given pairwise disjoint orbits (orbits of distinct radii in ℂ); and the classification "compatible
  iff m = 1, m = 2^a, or m odd with 2^(m−1) ≡ 1 (mod m)" for every m ≥ 1, with the example m = 341.
- `L0Check.lean` (`05a67c3b…`): for m ≥ 2, if a finite S ⊂ ℂ is invariant under z ↦ e^(2πi/m) z and |S| = 2^(m−1),
  then either m is odd, O ∈ S and m is prime or `Nat.FermatPsp m 2`, or O ∉ S and m = 2^j. No general position is
  assumed.
- Not formalized here: Fermat's little theorem (all odd primes are compatible), and the paper argument that generic
  radii and phases give compatible sets in general position.

**Exact computation.** `compat_check.py` computes 2^(m−1) mod m for m < 3000 in three ways. The compatible m in
[2, 3000) are 2, 4, …, 2048, all 429 odd primes, and the composites 341, 561, 645, 1105, 1387, 1729, 1905, 2047, 2465,
2701, 2821. `numerology.py` finds no exception for m ≤ 10^6 and counts 3, 22, 78 and 245 odd base-2 pseudoprimes below
10^3, 10^4, 10^5 and 10^6 (the known counts).

## 2. Small k

- **k = 3, 4** (trivial). Two points (2-fold); an equilateral triangle with its centre (3-fold).
- **k = 5 (4-fold, 8 points).** Eppstein's figure (Wikipedia File:8-points-no-pentagon.svg, 2007; Fig. 1.2 of
  *Forbidden Configurations in Discrete Geometry*, 2018) is two nested squares. With 342.002 replaced by 342 it is
  exactly 4-fold symmetric about (180,180), in general position (min |orient| 8019), with 38 convex 4-sets and 0 convex
  5-sets (`printed/exact_check.py`). As drawn it is symmetric to 4.4·10⁻⁶ of the diameter, with the same orientation
  table. The texts inspected do not call it symmetric.
- **k = 5 classification** (`k5/`; exact computation and written proof, not refereed). An 8-point 4-fold set is two
  concentric squares; unless one lies strictly inside the other, it is a convex octagon or has three collinear points.
  So take the outer square {1, i, −1, −i} and the inner square {iˡb}, with b = x + iy, x, y > 0 and x + y < 1.
  - The set is in general position with no convex pentagon iff x² + y² < |x − y|. It is degenerate on the arcs
    x² + y² = ±(x − y), and has exactly 20 convex pentagons elsewhere.
  - So the pentagon-free 4-fold 8-point order type is unique up to reflection (a chiral pair); an example is
    {(±10,0), (0,±10), (3,1), (−1,3), (−3,−1), (1,−3)}. Method: the 56 orientation determinants are integer
    polynomials in (x, y). An independent check re-derived it and tested 80,199 grid points.
  - Regions, with C1 = x² + y² − x + y and C2 = x² + y² + x − y: 4C1 = (2x−1)² + (2y+1)² − 2, so {C1 < 0} meets the
    triangle in a convex set; C2 is its mirror image, and C1 − C2 = 2(y − x), so the arcs do not meet. On each line
    x + y = c each of C1, C2 has one root, so the rest is connected: three components (identities: `k5/grid_check.py`).
  - O is never in a 4-fold set in general position (O, p, −p are collinear), so sizes are multiples of 4, and 8 is
    the maximum by ES(5) = 9.
  - Not consulted: the order-type database of Aichholzer, Aurenhammer and Krasser (all order types of 8 points), which
    may already contain this classification.
- **k = 6 (5-fold, 16 points).** SMQH, App. C Table 2 (also Mackey, Fig. 3.33): the orbits of (−12,−17), (−15,2),
  (−13,0), plus (0,0).
  - Exact computation in Q(√5)(√(10+2√5)) (`printed/exact_check.py`): general position (min |det| 1.433551), 1185
    convex 4-sets, 978 convex 5-sets, 0 convex 6-sets. It is maximal by ES(6) = 17. SMQH report 46 realizable
    5-fold classes.
  - Both rotated-cluster sets for m = 5 (§4; `sets/k6/`) have the order type of Table 2, by an orientation-preserving
    isomorphism (exact computation, `printed/compare_printed_*.out`).
- **k = 7** is not compatible: 32 ≡ 2 (mod 6). SMQH §6.2 also allows only s ∈ {1, 2, 4} for 32 points.

## 3. k = 8: 7-fold sets of 64 points (`sets/k8/`, `check64/`)

Each file is the centre plus 9 orbits, with coefficient rows in Z[ζ₇]. `check64/run_all.sh` checked all of them in
one run (`check64.log`; exact computation): distinctness, exact 7-fold invariance, all 41,664 orientation signs
nonzero, a 110-digit decimal recomputation of every sign, and convex k-gon counts by an anchor DP and again by a
separate C enumerator. Each set had also been checked earlier with other code. Five of the files are also in
`ES8SYM/sets/` (§6 there).

All have largest convex subset 7 (no convex octagon). Convex k-gon counts do not change under relabelling or
reflection, so the seven rows are pairwise non-equivalent order types.

| file | structure | convex 4-gons | convex 7-gons | line-modules, size 2..20 | SHA-256 |
|---|---|---|---|---|---|
| `c7_64pts_small` | annealing of layer radii and phases | 416,052 | 4,688,763 | none (none up to 60) | `ebe028f6…` |
| `c7_64pts_9layers_centre` | same float configuration, other scale | 416,220 | 4,691,381 | none (none up to 60) | `23e1389d…` |
| `c7_64_own_s1000` | second annealer | 392,966 | 3,328,145 | none | `c9942cc1…` |
| `c7_64pts_9layers_centre_own` | second annealer, other scale | 392,553 | 3,252,475 | none | `ec481469…` |
| `p7_compound_64` | one orbit of a two-level 9-point cluster | 470,764 | 18,396,499 | 91, incl. seven of size 9 | `ef50ee00…` |
| `rule_p7_64pts` | rotated-cluster rule, h = 3 (§4) | 487,711 | 30,031,745 | 91, incl. seven of size 9 | `bb38d29a…` |
| `m7_x2_G9s_centre` | one orbit of chord-aligned flat 9-point clusters | 462,581 | 14,719,287 | 77, incl. seven of size 9 | `ac524df7…` |

- `p7_two_orbit_64` (`9a55f245…`) has the same orientation table as `p7_compound_64` under the row labelling.
- "None up to 60" is from `check64/modules60/` (exact computation). So the first two sets are not blow-ups with
  clusters of 2 to 60 points.
- 64 points is the largest possible size only if ES(8) = 65, which is open.

## 4. The rotated-cluster construction (`cluster/`, `rule/`)

**The family.** Take a regular m-gon, replace each vertex by the same tiny cluster C (rotated with the vertex), and add
the centre for odd m. It gives sets of 2^(k−2) points for k = 3, 4, 5, 6 and 8 (cluster sizes 1, 1, 2, 3, 9): for
k = 5 and 6 with the order types of the printed sets of §2 (for k = 5 up to reflection, by the classification), for
k = 8 the last three rows of §3. The 253- and 991-point sets of §5 are also of this kind. The proofs are in
`cluster/PROOFS.md`, whose header lists the corrections.

**Lemma 1** (written proof, not refereed): a blow-up formula for tiny clusters with rotated directions, the tiny-cluster
form of the blow-up method of Erdős–Szekeres, Valtr and Baek–Balko. It needs the stated genericity (no cluster segment
parallel to a line through two base points); without it the formula is false. An independent check filled a small gap.

**Proposition C** (written proof, not refereed). One orbit of rotated copies of a generic tiny cluster C (with the
centre for odd m) has no convex (m+1)-gon iff (i) g(x) + h(x) ≤ x + 1 for x = 1, …, m−1, (ii) a centre condition holds
(only with O), and (iii) mc(C) ≤ m. Here g and h are the longest chains of C with directions in (0, x) and (−x, 0), in
units of π/m from the tangent. An independent check compared it with about 72,000 exact cases (scripts not copied). A
cluster of (2^(m−1)−1)/m points (odd m) or 2^(m−1)/m points (m = 2^a) satisfying (i)–(iii) would give k = m + 1.

**Theorem E** (certificate accepted by lrat-check only; it also uses Lemma 1, Proposition C (i) and the soundness of
the encoding, written arguments not refereed). A sound SAT relaxation of (i) is UNSAT for (m, n) = (4,3), (5,4),
(6,6), (7,10), (8,15) (`cluster/clsat.py`, `clsat2.py`).
- On 2 November the seven CNFs were regenerated with their recorded SHA-256 (e.g. `m8_n15`: `03329897…`) and
  re-solved with CaDiCaL 3.0.1; lrat-check accepted every proof (`cluster/sat/rerun.log`; the largest has
  25,378,109 bytes). cake_lpr was not run.
- An independent encoder (`cluster/check/enc_te.py`) gives the same UNSAT results, with and without the signotope
  axiom, and SAT at n−1. Its soundness was tested on 4,322 real clusters.
- So a generic cluster has at most 2, 3, 5, 9, 14 points for m = 4, …, 8, and the family at most 8, 16, 30, 64, 112
  points. For m = 8 it cannot reach 128: **this family cannot give k = 9.**
- The bounds for m = 4, …, 7 are attained by exact point sets: `sets/k5/c4_8_k5.txt`, the two sets in `sets/k6/`,
  the last three sets of §3, and for m = 6 a 5-point cluster found by the independent check (30 points, largest
  convex subset 6 by an exact DP and by the enumerator of `check64/`; `cluster/check/m6_cluster5.py`,
  `m6_cluster5_exact.log`). For m = 8, 14 is an upper bound only.
- Not covered: clusters with a segment exactly parallel to a chord, and sets with several orbits.

**The rule** (`rule/`; computational evidence). A max/min recursion gives an explicit binary-tree cluster (`recdp.py`,
`rule.py`, `gen_points.py`) of B(h) = 1, 3, 9, 28, 90, 297, 1001 points for h = 1..7 (m = 2h+1). The log covers
h ≤ 6; h = 7 (about 2.3 GB) was computed in the session and its log was not kept.
- For these h, B(h) = C(2h, h−1) − C(2h, h−2) (OEIS A000245). It equals (2^(m−1)−1)/m for m = 3, 5, 7, its floor for
  m = 9, and is smaller for m = 11, 13, 15.
- The clusters are realized and checked exactly for h = 2..5 (16, 64, 253, 991 points); h = 6 only in the cluster
  model. `rule/run_all.sh` rebuilds `rule/rule_p5.reps.pts`, `rule/rule_p7.reps.pts` and the 253- and 991-point files
  byte for byte (`rule/logs/rerun/rebuild.log`). The first two have the orientation tables of
  `sets/k6/rule_p5_16pts.pts` and `sets/k8/rule_p7_64pts.pts`.
- Conjecture: B(h) is the largest cluster of this design, so the rule stops at 991 points for m = 11.

**Flat clusters.** Theorems A and B of `PROOFS.md` are **refuted** as stated.
- `cluster/thmA/m11_beta0_ES54.pts` (111 points, 11-fold, radial flattening x = m/2) meets conditions (a)–(c), yet has
  12 points in convex position.
- `m7_x2_G9s_centre` (flattening along a chord) has flat clusters of 9 points, above the bound M(7) = 6.

Corrected versions (written proof, not refereed; M(m) and the inequality checked exactly for m ≤ 3000; full
hypotheses in the `PROOFS.md` header):
- A: for generic flattening directions (x not an integer, x ≠ m/2 with O, β normalised to (−π/2, π/2)), one orbit of
  flat clusters has at most m·M(m) points (plus the centre for odd m), less than 2^(m−1) for every m ≥ 7. M(m) comes
  from the Erdős–Szekeres cup–cap theorem. It is tight for m = 4, 5, 7 (8, 16, 43 points; `cluster/thmA/p7_33.pts`).
- B: if each cluster is flat relative to its own orbit, 2^(m−1) points need at least 2 orbits for m = 7 and at least
  3 for m = 11.

## 5. Records for k = 9, 10, 12 (`sets/`; exact computation)

**8-fold, 120 points** (k = 9; `sets/k9/c8_120pts_15layers.pts`, `6d8a4a09…`): 15 nested regular octagons, Z[ζ₈]
coefficients up to 9,675,611.
- The orientations of all 280,840 triples agree under two exact methods, and none is zero.
- Convex k-gons for k = 3..9: 280,840; 5,419,058; 54,588,512; 298,410,024; 871,843,824; 1,153,006,585; 0. These come
  from two DPs and a full enumeration (`check120/`), and again from the original pipeline (`check120/producer/`).
- The 104- and 112-point sets (13 and 14 layers; `1ff5d997…`, `ab6f43fd…`) are separate configurations, also without
  9 points in convex position.
- None of the three has a line-module of size 2..n−5. The only nontrivial ones are the complements of 2, 3 or 4
  consecutive hull vertices, 8 of each (`check120/modules/`). So none is a symmetric blow-up with clusters of 2 to
  n−5 points. (For 120 points, Theorem E alone excludes a generic single-orbit blow-up, since 120 > 112.)

**9-fold, 253 points** (k = 10; `sets/k10/rule_p9_253pts.pts`, `05af4d5b…`, 28 layers + centre). All 2,667,126
orientations are certified nonzero, and a 150-digit decimal recomputation of every sign agrees. The largest convex
subset is 9, by three DPs that were checked against brute force in 105 tests (`check253/`). k = 10 is not compatible:
a 9-fold set has 9t or 9t+1 points, so if ES(10) = 257, then 253 is the largest possible 9-fold size.

**11-fold, 991 points** (k = 12; `sets/k12/rule_p11_991pts.pts`, `e0e172a4…`, 90 layers + centre, coefficients up to
1.0018·10³⁰).
- All 161,716,335 orientations are nonzero, computed without using the symmetry (min |det| ≈ 3.69·10¹⁸).
- The largest convex subset is 11, by two DP variants over all anchors, with a checked 11-gon (`check991/`). A re-run
  on 2 November reproduced the sign table byte for byte (SHA-256 `d097369c…`, `check991/logs/rerun/`). The set is 3
  layers (33 points) short of 1024.
- The rule's GMP verifier (`rule/sym_cvx.c`) also passes for the 253- and 991-point sets, with 120-digit decimal
  re-checks of 94,072 and 196,385 sampled signs. Its floating-point filter bound is not formally derived; the checks
  in `check253/` and `check991/` do not use it.

## 6. Searches that failed (computational evidence only; none is an impossibility result)

- k = 9, 16 layers: about 3 CPU-hours of annealing and insertion scans; the best stall at cost 152 (a weighted count
  of convex 9-gons; 0 is needed).
- k = 12, one cluster, in the cluster model: no valid 91st layer in 36,158 single-leaf insertions or 1,600 grid
  positions for an extra layer, and annealing at 91 and 93 layers failed (from a random start it does not reach even
  90). Other rotated blow-ups (up to 5 flat blocks; 448 random tree clusters) reached a largest convex subset of 12
  (11 is needed).

## 7. Conjecture

**Conjecture.** For every size-compatible k ≥ 3 there is a (k−1)-fold rotationally symmetric set of 2^(k−2) points in
general position with no k points in convex position.
- True for k = 3, 4, 5, 6, 8. Open for k = 9, 12, 14, 17, 18, 20, …, and 342, 562, 646, ….
- It is a specific form of the suspicion in SMQH, arXiv:2506.00224v1, §7: "In particular, for the Erdős-Szekeres
  problem, we suspect that there are symmetric constructions for all k≥7, and proving this could represent progress
  toward the conjectured bound g(k)=2^{k−2}+1, since it might be easier to prove optimality for more structured
  solutions."
- SMQH name no symmetry type or order. The conjecture here fixes the order k−1 and the size 2^(k−2), and covers only
  compatible k.

## 8. Literature and credit

**Credit.**
- Erdős–Szekeres: the conjecture, the 2^(k−2)-point construction and the cup–cap theorem (used for M(m) in §4).
  ES(5) = 9 (Makai and Turán, credited in Erdős–Szekeres 1960/61; Kalbfleisch–Kalbfleisch–Stanton 1970) and
  ES(6) = 17 (Szekeres–Peters 2006) make the k = 5 and 6 sets maximal.
- Eppstein's figure (k = 5); SMQH Table 2 and Mackey Fig. 3.33 (k = 6), and SMQH's 46 realizable 5-fold classes; the
  divisibility remark of SMQH §6.2 and Mackey's 16-point layer formations; Fermat's little theorem.
- The blow-up method of Erdős–Szekeres, Valtr and Baek–Balko ((X,Y)-blow-ups, SoCG 2025); Lemma 1 is its tiny-cluster
  form with rotated directions. The layer lemma is in `SYM5/README.md` (SMQH §3.2 uses its 16-point 4-fold case).
- arXiv:2511.02864v3 (Georgiev–Gómez-Serrano–Tao–Wagner), item 38: 2^(k−2)-point sets without convex k-gons for
  k ≤ 8, no symmetry stated. Their published 65-point set has exactly one convex 8-gon (exact computation in the
  literature check, not copied).

**Sources inspected.**
- SMQH arXiv:2506.00224v1 (the only arXiv version) and its code repository; Mackey CMU-CS-25-108; arXiv:2511.02864v3
  and its repository; Baek–Balko SoCG 2025; B. C. Dumitru, arXiv:2512.24061v1.
- Krapivin–Przybocki–Heule arXiv:2607.02958v1; Koshelev–Koshka arXiv:2604.20120v1; arXiv:2505.15366; Aichholzer et
  al. (EuroCG 2019); Szekeres–Peters 2006; Eppstein's book excerpt and blog; Wikipedia; erdosproblems.com #107;
  `LIT/RELATED.md`.
- arXiv API listings up to late October 2026; OpenAlex, Semantic Scholar and Crossref citation data; the 45 logged
  searches in `lit/searches.tsv`.
- Not accessible: the Baek–Balko JCTA 2026 full text, the SMQH CICM chapter, Scheucher's BSc thesis, Google Scholar.

**No matching prior result was found in the sources inspected** for: rotationally symmetric sets for k ≥ 8 (the 7-fold
sets and the 8-, 9- and 11-fold records); the k = 5 classification (see the caveat in §2); the size-compatibility rule
stated for all k (elementary, §1); the rotated-cluster family as a general construction, with Theorem E (its k = 5 and
6 members have the order types of printed sets); and the conjecture in this form (the closest is the SMQH sentence
above). The sources contain symmetric sets only for k ≤ 7. Whether the clustered 64-point sets are order-type
equivalent to some Baek–Balko blow-up was not checked. This is not a novelty claim.

## 9. Independent checks (1–2 November 2026)

Every claim of §1–§5 was re-checked by an independent check that wrote its own code, except the rule values B(6) and
B(7); the failed searches of §6 and most of the literature notes were not re-run. Statuses after the checks:

| claim | status |
|---|---|
| size compatibility (§1) | core Lean-checked; scans exact computation |
| printed k = 5, 6 sets; k = 5 classification | exact computation; region argument written proof (not refereed) |
| point sets of §2–§5 | exact computation (two implementations; one for the 111-point set of §4) |
| Lemma 1, Proposition C | written proof (not refereed); wording fixes in `PROOFS.md` |
| Theorem E | certificate accepted by lrat-check only; generic clusters only; m = 6 lower bound now exact |
| Theorems A and B as stated | refuted; corrected versions in §4 |
| "no line-module of size 2..n−4" for the 8-fold sets | refuted (off by one); corrected version in §5 |
| rule sizes B(h) | computational evidence; their maximality is a conjecture |
| §7 | conjecture |

Two earlier errors were also corrected. The first interval certificate for SMQH Table 2 was not rigorous
(`Decimal.sqrt` ignores directed rounding); the exact computation of §2 replaces it. Two earlier texts called a
64-point set "the second" 7-fold order type; §3 lists seven.

## Reproduction

From `cloud/es7-2026-10-19/results`. On the Mac used here the default macOS SDK did not link, so the C programs were
built with `CFLAGS="-isysroot <Command Line Tools SDK directory>/MacOSX26.sdk"`; GMP may need `-I`/`-L` flags.

```sh
python3 -I PRIMEFOLD/compat/compat_check.py; python3 -I PRIMEFOLD/compat/numerology.py 1000000
lake env lean <path>/PCompatCore.lean        # inside a Lean 4.24.0 + Mathlib project; same for L0Check.lean
python3 -I PRIMEFOLD/printed/exact_check.py
python3 -I PRIMEFOLD/printed/compare_printed.py PRIMEFOLD/printed/verify_small.py \
    PRIMEFOLD/sets/k5/c4_8pts_2layers.pts PRIMEFOLD/sets/k6/m36_cup.pts    # and with sets/k6/rule_p5_16pts.pts
python3 -I PRIMEFOLD/k5/k5_exact.py; python3 -I PRIMEFOLD/k5/verify_k5.py; python3 -I PRIMEFOLD/k5/grid_check.py
sh PRIMEFOLD/check64/run_all.sh                    # 30 s; rewrites check64/check64.log
(cd PRIMEFOLD/check64/modules60 && python3 otable.py ../../sets/k8/c7_64pts_small.pts t.otv \
    && python3 run_modules.py ../../sets/k8/c7_64pts_small.pts t.otv)
bash PRIMEFOLD/check120/reproduce.sh               # minutes; rewrites the logs in check120/
sh PRIMEFOLD/check253/run_all.sh                   # 20 s
sh PRIMEFOLD/check991/run_all.sh <outdir>          # 35 s, GMP
sh PRIMEFOLD/rule/run_all.sh <outdir>              # 90 s, GMP
CADICAL=cadical LRATCHECK=lrat-check bash PRIMEFOLD/cluster/sat/run_all.sh <outdir>
python3 -I PRIMEFOLD/cluster/check/m6_cluster5.py m6.signs && PRIMEFOLD/check64/cvxenum m6.signs   # after check64
python3 -I PRIMEFOLD/cluster/thmA/zeta_cert.py PRIMEFOLD/cluster/thmA/m11_beta0_ES54.pts 11   # 2 min
```

**Changes from the session files.** Absolute paths were made relative, and names of earlier working directories were
removed from comments (not in the two Lean files, which are byte-identical to the compiled files). `compat_check.py`
and `verify_small.py` have one renamed output label each, `compare_printed.py` prints the isomorphism it finds,
`recdp.py` takes an optional largest h, `cluster/check/e2e.py` has a relative import path, and `PROOFS.md` has a
corrections header. `m6_cluster5.py` (the independent check's command for the m = 6 cluster) and the run scripts were
written or adapted for this directory. Logs of runs on 2 November: `check64/check64.log`, `check64/modules60/*.log`,
`check253/logs/run_all.log`, `check991/logs/rerun/`, `rule/logs/rerun/`, `cluster/sat/rerun.log`,
`cluster/check/m6_cluster5_exact.log`, `printed/compare_printed_*.out`. `SHA256SUMS` lists every file.

## Addendum (2 November 2026): m = 8 cluster sets

- `sets2/c8_112pts_1orbit14.pts` (SHA-256 `014aee04…`): an 8-fold set of 112 points in general position with no 9 points
  in convex position that is one orbit of rotated copies of a 14-point cluster. The single-orbit cluster bound 14 for
  m = 8 (Theorem E, generic clusters) is therefore attained. Exact computation (three sign methods, two dynamic
  programs) and an independent re-check from scratch.
- `sets2/c8_120pts_blowup2orb.pts` and `sets2/c8_120pts_blowup3orb.pts`: 120-point sets of the same kind built as
  rotated blow-ups with two and three base orbits (exact computation, independent re-check). They match, but do not
  exceed, the 15-layer record; a 16-layer (128-point) set was not found (about 46 minutes of further searches, best
  remaining weighted count of convex 9-gons 151). A failed search is not impossibility.
