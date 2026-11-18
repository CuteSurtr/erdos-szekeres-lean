# LOWERBOUND_RUN_1118: third block of the lower-bound plan (track L, 18 Nov 2026, 02:30-08:30 KST)

**Status: IN PROGRESS (skeleton written 02:50 KST; updated after each milestone; last update 04:00).**

**Headline (all CERTIFIED + PROVED soundness, computer-assisted, unrefereed; each with a filed claim; all nine claims filed by 03:48 were CONFIRMED by independent verifiers VS and VB with their own code by 03:49).**
Saturation numbers of the Erdős–Szekeres problem (DDSZ, arXiv:2312.01223: sat_g(n) = the smallest n-gon-free set in
general position to which no point can be added without an n-gon; their Thm 4 gives sat_g(n) ≤ 7/8 · 2^(n−2) for
n ≥ 7, i.e. 28 and 56):

- **sat_g(6) ≤ 14 < 16 = ram_g(6)** (a 14-point centrally symmetric set; also checked by exhaustive cell enumeration);
- **sat_g(7) ≤ 20** (four 4-fold 20-point sets; 21-, 24- and 26-point sets too);
- **sat_g(8) ≤ 31** (a 31-point set found by a saturation-directed local search from the 36-point 5-fold set; first 36).
- Saturation is a property of the realization, at k = 8 as at k = 7 (a 56-point DDSZ-type set); and saturation of every
  realization (order-type level) does not imply maximum size (sets of 26 and 28 points at k = 7, 51 at k = 8).

A bounded arXiv search (18 Nov) found no bound on sat_g after DDSZ: "not found in this search", not a priority claim.
Nothing here changes ES(7) or ES(8).

Plan being run: [LOWERBOUND_PLAN_1115PM.md](LOWERBOUND_PLAN_1115PM.md), after [LOWERBOUND_RUN_1115EV.md](LOWERBOUND_RUN_1115EV.md),
[LOWERBOUND_RUN_1116.md](LOWERBOUND_RUN_1116.md) and the literature check
[LOWERBOUND_EV_CHECK.md](../NOVELTY20261115/LOWERBOUND_EV_CHECK.md).
Work dir: `/home/jay/research/data/roadmap-20261115/pm1115/l1118/` (below `$L`). Units: `esr-agl-*`, at most 40 %
CPUQuota in total, at most 1.4 GB memory in total. Tools copied unchanged from `pm1115/ln` and `pm1115/agl` (hashes in
`$L/logs/copied_sha256.txt`; `l1enc` `60fee0ce…`, `l1check` `12a7d6f4…`, `l1enc_big` `d45f89a5…` as in
ABSAT8_INDEPENDENT §8; both self-tests pass).

| item | question | status | label |
|---|---|---|---|
| (1) k = 8 | is geometric octagon saturation an order-type invariant? | **no** (02:43): an explicit DDSZ-type 56-point set S is geometrically octagon-saturated (certified), and another realization S′ of its labelled order type plus a point p has no convex octagon (claim `lb-l18-oct56-real`) | CERTIFIED + PROVED soundness; EXACT |
| (1b) k = 7, 8 | does order-type saturation (`l1enc S k` UNSAT: every realization saturated) imply maximum size? | **no** (02:57): six symmetric non-maximum sets are order-type saturated, among them a 51-point octagon-free set, so **sat_g(8) ≤ 51** (DDSZ Thm 4 gives 56), and a 28-point heptagon-free set (claim `lb-l18-otsat-nonmax`) | CERTIFIED + PROVED soundness |
| (1c) k = 6, 7, 8 | how small can a saturated set be? | **sat_g(8) ≤ 31** (03:48; claim `lb-l18-satg8-31`), after ≤ 36 (03:16; claim `lb-l18-satg8-36`: a 36-point 5-fold octagon-free set is geometrically saturated; DDSZ: 56), **sat_g(6) ≤ 14 < 16** (03:11; claim `lb-l18-satg6-14`) and **sat_g(7) ≤ 20** (03:12; claim `lb-l18-satg7-20`, four 4-fold 20-point sets) after ≤ 21 (03:03): a 21-point heptagon-free set (5-fold, 4 orbits + centre) is geometrically 7-gon-saturated; also three 24-point sets and two 26-point sets saturated in every realization (claim `lb-l18-satg7-21`). DDSZ Thm 4: 28 | CERTIFIED + PROVED soundness |
| (2) E7-2 | joint two-point (radius-1) extension model at k = 7: soundness note, controls, cheapest targets | soundness note written; 66 symmetric-maximum bases all UNSAT (claim `lb-l18-e72-sym`, 03:20); 203 AE33 pairs running | CERTIFIED + PROVED soundness |
| (3) E7-3 | more seeds | not started | - |

## (1) k = 8: geometric octagon saturation depends on the realization (CERTIFIED + EXACT)

**Why a non-maximum set.** At 64 points the question has only one possible answer short of a counterexample: a 64-point
octagon-free set with one realization that extends would refute ES(8) = 65. All 1,592 stacking types, the 28
ABSAT8-core sets, the 7 seven-fold types and the 56 octagon-vertex deletions are certified order-type non-extendable
(every realization saturated). So the k = 8 analogue of `lb-ln-ddsz28-real` has to live below 64 points; DDSZ Thm 4
gives 7/8 · 64 = 56.

**The set S** (`$L/d56/d56_S.txt`, SHA-256 `8bc71af7…`; builder `src/build_d56.py`, own code). DDSZ Prop. 14 for n = 8:
blocks P_1..P_7 at L(i, i²), block map (x, y) ↦ L(i, i²) + (F x, y), L = 10⁹, F = 10⁴ (36-bit coordinates).

- P_1, P_7: one point; P_2: a 6-cap; P_6: a 6-cup.
- P_3 = comb(5-cap, D) (a (4,6) block, 13 points), P_4 = comb(D, Dm) ((5,5), 16 points), P_5 = comb(Dm, 5-cup) ((6,4),
  13 points). D = DDSZ Thm 11's 8-point (4,5)-cup-cap-saturated set (coordinates as in `agl/src/ddsz28.py`), Dm its
  mirror image (y ↦ −y). comb(A, B) is DDSZ Lemma 13: A left of a gap G = 50, B right of it and shifted up by H = 20,000;
  the builder asserts exactly that every A point is below every line through two B points and every B point above every
  line through two A points, and that each composite block is (i+1, 9−i)-cup-cap-free (DP).
- 1 + 6 + 13 + 16 + 13 + 6 + 1 = 56 points, distinct x, no three collinear.

**(a) Octagon-free (EXACT).** `l1check S - 0 0 8 self` (L1's DP): 0 points on a convex octagon. `convk` (ln's brute
force): largest convex subset 7, convex m-gon counts 27,720 / 249,544 / 1,174,834 / 2,700,225 / 2,373,304 for m = 3..7.

**(b) Geometrically octagon-saturated (CERTIFIED + PROVED soundness).** `src/geosat56.py` (own code, a new CEGAR):

- Start from `l1enc S 8` (1,540 variables, 278,906 clauses; CNF `04822e33…`). By ABSAT8 §3 (k-generic reading in
  LOWERBOUND_RUN_1115EV E7-1), every real p with S ∪ {p} in general position and no convex octagon through p gives a
  model X(a,b) = [orient(a,b,p) > 0].
- Realizability clauses: a clause forbids a sign pattern of orient(a_i, b_i, p) on 2 or 3 lines through pairs of S
  whose open half-planes have empty intersection. Every real p in general position satisfies them.
- Finding them: R2 at a point a forces the signs of the 55 lines through a to be those of one open sector at a, i.e.
  of the two lines bounding it. So a model's cell is the intersection of at most 112 half-planes, and by Helly's
  theorem it is empty iff some 2 or 3 of them are. Emptiness test (Motzkin): open half-planes n_i·p + c_i > 0 have
  empty intersection iff some λ ≥ 0, λ ≠ 0, has Σ λ_i n_i = 0 and Σ λ_i c_i ≤ 0; for three pairwise non-parallel
  normals λ is a multiple of (det(n₂,n₃), det(n₃,n₁), det(n₁,n₂)). All empty triples and pairs among the 112 are added
  per round; a model with a nonempty cell would be a real non-saturating point (none occurred).
- Run (unit `esr-agl-geo56`, 1.4 s): 17 rounds, **4,041 triple clauses**, then UNSAT. Final CNF `d56g_final.cnf`
  (`1923fd2a…`) = the l1enc clauses verbatim, then the added ones.
- **Certified:** `certify_cnf.sh` (heap 500 MB, peak RSS 476 MB): exactly one `s VERIFIED UNSAT`; LRAT `f373582f…`
  (54,978 bytes, kept as zstd).
- **Independent check of the added clauses** (`src/verify_trip.py`, a different method): for each clause, every cell
  of the arrangement of its 2-3 lines is sampled exactly (one rational point per sector around every vertex, step
  halved until no other line separates it from the vertex); the forbidden pattern is realized by none: 0 of 4,041.
  It also checks that the final CNF is the base CNF followed by exactly these clauses.
- **Method control on the known case:** the same CEGAR on d28_h at k = 7 (whose saturation `lb-e1-ddsz28` certified
  with tripgeo's full triple table): 10 rounds, 914 clauses, UNSAT; verify_trip 0 of 914 non-empty; cake_lpr one
  verdict line (CNF `ea526ebb…`, LRAT `60da8921…`).

**(c) Same order type (EXACT).** S′ (`d56sub_S.txt`, `6598e41f…`) is S with D in block P_3 replaced by the 8 old
points of ln's realized 4-cup/5-cap-free extension `d45ext_t3_000_real.json` (claim `lb-ln-ddsz-block`, CONFIRMED),
built by the same code with the same parameters. Own check: all 27,720 triples have the same orientation sign in S and
S′; both x-orders are the identity. `convk` gives S′ exactly S's convex m-gon counts.

**(d) S′ + p is octagon-free (EXACT).** p = (3003890000, 9000020197) is the new point of that extension, mapped with
its block (`d56sub_Sp.txt`, `a24e6190…`; x-position between labels 14 and 15, inside the D′ part of P_3). No three of
the 57 points collinear (own check); `l1check … 8 self`: 0 points on an octagon; `convk`: largest convex subset 7.
Inside the block, P_3 ∪ {p} has longest cup 3 and longest cap 5, so it is still (4,6)-cup-cap-free. Control: the real
(S′, p) satisfies all 278,906 clauses of `l1enc S 8` (`src/evalcnf1.py`, own evaluator: 0 violated), as order-type
invariance of the encoding requires.

**(e) The abstract extensions (CERTIFIED count).** `src/enum_models.py` (pysat CaDiCaL, blocking clauses on all 1,540
variables): `l1enc S 8` has **exactly 194 models**. The CNF plus the 194 blocking clauses (`d56/enum/e56_blocking.cnf`,
`36806431…`) is UNSAT: cake_lpr one `s VERIFIED UNSAT` (LRAT `7026a830…`, 2.47 MB, kept as zstd). Whether all 194 are
realized by realizations of S's order type (as for d28's 34) was not tested.

**Statement (claim `lb-l18-oct56-real`, filed 02:43 KST).** S is geometrically octagon-saturated, and S′, which has the
same labelled order type and x-order, is not: S′ ∪ {p} is in general position without a convex octagon. Geometric
octagon saturation is a property of the realization, not of the order type — at k = 8 as at k = 7, and by the same
mechanism (the D block is saturated only in its coordinates). Side fact: (a)+(b) are an explicit certified instance of
DDSZ Thm 4 at n = 8 (sat_g(8) ≤ 56); that half is DDSZ's theorem, re-checked here. Nothing about ES(8) follows.

## (1b) Order-type saturation does not imply maximum size; sat_g(8) ≤ 51 (CERTIFIED + PROVED soundness)

**Question** (open since LOWERBOUND_RUN_1115EV: "no non-maximum set with ABSAT UNSAT is known here"). Is there a
k-gon-free set with fewer than 2^(k−2) points all of whose realizations are geometrically saturated?

**Test.** `l1enc S k` + CaDiCaL on the repository's symmetric sets below 2^(k−2) points (integer inputs with the same
labelled order type: `src/conv_sym.py`, `src/c5int.py`; Gaussian (4-fold) conversion exact; Eisenstein pairs (3-, 6-fold)
read as Cartesian integers, an orientation-preserving linear image; 5-fold sets rounded from 60-digit decimals with all
orientation signs compared exactly with SYMMAX/verify5.py's Z[√5] signs, 0 mismatches).

| k | set (repository file) | n | `l1enc S k` | cake_lpr |
|---|---|---|---|---|
| 8 | `ES8SYM/sets/c5_51pts_10layers_centre.pts` | 51 | **UNSAT** | 1 verdict line (CNF `538c8785…`) |
| 8 | `ES8SYM/sets/c4_52pts_13layers.pts` | 52 | **UNSAT** | 1 (`6e01eae8…`) |
| 8 | `ES8SYM/sets/c3_55points_k8.txt` | 55 | **UNSAT** | 1 (`b7795ba3…`) |
| 8 | mirror46, c6_54 (two files), c5_56, c6_60 A/B/C/C2/D, c3_60 (two), c3_61 | 46-61 | SAT | - |
| 7 | `SYMMAX/c4_28points.txt` | 28 | **UNSAT** | 1 (`1a6f5452…`) |
| 7 | `SYMMAX/c3_31points.txt` | 31 | **UNSAT** | 1 (`0515c484…`) |
| 7 | `SYMMAX/c5_31points.txt` | 31 | **UNSAT** | 1 (`e43a342c…`) |
| 7 | c3_27, c3_30, c6_30 | 27-30 | SAT | - |
| 6 | mirror12, c3_13 (SAT); c4_16, c2_16, c5_16 (UNSAT, 16 = maximum) | | | not certified |

**Statement (claim `lb-l18-otsat-nonmax`, filed 02:57 KST).** For the six UNSAT sets, every realization of the order type
(and of its mirror image) is geometrically k-gon-saturated (ABSAT8 §3's soundness, k-generic reading). Hence:

- **sat_g(8) ≤ 51**, with DDSZ's saturation number sat_g; their Thm 4 gives 7/8 · 64 = 56 at n = 8. A bounded arXiv
  search on 18 Nov (four queries plus DDSZ's citation graph) found no later bound; this is "not found in this search",
  not a priority claim. DDSZ's final remarks call the gap between their exponential upper and linear lower bounds the
  obvious problem.
- At k = 7, c4_28 is saturated in every realization: DDSZ's size 28, with the order-type property that DDSZ's own
  28-point construction lacks (item (1) at k = 7 and `lb-ln-ddsz28-real`).
- Order-type saturation is not maximality: c5_51 is saturated in every realization, while the larger 5-fold set c5_56
  is abstractly extendable.

**Controls (all passed; `$L/logs/ctrl_otsat.jsonl`, `bin/ctrl_otsat.sh`).** C2: k-gon-free by L1's DP and ln's brute
force (largest convex 6 at k = 7, 7 at k = 8; general position). C1: 4,693-9,233 real random, far and wedge points per
set (L1's `l1check gen`): every point lies on a convex k-gon and violates an OCT clause; 0 R2/AC violations; 0
mismatches. C3: 4 deletions per set: the deleted real point satisfies every clause of `l1enc (S − w) k`, has no k-gon
through it, CaDiCaL SAT.

**Negative side results (EXACT).** The given realizations of mirror46 (k = 8) and c3_27 (k = 7) are not geometrically
saturated: geosat56's CEGAR stops at a model whose cell is nonempty, and `src/cellpoint.py` turns it into an exact
witness point (mirror46 + p: 47 points, largest convex subset 7; c3_27 + p: 28 points, largest convex subset 6;
l1check and convk). So the search for smaller saturated sets must look beyond these files (item (1c)).

## (1c) Small saturated sets: sat_g(7) ≤ 21 (CERTIFIED + PROVED soundness)

**Method** (`bin/satsearch.sh`, own driver). SYMMAX's annealers (`annealg.c` for 2-, 3-, 4-, 6-fold and mirror symmetry,
`anneal5.c` for 5-fold; unchanged copies, `a6567806…`, `7053e19b…`) find symmetric k-gon-free sets of a given size;
5-fold sets are converted to integers by `conv_sym.py` with the exact orientation check. Each set gets (1) the
order-type test `l1enc S k` + CaDiCaL and, if that is SAT, (2) the geometric test of its own coordinates: geosat56's
CEGAR (item (1)(b)). Every UNSAT is re-checked: realizability clauses by `verify_trip.py`, the final CNF by
`certify_cnf.sh` (cake_lpr), the CNF regenerated from the point file (hash equal), plus a sanity control of
22,000-34,000 real random, far and wedge points (L1's `l1check gen`: each lies on a convex k-gon by its own DP).

**Results at k = 7** (DDSZ Thm 4: sat_g(7) ≤ 28; their construction cannot go lower, since sat_c(4,5) = 8):

| set (`$L/…`) | n | symmetry | order type (`l1enc` alone) | given coordinates | certificate |
|---|---|---|---|---|---|
| `sat21/g5_m4_f1_k7_s2.txt` | **21** | 5-fold, 4 orbits + centre | SAT (extendable abstractly) | **saturated** | l1enc 9,952 + 5,193 realizability clauses UNSAT; cake_lpr 1 line (CNF `5207ce67…`, LRAT `47b9d514…`); 33,840 random points all on a 7-gon |
| `sat20/r6_g4_m5_f0_k7_s8.txt` (and `_s6`, `_s9`, `_s20`) | **20** | 4-fold, 5 orbits | SAT | **saturated** | l1enc + 2,491 (3,348; 2,898; 3,337) realizability clauses UNSAT; cake_lpr 1 line each (`6929bbcc…`, `18762131…`, `f5b8bc24…`, `fefb26ca…`); about 22,700 random points each, all on a 7-gon. **Claim `lb-l18-satg7-20`** filed 03:12 |
| `sat24/g6_m4_f0_k7_s2.txt` | 24 | 6-fold | SAT | saturated | + 10,201 clauses; 1 line (`7240f0f5…`); 23,092 points |
| `sat24/g4_m6_f0_k7_s3.txt` | 24 | 4-fold | SAT | saturated | + 6,442; 1 line (`bb761447…`); 23,100 points |
| `sat24/g4_m6_f0_k7_s4.txt` | 24 | 4-fold | SAT | saturated | + 3,190; 1 line (`0114d5fb…`); 23,094 points |
| `sat26/a5_m5_c1_k7_s1.txt`, `_s2.txt` | 26 | 5-fold, 5 orbits + centre | **UNSAT**: saturated in every realization | - | `l1enc` alone; 1 line each (`7f42493a…`, `b8a1247d…`); controls C1-C3 as in (1b) |

All are in general position with largest convex subset 6 (L1's DP and ln's brute force). The 21-point set's Z[ζ5]
coordinates are in `sat21/g5_m4_f1_k7_s2.pts`; the integer file is its rounding at scale 10³, same labelled order type
(exact check), and saturation is claimed for the integer set (it is a property of the realization). **Claim
`lb-l18-satg7-21`** filed 03:04 KST.

**Result at k = 8: sat_g(8) ≤ 36** (claim `lb-l18-satg8-36`, filed 03:17 KST; DDSZ Thm 4: 56; item (1b): 51).

| set (`$L/…`) | n | symmetry | order type | given coordinates | certificate |
|---|---|---|---|---|---|
| `sat36/g5_m7_f1_k8_s1.txt` | **36** | 5-fold, 7 orbits + centre (Z[ζ5] file `.pts`, rounded at 10³, exact orientation check) | SAT | **saturated** | `l1enc S 8` (630 variables, 52,797 clauses) + 20,543 realizability clauses UNSAT; verify_trip 0 of 20,543 realized; cake_lpr 1 line (CNF `8ea6d03b…`, LRAT `26ffdc99…`); 24,520 random points all on an octagon |

It was the second k = 8 configuration tried (anneal5, 7 orbits + centre, 15 s). Annealed 5-fold sets of 30, 31 and 35
points, 4-fold 28 and 32, 6-fold 30, 3-fold 31 and 2-fold 32 (12 sets in all) were not saturated.

**sat_g(8) ≤ 31** (claim `lb-l18-satg8-31`, filed 03:48 KST). A saturation-directed local search (`src/satlocal.py`,
HEURISTIC search only): the state is a set of orbit representatives (floats) of a G-fold rotation, the point set their
orbits rounded at scale 10⁶; the objective is the fraction of L1's `l1check gen` sample points (random, far and wedge
points; exact) with no k-gon through them; moves perturb one representative; a move is kept if the set stays in general
position and k-gon-free (exact) and the fraction does not grow. Started from the 36-point set with one orbit removed
(31 points), it reached fraction 0 at step 36; geosat56 then returned UNSAT.

| set | n | certificate |
|---|---|---|
| `sat31/sl31.txt` (centre + 6 orbits, approximately 5-fold, 20-bit coordinates; not claimed symmetric) | **31** | `l1enc S 8` (465 variables, 31,822 clauses) + 16,462 realizability clauses UNSAT; verify_trip 0 of 16,462 realized; cake_lpr 1 line (CNF `47ca0a38…`, LRAT `cc4234b4…`); 23,860 random points all on an octagon |

Further local-search attempts (negative so far; HEURISTIC; `$L/satlocal/results*.jsonl`, per-attempt logs in
`$L/satlocal/<tag>/log.jsonl`): from the 36-point set without orbit 1 (31 points) the sampled free fraction stalled at
0.003 (500 steps); one level further, the 31-point set without orbit 0 (26 points) reached 0.003 in 1,007 steps (1,500 s
cap); the 14-point k = 6 set without one antipodal pair (12 points), 7 attempts of 600 steps: best 0.002-0.026; the
6-fold 24-point k = 7 set (Cartesian copy `sat24/g6_m4_f0_k7_s2_cart.txt`, same order type) without one orbit
(18 points): best 0.027. The run continues (units `esr-agl-satlocal2`, `esr-agl-satlocal3b`: 16-point k = 7 starts from
the 20- and 21-point sets, then 31-point k = 8 starts).

**Results at k = 6: sat_g(6) ≤ 14 < 16 = ram_g(6)** (claim `lb-l18-satg6-14`, filed 03:11 KST). DDSZ's block method
gives 16 at n = 6 (sat_c(4,4) = ram_c(4,4) = 6), and their theorem is stated for n ≥ 7.

| set (`$L/…`) | n | symmetry | certificate 1 (CERTIFIED) | certificate 2 (EXACT, exhaustive) |
|---|---|---|---|---|
| `sat14/r_g2_m7_f0_k6_s13.txt` | **14** | central (7 antipodal pairs) | `l1enc S 6` (2,514 clauses) + **3** realizability clauses UNSAT; cake_lpr 1 line (CNF `8cc63745…`, LRAT `f275fe9b…`) | all 3,206 open cells of the 91-line arrangement (Euler count asserted) have a sample on a convex hexagon (`src/cellsat.py`: ln's `arrcells.py` + L1's DP) |
| `sat15/g5_m3_f0_k6_s1.txt` | 15 | 5-fold, 3 orbits | + 96 clauses; 1 line (`deb2483d…`) | 4,396 of 4,396 cells |
| `sat15/more/` (3 sets) | 15 | 5-fold | CEGAR UNSAT (not yet certified) | - |

The 14-point set: (−776, 1572), (−523, 907), (2528, 163), (−1740, −124), (−1358, 2386), (122, −149), (334, 422) and
their negatives. Negative controls of the cell check: mirror12 (50 of 1,642 cells without a hexagon through p) and a
12-point 4-fold set (136 of 1,632). Search at k = 6: 78 symmetric hexagon-free sets of 10-15 points, 5 saturated (the
14-point set and four 15-point 5-fold sets), 73 not (the CEGAR ended at a realizable model). At k = 5, 48 symmetric
pentagon-free sets of 4-7 points: none saturated.

**The 14-point set is saturated only in its coordinates (claim `lb-l18-sat14-realdep`, filed 03:43 KST).**
`l1enc S 6` has exactly **56 models** (CERTIFIED: CNF + 56 blocking clauses UNSAT, cake_lpr one line; own check that
the models satisfy the base, are distinct, and the blocking clauses are their negations), and **all 56 are realized**
(EXACT): for each, `src/realize_ext.py` finds the x-positions where the extended sign string is a signotope (5 or 8),
`realize_sig.py` (float search only) realizes it, and the integer result is checked exactly: the 14 old points have S's
labelled order type and x-order, p's 91 signs equal the model, general position, and no convex hexagon (L1's DP, ln's
brute force; 56 of 56). So at k = 6 as at k = 7 (d28, all 34 models realized) and k = 8 (d56), geometric saturation of
a small saturated set is a property of its realization.

Search statistics of the second k = 7 run (`r6_`, 03:05-03:13, 10 s runs; `satsearch/found.jsonl`): 4-fold 20 points 5 of 38 saturated; 5-fold 20 (no centre) 1 of 38; 5-fold 21 (centre) 12 of 36; **0 of 224 sets with 16-19 points** (2-fold 18: 37; 3-fold 18: 37, 19: 38; 4-fold 16: 37; 5-fold 16: 37; 6-fold 18: 38) and 0 of 110 mirror and 2-fold 20-point sets. So 20 is the smallest size found; nothing is claimed below it.

Search statistics of the first run (03:05, one 10 % unit, 8-10 s annealing runs): 5-fold 21 points: 3 of 4 found sets saturated;
4-fold 24: 3 of 6; 6-fold 24: 2 of 6; 5-fold 25: 1 of 2; 20-point sets (4-fold 5 of 5, 5-fold without centre 2 of 2,
2-fold 2 of 2), 18 (6-fold, 1), 21-22 (3-fold, mirror; 7 sets): none saturated. The search continues (units
`esr-agl-sat6` for k = 7 sizes 16-21, `esr-agl-sat8` for k = 8 sizes 42-50).

## (2) E7-2: the joint two-point (radius-1) model at k = 7

**Encoder.** `l2enc` (written by track L on 16 Nov, never recorded or reviewed; source `$L/copied/l2enc.cpp`
`171a3e7c…`). I reviewed the source line by line and rebuilt it (`g++ -O2 -std=c++17`): the binary is byte-identical to
the 16 Nov one (`af75c610…`). Usage `l2enc B.txt k out.cnf [--allow-kgon]`; it aborts if B has a convex k-gon or three
collinear points.

**Soundness note (PROVED; written for this record).** Let B = (b_0, …, b_{n−1}) be integer points in general position,
k ≥ 5, and let p, q be two new points. Variables: X(a,b) = [orient(a,b,p) > 0] (variable 1 + r(a,b), r = lexicographic
rank of a < b), Y(a,b) = [orient(a,b,q) > 0] (N2 + 1 + r(a,b), N2 = n(n−1)/2), W(a) = [orient(a,p,q) > 0]
(2·N2 + 1 + a). Claim: if B′ is any realization of the labelled order type of B, and p, q are points with B′ ∪ {p, q} in
general position and **no convex k-gon containing p or q**, then this real assignment satisfies every clause. Family by
family (an orientation of three base points is a constant of the order type; the encoder's χ is alternating, as real
orientations are):

1. **R2X, R2Y** (l1enc's rotation clauses for p, for q) and **ACX, ACY** (no new point in all three outer half-planes
   of a base triangle): ABSAT8 §3's Cramer and barycentric arguments, per new point. The R2 cone conditions are sign
   conditions on orientations with the folding signs ε fixed from B: if the folded vectors satisfy
   cross(w_i, w_{i+1}) > 0, cross(w_{i+1}, w_k) > 0, cross(w_i, w_k) > 0, then w_{i+1} = α w_i + β w_k with α, β > 0, in
   every realization; so they hold for B′ too.
2. **RAD** on {a, b, p, q}: for four points, [bpq] − [apq] + [abq] − [abp] = 0 (first coordinate of the vector identity
   [v₂v₃v₄]v₁ − [v₁v₃v₄]v₂ + [v₁v₂v₄]v₃ − [v₁v₂v₃]v₄ = 0 in homogeneous coordinates). In general position all four terms
   are nonzero, so they are not all of one sign; the clauses forbid exactly the sign patterns with all four equal.
3. **GPA, GPP, GPQ**: the 3-term Grassmann–Plücker identity [efg][ehi] − [efh][egi] + [efi][egh] = 0 for any five
   points (homogeneous coordinates), with pivot e = a ∈ B (and f, g ∈ B, h = p, i = q), e = p (f, g, h ∈ B, i = q) or
   e = q. The three products are nonzero, so (T₁, −T₂, T₃) are not all of one sign. The encoder emits, for each
   assignment of the involved literals with that property, a clause excluding it, shortened only by dropping literals
   whose every completion is also excluded; each clause is implied, so it holds for real configurations.
4. **OCTX, OCTY**: l1enc's OCT for p (resp. q) from every 4-chain (a, b, c, d) of consecutive vertices of a ccw convex
   (k−1)-gon Q of B: ¬(sees(b,c) ∧ ¬sees(a,b) ∧ ¬sees(c,d)), sees(x,y) ⟺ orient(x,y,new) < 0. Convexity of Q and its
   ccw order are order-type properties, so Q is a convex (k−1)-gon of B′. If violated, the visibility and slot lemmas
   (ABSAT8 §3) make Q ∪ {p} a convex k-gon through p — excluded by hypothesis.
5. **JK** (new): for every ccw convex (k−2)-gon Q = (Q_0, …, Q_{m−1}) of B (m = k − 2 ≥ 3), every slot i and every edge
   (v, w) of Q1 = (Q_0, …, Q_i, p, Q_{i+1}, …, Q_{m−1}) with its neighbours u (before v) and z (after w):
   ¬[sees_p(Q_i,Q_{i+1}) ∧ ¬sees_p(Q_{i−1},Q_i) ∧ ¬sees_p(Q_{i+1},Q_{i+2}) ∧ sees_q(v,w) ∧ ¬sees_q(u,v) ∧ ¬sees_q(w,z)].
   Here sees_q(x, y) is a Y literal for x, y ∈ B and a W literal when x or y is p. If violated: by the slot lemma for Q
   (m ≥ 3), p sees exactly the edge Q_iQ_{i+1}, so Q ∪ {p} is in convex position with p between Q_i and Q_{i+1}, and Q1
   in this cyclic order is a ccw convex (m+1)-gon; by the slot lemma for Q1 (m + 1 ≥ 4), Q1 ∪ {q} is a convex
   (m+2) = k-gon through p and q — excluded by hypothesis. Duplicate and tautological clauses are dropped, which does
   not affect soundness. Completeness (not needed for UNSAT claims): every convex k-gon through both p and q is
   R = Q ∪ {p, q} with Q a convex (k−2)-gon of B, p in some slot of Q and q in some slot of Q1, so some JK clause is
   violated; k-gons through only one new point violate OCTX or OCTY.
6. **Order type and mirror.** All constants (base orientations, the convex (k−1)- and (k−2)-gons with their ccw orders,
   the R2 cone signs) depend only on the labelled order type of B. A realization of the mirror order type is turned
   into one of B's by reflecting B′ ∪ {p, q}, which keeps general position and convex position.

**Conclusion.** If `l2enc B k` is UNSAT, then for every realization B′ of the labelled order type of B (or of its
mirror) and all p, q with B′ ∪ {p, q} in general position, B′ ∪ {p, q} has a convex k-gon through p or q. Since B is
k-gon-free, no (n+2)-point set in general position without a convex k-gon contains an n-point subset with B's order
type. (Note: `l1enc B k` is the R2X + ACX + OCTX part, so a one-point UNSAT already implies the two-point UNSAT.)

**Controls (exact; `bin/ctrl_e72.sh`, `bin/ctrl_e72b.sh`; `$L/e72/ctrl/controls.jsonl`).** The evaluators
`src/evalcnf2.py` (streams the CNF file) and `src/ctrl_rand.py` (numpy) are written from the note's variable semantics,
not from l2enc's code; 7-gons through p or q are found by an own brute force (convex = every 4-subset convex).

- `l2enc --selftest`: 15,982 real (p, q) configurations on 400 random bases (k = 5, 6): consistency families never
  violated; OCTX/OCTY/JK violated exactly when brute force finds a k-gon through p only / q only / both.
- C1, k = 6 known answers (ES(6) = 17): B = es16 − v (15 points; ln's two 16-point hexagon-free sets) gives 8 CNFs, all
  UNSAT with one cake_lpr verdict line; B = es16 − {u, v}: the 8 real deleted pairs satisfy every clause, CaDiCaL SAT.
- C2, k = 7 at full size: B = S − {u, v} (29-30 points) for 10 heptagon-free sets S (mirror32, sym7_32, c5_31i, c3_31,
  three pool sets, a near-full deletion, two AE33 heptagon-vertex deletions), 3 pairs each: the real pair satisfies every
  clause, CaDiCaL SAT; on the first pair of each set 40 random or perturbed real pairs (`ctrl_rand.py`). The first unit
  (`esr-agl-e72c`) was stopped cleanly by the memory guard at 02:51:47 (384 of 400 MB, the old list-based `ctrl_rand`);
  `ctrl_rand` was rewritten with numpy (135 MB) and the rest restarted as `esr-agl-e72c2`.
- C4: AE33 − {u, v} with u, v both off the heptagon (`--allow-kgon`, the base keeps the heptagon): the real pair must
  satisfy every clause. In the target run, every AE33 target's real pair must violate a k-gon clause and no consistency
  clause (it lies on AE33's heptagon).
- C3: 30 random pairs on three certified target CNFs.

**Results so far (03:20).** 74 of 269 targets done, all UNSAT, each with one cake_lpr verdict line (`e72/summary.jsonl`;
CNFs 844k-1.18M clauses; about 50 s wall per target at 15 % CPU). The 66 symmetric-maximum bases are complete:
**claim `lb-l18-e72-sym`** filed 03:20 KST (mirror32 − u and sym7_32 − u for all 32 u, c3_31, c5_31). AE33 pairs:
8 of 203 done; each real pair violates exactly one OCTY clause (the heptagon through its on-heptagon point) and nothing
else. **Controls: all passed (unit finished 03:58:43).** C1: 8 forced-UNSAT k = 6 CNFs certified (one verdict line each), 8 real
pairs satisfy every clause. C2: 30 of 30 real pairs on 10 heptagon-free sets satisfy every clause, CaDiCaL SAT;
400 random or perturbed real pairs on those bases: 128 without a 7-gon through p or q violate nothing, 272 with one
violate a k-gon clause, 0 consistency violations. C4: 10 of 10 AE33 pairs off the heptagon satisfy every clause.
C3: 60 random pairs on the certified c3_31 and m32_d0 CNFs, each with a 7-gon through p or q and a violated k-gon clause
(the third target, ae_d14_15, was not finished when C3 ran). Target-run evaluations: every AE33 real pair done so far
violates exactly one OCTY clause and nothing else (74 of 74 at 04:00).

## Claims filed (pm1115/claims/)

| claim | statement (short) | label | verdict |
|---|---|---|---|
| `lb-l18-oct56-real` | 56-point DDSZ-type S geometrically octagon-saturated; S′ with S's labelled order type plus p octagon-free | CERTIFIED + EXACT | **VS CONFIRMED 03:00** (own octagon encoding and Motzkin test explain every base and added clause; fresh cake_lpr) |
| `lb-l18-otsat-nonmax` | c5_51, c4_52, c3_55 (k = 8) and c4_28, c3_31, c5_31 (k = 7) saturated in every realization; sat_g(8) ≤ 51 | CERTIFIED | **VB CONFIRMED 03:14** (own l1enc equal as clause multisets; fresh cake_lpr; conversions exact) |
| `lb-l18-satg7-21` | 21-point set 7-gon-saturated (plus 24- and 26-point instances) | CERTIFIED | **VS CONFIRMED 03:17** (every clause justified by own exact code; fresh cake_lpr on all six) |
| `lb-l18-satg6-14` | 14-point set hexagon-saturated, two methods (note from filer: side count 73, not 66) | CERTIFIED + EXACT | **VB CONFIRMED 03:24** (own exhaustive cell enumeration 3,206/3,206 and own l1enc + Motzkin + fresh cake_lpr; also the 15-point sets) |
| `lb-l18-satg7-20` | 20-point 4-fold sets 7-gon-saturated | CERTIFIED | **VB CONFIRMED 03:27** (own exhaustive cell enumeration: 14,960 cells, all four sets; own l1enc + Motzkin + fresh cake_lpr) |
| `lb-l18-satg8-36` | 36-point 5-fold set octagon-saturated | CERTIFIED | **VS CONFIRMED 03:26** (own octagon encoding + Motzkin explain all 52,797 base and 20,543 added clauses; fresh cake_lpr) |
| `lb-l18-sat14-realdep` | the 14-point set's order type has exactly 56 abstract extensions, all realized | CERTIFIED + EXACT | **VS CONFIRMED 03:44** (own hexagon encoding; own enumeration finds the same 56 models; fresh cake_lpr; 56/56 files checked) |
| `lb-l18-satg8-31` | 31-point set octagon-saturated (local search) | CERTIFIED | **VS CONFIRMED 03:49** (own octagon encoding + Motzkin explain all clauses; fresh cake_lpr) |
| `lb-l18-e72-sym` | radius 1 (two new points) around mirror32, sym7_32, c3_31, c5_31: 66 CNFs UNSAT | CERTIFIED + PROVED soundness | **VB CONFIRMED 03:45** (fresh cake_lpr at heap 1000 MB, 66/66; all 70,967,624 clauses justified by VB's own generated families and the RAD/GP identities; soundness note reviewed). VS had released it at 03:27 (heap above 300 MB needed) |

## What remains

- **Verification** of all six claims (own code; the cheapest independent route for the saturation claims is an own
  encoder of R2 + AC + OCT, an own emptiness test of the added patterns, and cake_lpr on the kept LRATs; for the
  14- and 15-point sets an exhaustive cell check is already done here with ln's and L1's code).
- **Smaller saturated sets**: k = 8 below 36 (search running), k = 7 below 20 (0 of 224 symmetric sets of 16-19
  points), k = 6 below 14 (0 of about 36 per 12-13-point configuration). Lower bounds on sat_g beyond n − 1: none here.
- **Literature**: a fuller check than the bounded arXiv search (citers of DDSZ in Semantic Scholar were empty; the
  journal version Eur. J. Combin. 131 (2026) 104236 was not read).
- **The 194 abstract extensions of d56** (item (1)(e)): realizability not tested.
- **E7-2** (item (2)): see its section.

## Resume

```
L=/home/jay/research/data/roadmap-20261115/pm1115/l1118; cd $L
./bin/l1enc --selftest && ./bin/l1check --selftest && ./bin/l2enc_l18 --selftest
# geometric saturation of a set S at k (CEGAR, then certify, then independent clause check):
python -B src/geosat56.py S.txt S.cnf OUT      # S.cnf = bin/l1enc S.txt k S.cnf
bash /home/jay/research/lean/erdos-szekeres-lean/.claude/skills/es-research/scripts/certify_cnf.sh OUT_final.cnf cert 400 --keep
python -B src/verify_trip.py S.txt S.cnf OUT_added.txt OUT_final.cnf
python3 src/cellsat.py S.txt k S.cnf cells.txt   # exhaustive cell check (small sets only)
# saturated-set search (CONFIGS lines 'G m F K box'; G = 2,3,4,6,M (annealg) or 5 (anneal5)):
systemd-run --user --unit=esr-agl-satX -p CPUQuota=10% -p MemoryMax=500M -p MemorySwapMax=0 -p RuntimeMaxSec=7200 \
  --nice=10 --working-directory=$L/satsearch $L/bin/satsearch.sh CONFIGS.txt $(date -d '+2 hours' +%s) SECONDS TAG_ 1
# E7-2 targets (skips names already in e72/summary.jsonl) and controls:
systemd-run --user --unit=esr-agl-e72t ... --working-directory=$L/e72 $L/bin/run_e72.sh targets.txt
systemd-run --user --unit=esr-agl-e72c2 ... --working-directory=$L/e72/ctrl $L/bin/ctrl_e72b.sh
```
