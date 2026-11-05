# ES8SYM: symmetric point sets without a convex octagon (k = 8)

Local runs on an Apple M5 Pro, 1 November 2026 (UTC).

**Statement.** For a symmetry type, N(type) is the largest number of points in general position that have this
symmetry and no 8 points in convex position. If ES(8) = 65, every N(type) is at most 64. The table in §1 gives what is
known. All point sets are in `sets/`.

**Status.**
- Mirror: **N = 46 exactly.** The upper bound is a corollary of Baek's theorem N(8, 4, 8) = 22 (written proof
  (refereed), Eur. J. Combin. 2025) and the elementary mirror lemma. The whole bound is Lean-checked in the repository
  (`SYMLEAN/mirror`, `MirrorOdd.mirror_eight_line`, from its formalization of Baek's theorem; not re-run here). Two
  separate SAT encodings give two independent certificates, each accepted by both checkers. 46 is attained (exact
  computation).
- Rotation of order >= 8: only the centre (Lean-checked).
- Every other entry is a lower bound by exact computation; the half-turn bound 64 also follows from published results
  (§5). Upper bounds added on 3 November (certificate, both checkers): 7-fold at most 64, hence exactly 64 (`C7UPPER`),
  and 6-fold at most 60 (`C6UPPER`). For the other rotation types the only upper bounds come from ES(8) <= 311. The
  half-turn value equals 64 if ES(8) = 65; that it equals 64 is a conjecture.
- One lemma of the first draft (rotation chains) was false; it is corrected here. Seven other tempting statements
  are refuted with explicit counterexamples (§7).

## 1. The table

| symmetry | possible sizes | largest set here | N(type) | status |
|---|---|---|---|---|
| half-turn (2-fold) | 2m (no centre) | 64: `c2_64points_k8.txt`, `c2_64points_k8_bb.txt` | >= 64; = 64 if ES(8) = 65 | exact computation; implied by published results (§5) |
| 3-fold | 3m, 3m + 1 | 61 with centre: `sets4/c3_61pts_centre.txt`, `sets4/c3_61pts_blowup.txt` (3 November); 60 without centre: `sets2/c3_60pts_nocentre.txt`, `sets2/c3_60pts_nocentre_b.txt` (2 November); earlier 55 with centre: `c3_55points_k8.txt` | >= 61 | exact computation |
| 4-fold | 4m | 52: `c4_52pts_13layers.pts` | >= 52 | exact computation |
| 5-fold | 5m, 5m + 1 | 56 with centre: `sets3/c5_56pts_11layers_centre.pts` (2–3 November); earlier 51 with centre: `c5_51pts_10layers_centre.pts` | >= 56 | exact computation |
| 6-fold | 6m | **60** (5 November): `../SIX60/sets/c6_60pts_{A,B,C,C2,D}.pts` (five order types); earlier 54: `c6_54pts_9layers.pts`, `sets3/c6_54pts_1orbit.pts` | **60** | lower bound exact computation (`SIX60`, three implementations); upper bound 60 certificate accepted by cake_lpr (`C6UPPER`, 3 November; 6 of 64 cube verdicts hash-bound so far, `C6UPPER` §5) |
| 7-fold | 7m, 7m + 1 | 64 with centre: five order types here (§6), seven in all with the two of `PRIMEFOLD` §3 | **64** | lower bound exact computation; upper bound certificate accepted by cake_lpr (`C7UPPER`, 2–3 November) |
| order >= 8 | 0 or 1 | the centre alone | 1 | Lean-checked |
| mirror | 2m + b, b <= 2 on the axis | 46: `mirror_46points_k8.txt`, `mirror46_A_S.txt` | **46** | upper bound Lean-checked (`SYMLEAN/mirror`) and a corollary of Baek's theorem (refereed); certificates accepted by both checkers (§4); lower bound exact computation |

*Updated 4 November 2026.* The 3-, 5-, 6- and 7-fold rows now agree with the addenda at the end of this file and with
`WRITEUP/note/symmetric_extremal.tex`, Table `tab:k8` (3-fold 61, 4-fold 52, 5-fold 56, 6-fold 54, 7-fold exactly 64).
Two upper bounds were added after 1 November:
- 6-fold, `C6UPPER`: every 6-fold symmetric set of at least 61 points in general position contains a convex octagon.
  Sizes are multiples of 6, so the 6-fold maximum is 54 or 60.
- 7-fold, `C7UPPER`: every 7-fold symmetric set of at least 65 points in general position contains a convex octagon,
  so the 7-fold maximum is exactly 64.

Both are certificates (both checkers): for each of two separately implemented encoders, every LRAT proof is accepted by
lrat-check and cake_lpr, on top of a written soundness proof of the encoding. The reduction to the certified
statements is Lean-checked (`LAYERLEAN`, 4 November).

- **Upper bounds for rotations.** For the half-turn, 3-, 4- and 5-fold types, the project's ES(8) <= 311 (Lean-checked;
  repository root `experiments/omission-final311-2026-10-14/`, not re-run here) gives N <= 310. The refereed ES(8) <= 408
  (Mojarrad–Vlachos, Discrete Comput. Geom. 56 (2016)) gives 407.
- **What ES(8) = 65 would need.** A symmetric counterexample needs at least 66 points (half-turn), 66 without centre
  (3-fold, 22 orbits), 68 (4-fold), 65 (5-fold), 66 (6-fold; excluded by `C6UPPER`) or 70 (7-fold; excluded by `C7UPPER`);
  §3. The mirror case is settled: 46 < 65.
- Without centre: 63 points for 7-fold (`c7_63pts_9layers.pts`); 60 for 3-fold (`sets2/c3_60pts_nocentre.txt`,
  `sets2/c3_60pts_nocentre_b.txt`; earlier 54, the 55-point set minus its centre).

## 2. The point sets and their checks

**Formats.** `.pts`: one point per line, integers w_0..w_{m-1} for the point Σ w_j ζ^j, ζ = e^{2πi/m}; the rotation is
a cyclic shift, so the symmetry is exact. `c3_55points_k8.txt`: a line `a b` is a + bω, ω = e^{2πi/3}; the map to the
plane is linear with positive determinant, so orientations are those of the integer pairs. Other `.txt`: integer x y.

| file | symmetry | n | SHA-256 | convex 4-sets | convex 7-sets |
|---|---|---|---|---|---|
| `c2_64points_k8.txt` | half-turn | 64 | `25576cf2…` | 345,986 | 1,032,956 |
| `c2_64points_k8_bb.txt` | half-turn | 64 | `9880dc42…` | 366,356 | 841,636 |
| `c3_55points_k8.txt` | 3-fold | 55 | `fdfad364…` | 191,739 | 244,887 |
| `c4_52pts_13layers.pts` | 4-fold | 52 | `dc4cf913…` | 141,809 | 45,220 |
| `c5_51pts_10layers_centre.pts` | 5-fold | 51 | `6d7aae98…` | 128,980 | 88,920 |
| `c6_54pts_9layers.pts` | 6-fold | 54 | `235472b5…` | 188,055 | 70,134 |
| `c7_63pts_9layers.pts` | 7-fold | 63 | `811b47a6…` | 382,137 | 4,001,636 |
| `c7_64pts_small.pts` (and four more, §6) | 7-fold | 64 | `ebe028f6…` | 416,052 | 4,688,763 |
| `mirror_46points_k8.txt` | mirror x = 0 | 46 | `bf3b8e95…` | 106,853 | 427,054 |
| `mirror46_A_S.txt` | mirror y = 0 | 46 | `ac4a3e22…` | 106,131 | 416,878 |

Every set has 0 collinear triples, 0 convex 8-subsets and largest convex subset 7. `tools/run_all.sh` (about one
minute; log `logs/run_all.log`) checks each set with at least two separate exact methods:
- `.pts` sets: `layer_order.py` puts the rows in layer order; `verify_cfg.py --pts` checks distinctness, invariance,
  nested orbit layers and every orientation, with exact algebraic signs and with rigorous interval arithmetic, which
  must agree; `cvx2.c` counts convex k-subsets with two dynamic programs anchored differently; `cvxcheck.c` counts
  them again by depth-first search with the 4-point criterion; `crosscheck_decimal.py` recomputes every sign with
  160-digit decimals.
- Integer sets: `verify_set.py` (big-integer dynamic program) and `enum_convex.c` (depth-first listing of every convex
  polygon with its own `__int128` orientations).

All counts agree across methods and with the counts recorded when the sets were found. Before this rerun, every set
had been checked by at least two exact implementations; except for `mirror46_A_S.txt` and `c2_64points_k8_bb.txt`, one
of them was written separately by a review.

## 3. Rotations (orders m >= 4: `proofs/layers.md`; threefold: below)

- **Layers.** By the layer lemma (`SYM5/README.md` §2; K = 8 <= 2m), S \ {O} is t nested regular m-gons, and the
  centre O can be in S only for odd m.
- **Sizes (Lemma 2).** For m >= 8, S ⊆ {O}. For m = 4, 5, 6, 7, at least 65 points need t >= 17, 13, 11, 10 layers.
  Written proof (not refereed); the m >= 8 part and the arithmetic are Lean-checked (`lean/C6check.lean`).
- **Polar form (Lemma 1).** With u_i = 1/r_i, each orientation of nested regular m-gons is the sign of a linear form in
  the u_i whose coefficients depend only on the phases. Lean-checked (`lean/PolarOrient.lean`).
- **Zones (Lemma 4, m = 7).** Every vertex of an outer heptagon lies beyond at least two edge-lines of every inner
  one, so r_j / r_i < cos(|w| + π/7)/cos(π/7), w being the angular offset to the nearest inner vertex (0.692... when
  the vertex faces an inner edge midpoint); no two points in the double zone of an inner vertex form a convex chain
  with its two neighbours. Written proof (not refereed).
- **Rotation chains (Lemma 3, corrected).** Let d >= 2 divide m, Q be the rotation by 2π/d and a a vertex of a layer
  L. If c_1, ..., c_j are points of S in the part of conv(L) beyond the chord [a, Qa] and a, c_1, ..., c_j, Qa are in
  convex position, then d(j + 1) <= 7: j <= 2 for d = 2, j <= 1 for d = 3. Written proof (not refereed). The first
  version assumed only left turns at the c_l and is refuted (§7).
- **Layer counts.** Reached: 13, 10 (+ centre), 9, 9 (+ centre) layers for m = 4, 5, 6, 7. Needed for 65 points:
  17, 13, 11, 10. Upper bounds from ES(8) <= 311: 77, 62, 51, 44 (Lemma 5).
- **Searches** for one more layer (m = 4, 5, 6, 7) and for threefold sets beyond 55 found nothing in runs of 5 to 10
  minutes (one to three per case). Calibration on k = 7 showed such failures say little. Computational evidence only.
- **Threefold** (written proof (not refereed)). Orbits have 3 points except the centre, so sizes are 3m or 3m + 1;
  64 = 3·21 + 1 is a possible size (unlike 32 for k = 7). The centre is the centroid of every orbit, so it is never a
  hull vertex; the hull vertices form whole orbits, and three orbits would be 9 points in convex position, so every
  convex layer is a triangle, a hexagon or the centre. Since 3·21 + 1 < 65, a threefold counterexample to ES(8) = 65
  exists iff some 22-orbit threefold set without centre is octagon-free.
- **Shape.** `c7_64pts_small.pts` is one outer heptagon and a tight cluster of 8 layers with slowly drifting phase: in
  each of the 7 directions a "needle" of 8 points. The 6-fold set has the same shape; the 5-fold set has two clusters
  of 5 layers at very different scales, plus the centre.

## 4. Mirror symmetry: N = 46 (`proofs/mirror.md`)

**Reduction.** Put the axis on the x-axis and let R be the points above it. R has distinct x-coordinates, and by the
mirror lemma of `SYMMAX/README.md` (a cap of R together with its mirror image is in convex position) it has no 4-cap.
At most 2 points lie on the axis. So |S| <= 2r + 2, where r is the largest size of a set with distinct x-coordinates,
no 4-cap and no 8 points in convex position.

**r = 22 is known.** J. Baek, *On the Erdős–Tuza–Valtr conjecture*, Eur. J. Combin. 124 (2025) 104085
(arXiv:2206.04260), proves that C(n − 1, 2) + 2 points in general position with distinct x-coordinates contain a
4-cap or n points in convex position: the case a = 4 of the Erdős–Tuza–Valtr conjecture, N(n, 4, n) = C(n − 1, 2) + 1
in his notation, with the matching Erdős–Tuza–Valtr construction. n = 8 gives r = 22. Earlier, Balko and Valtr
(Electron. Notes Discrete Math. 49 (2015)) reported N(4, 8, 8) = 22 (their notation) from a SAT computation in the
pseudolinear model. So **|S| <= 46 is a corollary of Baek's theorem**; it is attained by the two sets in `sets/`. (The
cups–caps bound gives only 58, as recorded in `SYMMAX/README.md`.)

**Lean.** Baek formalised his theorem in Lean 4, and the repository has a port (repository root
`docs/THIRD_PARTY.md`; geometric n = 8 case `ErdosSzekeres.Omission.BaekGeometry.geometric_capacity22`).
`SYMLEAN/mirror` derives the whole bound from it: `MirrorOdd.mirror_eight_line` states that a finite set in general
position, symmetric in a line, with no 8 points in convex position, has at most 46 points (standard axioms only;
compiled and reviewed there, not re-run here).

**Two further certificates for r <= 22** (no 23-point set), independent of Baek's proof and of each other: encoding A
was written without access to encoding B. Each has a written soundness proof (not refereed); a review re-derived the
reduction and encoding B's proof. Both CNFs regenerate byte for byte.

| | encoding A, `mirror/encode.py` | encoding B, `mirror/enc_rmax.py` |
|---|---|---|
| CNF | `p cnf 8521 124939`, SHA-256 `d7088e45…` | `p cnf 12102 144991`, SHA-256 `47f4cc18…` |
| CaDiCaL 3.0.1 `--lrat` | UNSAT, 790 s | UNSAT, 768 s |
| LRAT proof | 1,848,737,159 bytes, `c81ea660…` | 1,865,183,930 bytes, `46f99989…` |
| lrat-check | `c VERIFIED` (19.6 s) | `c VERIFIED` (21.0 s) |
| cake_lpr (heap 3,000 MB) | `s VERIFIED UNSAT` (127 s) | `s VERIFIED UNSAT` (99 s) |

- The proofs are in the local archive `es8-mirror46-2026-11-01` (outside Git); hashes and logs are in `mirror/`. The
  cake_lpr outputs record verdict, time and memory but not file names; the input hashes are in `mirror/hashes.txt`.
- Controls: n = 22 is satisfiable in both encodings, and the real 22-point halves satisfy them; one flipped literal
  makes lrat-check reject encoding B's proof. A review also rebuilt encoding B's clause multiset from the mathematical
  description and accepted its proof with a separately written RUP-only checker.

## 5. Half-turn symmetry: N >= 64 (`proofs/central.md`)

- `c2_64points_k8.txt` places clusters on the cubic y = x³, with a centrally symmetric middle cluster much narrower
  than the others. It is the first variant named in `SYMEVEN/README.md` §2 (base positions ±2^(j−1)), checked here
  directly; `SYMEVEN/` proves a construction of this kind for every even k, and `SYM2` is the odd-k version. With the
  middle cluster scaled down by a factor 3 instead of 100 relative to the others, the same construction fails:
  `sets/control_wide_middle_k8.txt` has 179,421 convex octagons.
- **The bound 64 also follows from published results**, though no source inspected states it: Baek–Balko's blow-up
  lemma (SoCG 2025, Lemma 14) applied, with a half-turn-symmetric labelling, to the fourfold 16-point hexagon-free set
  of Subercaseaux, Mackey, Qian and Heule (SMQH, arXiv:2506.00224, App. C, Table 1) or to that of Mackey's thesis
  (CMU-CS-25-108, Fig. 3.28). `c2_64points_k8_bb.txt` is this blow-up of the SMQH set, checked here exactly. The SoCG
  version omits the proof of Lemma 14. The two 64-point sets are different order types.
- **No elementary upper bound.** Sizes are even and a 64-point set exists, so a bound below 66 is exactly the central
  case of ES(8) = 65 and must be tight. The mirror argument does not transfer: the projective map that turns the
  half-turn into a reflection keeps convex position only inside one half (Proposition 1); an outward chain with its
  antipodes is convex iff two closing turns are left turns (Proposition 2). Positive partial results: a set with a
  "deep" half has at most 56 points (Lemma 3; `sets/deep42.txt` is a 42-point example); chains anchored at hull
  vertices always close (Proposition 4). All written proofs (not refereed).

## 6. The 7-fold sets: five order types and their structure

| file | origin | convex 4-sets | convex 7-sets | halving lines | nontrivial line-modules |
|---|---|---|---|---|---|
| `c7_64pts_small.pts` | annealing in (log r, phase), exact rounding | 416,052 | 4,688,763 | 49 | 14, sizes 61, 62 |
| `c7_64pts_9layers_centre.pts` | same float configuration, other scale | 416,220 | 4,691,381 | 42 | 14, sizes 61, 62 |
| `c7_64pts_9layers_centre_own.pts` | separate annealing run | 392,553 | 3,252,475 | 49 | 22, sizes 57, 60, 61, 62 |
| `rule_p7_64pts.pts` | explicit rule: 7 clusters of 9 points + centre | 487,711 | 30,031,745 | 35 | 98, incl. seven of size 9 |
| `p7_compound_64.pts` | one orbit of two-level 9-point clusters + centre | 470,764 | 18,396,499 | 35 | 98, incl. seven of size 9 |

All five (exact computation, `logs/run_all.log` §1 and §5):
- have exactly the 7 rotations as orientation-preserving automorphisms and no orientation-reversing one;
- are pairwise different order types (the 4-set counts do not change under relabelling or reflection). `PRIMEFOLD/`
  §3 lists two more (392,966 and 462,581 convex 4-sets; seven in all), not included here. The first two files come
  from one float configuration rounded at scales 700 and 5.4·10^11; rounding flips 42 labelled triples;
- are not equivalent to the classical Erdős–Szekeres 64-point set (`structure/es_64points.txt`: 422,186 convex
  4-sets, 42 halving lines). That set has no nontrivial automorphism, so no set with a rotation or reflection symmetry
  is order-type equivalent to it. Nor are they equivalent to `c2_64points_k8.txt` (345,986).

**No cluster structure in the first three** (`proofs/structure.md`): clusters of Baek–Balko (X, Y)-blow-ups and of
generic tiny-cluster blow-ups are line-modules, an order-type invariant. The first two sets have no line-module with 2
to 60 points, the third none with 2 to 56. So they are not equivalent to any such blow-up with a cluster of that size,
in particular not to the classical construction (modules of 6, 15, 20 points), to Valtr's construction in the form of
Baek–Balko §6.1, or to the sets of Baek–Balko Theorem 19. For their given coordinates, the first two are not
(X, Y)-blow-ups of any base with 2 to 63 points (no hull vertex is deep; this part depends on the coordinates). Exact
computation and written proof (not refereed). The last two sets do consist of 7 tiny 9-point clusters around a
heptagon plus the centre; their constructions belong to the (k − 1)-fold study in `PRIMEFOLD/`.

## 7. Refuted statements (counterexamples checked exactly, `logs/run_all.log` §2–§3)

1. *Rotation-chain lemma as first written* (left turns at the c_l suffice): in `c6_54pts_9layers.pts`, rows 1, 7, 8,
   12, 4 (a, c_1, c_2, c_3, Qa) satisfy that hypothesis with j = 3, so d(j + 1) = 8; likewise rows 1, 2, 9, 7, 3 of
   `c4_52pts_13layers.pts` (`tools/rotation_chain_cex.py`). A review found that the closed polygon winds twice.
2. *Central chain lemma* (an outward chain plus its antipodes is convex): p = (10, 1), (0, 10), (−1, 3) is outward but
   orient(p_2, p_3, −p_1) < 0. In `c2_64points_k8.txt` each of the 32 halves has 3,644 to 16,682 outward 4-chains and
   none closes.
3. *The mirror bound 58 transfers to centrally symmetric sets*: the 64-point sets.
4. *The projective map ψ keeps octagon-freeness*: ψ(`c2_64points_k8.txt`) has 25,739,849 convex octagons, all crossing
   the axis, and a convex 14-gon.
5. *The cubic construction works for even k without a much narrower middle cluster*: the control (middle cluster
   scaled down by 3 instead of 100) has 179,421 convex octagons.
6. *Rotations of order at least 3 fall short of 2^{k−2} = 64, as they do for k = 7* (at most 31 < 32, `SYMMAX`):
   the 7-fold 64-point sets.
7. *Each needle is pentagon-free*: the 8-point needle of `c7_64pts_small.pts` (rows 7, 15, 23, 31, 36, 44, 49, 60,
   counted from 0) has 12 convex pentagons and no convex hexagon (`tools/subset_convex.py`).
8. *The mirror bound 58 is attained*: the maximum is 46.

## 8. Literature (1 November 2026)

**Antecedents.** The mirror bound 46 is Baek's theorem plus the mirror lemma (§4); Balko and Valtr reported r = 22 by
SAT in the pseudolinear model (2015). The half-turn bound 64 follows from Baek–Balko Lemma 14 and the SMQH or Mackey
16-point sets (§5). The 7-fold sets have a k = 6 analogue in print, the 5-fold 16-point hexagon-free set with centre
of SMQH (App. C, Table 2; also Mackey's thesis, Fig. 3.33); SMQH write "we suspect that there are symmetric
constructions for all k≥7" (§7), naming no order and no construction. The layer lemma is `SYM5` (SMQH §3.2 uses its
case of 16 points with 4-fold symmetry); the deep-halves bound uses the Erdős–Szekeres cups–caps theorem (1935); the
classical 64-point set is the Erdős–Szekeres construction (1960/61); Valtr's construction is described by Baek and
Balko (§4 there, from a private communication).

For the 7-fold 64-point sets, the 3-, 4-, 5- and 6-fold lower bounds, the corrected rotation-chain and zone lemmas,
the statements of §5 other than the bound 64, the statements of §6, and the value 46 as a statement about
mirror-symmetric sets, **no matching prior result was found in the sources inspected**:
- SMQH, arXiv:2506.00224v1 (full text: rotations only, k <= 7); E. Mackey, CMU-CS-25-108 (M.S. thesis, 2025); Baek–Balko, SoCG
  2025 (LIPIcs 332, 13: no occurrence of "symmetr"); Baek, arXiv:2206.04260v2; Balko–Valtr, ENDM 2015.
- Georgiev–Gómez-Serrano–Tao–Wagner, arXiv:2511.02864v3, item 38: 64-point octagon-free sets with no symmetry stated;
  its published 65-point set is far from symmetric.
- Koshelev–Koshka, arXiv:2604.20120 §9.1.2: axially symmetric sets of at least 18 points contain an empty convex
  hexagon (a different property, in a signotope model).
- Krapivin–Przybocki–Heule, arXiv:2607.02958; B. C. Dumitru, arXiv:2512.24061; Morris–Soltan, Bull. AMS 37 (2000);
  Szekeres–Peters 2006; `LIT/RELATED.md`; searches of arXiv, OpenAlex, Semantic Scholar, zbMATH, OEIS, MathOverflow and
  the web.
- Not inspected: the journal versions of Baek (2025), Baek–Balko (JCTA 2026) and Balko–Valtr (Eur. J. Combin. 66
  (2017)), the SMQH CICM chapter, Erdős–Tuza–Valtr 1996 (relayed through Baek and Balko–Valtr), paywalled databases.

This is not a novelty claim.

## 9. Not claimed

No upper bound for the half-turn, 3-, 4- or 5-fold types beyond what ES(8) <= 311 gives (the 6- and 7-fold bounds are
in `C6UPPER` and `C7UPPER`); no exact value except mirror, 7-fold and order >= 8; no optimality of the 3-, 4-, 5- or
6-fold sets. General even k (`SYMEVEN/`), the (k − 1)-fold family for other k
(`PRIMEFOLD/`) and mirror sets for other k (`MIRRORETV/`) are treated separately. The Lean proof of the mirror bound is
in `SYMLEAN/mirror`, not here. The two Lean files here were compiled with the repository's Lean 4.24.0 and Mathlib
(`lean/*.out`); the copies differ from the compiled files only in four comment lines (SHA-256 of the compiled files
`8c090168…`, `4d42e2fb…`).

## Reproduction

From `cloud/es7-2026-10-19/results`:

```sh
sh ES8SYM/tools/run_all.sh ES8SYM OUTDIR          # all checks of §2-§7; Python 3 and a C compiler
(cd ../../.. && lake env lean cloud/es7-2026-10-19/results/ES8SYM/lean/C6check.lean)
(cd ../../.. && lake env lean cloud/es7-2026-10-19/results/ES8SYM/lean/PolarOrient.lean)
(cd ../../.. && lake env lean --threads=1 cloud/es7-2026-10-19/results/SYMLEAN/mirror/ReductionThreeClasses.lean)
lrat-check OUTDIR/es_n23_K8.cnf es_n23_K8.lrat     # proofs from the archive, decompressed
cake_lpr --CML_HEAP_SIZE=3000 OUTDIR/es_n23_K8.cnf es_n23_K8.lrat
lrat-check OUTDIR/r23.cnf r23.lrat; cake_lpr --CML_HEAP_SIZE=3000 OUTDIR/r23.cnf r23.lrat
```

`run_all.sh` writes both CNFs to OUTDIR. To solve again: `cadical --lrat --binary=false OUTDIR/r23.cnf r23.lrat`
(about 13 minutes each). On some macOS installs the C compiler needs `CFLAGS="-O2 -isysroot <SDK path>"` (see the
header of `run_all.sh`).

## Addendum (2 November 2026): threefold 60 points

Two threefold symmetric sets of 60 points (20 orbits, no centre) in general position with no 8 points in convex
position, of different order types (`sets2/c3_60pts_nocentre.txt`, SHA-256 `2673c45c…`; `sets2/c3_60pts_nocentre_b.txt`,
`0fb9f5a5…`). Integer coordinates in the lattice form of this directory: the order-3 map (a, b) -> (-b, a - b), which is
a rotation after a linear change of coordinates with positive determinant. Exact computation: integer symmetry and
general position, largest convex subset 7 by the big-integer O(n^4) dynamic program and by an independent __int128
enumeration of all convex polygons (logs in `sets2/`), and an independent re-check from scratch with two further
exact algorithms. So the threefold octagon-free maximum is at least 60 (previously 55); 64 = 3·21 + 1 remains open.

## Addendum (2–3 November 2026): fivefold 56 points and single-orbit bounds

- `sets3/c5_56pts_11layers_centre.pts` (SHA-256 `4cdd24bb…`): a fivefold set of 56 points (11 nested regular pentagons
  plus the centre) in general position with no 8 points in convex position, built as a rotated blow-up with two base
  orbits. Exact computation in Z[zeta_5] (two algorithms) and an independent re-check from scratch. The fivefold
  octagon-free maximum is therefore at least 56 (previously 51); 61 = 5·12 + 1 is the largest size allowed if
  ES(8) = 65.
- Single-orbit limits (computer-assisted and written proofs, `sets3/single_orbit_bounds/`): one orbit of generic tiny
  clusters gives at most 54 points for sixfold (cluster size <= 9, SAT relaxation with an LRAT proof checked by
  lrat-check) and at most 51 for fivefold (cluster size <= 10, a written proof from the cups–caps theorem, also checked
  by the same encoder). The sixfold bound is attained (`sets3/c6_54pts_1orbit.pts`, a second order type of 54 points).
- Threefold: eight more 60-point octagon-free sets of new order types (`sets3/threefold60/base60_cost3_minus*.txt`),
  obtained by deleting one orbit from an exact 63-point set with exactly three convex octagons
  (`sets3/threefold60/control_cost3_63pts.txt`). For these eight sets, no infinitesimally small new orbit can be added
  without a convex octagon (exact computation of the blocking arcs plus a short written argument). A threefold 64-point
  octagon-free set would contain a 63-point one (delete the centre). The threefold maximum stays at least 60.

## Addendum (3 November 2026): 7-fold exact value, threefold 61

- The 7-fold value is now exact: every 7-fold symmetric set of at least 65 points in general position contains a convex
  octagon (`C7UPPER`, certified by two encoders and both checkers), so the 7-fold maximum is exactly 64.
- Threefold: two sets of 61 points (20 orbits plus the centre) in general position with no convex octagon, of different
  order types (`sets4/c3_61pts_centre.txt` `006a0cae…`, `sets4/c3_61pts_blowup.txt` `a61fcbd9…`; exact computation by
  two algorithms in the logs and an independent re-check from scratch). Near misses: an exact 64-point threefold set and
  its 63-point subset without the centre, each with exactly 3 convex octagons (`sets4/c3_6[34]pts_3octagons*.txt`). The
  threefold maximum is therefore at least 61.
