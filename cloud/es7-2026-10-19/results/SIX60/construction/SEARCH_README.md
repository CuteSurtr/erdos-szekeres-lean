# Direct search for a 60-point sixfold octagon-free set (5 November 2026, 00:05-03:30 KST)

Work dir: `<six10-work-dir>/search` (this file). Repository untouched (read-only use of
`C7UPPER/gen.py`, `ES8SYM/tools`, the hard models). Rigor labels: **exact computation** / **written argument** /
**evidence only**.

## 0. Headline

**A 60-point 6-fold rotationally symmetric set in general position with no 8 points in convex position exists
(exact computation).** Together with `C6UPPER` (61 or more points always contain a convex octagon; certificate), the
largest 6-fold octagon-free set has **exactly 60 points**: the open question "54 or 60" is settled as **60**.

Certificate files (`cert60/`):

| file | sha256 | max coeff | convex 4-sets | convex 7-sets | convex 8-sets |
|---|---|---|---|---|---|
| `c6_60pts_10layers.pts` | `61ed920d90debaee7d231d7f88879bc558ca57d1a817aeb42076e62395d14ece` | 10^12 | 284,577 | 221,976 | **0** |
| `c6_60pts_10layers_small.pts` | `8ba0b2e964dc5135d66abcd2ab76efdddfcd362220819301d751e1189b5b9480` | 10^9 | 284,607 | 223,416 | **0** |

Format as in `ES8SYM`: one point per line, integers w_0..w_5 of sum_j w_j zeta^j, zeta = e^{2 pi i/6}; layer o is rows
6o..6o+5 (outermost first), row 6o+k = zeta^k * row 6o, so the rotation symmetry is exact by construction.

Exact checks, each run on both files (logs `cert60/cert.log`, `cert60/cert_small.log`, `cert60/eis_checks.log`):
1. `ES8SYM/tools/layer_order.py` + `verify_cfg.py --pts ... 6 0 8`: exact Z[zeta_6] arithmetic: 60 distinct points,
   invariant under zeta, **0 zero orientations** (all 34,220 triples; cross-checked by rigorous interval arithmetic
   2^-300, 0 mismatches/undecided), layers are nested convex orbits, radii strictly decreasing: `EXACT-PREP PASS`.
2. `cvx2.c` on the exact orientation table: two differently anchored dynamic programmes agree: convex 8-gons 0,
   largest convex subset 7: `CVX2 PASS`.
3. `cvxcheck.c`: depth-first enumeration with the 4-point criterion: 0 convex 8-subsets; its own DP: largest 7.
4. `crosscheck_decimal.py`: every orientation recomputed with 160-digit decimals: `CROSSCHECK PASS`.
5. `verify/indep_check.py` (written here from scratch, shares no code with ES8SYM): reduces every point to Eisenstein
   form a + b zeta, checks distinctness, origin absent, invariance under (a,b) -> (-b, a+b), all 34,220 integer
   determinants non-zero, and counts convex k-gons with its own DP: 0 convex 8-gons, largest convex subset 7 (counts
   for k = 3..7 identical to cvx2/cvxcheck): `INDEPENDENT CHECK PASS`.
   Calibration of this checker: on `ES8SYM/sets/c6_54pts_9layers.pts` it reproduces the recorded counts
   (188,055 convex 4-sets, 70,134 convex 7-sets, 0 convex 8-sets).
6. Integer-pair route (`cert60/*.eis.txt`: the Eisenstein coordinates (a, b) of every point; the linear map
   (a,b) -> a + b zeta has determinant sqrt3/2 > 0, so orientations are those of the integer pairs):
   `ES8SYM/tools/verify_set.py FILE 8 none` (geom.py DP): no collinear triple, largest convex subset 7, `PASS`;
   `enum_convex.c` (__int128 orientations, depth-first listing of every convex subset, its own sign table compared with
   verify_set's: 0 differences): largest convex subset 7, same counts for k = 3..7. Log `cert60/eis_checks.log`.

Reproduce (from this directory; stdlib Python 3 and a C compiler):
```sh
T=ref/es8tools   # copy of ES8SYM/tools
gcc -O2 -o verify/cvx2 $T/cvx2.c; gcc -O2 -o verify/cvxcheck $T/cvxcheck.c
python3 -B $T/layer_order.py cert60/c6_60pts_10layers.pts 6 /tmp/L.pts
python3 -B $T/verify_cfg.py --pts /tmp/L.pts 6 0 8 /tmp/c6_60
verify/cvx2 /tmp/c6_60 8
python3 -B $T/otab2txt.py /tmp/c6_60 /tmp/c6_60.orient && verify/cvxcheck /tmp/c6_60.orient 8
python3 -B $T/crosscheck_decimal.py /tmp/c6_60 6
python3 -B verify/indep_check.py cert60/c6_60pts_10layers.pts 8
```

**Shape** (float values read from the exact file `c6_60pts_10layers.pts`; phases mod 60 degrees):

| layer | r / r_0 | log(r/r_0) | phase (deg) |
|---|---|---|---|
| 0 | 1 | 0 | 0 |
| 1 | 7.268e-3 | -4.924 | 30.194 |
| 2 | 7.037e-3 | -4.957 | 31.306 |
| 3 | 6.930e-3 | -4.972 | 31.850 |
| 4 | 3.942e-3 | -5.536 | 32.434 |
| 5 | 3.839e-3 | -5.563 | 33.421 |
| 6 | 3.815e-3 | -5.569 | 33.874 |
| 7 | 3.747e-3 | -5.587 | 34.015 |
| 8 | 3.698e-3 | -5.600 | 34.885 |
| 9 | 5.437e-6 | -12.122 | 35.115 |

An outer hexagon; six "needles" (layers 1-8) pointing at the outer edge midpoints (phases 30-35 degrees), each needle
made of a 3-point and a 5-point sub-cluster at two radii (ratio 0.54), phases increasing inwards; and a tiny hexagon
(layer 9, radius 5e-6) at the centre. Phase order psi_1 < ... < psi_9 (cube c11111 of `C6UPPER`). This is the shape
predicted by the hard-core SDP lifts in `probe/lift_shapes.txt` ("an outer hexagon, a needle cluster, and an inner
hexagon shrinking to the centre").

**Consistency checks** (exact computation): the exact sign vector of the 60-point set (with its phase order)
satisfies the 10-layer CNF of `C7UPPER/gen.py 6 8 10` (chain variables solved by CaDiCaL under assumptions), all
10,608 clauses of `SIX10CEGAR/cuts_verified.clauses`, the `SIX10REFINE` model0090 cut, and the new diameter /
half-sector clauses of section 4 (script in section 6). So nothing certified earlier is contradicted.

**More certified 60-point sets** (exact, same five checks, produced automatically by `verify/certifier.sh`; list in
`verify/certified.tsv`, files `verify/auto/*.pts`): at the time of writing 12 pairwise different order types (the
number of convex 4-subsets, an order-type invariant, takes 12 different values between 283,647 and 290,409). They
include phase orders other than 1<...<9 (e.g. 9<1<...<8 and 2<...<9<1, the latter the mirror image of cube c11000),
needle radii from 0.24 down to 0.004, and inner-hexagon radii from 1.3e-4 down to 5e-6; the inner hexagon's phase is
almost free (15-56 degrees).

## 1. How it was found

1. **Fast float evaluator** (`src/cvxeval.c`, ctypes wrapper `py/ev.py`): counts convex k-gons (k <= 8) by the
   lowest-vertex chain DP with long-double orientation signs; about 0.5 ms for 60 points. Calibrated (exact match) on
   both certified 54-point sets (all counts k = 3..8 as recorded in ES8SYM) and on 18 random sets against brute force
   (`py/test_ev.py`).
2. **Multi-scale annealing** (`py/anneal.py`; log-polar coordinates, block translate/zoom moves, step sizes over 7
   decades, energy log(1+N8) + w7 log(1+N7)): about 21 million evaluations in waves 1-2 (8 + 4 workers). **Pure
   annealing never reached 0: best N8 = 90** (reached independently 6 times; the residual 90 octagons all lie in the
   outer 6 layers; the same value 90 as the earlier (6,4) blow-up search of `ES8SYM/sets3/single_orbit_bounds`). Best
   configurations: `wave1/best_*.json`, `wave2/`.
3. **Phase-fixed LP-CEGAR** (new, `cegar/lpcegar.py`). Key fact (written argument, Lemma 1 of ES8SYM): with the
   phases theta_i fixed, every orientation is the sign of a linear form in u = (1/r_0, ..., 1/r_9):
   2 area(p,q,s)/(r_p r_q r_s) = u_p sin(a_s - a_q) + u_q sin(a_p - a_s) + u_s sin(a_q - a_p).
   So for fixed phases the existence of radii is decided by SAT + LP: CaDiCaL (PySAT) on the gen.py CNF
   (`gen.py 6 8 10`) with the phase-order units, plus phase-specific implication chains among the 2-layer forms
   (thresholds on r_i/r_j); each model's sign vector goes to an LP (max-min normalized margin, HiGHS); infeasible ->
   Farkas support from the LP duals -> clause; feasible -> radii -> float check -> exact verification. UNSAT answers
   are evidence only (float LP cuts); a feasible answer is a candidate that must pass section 0's exact checks.
   Validation: at 9 layers with the phases of the certified 54-point set it returns realizations (one of them is a
   new certified 54-point order type, 189,783 convex 4-sets, `verify/t9cand_pert1.*`); every real configuration
   tested satisfies the threshold clauses (36,315 clause checks, 27 configurations); with K = 9 it never answers
   UNSAT on phases that are realizable.
4. **The hit.** Phase scans (`cegar/phasescan.py`) of perturbed phases of annealing optima (family `pert`, sigma
   0.1-3 deg): the vector `pert gbest_w5 k=20 sigma=0.385` (phases of an annealed configuration with N8 = 198, moved
   by about 0.4 deg) timed out at 60 s; a long run (`cegar/long/log_L1.txt`) produced, after 2,284 SAT/LP rounds
   (160 s), a realizable octagon-free sign vector: LP margin 9.3e-4, float N8 = 0. Exact verification passed at scales
   1e9-1e14 (section 0).

## 2. Extension searches ("one more layer"), evidence only

- **Fixed radii** (base layers exactly as in the certified sets, one new layer on a grid, `py/scan_ext.py`,
  `scans/*.log`): `c6_54pts_9layers`: minimum 414 convex octagons (lr in [-18, 4], up to 1801 x 600 grid points per
  range; per slot: new outermost >= 4,008; between outer and cluster 450; inside the cluster 414-1,824; new innermost
  >= 1,053). `c6_54pts_1orbit`: minimum 576 (new outer hexagon at 3.8x radius); inside the cluster >= 1,143.
- **Free radii** (LP-CEGAR with the 9 base phases fixed exactly and the new phase on a 0.5-degree grid at each of the
  10 radial slots; all 10 radii free): 2 x 1,200 phase vectors, **all UNSAT** at the first SAT call
  (`cegar/scans/res_e9.tsv`, `res_e1.tsv`). So neither certified 54-point set extends with its own phases (evidence).
- **Random phases**: 400 uniformly random phase vectors: all UNSAT (`res_r1.tsv`). Perturbations of annealing optima:
  293 of 300 UNSAT, 7 timeouts at 60 s (`res_p1.tsv`); one of the timeouts gave the 60-point set. So the realizable
  phase region is thin, which explains why phase-blind annealing stalls at 90.

## 3. Search effort

- Annealing: ~21.4 million float evaluations in waves 1-2 (about 4.2 core-hours; ~0.7 ms per evaluation incl. early
  aborts), best N8 = 90 without LP-CEGAR.
- Extension grids: ~5.6 million float evaluations.
- LP-CEGAR: ~3,500 phase vectors decided or timed out (scan TSVs), plus long runs and walkers (`cegar/long/`).
- Certification: section 0 (seconds per set).
- Wave 3 (`wave3/`): annealing seeded with the certified set at low temperature, energy 0.05 log(1+N7) while N8 = 0;
  every new N7 minimum is written to `wave3/found_*.json` and exact-verified by the certifier.

## 4. Side result: the SIX10CEGAR hard models are excluded by two elementary angular rules (exact + written argument)

gen.py's angular family skips triples containing an antipodal pair of one layer ("degenerate", `C6UPPER` §3b), and for
even m it has no half-sector variables. Two sound rules are therefore missing:

- **Diameter rule** (`cegar/diameter_rules.py`; written argument in its docstring). For p = (i,k), p' = (i,k+3) and x =
  (j,l), j != i: orient(p,p',x) = 2 r_i r_j sin(ang(p) - ang(x)), with ang(p) - ang(x) = (theta_i - theta_j) + (k-l)
  60deg; its sign is fixed for (k-l) mod 6 in {1,2,4,5} and equals the phase-order literal for {0,3}. 342 clauses at
  t = 10 (198 units, 144 binary with a Y literal).
- **Half-sector rule** (`cegar/halfsector_exact.py`, exact). (R1) orient((0,0),(i,3),(i,5)) is proportional to
  (sqrt3/2) u_0 + sqrt3 u_i sin(30deg - theta_i), so a negative sign forces theta_i > 30 deg; (R2) orient((0,0),(i,0),
  (i,2)) is proportional to (sqrt3/2) u_0 - sqrt3 u_i cos(theta_i + 60deg), so a negative sign forces theta_i < 30
  deg. Clauses (`cegar/halfsector_clauses.py`, 81 at t = 10): v1_i or v2_i; v1_i or v2_j or not[psi_i < psi_j].
- **Result on the 101 blocked hard models** (`models/*.json`): 90 violate diameter clauses
  (`cegar/diameter_models.txt`), 49 violate the half-sector rule (`cegar/halfsector_exact.txt`), **all 101 violate at
  least one** (the 11 diameter-consistent ones, all in c11000 with order 9<1<5<4<8<7<6<3<2, have theta_9 > 30 > theta_1
  forced by R1/R2 but psi_9 < psi_1). So the "hard cores" were artefacts of the weaker encoding plus SDP checks run
  with `--no-phase`; they were not near-realizations. Both clause families are satisfied by every certified 60-point
  set and by 300 random real configurations (0 violations), and CNF + both families is still satisfiable (as it must
  be, now that 60 is realized).

## 5. Rigor summary

| claim | status |
|---|---|
| 60-point sixfold octagon-free set in general position exists (`cert60/*.pts`, plus `verify/auto/*.pts`) | exact computation: six checks for the two `cert60` files (incl. one implementation written here from scratch); five for `verify/auto` |
| sixfold maximum = 60 | the above + `C6UPPER` certificate |
| all 101 SIX10CEGAR hard models violate the diameter or half-sector rule | exact computation (literal check) + written argument (rules) |
| neither certified 54-point set extends with its own phases; random phases are almost never realizable | evidence only (float LP cuts, phase grids) |
| pure annealing stalls at 90 octagons | evidence only |

## 6. Files

- `cert60/`: the certificates (`.pts`, float configuration `.float.json`, logs `cert.log`, `cert_small.log`, exact
  tables `.otab`/`.lex`, and `*.model.json`: the same sets as gen.py Enc(6,8,10) models, i.e. the sorted list of true
  variables among 1..5746 (5710 orbit signs from the exact table, 36 phase-order variables); cube c11111).
- `verify/`: `verify_found.sh` (float JSON -> exact pipeline), `indep_check.py` (independent checker), `certifier.sh`
  (background loop), `certified.tsv`, `auto/` (all automatically certified sets and logs).
- `src/cvxeval.c`, `src/enumk.c`: float evaluator / octagon lister. `py/`: `ev.py`, `anneal.py`, `scan_ext.py`,
  `analyze.py`, `base.py`, `test_ev.py`.
- `cegar/`: `lpcegar.py` (phase-fixed LP-CEGAR), `phasescan.py`, `walk.py`, `gen.py` (copy of `C7UPPER/gen.py`),
  `diameter_rules.py`, `halfsector_exact.py`, `halfsector_clauses.py`, `halfsector.py` (grid version),
  `modelfit*.py` (LP fit of fixed sign models; superseded by section 4), clause files `diameter_t10.clauses`,
  `halfsector_t10.clauses`, scans `scans/res_*.tsv`, long runs `long/`.
- `scans/`: fixed-radii extension grids (`.npz`, `.log`). `wave1/`, `wave2/`, `wave3/`: annealing logs and configs.
- `STATUS`: short status for monitoring.

## 7. Background jobs

See `STATUS` for the list (pids, stop times). All stop by themselves at 03:20 KST (searches) or 04:35 KST (certifier).
