# realize/p2: work of the original realize agent after 00:40 KST, 5 Nov 2026

From 00:40 another agent wrote into `realize/`: a fork with the same context, which built the 60-point set cand1. To
avoid clobbering it, this agent's later work lives here. The main page is `realize/README.md` (sections 4–5 were
written by this agent).

**Rigor labels.**
- *exact*: integer arithmetic or LRAT, accepted by a checker.
- *written*: a proof sketch given in a docstring.
- *evidence*: numerical results.

## 1. Neither certified 54-point order type extends to 10 layers (exact)

**Statement.** Let X be a 6-fold octagon-free set of 60 points (10 layers) in general position. Remove one layer from
X. The 9 remaining layers do **not** have the encoder pattern (orbit-triple signs plus phase order, in the 9-layer
labelling) of:
- `ES8SYM/sets/c6_54pts_9layers.pts`;
- `ES8SYM/sets3/c6_54pts_1orbit.pts`.

**Method.** `tools/extend54.py`, a copy of which is in `realize/tools`.
- The old triple signs are computed exactly from the integer Z[zeta] coordinates (oblique (a,b) = (w0-w2-w3+w5,
  w1+w2-w4-w5)). Labels come from float angles; the smallest label margin is reported per case, at least 3.6e-6 deg.
- The new layer is inserted at every radius rank p = 0..9. For p = 0 the new layer is outermost, so the old labels
  shift; all 9 phase gaps are enumerated.
- Each case is solved with the old signs as assumptions:
  - 9-layer set: encoder A alone (`cegar/base/encA_6_8_10.cnf`, the output of `C7UPPER/gen.py 6 8 10`).
  - 1-orbit set: also encoder A alone, except the innermost insertion (p = 9). That case is SAT with encoder A alone
    and UNSAT once the verified cuts are added:
    - `cegar/base/cuts_verified.clauses` and `cut_model0090_sparse.clauses`;
    - `ext54/cuts_snapshot.clauses`, a copy of `cegar/shared/cuts.clauses` at 00:33;
    - `ext54/gp_snapshot.clauses`, the GP clauses at 00:33, re-checkable with `cegar/tools/check_gp_file.py`.
    - The GP snapshot alone or the cuts alone do not suffice; both together do.
- **Validation.** With `gen.py 6 8 9`, each set's own full pattern is SAT (`tools/validate_ext.py`). So the label and
  sign semantics match the encoder.

**Proofs** (`tools/lrat_ext.sh`, log `logs/lrat_ext.log`).
- Each case's CNF is encoder A (+ the extra files for that one case) plus unit clauses for the solver's failed-
  assumption core only, which is 126–290 old signs.
- `cadical --lrat`, then `lrat-check`: **36/36 verified** (18 + 17 + 1). The proofs were deleted after checking;
  hashes are in the log, and they regenerate in seconds.
- Soundness rests on: encoder A (written proof, gen.py docstring); the clause files above for the one 1-orbit case;
  and the GP identity.

This is consistent with cand1 and cand2, which contain neither order type.

## 2. Relaxed extension family (evidence)

**Setup.** Drop 1 or 2 old layers: their signs are freed but they keep their slot. Insert the new layer.
`tools/extend_lazy.py` solves this with lazy GP. `p2/tools/extend_lazy.py` re-runs it with ALL certified clause sets
(the lane cuts, GP, and every inbox file that has a log, snapshot `ext/inbox_snapshot.clauses`).

**Results.**
- No GP-consistent model with only 1 old layer dropped exists for the 9-layer set.
- The 1-orbit set has 2 models with 1 layer dropped (drop layer 5 or 6, new layer innermost) and 29 with 2 dropped.
- Many of them have **positive** degree-2 SDP margin with phase and radius rows, up to 3.3e-5
  (`ext/lazy2_margins.json`).
- The best near-realization is `runs/se_1orbit_d6_p9_allfree_best.json`. It has 2 wrong signs, with exact signs in
  integer arithmetic, but 3,990 convex octagons (float count). The persistent record is (0,0),(9,3),(9,5): +
  requires sin(theta_9 - 30 deg) < r_9/2 (r_0 = 1).

## 3. Frontier models with positive SDP margin (evidence)

Six blocked CEGAR models had a strictly positive margin with phase and radius rows (`probe/blocked/`).

**Fits.** `tools/lift_sweep.py` does rank-1 / Gaussian rounding of the lift, then exact block-coordinate sweeps:
- per layer, the number of wrong signs is minimised exactly over theta (an arc sweep) and over R (root intervals).

| model | best wrong (of 5710) |
|---|---|
| c00000 r31 | 43 |
| c11100 r21 | 51 |
| c00001 r37 | 61 |
| c10100 r20 | 74 |

**Rank reduction.** Convex iteration (`tools/rank1_iter.py`) on c10100 r20 stalls at rank 2, with eigenvalues 0.941
and 0.059, even when the required margin is very small.

**Small non-realized subsets of c10100 r20** (`tools/subset_real.py`, `runs/sub_c10100_r20_s3.json`).
- Every 3-layer subset {a,7,9} and {a,8,9} stays at 2 wrong signs. The records are 5661 (7,0),(9,0),(9,4) and 5664
  (7,0),(9,1),(9,3), or 5695 and 5698 for layer 8.
- These are short-diagonal chord records of the innermost hexagon.
- Other 3-layer subsets are realized, and those realizations are exactly checked.
- Calibration: the same optimiser realizes 4- and 6-layer subsets of random realizable patterns in seconds.

## 4. Old SIX10CEGAR hard cores (exact, from before 00:40)

Exact NSD certificates were found on small layer subsets for 6 of the 10 cores. They are listed in
`realize/README.md` §1.1; files are `certs/*/nsd_witness.json`, checked by `tools/check_nsd.py`.

## 5. m-fold alternating projections (`mfold/`, from 01:15)

**Targets.**
- 4-fold: 14 layers = 56 points; the best known is 52.
- 5-fold: 12 layers = 60 points without the centre, or 61 with it; the best known is 56.

**Method.** The same scheme as cand1 (`mfold/tools/mf_altproj.py`, generic m):
1. Start: the certified (t-1)-layer set plus one random new layer, annealed on N8.
2. Rounds of phase-guided SAT (encoder `gen.py m 8 t`, cube = phase order of layers 1–4) and a scale-free fit.
3. Anneal N8.

**Validation.** With `gen.py 4 8 13` and `5 8 11`, the certified sets' own patterns are SAT (`mfold/tools/validate.py`).
The exact pipeline `mfold/tools/verify_mf.sh` (verify_cfg + cvx2 + cvxcheck + crosscheck_decimal) passes on
re-roundings of the 52- and 56-point sets.

**Runs.** The first batches (tags `m4t14*`, `m5t12*`, `m4c_full_s31`, `m5c_full_s41`, `m*_cube_*`, `m*t_trust_s*1`) were
stopped after a few minutes and replaced by variants. The final set, started 01:23–01:31:

| run | m | pre-anneal | SAT step | other |
|---|---|---|---|---|
| `m4c_fullT_s33`, `m5c_fullT_s43` | 4, 5 | 60k | phases = R's signs; full phase order of R (all Y, H) assumed | altproj only if N8 <= 1500 after the pre-anneal |
| `m4t2_trust_s52`, `m5t2_trust_s62` | 4, 5 | 100k | trust region: R's signs assumed on all but the K most nearly degenerate records | K = 300 … 3500 with the phase order, then 2000 … 5000 without it |
| `m4ch_full_s71`, `m5ch_full_s81` | 4, 5 | 100k | full phase order | CHAIN: an annealed result that improves on its start becomes the next start (up to 12 steps) |

- All six runs: `mfold/runs/<tag>.{out,log,_results.json}`; started 01:23; they stop at 04:25; `ulimit -v` 8 GB.
- The generic fit was validated: on a random realizable 4-fold pattern perturbed to 52 wrong signs it returns to 0
  wrong in 3.5 s, and its gradient agrees with finite differences to 3e-9.
- `mfold/tools/watch_verify.sh` exact-verifies every float N8 = 0 output at 2^40, 2^50 and 2^60; for m = 5 also with
  the centre. Results go to `mfold/exact/VERIFIED.tsv`.
- Results at hand-off: see the status section of `realize/README.md`.

### 5.1 Do the certified 4-fold and 5-fold sets extend by one layer? (exact for UNSAT, modulo encoder A: LRAT 26/26 and 32/32 verified, `mfold/ext/lrat_ext4.log`, `lrat_ext5.log`)

`mfold/tools/mf_extend.py` is the m-fold analogue of section 1.
- The triple signs among the old layers are fixed, together with their phase order (Y, plus H for odd m), all
  rotated into the new labelling.
- The new layer is inserted at every radius rank. When it is outermost, every phase gap is enumerated; for odd m the
  breakpoints are theta_j and theta_j + pi/m.

**4-fold, `ES8SYM/sets/c4_52pts_13layers.pts` → 14 layers (`gen.py 4 8 14`): UNSAT in all 26 cases** (13 phase gaps
plus ranks 1..13), with encoder A alone. So no 56-point 4-fold octagon-free set contains 13 layers with this pattern.

**5-fold, `ES8SYM/sets3/c5_56pts_11layers_centre.pts` with the centre dropped → 12 layers (`gen.py 5 8 12`).**
- UNSAT in 32 of the 33 cases.
- The exception is the new layer **innermost**, which is SAT with encoder A alone. The model is in
  `mfold/ext/ext5_56_model_p11_gNone.json`.
- Realization attempts (evidence):
  - With the old layers fixed, a 200 x 150 grid over the new seed (`mfold/tools/grid_inner.py`) gives at best
    N8 = 13,860.
  - Fitting the SAT model with all layers free leaves 103 wrong signs. These are mostly (0,0),(k,0),(11,·) records,
    whose signs encode on which side of the line through O-near points the tiny inner layer sits.
  - Annealing after that ends at N8 = 3,125.
- No GP refinement was done for m = 5, so this SAT model may well violate GP.

**Validation.** For p >= 1 the assumption semantics are those of `mf.MF.lits`, which section 5 validated with
gen.py 4 8 13 and 5 8 11.

**Relaxation of the 4-fold extension** (`mfold/run_relax4.sh`, `DROP=d`, results `mfold/ext/relax4_d*.json`). One old
layer d is freed: its triples and phases are unassumed, but it keeps its radius slot. The new layer is inserted at
every rank and phase gap.
- **338 / 338 cases UNSAT** with encoder A alone (13 drops x 26 cases). These are solver results from CaDiCaL;
  LRAT proofs are made only if time permits, see `mfold/ext/lrat_relax4.log`.
- So no 14-layer octagon-free 4-fold model contains 12 of the 13 layers of the 52-point set, with their pattern,
  plus a free layer in the vacated slot.

**Relaxation of the 5-fold extension** (`mfold/run_relax5.sh`, results in `mfold/ext/relax5_d*.json`).
- 349 of 363 cases are UNSAT (11 drops x 33 cases; solver results, not LRAT-checked).
- The 14 SAT cases all put new material at the centre: the new layer innermost (p = 11) for every drop, plus
  p = 8..10 when the innermost old layer 10 is freed.
- Realization attempts for these 14 models (`mfold/tools/fit_relax5.py` → `mfold/runs/fit_relax5.json`, evidence):
  the best fit leaves 52 wrong signs and the best anneal ends at N8 = 1,755. No GP refinement exists for m = 5, so
  these SAT models may violate GP.

**State at hand-off (02:04).** Best float N8 of the alternating-projection runs: 4-fold 240 (`m4ch_full_s71`), 5-fold
590 (`m5t2_trust_s62`). No N8 = 0 configuration yet; `mfold/exact/VERIFIED.tsv` is empty. The runs continue until
04:25. LRAT proofs for the relaxed cases are running (`mfold/ext/lrat_relax{4,5}.log`).
