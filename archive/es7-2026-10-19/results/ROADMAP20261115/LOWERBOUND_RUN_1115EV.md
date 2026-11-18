# LOWERBOUND_RUN_1115EV: first block of the lower-bound plan (track E1, 15 Nov 2026 evening, 19:00-22:35 KST)

**Status: DONE (final 21:50 KST).** All units of this track stopped by 21:49:52 KST (0 active `esr-agl-*` units at 21:50).
No bound on ES(7) or ES(8) changes, and no counterexample was found. Every target CNF of E8-1 and E7-1 was UNSAT; the
only SAT answer is the calibration CNF of the DDSZ-type 28-point set (item E7-1.5), as the calibration intended to test.
All five claims filed by this track were CONFIRMED by independent verifiers (VS, VB) with their own code.
Literature (16 Nov): [LOWERBOUND_EV_CHECK.md](../NOVELTY20261115/LOWERBOUND_EV_CHECK.md).
- E8-1.3 and E8-1.2: not found in this search.
- E7-1: related; the same check at k = 7 is public on fewer sets.
- E7-1.5: its saturation half is DDSZ Thm 4.

Plan being run: [LOWERBOUND_PLAN_1115PM.md](LOWERBOUND_PLAN_1115PM.md), first block (E8-1, E7-1, E8-2, E7-3).
Encoder: L1's `l1enc` and `l1check`, copied unchanged. The SHA-256 of `l1enc.cpp` (`41037548…`), `l1check.cpp`
(`0f5a03e9…`), binary `l1enc` (`60fee0ce…`) and binary `l1check` (`12a7d6f4…`) equal ABSAT8_INDEPENDENT §8, and both
self-tests pass. Certifier: the house `certify_cnf.sh` (CaDiCaL 2.1.3 LRAT, then cake_lpr; a verdict counts only with
exactly one line `s VERIFIED UNSAT`, grepped per file). Work dir: `/home/jay/research/data/roadmap-20261115/pm1115/agl/`
(below `$AGL`). Units: `esr-agl-*`, at most 100 % CPUQuota in total.

| item | target | status | label |
|---|---|---|---|
| E8-1.1 | SMQH crossed 64-point set; Mackey-base crossed set | **already covered**: SMQH file = certified `c2_64points_k8_bb` byte for byte; Mackey-base set = same labelled order type (identical CNF) | EXACT (identity) |
| E8-1.3 | octagon-vertex deletions of the 7 one-octagon 65-point sets | **56/56 UNSAT**; 49 nontrivial deletions = 8 new order types; claim `lb-e1-octdel65` CONFIRMED (VS) | CERTIFIED + PROVED soundness |
| E8-1.2 | 1,592 stacking order types (359 never tested) | **1,592/1,592 UNSAT**; claim `lb-e1-stack1592` CONFIRMED (VB) | CERTIFIED + PROVED soundness |
| E7-1 | ABSAT7 (l1enc at k = 7): 2 symmetric maxima, 7 AE33 deletions, 1,911 near-full deletions, 8,537 pool sets; plus F2's 93 glued types | **10,457/10,457 UNSAT**, F2 136/136 UNSAT; controls all passed; claim `lb-e1-absat7` CONFIRMED (VB) | CERTIFIED + PROVED soundness |
| E7-1.5 | calibration: DDSZ-type 28-point set | saturated (CERTIFIED), but ABSAT CNF **SAT** (model checked); claim `lb-e1-ddsz28` CONFIRMED (VB) | CERTIFIED / EXACT |
| E8-2 | CONE4 gate | **deferred** (memory above this track's 2 GB budget; threshold port missing) | - |
| E7-3 | (7,6,6)@31 seed miner, 10,593 realized 32-point sets | **no 31-point hit**; 30-point seeds in 10,002 sets; claim `lb-e1-miner766` CONFIRMED (VS); windows r = 2..6 on 5 seeds: 89,265 calls, 0 SAT, 0 UNKNOWN | EXACT (negative); windows COMPUTED |

## E8-1.1: the SMQH crossed 64-point set (EXACT: it is a set already certified)

- `SYMEVEN/lit/smqh_crossed_k8_64points.txt` (SHA-256 `82ed0a5b…`) is one comment line plus 64 coordinate lines.
  Without the comment line it is **byte-identical** to `c2_64points_k8_bb.txt` (`$L1/sets/`, SHA-256 `8963eefe…`, `cmp`).
- So its l1enc CNF is byte-identical to the certified one (CNF SHA-256 `e0688763…`, the value in ABSAT8_INDEPENDENT §5),
  and the claim `absat8-l1-indep` (CONFIRMED) already covers it. I certified it again directly (LRAT SHA-256
  `8dc6438b…`, equal to §5's; 1 verdict line). My own canonical-form code (`$AGL/src/ot.py`, `isomap.py`) also finds
  the identity map, checked on all 249,984 ordered triples.
- The plan's further target, the crossed set on Mackey's base, was built at 20:14 with SYMEVEN's unchanged builder
  (`python3 -I -B lit/build_labelled_x1.py lit/mackey_fig328_x10.txt 6 607 27 1,2,3,4,5,6,7,9 OUT`, the parameters of
  SYMEVEN's README; output `$AGL/sets8/mackey_crossed_k8_64.raw.txt`, SHA-256 `09b81433…`, points only
  `mackey_crossed_k8_64.txt` `495c5840…`). Different coordinates, but **the same labelled order type** as the SMQH set:
  `isomap.py` finds the identity map, checked on all ordered triples, and l1enc's CNF is byte-identical
  (`e0688763…`). It is octagon-free (`l1check`), and its direct certification gave the same LRAT (`8dc6438b…`, one
  verdict line). So both literature crossed sets are covered by `absat8-l1-indep`; neither is a new order type.

## E8-1.3: octagon-vertex deletions of the seven one-octagon 65-point sets (CERTIFIED + PROVED soundness)

**Inputs.** `experiments/es8-lower-bound-search-2026-10-11/anneal/init_w8p_1..4.txt`, `init_v8p_1..3.txt` (copied to
`$AGL/sets8/`, SHA-256 equal). Each has 65 points; its first 64 lines equal `w8.txt` (witness(8)) or `v8_<i>.txt`.
`l1check … 8 self` (independent DP) finds exactly 8 points on a convex octagon in each, and none on a convex 9-gon:
vertices {0,…,6, 64} for `init_w8p_1..4` and `init_v8p_3`, and {57,…,63, 64} for `init_v8p_1,2`. So each set has
exactly one convex octagon.

**Statement (CERTIFIED + PROVED soundness, computer-assisted, unrefereed).** Let T be one of these 7 sets and v one of
its 8 octagon vertices. For every realization S′ of the labelled order type of T − v and every point p with S′ ∪ {p} in
general position, S′ ∪ {p} has a convex octagon through p. With the octagon kept when v is off it, this gives: **no
65-point set in general position without a convex octagon contains a 64-point subset with the order type of T − v,
for any of the 65 points v of T** (the "move one point" neighbourhood of each of the 7 near misses is empty).

**Results.** 56 CNFs (`$AGL/cnf8/*.cnf.zst`), all UNSAT, each `cake.out` with exactly one `s VERIFIED UNSAT` line
(56/56; cake_lpr heap 400 MB, peak RSS about 413 MB, 33 s in all). Table with every CNF/LRAT SHA-256:
`$AGL/logs/summary_e81a.tsv` (SHA-256 `90a44f25…`); raw `$AGL/cert8/certify.jsonl`.

- The 7 deletions of the added point (`*_d64`) have witness(8)'s order type (canonical key equal to `ot0000`'s); the
  4 `init_w8p_*_d64` CNFs are byte-identical to ABSAT8's `ot0000` CNF (`2d5768ff…`).
- The 49 other deletions fall into **8 distinct order types** (canonical keys `68ad95ba`, `1d472bf2`, `1a5e9f6b`,
  `d33dfc5d`, `c171fd13`, `8569a711`, `a810fd1e`, `5ea69360`), none equal to witness(8)'s. They are not compared here
  with the other 27 ABSAT8 sets; each is certified directly.

**Together with ABSAT8.** ABSAT8_INDEPENDENT certified the 8 octagon-vertex deletions of AE65 (CONFIRMED). With
the 56 CNFs above, the "move one point" neighbourhood of **every recorded one-octagon 65-point set** (AE65 and the
seven stacking near misses) is empty at the order-type level: no 65-point octagon-free set in general position shares a
64-point order type with any of them.

**Controls: 750/750 passed** (`$AGL/ctrl/controls.jsonl`, tag `e81a`; every point evaluated exactly by `l1check`).

- C2 (octagon-freeness of the 57 sets by `l1check`'s own DP): 57/57.
- C4 (the near misses themselves, 7 × 65 = 455 cases): for each T and each point v, the CNF of T − v is evaluated at
  the real point v. For the 8 octagon vertices the CNF's SHA-256 equals the certified CNF's, v violates ≥ 1 OCT clause
  and the DP finds the octagon through v (56/56). For the 57 other points (encoded with `--allow-kgon`, T − v keeps the
  octagon) v satisfies every clause, the DP finds no octagon through v, and CaDiCaL says SAT (399/399). These are
  full-size positive controls with exactly the structure of the certified CNFs.
- C1 (real points on the 10 distinct order types: SMQH and one set per class): 91,606 random, far and wedge points;
  every one lies on a convex octagon and violates ≥ 1 OCT clause; 0 R2/AC violations, 0 mismatches (10/10).
- C3 (delete w = 0, 21, 42, 63 and re-extend, 57 sets): w satisfies every clause, no octagon through w, CaDiCaL SAT
  (228/228).

**Claim `lb-e1-octdel65`** filed 19:15 KST (with the SMQH identity fact). **Verifier VS CONFIRMED it at 19:40 KST**
([VERIFY_LOWERBOUND_E1_OCTDEL65.md](VERIFY_LOWERBOUND_E1_OCTDEL65.md)): own encoder equal as clause sets 57/57, hashes
57/57, fresh cake_lpr run at heap 200 MB 57/57, own canonical order types (the same 8 classes), own octagon
enumeration; VS did not re-run C1/C3/C4.

## E8-1.2: the 1,592 order types of the stacking family (CERTIFIED + PROVED soundness)

**Regeneration (EXACT).** `family/generate.py` was copied with `family.py`, `dp.py` (SHA-256 equal to the repo's:
`0cc8e3dd…`, `7ab2654f…`, `affbe9a2…`) to `$AGL/gen/exp/family/`, with a symlink `$AGL/gen/scripts` → the repo's
`scripts/` (imported read-only, `python -B`). The copy `gen_e1.py` differs in 4 lines: it writes `sets/` and
`manifest.json` under `$AGL/stack/`, and it skips the slow pure-Python largest-convex-subset DP (octagon-freeness is
checked instead by `l1enc`, which aborts on any convex octagon, and by `l1check`'s DP in control C2). Run in unit
`esr-agl-regen` (167 s): 4,132 candidate trees, 4,128 distinct, all bound-certified (64 points, cup, cap and convex ≤ 7
by the recursion), **1,592 distinct order types**, 2,673 distinct x-order sign vectors, all representatives in general
position with distinct abscissae, coordinates up to 41 bits — the numbers in the experiment README.

- 1,195 regenerated representatives have a file of the same name in `family/sets/`, and all 1,195 are
  byte-identical to it.
- 397 have no such file. For 38 of them the repo holds an `otNNNNm.txt` file, and its canonical order type (my
  `ot.py`) equals that of my `otNNNN` in all 38 cases. The other **359** are exactly the types the README calls
  untested (`$AGL/names_stack_untested359.txt`, SHA-256 `66086fd8…`).

**Statement (CERTIFIED + PROVED soundness, computer-assisted, unrefereed).** For each of the 1,592 order types: for
every realization of the representative's labelled order type (and of its mirror image) and every point p in general
position, there is a convex octagon through p. So no 65-point set in general position without a convex octagon
contains a 64-point subset of any of these 1,592 order types. This covers the whole stacking family at the
order-type level, including the 359 types with no earlier test. Nothing follows about ES(8) = 65 beyond these types.

**Results.** 1,592 CNFs (2,016 variables; 362,542-452,342 clauses, corrected at 20:05 after VB's note: the first
version said 357k-438k; `l1enc` found convex8 = 0 in every set), all UNSAT,
each `cake.out` with exactly one `s VERIFIED UNSAT` line (1,592/1,592; unit `esr-agl-e81b`, 19:07-19:29, heap 400 MB,
peak RSS about 413 MB; LRATs 22-141 KB). The untested 359 ran first. Table with every CNF/LRAT SHA-256:
`$AGL/logs/summary_e81b.tsv` (SHA-256 `32b18393…`); raw `$AGL/stack/cert/certify.jsonl` (`38e222b9…`). CNFs kept as
zstd in `$AGL/stack/cnf/` (995 MB), LRATs as zstd in `$AGL/stack/cert/`.

**Controls** (tags `e81b`, `e81c`; exact `l1check` evaluations):

- C2 (octagon-freeness by `l1check`'s own DP) on all 1,592 representatives: 1,592/1,592.
- C1 (real random, far and wedge points) on 50 representatives, 30 of them from the untested 359: 458,195 points, each
  on a convex octagon and violating ≥ 1 OCT clause; 0 R2/AC violations, 0 mismatches. 50/50.
- C3 (delete w = 0, 21, 42, 63 and re-extend) on the same 50: 200/200.
- C3 on every representative (one deletion each, w = 7 × list position mod 64; the plan asks for C3 on every set):
  the deleted real point satisfies every clause of its CNF, has no octagon through it, and CaDiCaL says SAT:
  1,592/1,592 (unit `esr-agl-ctrl8c`, 20:07-20:25).

**Literature.** The plan asks whether DDSZ Prop. 14 or Baek–Balko already cover these types; not checked here. No
novelty statement is made.

**Claim `lb-e1-stack1592`** filed 19:30:25 KST. **Verifier VB CONFIRMED it at 19:58 KST**
([VERIFY_LOWERBOUND_E1_STACK1592.md](VERIFY_LOWERBOUND_E1_STACK1592.md)): VB regenerated all 1,592 CNFs (certified
hashes), ran a fresh cake_lpr on all 1,592 (exactly one verdict line each, the 359 included), re-ran the generator copy
(byte-identical representatives and manifest), checked general position and largest convex subset 7 with its own
exact code, and reproduced the 1,592/1,195/38/359 split with its own canonical form. VB noted the clause-range error
fixed above; VB did not re-run my controls.

## E7-1: ABSAT7, the same encoder at k = 7 (CERTIFIED + PROVED soundness)

**k-generic reading of the soundness proof (PROVED; this paragraph is the plan's prerequisite).** ABSAT8_INDEPENDENT §3
proves soundness for the CNF `l1enc S 8`. Nothing in it uses k = 8 or n = 64:

- R2 and AC do not depend on k at all (Cramer's rule at each point a; barycentric coordinates in each triangle).
- `l1enc S k` builds OCT from every convex (k − 1)-gon Q of S. The visibility lemma (the edges of a convex polygon that
  p sees form a cyclic interval) and the slot lemma (if p sees edge e_i of Q and neither neighbour edge, then every
  vertex of Q and p are vertices of conv(Q ∪ {p})) hold for every convex polygon Q with at least 3 vertices, so that
  e_{i−1} ≠ e_{i+1}. For |Q| = k − 1 = 6 a violated OCT clause therefore gives a convex 7-gon Q ∪ {p} through p.
- Hence, for every real p with S ∪ {p} in general position and no convex 7-gon through p, the assignment
  X(a,b) = [orient(a,b,p) > 0] satisfies every clause of `l1enc S 7`. Order-type invariance (§3, last part) is
  unchanged: AC and OCT depend only on orientation signs, and R2's cone conditions are sign conditions that hold for
  every realization with the same ε_x. Reflection: reflect S′ ∪ {p}.
- So UNSAT of `l1enc S 7` proves: for every realization S′ of the labelled order type of S (or of its mirror image)
  and every p with S′ ∪ {p} in general position, S′ ∪ {p} has a convex 7-gon through p.

**Targets (`$AGL/src/prep7.py`; 10,457 sets of 32 points).**

1. The two symmetric 32-point maxima `SYMMAX/mirror_32points.txt` (`mirror32`) and `SYM2/sym7_32points.txt` (`sym7_32`).
2. The 7 heptagon-vertex deletions of AE33. AlphaEvolve's `points_7` decimals were read as exact fractions and scaled
   by their lcm 10^17 (the AE65 conversion of ABSAT8; exactness asserted; 56-bit coordinates). `l1check … 7 self` finds
   exactly the 7 heptagon vertices {14, 15, 17, 20, 23, 25, 32}, as A/README §1 records.
3. The heptagon-vertex deletions of the 273 near-full sets (`inputs/nearfull_p2c.txt`, `nearfull_p2d.txt`): `l1check`
   finds exactly 7 points on a convex 7-gon in each (list in `$AGL/logs/nearfull_heptagons.json`), giving 1,911 sets.
4. The 8,537-set pool `inputs/distinct_K7*.txt` (all 7 files; 5,354 + 510 + 459 + 732 + 608 + 700 + 174).

**Results (CERTIFIED + PROVED soundness, computer-assisted, unrefereed).** 10,457 CNFs (496 variables; 40,731-48,964
clauses; `l1enc` found convex7 = 0 in every set), all UNSAT, each `cake.out` with exactly one `s VERIFIED UNSAT` line
(**10,457/10,457**; unit `esr-agl-e71`, 19:29:54-19:53:19 KST, heap 300 MB, peak RSS about 81 MB; LRATs 6-32 KB).
Table with every CNF/LRAT SHA-256: `$AGL/logs/summary_e71.tsv` (SHA-256 `9be76d13…`); raw `$AGL/cert7/certify.jsonl`
(`b6a7d228…`). CNFs kept as zstd in `$AGL/cnf7/` (1.2 GB), LRATs as zstd in `$AGL/cert7/` (180 MB).

**Statement.** For each of the 10,457 sets S: for every realization S′ of the labelled order type of S (or of its
mirror image) and every point p with S′ ∪ {p} in general position, S′ ∪ {p} has a convex 7-gon through p. Hence:

- no 33-point set in general position without a convex 7-gon contains a 32-point subset with the order type of either
  symmetric 32-point maximum, of any AE33 heptagon-vertex deletion, of any near-full heptagon-vertex deletion, or of
  any of the 8,537 pool sets;
- with the heptagon kept when the deleted point is off it: the "move one point" neighbourhood of AE33 and of each of
  the 273 near-full sets is empty (all 274 recorded one-heptagon 33-point sets);
- for the pool this strengthens record A's result (COMPUTED, x-sorted signotope model, one or two sweep directions)
  in the geometric reading: every realization of each order type and every real point p, with no sweep direction
  fixed, CERTIFIED (the l1enc model has no x-order constraint on p). The abstract reading (every acyclic uniform
  one-element extension) rests on ABSAT8_INDEPENDENT §3's remark, which was not checked here either.

Nothing about ES(7) = 33 follows beyond these order types.

**Extra target: F2's 93 glued sets** (`F2/data/sets32/gg*_d<k>.pts`, coordinates of 58-114 bits as measured on the
files; the first version of this line quoted F2's "60-103 bits", corrected at 20:14 after VB's note; 93 distinct order types
by my canonical form) and the 43 small-coordinate realizations `*_small.pts` there (each has the canonical order type
of its big set, 43/43). Encoded with L1's `l1enc_big` (GMP coordinates; L1 recorded byte-identical output to `l1enc`
on 35 sets), certified: **136/136 UNSAT**, one verdict line each (unit `esr-agl-e71f2`; `$AGL/logs/summary_e71f2.tsv`,
SHA-256 `bdab200a…`; `$AGL/cert7f2/certify.jsonl` `6b9501b7…`). Same statement for these 93 order types. Control C2
for the big sets rests on `l1enc_big`'s own convex-7-gon count (0) and on C2 of the 43 small realizations; `l1check`
cannot read more than 64-bit input.

**Controls at k = 7: all passed** (`$AGL/ctrl/controls.jsonl`, tag `e71`; exact `l1check` evaluations).

- C2 (heptagon-freeness by `l1check`'s own DP): 10,457/10,457.
- C4 (the near misses themselves): AE33 and all 273 near-full sets, every point v (274 × 33 = 9,042 cases). For the
  1,918 heptagon vertices the CNF of T − v has the certified SHA-256, v violates ≥ 1 OCT clause and lies on the 7-gon;
  for the 7,124 other points (`--allow-kgon`) v satisfies every clause, the DP finds no 7-gon through v, and CaDiCaL
  says SAT. 9,042/9,042.
- C1 (real random, far and wedge points on 51 certified CNFs: the 9 symmetric/AE sets, 21 near-full and 21 pool
  sets): 157,272 points, each on a convex 7-gon and violating ≥ 1 OCT clause; 0 R2/AC violations, 0 mismatches. 51/51.
- C3 (delete w = 0, 4, …, 28 and re-extend, the same 51 sets): 408/408.
- C7 (both directions of OCT on the prefixes S[:18], S[:22], S[:26] of the 51 sets): 480,998 points, both outcomes
  present in 153/153 subsets, 0 mismatches, 0 R2/AC violations. 153/153.

**Claim `lb-e1-absat7`** filed 19:57:30 KST (C4 on the near-full sets was still running then; it passed at 20:05).
**Verifier VB CONFIRMED it at 20:11 KST** ([VERIFY_LOWERBOUND_E1_ABSAT7.md](VERIFY_LOWERBOUND_E1_ABSAT7.md)): VB rebuilt
all inputs from the repository with its own code (byte-identical), regenerated every CNF (certified hashes), ran a fresh
cake_lpr on all 10,457 + 136 proofs (exactly one verdict line each), checked general position and largest convex
subset 6 with its own code, and re-derived the k = 7 soundness. VB noted the F2 coordinate-size error fixed above;
VB did not re-run my controls.

**Item 5: calibration on a DDSZ-type saturated set (done; result: the abstract test sees more than saturation).**

- *Instance.* `$AGL/src/ddsz28.py` builds DDSZ's Prop. 14 construction for n = 7 explicitly: blocks at L·(i, i²),
  i = 1..6, namely a point, a 5-cap, DDSZ's 8-point (4,5)-cup-cap-saturated set (their Theorem 11, coordinates as
  printed), its mirror image, a 5-cup and a point, each mapped by (x, y) ↦ L(i, i²) + (Ax, By). Ten parameter choices
  (L from 3·10^6 to 10^21, flattening B/A from 1/30 to 10^-9) all give **the same canonical order type** (`8ebe3989…`).
  The instance used below is `d28_h` (L = 3·10^6, A = 30, B = 1; 27-bit coordinates, SHA-256 `726c3a9e…`). The
  8-point block was copied from the arXiv text (v3, proof of Theorem 11); my exact check: general position, distinct
  abscissae, no 4-cup and no 5-cap (21 three-cups, 10 four-caps), as a (4,5)-cup-cap-free set must be.
- *Heptagon-free* (EXACT): `l1enc` count 0 and `l1check` DP 0.
- *Geometrically 7-gon-saturated* (**CERTIFIED** + exact clauses + PROVED soundness). The CNF `d28_h_geo.cnf` is
  `l1enc d28_h 7` plus realizability clauses of the line arrangement of d28_h: for a triple of lines (or a parallel
  pair), the clause excludes a sign pattern whose open half-planes have empty intersection. `$AGL/src/tripgeo.cpp`
  computes these patterns exactly (GMP; one empty pattern per non-concurrent triple, two per concurrent triple); its
  self-test agrees with an exact candidate-point search on 1,844,480 (triple, pattern) cases. By Helly's theorem in
  the plane, a sign vector is realized by an open cell iff every three of its half-planes meet, so every real p in
  general position satisfies all these clauses. `$AGL/src/geosat_cegar.py` adds only the clauses that the current
  model violates; after 9 rounds (1,075 triple and 9 pair clauses) the CNF was UNSAT, and `certify_cnf.sh` gave
  exactly one `s VERIFIED UNSAT` (CNF `5f655526…`, LRAT `7df09501…`). Control: 15,900 exact real points (random, and
  near the vertices of the lines in the added clauses) violate none of the added clauses. Agreement: D2's `satcount`
  (unchanged copy, SHA-256 `7e1f0fa6…`) sweeps all 62,523 faces (Euler-complete) and finds no face with m = 0
  (COMPUTED); so do 7,012 sampled real points.
- *ABSAT test SAT* (EXACT). The plain CNF `l1enc d28_h 7` (`79fd77b6…`; byte-identical for instance a) is
  satisfiable: the CaDiCaL model `d28_h.model` (`cb0ce33a…`) satisfies all 30,108 clauses (R2 18,200, AC 3,276,
  OCT 8,632), checked clause by clause. Its sign vector has an empty cell for d28_h's coordinates (exact rational
  clipping, `$AGL/src/cellcheck.py`; the clipper finds nonempty cells for real points' sign vectors in 3/3 tests).
- **Reading.** For this saturated 28-point set (non-maximum: 28 < 32) the order-type-level CNF has a solution (by
  ABSAT8 §3's remark, not checked here, an acyclic uniform one-element extension without a 7-gon through the new
  element). ABSAT UNSAT implies geometric saturation of every realization (soundness), and this instance shows that
  saturation of one realization does not imply ABSAT UNSAT. So the ABSAT property is strictly stronger than
  geometric saturation of a realization, and the ABSAT UNSAT results (ABSAT8, ABSAT7, E8-1) say more than
  saturation. Whether ABSAT UNSAT indicates maximality is not settled: no non-maximum set with ABSAT UNSAT is known
  here. Whether the abstract extension is realized by some other realization of the same order type was not tested.
- **Claim `lb-e1-ddsz28`** filed 20:06:48 KST. **Verifier VB CONFIRMED it at 20:15 KST**
  ([VERIFY_LOWERBOUND_E1_DDSZ28.md](VERIFY_LOWERBOUND_E1_DDSZ28.md)): instance rebuilt byte-identically, own geometry
  (largest convex subset 6), own l1enc build equal to the first 30,108 clauses, all 1,084 extra clauses checked as
  empty patterns by VB's own exact Motzkin test (with positive and negative controls), fresh cake_lpr run, model
  checked (it violates 178 of the extra clauses, so its sign vector has no point). VB did not check that the 8-point
  block equals DDSZ's Theorem 11 set (paper not consulted) and did not re-run satcount.

## E7-3: (7,6,6) seed miner over the realized 32-point pools (EXACT for the mined subsets; negative)

**Method.** `$AGL/src/miner.cpp` (exact integers; `miner_big.cpp` is the same code with GMP coordinates, generated by
`src/mkbig.py`, for the F2 sets). For a set S and each combinatorially distinct sweep direction u (one representative
strictly inside each arc between consecutive critical directions perp(p_j − p_i), over a half circle; the other half
gives the reversed orders, in which cups and caps swap, and (6,6) is symmetric), it sorts S by ⟨u, p⟩ and searches
for H with |H| ≤ 2 such that S − H has no 6-cup and no 6-cap (x-sorted chains; DP over consecutive triples). The search
branches over the points of one 6-chain (depth 2) and prunes when three pairwise disjoint 6-chains exist.

- Self-test: on 15,606 directions of 300 random sets (7-14 points, chains of length 4), the search equals brute force
  over all H with |H| ≤ 2 and all 4-subsets (6,047 pruned directions included); the enumerated orders are pairwise
  distinct. Coverage test (`src/miner_covtest.cpp`): 5,999,995 random directions on 300 random sets, every resulting
  order or its reverse is among the enumerated ones. `miner_big` output equals `miner`'s on 20 sets.
- Pool: all 10,593 realized heptagon-free 32-point sets of this run (10,457 E7-1 sets and the 136 F2 files);
  5,218,410 sweep directions in all. D2's swept walk states are not stored in the repository and were not mined.

**Result.** **No 31-point (7,6,6) subset in any sweep direction of any of the 10,593 sets** (0 one-point hits, and no
set is (7,6,6) as a whole). 30-point (7,6,6) subsets (two-point hits) exist in 10,002 of the 10,593 sets, in 1,138,393
directions. Outputs: `$AGL/logs/miner_main.out` (SHA-256 `5073acf2…`), `$AGL/logs/miner_f2.out` (`7ba80627…`); inputs
`$AGL/miner_list7.txt` (`830886e2…`), `$AGL/miner_list7_f2.txt` (`171ec8eb…`); `src/miner.cpp` `785db4b6…`. This is weak
negative evidence only: N(7,6,6) = 30 stays open.

**Claim `lb-e1-miner766`** filed 19:57:06 KST. **Verifier VS CONFIRMED it at 20:23 KST**
([VERIFY_LOWERBOUND_E1_MINER766.md](VERIFY_LOWERBOUND_E1_MINER766.md)): VS's own GMP-exact miner (exact angular event
sort, simultaneous swaps grouped) visited all 5,218,410 sweep orders (the same count) and found no 0- or 1-point hit;
VS re-derived the provenance of all 10,593 sets from the repository files. VS updated the verdict at 20:50 KST: the side
fact is confirmed too (exactly 10,002 sets have a direction with a 30-point subset free of 6-cups and 6-caps, the
other 591 have none); VS did not count the direction total 1,138,393.

**Window runs on 5 seeds (COMPUTED; weak evidence).** Seeds: the first two-point hit of 5 sets from different
sources (`$AGL/win/seeds_hits.txt`): `sym7_32`, `ae33_d32`, `nf_p2c_103_d13`, `pool_main_4836`, `f2_gg402_10_d9`.
`$AGL/src/seed_prep.py` maps each set by p ↦ (⟨u, p⟩, ⟨u⊥, p⟩) (determinant |u|² > 0, so orientations are kept and the
x-order is the sweep order), deletes the two hit points, and re-checks exactly: longest cup and cap 6 before the
deletion and 5 after it. The lower7 probe's `nbwin_v2.py` (unchanged copy) then fixes every old triple of the 30-point
seed in the x-sorted (7,6,6) signotope CNF `etv31_667.cnf` (gen_etv 31 6 6 7) and inserts m = r + 1 new points into the
gaps next to each window of r consecutive points (per-call conflict budget 10^6).

- Positive control (r = 2, m = 2, into `etv30_667.cnf`): each seed's own window re-inserted at its own gap is SAT,
  29/29 windows for each of the 5 seeds.
- r = 2, 3, 4, 5 on all 5 seeds (20 runs, 53,055 calls, 978 CPU-s): **0 SAT, 0 UNKNOWN**
  (`$AGL/win/win_runs.tsv`, SHA-256 `577cad50…`). Reading: for none of these seeds is there a 31-point x-sorted (7,6,6)
  signotope that keeps all triples of the seed minus a window of r ≤ 5 consecutive points and places the r + 1 new
  points in the gaps within two positions of the window (nbwin's gap rule; solver verdicts only).
- r = 6 (m = 7; 7,242 calls per seed) on all 5 seeds: units `esr-agl-win3` (`sym7_32`, 20:25-21:30) and
  `esr-agl-win4` (nf, pool, f2, ae33, 20:30-21:49). 36,210 calls, 4,893 CPU-s (per seed 1,950 / 237 / 266 / 734 /
  1,707 CPU-s; worst single call 8.4 s): **0 SAT, 0 UNKNOWN**, all complete (`$AGL/win3/win_runs.tsv` `b83467ef…`,
  `$AGL/win4/win_runs.tsv` `8df2d571…`). The plan's cap of 5 seeds at r = 6 is thereby used up; per seed r = 6 cost
  0.07-0.54 CPU-h, inside the plan's 0.2-0.65 CPU-h estimate except for the two cheap seeds.

## E8-2: CONE4 gate (deferred; not run)

Not run, for three reasons found while checking sizes:

- **Memory.** The plan sizes each gate call at 3-4 GB (unit MemoryMax 5G, RLIMIT_AS 4G). This track's memory budget
  is 2 GB in total, so no gate call fits. Nothing was measured here.
- **Port incomplete.** In the snapshot `/home/jay/research/data/roadmap-20261115/scratchpad-snapshot-20261115/cone4/`
  the cone families for m = 4 exist (`cone_m4t14.clauses`, 245 KB), but the threshold-chain files that variant (b)
  needs are empty (`thr2_m4t14.clauses` and `cellthr2_m4t14.clauses`, 0 bytes), and `posctrl.py` still has the
  empty-tuple bug the plan names (its 52-point loop iterates over `() and (...)`, which is empty).
- **Label.** Gate verdicts would be COMPUTED only, under the k = 9 soundness note's floating-point caveats.

What it needs: a unit of at least 5 GB beside the other jobs, the m = 4 threshold port (`thr_rules2.py`), the
`posctrl.py` fix and the positive control on the 15 known 52-point sets, then the 24 calls (plan §3, E8-2).

## Process notes

- **CPU.** Every job longer than a minute ran as an `esr-agl-*` unit; the summed CPUQuota of my active units was at most
  100 % at every start (checked from the unit start/stop times). Units: `e81a` 100 %; `regen` 70 % + `ctrl8a` 30 %;
  `e81b` 70 %; then `e71` 60 % + `ctrl8b` 20 % + `miner` 20 %; `ctrl7` 40 % + `e71f2` 20 %; `win` 40 %; `geosat` 40 %;
  `ctrl8c` 40 %; `win2` 20 %; then `win` raised to 60 %; `win3` 40 %; then `win3` 50 % + `win4` 50 %; `win4` 100 %
  after `win3` ended. Foreground commands were single-threaded and
  under a minute (self-tests, canonical keys, the DDSZ instance tests, one direct certification of the Mackey set).
- **Memory.** Anonymous memory stayed small: cake_lpr at heap 400 MB peaked at about 413 MB RSS (`/usr/bin/time`),
  at heap 300 MB at about 81 MB; all other units under 230 MB. systemd's "memory peak" (which includes page cache from
  writing CNFs and proofs) reached the configured limit for `e81b` (801.8M of 800M) and `e71` (601.9M of 600M); the
  memory guard had lifted the kernel limits and counts anonymous memory only, it stopped none of my units, and the
  journal shows no OOM kill. The sum of the configured MemoryMax values of concurrent units was above 2 GB for short
  spells (2.1 GB at 19:05-19:07, up to 2.8 GB for 5 s at 20:05:32, 2.6 GB at 20:11-20:13, 2.0 GB from 20:26); the
  actual usage was a few hundred MB.
- **Duplicate unit.** `esr-agl-win2` (started 20:11 for seeds 2-5) duplicated work that `esr-agl-win` had already
  begun; I stopped it at 20:13 (its two finished rows are in `$AGL/win2/win_runs.tsv`) and raised `win` to 60 %.
- **Corrections after verification.** Two numbers in this record were wrong and are corrected in place: the clause
  range of the stacking CNFs (VB) and the coordinate sizes of F2's sets (VB).
- No git command, no e-mail, no web request with the owner's name or the repository name; one arXiv text fetch
  (DDSZ, arXiv:2312.01223) for the 8-point set.

## Files and hashes (all under `$AGL` = `/home/jay/research/data/roadmap-20261115/pm1115/agl/`)

| what | files | SHA-256 |
|---|---|---|
| L1's encoder and checker (copies, unchanged) | `l1src/l1enc.cpp`, `l1src/l1check.cpp`, `l1src/l1enc_big.cpp`, `bin/l1enc`, `bin/l1check`, `bin/l1enc_big` | `41037548…`, `0f5a03e9…`, `8b223d4f…`, `60fee0ce…`, `12a7d6f4…`, `d45f89a5…` |
| driver (encode + `certify_cnf.sh` + verdict grep) | `bin/driver.sh` | - |
| order types | `src/ot.py`, `src/isomap.py`, `logs/keys_*.txt`, `logs/iso_smqh_vs_c2bb.json` | - |
| E8-1.3 | `sets8/`, `names_del8.txt`, `cnf8/*.cnf.zst`, `cert8/`, `logs/summary_e81a.tsv` | summary `90a44f25…` |
| E8-1.2 | `gen/exp/family/gen_e1.py`, `stack/manifest.json`, `stack/sets/`, `stack/cnf/*.cnf.zst`, `stack/cert/`, `logs/summary_e81b.tsv`, `names_stack_*.txt` | `dfb86289…`, `0a9ec140…`, -, -, certify.jsonl `38e222b9…`, `32b18393…` |
| E7-1 | `src/prep7.py`, `sets7/`, `sets7big/`, `names7_*.txt`, `cnf7/*.cnf.zst`, `cert7/`, `logs/summary_e71.tsv`; F2: `sets7f2/`, `cnf7f2/`, `cert7f2/`, `logs/summary_e71f2.tsv` | certify.jsonl `b6a7d228…`, summary `9be76d13…`; F2 `6b9501b7…`, `bdab200a…` |
| controls | `src/controls_e1.py`, `bin/ctrl_e81a.sh`, `bin/ctrl_e81b.sh`, `bin/ctrl_e81c.sh`, `bin/ctrl_e71.sh`, `ctrl/controls.jsonl`, `logs/ctrl_*.log` | - |
| E7-3 | `src/miner.cpp`, `src/miner_big.cpp`, `src/mkbig.py`, `src/miner_covtest.cpp`, `miner_list7.txt`, `miner_list7_f2.txt`, `logs/miner_main.out`, `logs/miner_f2.out` | `785db4b6…`, `3564d425…`, -, -, `830886e2…`, `171ec8eb…`, `5073acf2…`, `7ba80627…` |
| E7-3 windows | `src/seed_prep.py`, `bin/win_run.sh`, `win/` (copies of `nbwin_v2.py`, `etv31_667.cnf`, `etv30_667.cnf`, hashes equal to the lower7 probe's SHA256SUMS), `win/seeds_hits.txt`, `win/win_runs.tsv`, `win/win_run.log` | `nbwin_v2.py` `5a0a5f79…`, `etv31_667.cnf` `32b928fd…`, `etv30_667.cnf` `54e7850f…`, seeds `9c5d3a72…` |
| DDSZ calibration | `src/ddsz28.py`, `src/tripgeo.cpp`, `src/geosat_cegar.py`, `src/cellcheck.py`, `src/satcount_D2.c`, `ddsz/` | `6e91e346…`, `15248b40…`, `6254580e…`, `edde3706…`, `7e1f0fa6…`; `d28_h.txt` `726c3a9e…`, `d28_h.cnf` `79fd77b6…`, `d28_h.model` `cb0ce33a…`, `d28_h_geo.cnf` `5f655526…`, LRAT `7df09501…` |
| claims | `claims/lb-e1-*.json` (copies of the filed claims) | - |

Every proof is kept as zstd next to its `cake.out`; every CNF is kept as zstd. Nothing was deleted except temporary
control files under `$AGL/tmp/` (regenerable CNFs and point files written and removed by `controls_e1.py`).

## What remains

- **Verdicts.** All five claims are CONFIRMED (VS: `lb-e1-octdel65`, `lb-e1-miner766`; VB: `lb-e1-stack1592`,
  `lb-e1-absat7`, `lb-e1-ddsz28`). The verifiers did not re-run my controls.
- **Literature.** Not checked: whether DDSZ Prop. 14, Baek-Balko or other work already covers the stacking types, and
  whether order-type-level non-extendability of named sets is known. No novelty statement is made.
- **E8-2 (CONE4 gate)**: deferred (section above): needs a ≥ 5 GB unit, the m = 4 threshold port and the `posctrl.py` fix.
- **E7-3**: windows r = 2..6 ran on the plan's cap of 5 seeds (all UNSAT); further seeds or r = 7 (about 1.5 CPU-h
  or more per seed by the probe's scaling) were not run. D2's swept walk states were not mined (not stored in the
  repository).
- **Calibration follow-ups**: whether the abstract extension of the DDSZ-type order type is realized by another
  realization of that order type; a non-maximum set with ABSAT UNSAT (none known here).
- **Plan items not in this block**: E7-2 (joint two-point model), E7-4, E8-3, E8-4, E8-5, E7-5.

## Resume

```
AGL=/home/jay/research/data/roadmap-20261115/pm1115/agl; cd $AGL
./bin/l1enc --selftest && ./bin/l1check --selftest && ./bin/miner --selftest && ./bin/miner_covtest && ./bin/tripgeo --selftest
# re-certify a list (encode with L1's l1enc, certify_cnf.sh, grep the verdict line); e.g. the ABSAT7 sets:
systemd-run --user --unit=esr-agl-e71 -p CPUQuota=60% -p MemoryMax=600M -p MemorySwapMax=0 -p RuntimeMaxSec=7200 \
  --nice=10 --working-directory=$AGL $AGL/bin/driver.sh names7_all.txt sets7 7 cnf7 cert7 300 e71 l1enc
# (E8-1.3: names_e81a.txt sets8 8 cnf8 cert8 400; E8-1.2: names_stack_all.txt stack/sets 8 stack/cnf stack/cert 400;
#  F2: names7_f2.txt sets7f2 7 cnf7f2 cert7f2 300 e71f2 l1enc_big)
# regenerate the stacking representatives (about 3 min):
cd $AGL/gen/exp/family && /home/jay/research/data/six10-linux-20261105/venv.disk/bin/python -B gen_e1.py
# miner: ./bin/miner 6 miner_list7.txt; ./bin/miner_big 6 miner_list7_f2.txt
# DDSZ calibration: bin/geosat_run.sh (tripgeo + geosat_cegar.py + certify)
```
