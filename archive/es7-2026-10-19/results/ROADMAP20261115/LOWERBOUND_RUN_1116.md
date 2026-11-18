# LOWERBOUND_RUN_1116: second block of the lower-bound plan (track L, 16 Nov 2026 evening, 18:25-00:30 KST)

**Status: IN PROGRESS (skeleton written 18:40 KST; updated after each milestone).**

Plan being run: [LOWERBOUND_PLAN_1115PM.md](LOWERBOUND_PLAN_1115PM.md), after yesterday's block
[LOWERBOUND_RUN_1115EV.md](LOWERBOUND_RUN_1115EV.md) and the literature check
[LOWERBOUND_EV_CHECK.md](../NOVELTY20261115/LOWERBOUND_EV_CHECK.md).
Work dir: `/home/jay/research/data/roadmap-20261115/pm1115/ln/` (below `$LN`). Units: `esr-agl-*`, at most 100 %
CPUQuota in total, at most 1.9 GB memory in total. Tools copied unchanged from `$AGL` =
`/home/jay/research/data/roadmap-20261115/pm1115/agl/` (hashes in `$LN/logs/copied_sha256.txt`; `l1enc.cpp`
`41037548…`, `l1check.cpp` `0f5a03e9…`, binaries `60fee0ce…`, `12a7d6f4…`, as in ABSAT8_INDEPENDENT §8; self-tests
pass) and `realize_sig.py` from `round6/atn/` (`927e25b4…`).

| item | question | status | label |
|---|---|---|---|
| (1) DDSZ follow-up | is the abstract one-point extension of the 28-point DDSZ-type order type realizable by another realization of that order type plus one point? | **yes** (18:33): a 28-point set S' with the labelled order type (and x-order) of the saturated d28_h, plus a point p, has no convex 7-gon (`lb-ln-ddsz28-real`). The ABSAT CNF has exactly 34 models, and all 34 (44 x-positions) are realized (`lb-ln-ddsz28-all34`). Mechanism: DDSZ's 8-point block is (4,5)-saturated only in its coordinates (`lb-ln-ddsz-block`) | EXACT; count CERTIFIED |
| (2) E7-2 | joint two-point (radius-1) extension model at k = 7: encoder, soundness note, controls, cheapest targets | not started | - |
| (3) E7-3 | more seeds | not started | - |

## (1) DDSZ follow-up: geometric saturation depends on the realization (EXACT)

**Statement (EXACT, integer certificate).** Let S = `agl/ddsz/d28_h.txt`, the 28-point DDSZ-type heptagon-free set
of claim `lb-e1-ddsz28` (CONFIRMED), which is geometrically 7-gon-saturated (CERTIFIED there). Let
S′ = `$LN/ddsz/r29s1_S.txt` (28 points, |coordinates| < 2^21, in the labels of S) and p = (604, 510).

- S′ has the **same labelled order type** as S: all 3,276 triples have the same orientation sign. S′ also has the same
  x-order, so even the x-sorted signotope is the same. E1's canonical key (`ot.py`) agrees: `8ebe3989…` for both.
- S′ ∪ {p} (`$LN/ddsz/r29s1_Sp.txt`, S′ in label order, then p) is in general position and has **no convex 7-gon**:
  largest convex subset 6 by my own brute force (`src/convk.cpp`), and 0 points on a 7-gon by L1's `l1check` DP.
- So S′ is not geometrically saturated, although its order type is that of the saturated S. **Geometric saturation is
  a property of the realization, not of the order type.**
- p realizes exactly the abstract extension of `lb-e1-ddsz28`: its 378 signs orient(a,b,p) equal the model
  `d28_h.model`'s X(a,b).

**How it was found.**

1. `src/dec29.py` decodes `d28_h.model` into a 29-element chirotope. My exact check (`src/chi.py`): all 3-term
   Grassmann–Plücker relations (every pivot) and 4-point acyclicity hold on all 20,475 five-sets containing p, so the
   model is a uniform acyclic one-element extension (this confirms ABSAT8 §3's remark for this model).
2. Exactly one x-position of p gives a valid x-sorted signotope: between labels 17 and 18, inside block P₄ (the
   mirrored 8-point Theorem-11 block). Signotope check: every 4-subset has a monotone sign sequence.
3. With d28_h's own coordinates, the model's signs on the 28 lines of block P₄ alone already form no cell (exact cell
   enumeration `src/cells.py`: 278 cells; nearest differs on line (17,18)). So no small move of p helps; the block
   must be re-realized. The 9-point restriction (block P₄ plus p) has longest cup 4 and longest cap 4, so P₄ ∪ {p} is
   **not** (5,4)-cup-cap-free; the realized S′ is far from the flattened DDSZ shape (largest |coordinate| 1,968,005,
   others below 26,000).
4. `realize_sig.py` (unit `esr-agl-rs29a`, float search only) realized the 29-point signotope at its first start
   (2.3 s, 10-bit rounding). `src/verify29.py` then checked everything above in exact integers.

**Controls.** `convk` reports for S′ the same convex m-gon counts as for S (3,276 / 13,589 / 26,856 / 20,183 for
m = 3..6), as an order-type invariant must; on two toy sets it detects collinearity and counts a convex pentagon
correctly. `chi.py`'s self-test passes 200 real extensions and flags a non-chirotope.

**Claim `lb-ln-ddsz28-real`** filed 18:35 KST.

### (1b) All 34 abstract extensions are realizable (CERTIFIED count + 44 EXACT certificates)

- `src/enum_ext.py` (unit `esr-agl-enum28`, 216 s) enumerated the models of C = `l1enc d28_h 7` with blocking clauses
  on all 378 variables. **C has exactly 34 models** (CERTIFIED): C plus the 34 blocking clauses
  (`$LN/ddsz/enum/blocking.cnf`, `5b092707…`) is UNSAT, cake_lpr exactly one `s VERIFIED UNSAT` (LRAT `54059812…`,
  heap 400 MB). My own check (`src/check_enum.py`): every listed model satisfies all 30,108 clauses, the models are
  pairwise distinct, the blocking clauses are exactly their negations, and model 0 is E1's `d28_h.model`.
- Every model is a uniform acyclic chirotope extension (exact 5-set check) with 1-3 valid x-positions for p: 44
  (model, position) pairs, at x-positions 8, 9 (inside block P₃) and 16, 17, 18 (inside block P₄).
- **All 44 were realized** (`realize_sig.py`, first start each, 1-3 s) and checked exactly (`verify29.py` + `convk`):
  29 integer points, general position, the 28 old points with the labelled order type of d28_h (3,276/3,276 signs),
  p's 378 signs equal the model, largest convex subset 6. Table: `$LN/ddsz/enum/models.jsonl` (`34a2b1a0…`).
- Reading: for this saturated set the order-type-level test is exact. Every abstract one-point extension is a
  geometric extension of some realization of the same order type (with the same x-order). The SAT answer of
  `lb-e1-ddsz28` therefore reflects non-saturated realizations, not an artifact of the abstraction.

**Claim `lb-ln-ddsz28-all34`** filed 18:42 KST.

### (1c) The mechanism: DDSZ's 8-point block is saturated only in its coordinates (EXACT / CERTIFIED)

Let D be the 8-point (4,5)-cup-cap-saturated set of DDSZ Theorem 11, as copied in `agl/src/ddsz28.py`
(`$LN/ddsz/cupcap/d45.txt`; I did not compare it with the paper).

- **D is geometrically (4,5)-saturated (EXACT, own code).** `src/arrcells.py` enumerates every open cell of the
  arrangement of the 28 lines through two points of D and the 8 vertical lines through its points (one exact rational
  sample point per sector around every vertex; the 471 cells found equal the Euler count 1 + L + Σ_v (m_v − 1)).
  For every cell, D + p has a 4-cup or a 5-cap (`src/cupcap_sat2.py`). The self-test of `arrcells.py` compares with a
  rational grid on 40 random arrangements.
- **Its x-sorted signotope has exactly 9 one-element extensions without a 4-cup or a 5-cap** (2 at x-position 2,
  7 at x-position 3; `src/cupcap_ext.py`). CERTIFIED: for each of the 9 positions the CNF (signotope axiom on every
  4-set with the new element, no 4-cup, no 5-cap, blocking clauses of the listed extensions) is UNSAT, one verdict line
  each (9/9, `$LN/ddsz/cupcap2/cert/`). The encoding is a direct transcription of the definitions.
- **All 9 are realized (EXACT).** Each `$LN/ddsz/cupcap/d45ext_t*_real.json` has 9 integer points whose 8 old points
  have exactly the x-sorted signotope of D (56/56 signs) and which have longest cup 3 and longest cap 4
  (`src/verify_cupcap.py`, `logs/d45_cupcap_verify.jsonl`). The cell check finds 1 and 4 cells without a 4-cup or
  5-cap for two of these 8-point sets. So these sets realize D's signotope, and are not saturated.
- **Back to 28 points (EXACT).** `src/build_flat29.py` puts the 8 old points of `d45ext_t3_000_real.json` as block P₃
  and their mirror image as P₄ into the same DDSZ construction (block map of `ddsz28.py`; L = 3·10⁶, A = 30, B = 1, and
  also L = 10⁹, A = 1000 and L = 10¹², A = 10⁵). The 28 points have exactly d28_h's labelled order type (0 of 3,276
  triples differ; `src/same_ot.py`). With the new block point added, the 29 points have no convex 7-gon (largest
  convex subset 6). This is a second, flattened realization of (1), and it explains it: DDSZ's construction is
  saturated because its blocks are saturated in their coordinates, and block saturation is not a signotope invariant.

**Claim `lb-ln-ddsz-block`** filed 18:42 KST.

## Resume

```
LN=/home/jay/research/data/roadmap-20261115/pm1115/ln; cd $LN
./bin/l1enc --selftest && ./bin/l1check --selftest && ./bin/tripgeo --selftest
```
