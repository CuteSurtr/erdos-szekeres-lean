# realize/: the constructive side of the sixfold 10-layer question (night of 5 Nov 2026)

**Question.** Is the largest 6-fold rotationally symmetric set in general position with no 8 points in convex
position 54 or 60 points? C6UPPER excludes 61 and more.

**Answer: 60.** There is a 60-point example, and it is checked exactly. With C6UPPER, the sixfold maximum is exactly 60.

**Rigor labels.**
- *exact*: integer or algebraic arithmetic, accepted by a checker.
- *written argument*: a proof sketch given here or in a docstring, not refereed.
- *evidence*: numerical results.

## 0. The main result: a 60-point sixfold octagon-free set (exact)

**The set.** It has 10 nested regular hexagons and no centre point. Each layer i is the orbit
{zeta^k z_i : k = 0..5} with zeta = e^{i pi/3}. The seeds z_i = w0 + w1*zeta have integer coefficients (scale 2^28 = 268435456):

| layer | w0 | w1 | r / r_0 | theta (deg) |
|---|---|---|---|---|
| 0 | 268435456 | 0 | 1.000000000 | 0.0000000 |
| 1 | 74257719 | 6629426 | 0.289770220 | 4.2328286 |
| 2 | 65544021 | 6163452 | 0.256422971 | 4.4475076 |
| 3 | 54071730 | 10588904 | 0.223779191 | 8.7810440 |
| 4 | 53501118 | 10593050 | 0.221688340 | 8.8680251 |
| 5 | 43264300 | 15650877 | 0.196908071 | 14.8582338 |
| 6 | 42748054 | 15582152 | 0.194868873 | 14.9498726 |
| 7 | 29453840 | 15103124 | 0.146213636 | 19.4661334 |
| 8 | 29453745 | 15103180 | 0.146213461 | 19.4662327 |
| 9 | 2569808 | 3435 | 0.009579685 | 0.0662810 |

**Shape.** An outer hexagon, then four pairs of nearly coincident layers. The pairs climb in phase as the radius
decreases (4.3, 8.8, 14.9 and 19.47 deg), so in each sixth of the plane their points form a curved "needle". Layers 7
and 8 are almost twins (relative distance about 1e-6). Last comes a tiny inner hexagon at phase 0.066 deg.

**Files** (`exact/cand1/`).
- `cand1_s28.pts`: all 60 points, in the ES8SYM .pts format. sha256 `614469e928dbc68cdacb50b1ce20e74b7697ceea0f6689dfc95da7bf245f28b2`.
- `cand1_vc.pts`: the same configuration rounded at scale 2^40. sha256 `7d67447ebea6e789c1cca134c292df310083594b41285bfd30a0c152bb3b88d3`.
- `cand1.cfg`: the float source, as lines of "lr theta".
- `full/` and `full28/`: the outputs of every checker.

**Exact verification** (the ES8SYM `run_all.sh` sequence that certified the 54-point sets, run on both versions):
1. `layer_order.py`, then `verify_cfg.py --pts ... 6 0 8`. It checks: distinct points; invariance under
   multiplication by zeta; 0 zero orientations among all triples (exact Z[zeta] method A, plus 2^-300 interval method B
   with 0 mismatches and 0 undecided); every layer is a convex orbit strictly containing the later layers; radii
   decrease.
2. `cvx2` (two independent DPs): convex 8-gons DP1 = DP2 = 0; largest convex subset 7 and 7.
3. `otab2txt.py` + `cvxcheck` (DFS count of convex k-subsets plus a DP): convex 8-subsets 0, largest convex subset 7.
   Counts for k = 3..7: 34220, 292353, 1058232, 1454781, 296544.
4. `crosscheck_decimal.py`: PASS, 0 mismatches, min |det| = 4.3e15 at scale 2^40.
5. A fifth, independent enumerator, ES8SYM `enum_convex.c`. It uses no DP, computes orientations with __int128, and
   enumerates every subset in convex position. It runs on the integer oblique coordinates (a,b), with a = w0-w2-w3+w5
   and b = w1+w2-w4-w5, in `cand1_s28_oblique_xy.txt`.
   - Why this is valid (written argument): (a,b) -> (a + b/2, (sqrt3/2) b) is linear with positive determinant, so
     orientation signs and convex position are the same as for the real points.
   - Result: duplicates 0, collinear triples 0, C2 symmetry holds, origin not in the set. The convex j-gon counts for
     j = 3..7 are the same as above, and the largest convex subset is 7.

Reproduce from `realize/exact/cand1`, with `T=<results>/ES8SYM/tools`:

```
gcc -O2 -o cvx2 $T/cvx2.c; gcc -O2 -o cvxcheck $T/cvxcheck.c
python3 -B $T/layer_order.py cand1_s28.pts 6 c.L.pts
python3 -B $T/verify_cfg.py --pts c.L.pts 6 0 8 c
./cvx2 c 8
python3 -B $T/otab2txt.py c c.orient
./cvxcheck c.orient 8
python3 -B $T/crosscheck_decimal.py c 6
```

**Consistency with the CEGAR formula (exact).** `tools/check_set_vs_clauses.py` computes the set's encoder assignment
from the integer seeds. That is the 5710 triple-orbit signs, plus Y from the exact sign of det(z_i, z_j). It also
checks the labelling convention exactly: b_0 = 0; a_i, b_i > 0, so theta_i lies in (0, 60); radii decrease.
- The assignment violates **0 of 2,104,233** clauses. These cover `cegar/base/cuts_verified`, `cut_model0090`,
  `shared/cuts`, `shared/gp`, every `inbox/*.clauses` (chord_lemma, nfunits, nfpairs, linfam*, linfam2*, facial*,
  altcert*) and the clauses of this directory.
- Encoder A is SAT with all 5746 values as assumptions (`exact/cand1/encA_check.json`).
- The set lies in cube **c11111** (theta1 < theta2 < theta3 < theta4). That cube can therefore never become UNSAT
  with sound cuts.

**How it was found (evidence, method only).** By alternating projections (`tools/altproj.py`), followed by local
annealing of the octagon count (`tools/anneal8.py`):
1. Take a real configuration R. Here it was the search agent's `wave1/best_w0_r4.json`, which has N8 = 90.
2. Give CaDiCaL the lane formula, with R's orientation signs as its PHASES and R's phase order as the cube. This
   returns an octagon-free SAT model M close to R. GP violations are refined lazily, and lin2/lin certificates are
   added locally.
3. Fit M from R to a real configuration R' (`tools/opt.py`, `tools/search.py`).
4. Repeat. This trajectory got stuck at 34 wrong signs. Its best fit had N8 = 7620.
5. Annealing N8 from that fit reached N8 = 0 in about 15 s (30,000 moves). That is the float source, `cand1.cfg`.

The annealer alone, started from the search agent's configurations, had stalled at N8 = 90. The SAT-guided step moved
the configuration into a different basin.

**A second, structurally different example (exact): `exact/cand2/`.** It is also an outer hexagon, but here all 9 inner
layers form a tiny cluster at scale about 5e-4. Eight of them sit at phases 28–36 deg, and layer 9, at scale about
1e-5, sits at 55.8 deg.
- File: `c2_268435456.pts`, sha256 `2a0c981e6e240207a3a7ac20d7556b9c7899c1f7ce84521e12a6ad9fa1371ab7`. Integer oblique
  seeds: (268435456,0), (84911,75878), (82623,75568), (69289,76753), (68638,76095), (60816,78578), (60324,78009),
  (53911,72346), (50938,73485), (225,2559).
- The same full pipeline passes at scales 2^28 and 2^40 (`full/`). `enum_convex` gives largest convex subset 7 and
  301674 convex 7-gons.
- Its assignment differs from cand1's in 261 encoder variables, so it has a different order type. It is also in cube
  c11111, and it violates 0 of 2,177,170 lane clauses (`check_clauses_s28.log`).
- Found the same way, from `wave1/gbest_w5.json`: its fit had N8 = 6630, and annealing brought that to 0.
- **Compact exact version** (`exact/cand2/cand2_compact.pts`, sha256 `5f5fb01f278d73b23f5f996f626985b7ee5a37920bd7ed4da9ba44eee893829e`).
  Its seeds w0 + w1*zeta are:

  | layer | w0 | w1 |
  |---|---|---|
  | 0 | 524288 | 0 |
  | 1 | 5307 | 4742 |
  | 2 | 5164 | 4723 |
  | 3 | 4331 | 4797 |
  | 4 | 4290 | 4756 |
  | 5 | 3801 | 4911 |
  | 6 | 3770 | 4876 |
  | 7 | 3369 | 4522 |
  | 8 | 3184 | 4593 |
  | 9 | 14 | 160 |

  The 60 points are zeta^k times these seeds. The full ES8SYM pipeline passes (`fullc/`): cvx2 gives 0 convex 8-gons
  in both DPs, cvxcheck gives 0 convex 8-subsets, and crosscheck passes. `enum_convex` gives largest convex subset 7
  (301644 convex 7-gons). It was found by `tools/compact.py`, which rounds at decreasing scales and checks each
  rounding exactly.

**Robustness (evidence).** The smallest scale-free orientation, sin of the largest triangle angle, is 2.2e-5 for
cand1. A constrained local optimisation that keeps N8 = 0 (`tools/robustify.py`) raises it to about 1e-3 or more (see
"Results at hand-off").

## 1. Before the construction (00:05 to 00:40)

### 1.1 Exact certificates on small layer subsets (6 of the 10 old SIX10CEGAR cores)

**Calibration of the margin SDP (evidence).**
- Realizable patterns give clearly positive margins: the 54-point sets give 4e-5 and 4e-4; random multi-scale
  configurations give at least 1.4e-8.
- Phase rows can mislead. With them, the {0,1,9} restriction of c11110 has margin about 0. Its triple signs alone are
  realizable, exactly checked (`exact/c11110_L019.json`), but only with the opposite phase order.
- So the scans used **no** phase rows (`tools/sdp_core.py`, `PHASE=0`).

**The subset scan.** Every 3–9-layer subset of each core was scanned (`runs/sdp_subsets_nophase_*.json`, with
minimal zero-margin subsets in `runs/minimal_zero_margin_subsets_1e-8.json`). Several cores already have margin about
0 on 4–6 layers.

**Certificate search.** `tools/auto_cert.py` runs iterated facial reduction:
1. solve max t subject to P K = 0 and -P >= tI on the complement of K;
2. read the near-kernel, which is a complex subspace, and rationalise it over Q(w);
3. add it to K and repeat;
4. once t is clearly positive, round lambda exactly so that P K = 0 holds exactly;
5. accept only if a complete exact PSD test passes.

**Independent checker.** `tools/check_nsd.py` (stdlib):
- recomputes the forms in Cartesian coordinates over Q(sqrt3), with a different orientation formula;
- runs a complete LDL PSD test with exact signs of a + b sqrt3;
- binds each record to the encoder, to every member model file and to the cluster representative (non-free).

| core | layers | records | members |
|---|---|---|---|
| c10000 | {1,2,4,5} (also {1,2,4,6}) | 17 | 8/8 |
| c00001 | {2,3,5,6,9} (also {2,4,5,6,9}) | 15 | 13/13 |
| c11110 | {2,3,5,6,8} | 23 | 3/3 |
| c01001 | {3,4,5,7,9} (also {1,3,4,5,7,9}) | 42 / 26 | 16/16 |
| c11000 | {0,3,5,6,7,9} (also {0,5,6,7,8,9}) | 12 / 19 | 15/15 |
| c11001 | {2..9} (also {1..9}) | 64 / 59 | 1/1 |

**Status: exact.** The certificates use triple records only, so each is valid for every sixfold configuration.

**Sanity checks (evidence).**
- On random z, P(z) < 0.
- Every best numerical fit violates at least one record of every certificate of its core.

**Files.** Witnesses: `certs/*/nsd_witness.json`. Clauses: `certs/cuts_nsd.clauses`.
`certs/c00000_full_phase` is a full 10-layer witness that uses one convention row (pm(0,8)).

### 1.2 The antipodal rule: an independent rediscovery of the chord lemma's diameter case

**Written argument, checked exactly against the models.**
- Take p = (i,k), p' = (i,k+3) = -p and x = (j,l) with j != i.
- Then orient(p,p',x) = -2 r_i r_j sin(Delta + 60m), with Delta = theta_j - theta_i and m = (l-k) mod 6.
- Encoder A's `fam_angle` skips these triples, because O lies on the segment pp'.

**Consequences.**
- `tools/antipodal_clauses.py` writes 342 clauses (`certs/antipodal.clauses`).
- 90 of the 101 old hard models violate them. The other 11 (all in c11000) are covered by the exact certificate
  above.
- Random real configurations and the 54-point sets satisfy them.

**Independent agreement.** The coordinator had already derived this as the diameter case of the chord lemma
(`writeup/CHORD_LEMMA.md`, `main/chord_rules.py`). All 342 clauses are contained in, or subsumed by,
`main/chord_rules.clauses`, which the lanes already load as `cegar/inbox/chord_lemma.clauses`. The formulas agree.
This agent found the rule independently, while examining c00000. Its phase-row certificate needed theta_8 < 60 deg,
against the model's sign of orient((0,1),(0,4),(8,0)).

### 1.3 Numerical fits of the old cores (evidence)

Best wrong counts (of 5710): c11111 51, c00001 60, c11110 78, c00000 84, c01001 85, c10100 87, c11011 107,
c10000 115, c11001 117, c11000 119. The two-scale (first-order Puiseux) fit `tools/twoscale.py` did no better. Per
core, `persistent_wrong_<core>.json` gives the best-fit wrong records, the most frequent wrong records, the
certificate supports and the antipodal violations.

### 1.4 Models without any degree-2 certificate (evidence)

The phase-guided SAT step produced 74 models of the lane formula (`runs/altproj_B_work/`). All of them satisfy GP and
the chord/antipodal rules, and none has a lin2 or lin certificate.

17 of them have a robustly positive margin even with radius and phase rows, so no NSD/lin/facial certificate exists
for them on any layer subset. Examples: d9b6d730 2.8e-4, a5af92ac 9.3e-5, 46cc5bf7 2.7e-5. The table is
`runs/altproj_B_models_margins.json`.

Such models are what the lanes would have met in cube c11111. The 60-point set shows that the cube is SAT anyway.

## 2. Frontier watcher (00:40 to 00:57)

`tools/frontier.py` fitted the CEGAR's UNRESOLVED models: c01011 0ff7… and c11100 837d…, best 75 and 105 wrong. Both
have margin about 0. Outputs are `runs/frontier/*.json` and `persistent_wrong_frontier_*.json`. It was stopped
after the 60-point set was found.

## 3. Tools (`tools/`, copies; the repository was not modified)

| tool | purpose |
|---|---|
| `common.py` | encoder access, cores, model files, float orientations, .pts reader, seed normalisation |
| `opt.py` | scale-free fit loss with analytic gradient |
| `search.py` | multi-start fit with a per-layer global grid |
| `twoscale.py` | first-order two-scale fit |
| `sdp_core.py` | margin SDP on layer subsets, with or without phase and radius rows |
| `calib.py`, `calib2.py` | calibration of the margin SDP on realizable patterns |
| `auto_cert.py`, `auto_cert2.py`, `nsd_cert.py`, `face_sdp.py`, `face_kernel.py`, `lift_groups.py` | facial-reduction certificate search |
| `check_nsd.py` | independent exact checker (stdlib) for the certificates |
| `antipodal_check.py`, `antipodal_clauses.py` | the antipodal rule |
| `altproj.py` | alternating projections between real configurations and SAT models |
| `anneal8.py` | local N8 annealing |
| `robustify.py` | constrained robustification keeping N8 = 0 |
| `cvx.py` + `libcvxeval_copy.so` | float convex-k-gon counter, a copy of `search/src/cvxeval.c` |
| `rationalize.py`, `exact_check.py`, `verify_set.py`, `verify_float_config.py` | exact checks of a candidate's pattern and octagon-freeness (via `cvxcheck.c`) |
| `check_set_vs_clauses.py` | exact consistency of a real set with the clause files |
| `liftfit.py`, `rankred.py`, `frontier.py` | numerical realization attempts (evidence) |

Set `ES_RESULTS=<results dir>`. Use the venv python for the numeric tools. The exact checkers need only the standard
library.

## 4. Construction record of cand1 (provenance, parameters, seeds, wall times, reproduction)

Written at about 01:10 KST from the run's own logs and files. Two agents shared this directory: the original realize agent,
and a fork with the same context, which ran `altproj` / `anneal8` / `robustify` and found cand1. The record below was
reconstructed and re-run by the original agent.

### 4.1 Pipeline (method; the output is then checked exactly)

| step | what | where / parameters |
|---|---|---|
| 0. start | a real configuration from the search agent | `search/wave1/best_w0_r4.json` (sha256 `c19e8b84…fdfb71`), N8 = 90 (float). Converted into entry 0 of `runs/altproj_inits_D0.json` (sha256 `b75a2853…2efd0`; name `wave1/best_w0_r4.json#p0`; normalised and mirrored by `altproj.normalise`) |
| 1. launch | `run_altproj.sh ../runs/altproj_inits_D0.json D0` at 00:53:57 KST | runs `tools/altproj.py INITS ../runs/altproj_D0 STOP=04:35 CONFLICTS=1000000`. Environment defaults: `MAXCERT=25`, `FRESH=1` (a fresh solver per start), `ANNEAL=30000`. 1 core |
| 2. formula | CaDiCaL 3.0 (PySAT `cadical300`), **no** blocked-model assumptions | encoder A + `cegar/base` cuts + `cegar/shared` cuts and GP clauses + every `cegar/inbox/*.clauses` that had a checker log. 3,702,222 clauses loaded at 00:54:04. The live files were not archived, so the SAT step cannot be reproduced bit for bit |
| 3. phase-guided SAT step | phases = orientation signs of R; assumptions = R's phase order of layers 1–4 (cube c11111) | GP violations are refined lazily; each model goes to `lin2_cert.py` / `lin_cert.py` + exact checkers. Here gpR = 0 and certs = 0 in every round: the models were GP-consistent and uncertified |
| 4. fit | `opt.Problem` (softplus of s·sin(largest angle)) on all 5710 records, started at R | `search.lbfgs` with tau = 0.03, 0.01, 0.003, 0.001; 3 repetitions, rep r > 0 perturbed by `default_rng(r)` normal 0.02; per-layer grid `search.grid_layer(n=24, rng=default_rng(10r+j))` |
| 5. rounds | log `logs/altproj_D0.out` (sha256 `c2450770…cb62`) | d(M,R) = 576, 203, 35, 33, 34, 34; wrong(M,fit) = 274, 58, 32, 33, 34, 34; N8(fit) = 310830, 23967, 7620, 7620, 7620, 7620. Stop: the model repeated |
| 6. selection | the round with the smallest (N8_fit, wrong_fit) | round 2: N8 = 7620, 32 wrong signs, model hash `0cfc153d82837f79`; recorded in `runs/altproj_D0_elite.jsonl` line 1 (sha256 `11a33da8…6d07`) |
| 7. anneal | `anneal8.anneal(fit_lr, fit_th, iters=30000, seed=0, T0=0.05)`, seed = start index 0 | energy log(1+N8) + 0.02 log(1+N7); single-coordinate moves with log-uniform steps 1e-7..1e-1; float evaluator `cvxeval_copy.c` (long-double orientations). It reached **N8 = 0, N7 = 296544** at 00:54:46 |
| 8. float source | `runs/altproj_D0_N8ZERO_0.json` = `exact/cand1/config_float.json` (sha256 `ed5c8427…dfb3b`) = `exact/cand1/cand1.cfg` (lr, theta per layer) | |
| 9. rounding | integer oblique seeds z_i = w0 + w1·zeta at scale 2^40 (`cand1_S40.json` → `cand1_vc.pts`, 00:55:34) and 2^28 (`cand1_s28.pts`, 00:57:34) | the 2^28 representatives are in `RESULT.json` / `cert_s28_seeds.json`. `small_S28.json` is another rounding at the same scale; it differs by 1 in two coordinates. **The reference object is `cand1_s28.pts`** |

**Wall time.** 49 s from launch to the float N8 = 0 configuration: 6 s loading, 25 s for 6 SAT+fit rounds, 14 s
annealing. Exact verification followed within 3 minutes.

**Scripts used**, with sha256 at hand-off. None was modified after 00:53:23, so all predate the run:
`tools/altproj.py` 38607ad1…fe7ff, `tools/anneal8.py` 8077ff19…58441, `tools/opt.py` 06e49f1a…48889,
`tools/search.py` 3efa9a54…01a50, `tools/common.py` 687fec45…55434, `tools/cvx.py` fd6ba15c…86cd0,
`tools/cvxeval_copy.c` c97cdfd1…dfec, `tools/libcvxeval_copy.so` 133a814f…666365.

### 4.2 Reproduction recipe

1. **Exact verification only** (the claim; stdlib + gcc). In `exact/cand1/rerun/`, re-run at 01:07 KST:
   ```
   T=<results>/ES8SYM/tools
   gcc -O2 -o cvx2 $T/cvx2.c; gcc -O2 -o cvxcheck $T/cvxcheck.c; gcc -O2 -o enum_convex $T/enum_convex.c
   python3 -B $T/layer_order.py cand1_s28.pts 6 c.L.pts
   python3 -B $T/verify_cfg.py --pts c.L.pts 6 0 8 c        # EXACT-PREP PASS: distinct, invariant, 0 zero orientations (A + interval B)
   ./cvx2 c 8                                                # DP1 = DP2: 8-gons 0, largest 7, CVX2 PASS
   python3 -B $T/otab2txt.py c c.orient; ./cvxcheck c.orient 8   # DFS: 8-subsets 0, DP largest 7
   python3 -B $T/crosscheck_decimal.py c 6                   # CROSSCHECK PASS
   ./enum_convex cand1_s28_oblique_xy.txt                    # __int128, no DP: 0 collinear, largest convex subset 7
   ```
   Counts for k = 3..7, identical in cvx2 (both DPs), cvxcheck and enum_convex: 34220, 292353, 1058232, 1454781,
   296544. There are 0 convex 8-subsets.
   - Logs: `rerun/verify_rerun.log` (sha256 `cbba3cf2…bbfd`) and `rerun/enum_convex.log` (`86adb038…cfd1`).
   - The orientation table `rerun/c.otab` (`2af82342…cc28`) is byte-identical to `full28/c.otab` and `full/cand1.otab`.
   - `rerun/encA_exact_check.py` → `encA_exact_check.json` (`3bc749d9…8d78`). It recomputes the encoder assignment
     from the integer seeds, using an integer orientation and exact det(z_i, z_j) for Y, and confirms:
     - 0 zero orientations;
     - the convention holds exactly: b_0 = 0; a_i, b_i > 0; radii decrease;
     - the assignment equals `cert_s28_seeds_model.json`;
     - encoder A is SAT with all 5746 values assumed, so the chain family also certifies that there is no convex
       octagon.
2. **Float source from the recorded fit** (deterministic). From `tools/`:
   ```
   python -c "import json,anneal8; e=json.loads(open('../runs/altproj_D0_elite.jsonl').readline());
              print(anneal8.anneal(e['fit_lr'], e['fit_th'], iters=30000, seed=0)[:2])"
   ```
   It gives (0, 296544) in 6.7 s. The configuration is **bit-identical** to `config_float.json`: max |Δ| = 0.0 for lr
   and for theta (checked at about 01:06 KST). This run used the venv numpy and the `libcvxeval_copy.so` above.
3. **Whole pipeline**: `run_altproj.sh <inits> <tag>`. The SAT step depends on the clause files live at run time, so
   the SAT models need not repeat exactly.
   - The method found two independent float N8 = 0 configurations among the 64 starts of D0: best_w0_r4 at 00:54:46,
     and gbest_w5 at 01:02:22, which became cand2.
   - The annealer alone, from the same search configurations, had stalled at N8 = 90.

### 4.3 cand1 file list (sha256)

| file | sha256 |
|---|---|
| `exact/cand1/cand1_s28.pts` (reference, 60 points, scale 2^28) | `614469e928dbc68cdacb50b1ce20e74b7697ceea0f6689dfc95da7bf245f28b2` |
| `exact/cand1/cand1_vc.pts` (scale 2^40) | `7d67447ebea6e789c1cca134c292df310083594b41285bfd30a0c152bb3b88d3` |
| `exact/cand1/cand1_s28_oblique_xy.txt` (enum_convex input; equals the (a,b) of the .pts rows, rechecked) | `ba1f9575ebf69d13127bd52f419bd6d2cf0243b9a9641c139236967d1a3b5fa7` |
| `exact/cand1/cand1.cfg` (float source, lr theta) | `4a83485c8d0359830bb649127b839189b937f6ad6d3588f2d6b614c79470f64c` |
| `exact/cand1/config_float.json` (float source, JSON) | `ed5c8427594ccee62da23bbf819e586d63903c46f2e94833897938e8e78dfb3b` |
| `exact/cand1/cert_s28_seeds_model.json` = `cand1_S40_model.json` (encoder assignment, true vars) | `070f49d2788602888687f359eaecb8a6e18da1abd4fca8a4371979bd3ed79474` |
| `exact/cand1/RESULT.json` | `e7e981aacb732e1283a0223e13eeaf778510e38f6ee3667df89540e388c94585` |
| `exact/cand1/check_clauses_s28.log` (0 lane clauses violated) | `4d158fc1ca15c747200b1088f3851629550e57d2cd9bd9240c907d917928f1b5` |
| `exact/cand1/encA_check.json` | `7dcc00eee9574bfe13169b25a04c5ae4df1f1e920ca23d85fcb56ac8235c1775` |
| `exact/cand1/full28/c.otab` = `full/cand1.otab` = `rerun/c.otab` (exact orientation table) | `2af82342883d55211bc595ab6390511a1e927f3af1bfc9c99e197d3e854bcc28` |
| `exact/cand1/rerun/verify_rerun.log` | `cbba3cf2973576819965308d70ca30b0f286eee96108729380bc4d4f623bfbbd` |
| `exact/cand1/rerun/enum_convex.log` | `86adb0387dd15c4c6a0eca55d90306fe72b2e9161274e3cdaba4cb70cf6afcd1` |
| `exact/cand1/rerun/encA_exact_check.json` | `3bc749d989628799adea08efb7f8a5861d272daa7bd1a873142441b1aaf88d78` |

The coordinator re-verified cand1 independently with its own code (reported 01:05): rotation-closed, 0 collinear
triples, largest convex subset 7 by two DPs and an exhaustive DFS (296,544 convex 7-subsets, 0 8-subsets), and 0 of
2,157,010 clauses in 74 files violated.

### 4.4 Side observation (evidence)

Exchanging layers of cand2's float configuration gives float N8 = 0 configurations in the phase-order cube 2134 as
well as 1234 (background task "move candidate 2 into other cubes"). These are float only, not exactly checked.

## 5. Work of the original agent in `p2/` (exact and evidence)

All of it is in `p2/` (README there). In short:
- **Exact (LRAT, 36/36 cases): neither certified 54-point order type extends by one layer** when all 9 old layers'
  triple signs and phase order are fixed and the new layer is inserted at any radius rank (and any phase gap when it
  is outermost).
  - `ES8SYM/sets/c6_54pts_9layers.pts`: all 18 cases, with encoder A alone.
  - `sets3/c6_54pts_1orbit.pts`: all 17 encoder-A-only cases. The 18th, innermost insertion, is UNSAT only with the
    verified cuts + the GP snapshot (proof over those files too).
  - Tools: `tools/extend54.py`, `p2/tools/lrat_ext.sh`; log `p2/logs/lrat_ext.log`. This is consistent with cand1 and
    cand2, which contain neither order type.
- **Evidence.** Relaxing to 8 or 7 fixed old layers gives GP-, chord- and cut-consistent abstract models with positive
  degree-2 margin, up to 3.3e-5 (`p2/ext/`).
  - The best near-realization has 2 wrong signs and 3,990 convex octagons.
- **Evidence (frontier).** The 3-layer restrictions {a,7,9} and {a,8,9} of the blocked model c10100 r20 were never
  realized: 2 persistent short-diagonal chord records (5661, 5664, 5695, 5698). This holds although the model's SDP
  margin is +9.6e-6. Since the 6-fold value is now settled, this matters only as a hint for higher-degree certificates.

## Results at hand-off

See section 0 (cand1, the reference; cand2) and sections 4–5.

### cand1r: robustified cand1, smaller integers (exact; `exact/cand1r/`)

The coordinator asked to keep the robustified set as "cand2", but that name was already taken by the structurally
different example above, so it is called **cand1r**. **cand1 stays the reference.**

**How it was made.**
- `tools/robustify.py ../exact/cand1/config_float.json ../exact/cand1/robust1.json 1200` ran from 00:58 to 01:18,
  446k proposals with rng seed 1.
- It is a constrained local annealing that maximises the smallest scale-free orientation (sin of the largest triangle
  angle) while keeping float N8 = 0. That value rose from 2.2e-5 to **1.285e-3**.
- The float result was rounded with `p2/mfold/tools/to_pts.py 6 robust1_z.json S` (z = a + b·zeta, rounded at 2^S)
  and verified at S = 16..20:
  - S = 19 and S = 20 pass the full pipeline;
  - S = 16, 17 and 18 pass verify_cfg and crosscheck, but rounding changes the order type and creates octagons, so
    those fail at cvx2;
  - S = 10, 12 and 14 are not in general position.

**cand1r = `cand1r_s19.pts`**. Its seeds w0 + w1·zeta, with every coefficient at most 2^19 = 524288 (cand1 uses 2^28):
(524288,0), (131119,11665), (131103,11664), (107744,21423), (107703,21423), (88128,30720), (86762,30677),
(56942,30072), (56913,30089), (5569,389).

**Exact verification** (`v_S19/verify.log`, `v_S19/enum_convex.log`).
- verify_cfg: EXACT-PREP PASS, with 0 zero orientations and interval B 0/0.
- cvx2: DP1 = DP2, 0 convex 8-gons, largest 7, CVX2 PASS.
- cvxcheck: 0 convex 8-subsets, DP 7.
- crosscheck_decimal: PASS.
- enum_convex (__int128, oblique integers): 0 collinear, largest convex subset 7.
- Convex k-gon counts for k = 3..7: 34220, 297279, 1128000, 1651268, 316182. These differ from cand1, so this is a
  different order type: 37 encoder variables differ.

**Robustness.**
- min |det| = 3.42e4 at coordinate size 5.2e5. Relative to the squared coordinate size that is 1.2e-7; cand1 has
  2.6e8 at 2.7e8, which is 3.6e-9. So cand1r is about 35× more robust, with integers smaller by a factor of 2^9.

**Encoder and clause checks.**
- `encA_exact_check.json`: exact assignment, the convention holds, encoder A is SAT with all 5746 values.
- `check_clauses.log` (`tools/check_set_vs_clauses.py`): **0 of 2,195,325** lane clauses violated. These are
  `cegar/base` cuts, `shared/cuts`, `shared/gp` and all 80 `inbox/*.clauses`.

| file | sha256 |
|---|---|
| `exact/cand1r/cand1r_s19.pts` | `e2eaceb9e6483b461a72fc330a5d05b0ad6d7e238bfc557f5eed412d95d133c2` |
| `exact/cand1r/cand1r_s19_oblique_xy.txt` | `e06341b2ccbcd30f67f5daea679841e08990ac818f705796f9617a15ef719a06` |
| `exact/cand1/robust1.json` (float source) | `f5828d99e59c2dad4dfafa4933880e3f3f3456b08ec44b01041937c7577eb8d3` |
| `exact/cand1r/cand1r_seeds_model.json` (assignment) | `0e42a84d7eceea89ad31cd8b990c66039c3033323a97e241fa8ade0fdd42df20` |
| `exact/cand1r/v_S19/c.otab` | `193c0540a6ecc8c274f4795c24f23c1a4aaaedc85373745945f40363c08be00a` |
| `exact/cand1r/v_S19/verify.log` | `5511068ddea4de51263ac8c26394aecbd22a57919ce7760654dc1c21d2ca3830` |
| `exact/cand1r/v_S19/enum_convex.log` | `d2b93553e1d22d520b768813e9249d4546d73377e3c7a81ef02e9135e4370ec6` |
| `exact/cand1r/check_clauses.log` | `edeb36f969bfcb1677f161f4863d52642ab35c9c2e90ea1b146d9c8a6b640382` |

### m-fold alternating projections (running; `p2/mfold/`, `p2/README.md` §5)

- 4-fold: 14 layers, 56 points; the best known is 52.
- 5-fold: 12 layers, 60 points without the centre (61 with it); the best known is 56.
- 3 + 3 runs started at 01:15; they stop at 04:25.
- Any float N8 = 0 output is exactly verified automatically (`p2/mfold/exact/VERIFIED.tsv`).
