# LBK8SYM20261111: searches for larger 3-, 4- and 5-fold octagon-free sets (11–12 November 2026)

**Question.** Improve the lower bounds of the k = 8 table (`ES8SYM` §1 and addenda): 3-fold >= 61, 4-fold >= 52,
5-fold >= 56. Allowed sizes: 4-fold 4t (targets 56, 60, 64), 5-fold 5t or 5t + 1 (60, 61), 3-fold 3t or 3t + 1
(63, 64).

**Outcome.** **No row improves.** No configuration without a convex octagon was found for 4-fold with 14 layers,
5-fold with 12 layers (with or without the centre), or 3-fold with 21 orbits (with or without the centre). The table
stays 3-fold >= 61, 4-fold >= 52, 5-fold >= 56. Recorded here instead:
- a new phase-fixed CEGAR that needs no layer structure (`tools/pfenc.py`, §1.2), validated on the 4-, 5-, 6- and
  7-fold record sets, with two new ingredients (suffix-sum units, exact two-form "pair cuts");
- as a calibration, a **new order type of 6-fold 60-point octagon-free set** found by a template phase scan from
  scratch (one hit among 69 random template vectors, §2.4; exact computation; the 6-fold value 60 was already exact, so no table change);
- exact 4-fold 56-point near misses with exactly two convex octagons (§2.1);
- negative computational evidence for the three targets (§2.1–2.3).

**Rigor labels** as in the repository: exact computation / written proof (not refereed) / computational evidence.
Every "UNSAT" below is a solver answer on a formula with numerically derived clauses (sign units and pair cuts from
float forms, LP Farkas cuts): **computational evidence only**. No UNSAT claim is made, so no cake_lpr run applies.

## 1. Methods

All runs were single-threaded processes in one capped systemd slice (`lbk8sym.slice`: CPUQuota 800 %, MemoryMax
16G, Nice 10), units `lb-k8sym-*`, work directory `<lb-work-dir>` = `/home/jay/research/data/lb-k8sym-20261111`
(launchers in `tools/` use that path). Python: the venv of `<six10-work-dir>` (numpy, scipy/HiGHS, PySAT).

### 1.1 Float evaluator and local search (evidence)
- `tools/cvxm.c` + `evm.py`: the lowest-vertex chain DP of `<six10-work-dir>/search/src/cvxeval.c` (long-double signs)
  with an m-fold point generator (orbit i = r_i e^{i(theta_i + 2 pi k/m)}, optional centre). Calibrated: the counts
  of `ES8SYM/sets/c4_52pts_13layers.pts` (141,809 convex 4-sets, 45,220 convex 7-sets, 0 octagons),
  `c6_54pts_9layers.pts` (188,055 / 70,134 / 0), the 5-fold 56-point set and the 3-fold 64-point near miss (3
  octagons) are reproduced exactly.
- `annealm.py`: generic-m version of the six10 multi-scale annealer (energy log(1 + N8) + 0.02 log(1 + N7)); start
  shapes free, needle, clusters, orbit, two-orbit, spiral (outer polygon + spiral arm + inner layers, the shape of
  the 6- and 7-fold record sets) or a given configuration; optional moves focused on layers of current octagons and a
  radii-only mode. `lns.py` (remove k orbits, re-insert, anneal) and `reinsert.py` (remove orbits / add orbits on a
  2D (log r, phase) grid, beam search, local refinement).

### 1.2 Phase-fixed CEGAR without layers (`tools/pfenc.py`)
The encoding argument is a written proof (not refereed); all answers are evidence. With the phases theta_i fixed and
the radius ORDER fixed (orbit 0 outermost), every orientation of three non-centre points is the sign of a linear
form in u = (1/r_0, ..., 1/r_{t-1}) (ES8SYM Lemma 1); orientations with the centre are constants. Clauses:
- orbit variables, one per rotation orbit of triples (numbering identical to `C7UPPER/gen.py`);
- sign units: one-coefficient forms; two-coefficient forms whose zero lies at u_j/u_i <= 1; **suffix-sum units**:
  with c_k = u_k - u_{k-1} >= 0 (u_{-1} = 0), a.u = sum_k c_k S_k with S_k the suffix sums of a, so a form whose
  suffix sums share one sign has that sign;
- threshold implications between two-coefficient forms of one orbit pair (as in the six10 LP-CEGAR);
- **pair cuts** (`--pairs 1`): every sign combination of two non-unit forms that no ordered u realises. By Ville's
  theorem, {x.c > 0, y.c > 0, c >= 0} is infeasible iff lambda x + mu y <= 0 componentwise for some lambda, mu >= 0
  not both 0 (x, y the signed suffix-sum vectors); with the unit cases excluded this is an interval test in
  alpha = mu/lambda, applied with a conservative tolerance (a cut only when infeasibility holds with margin).
  Check: 0 violations by the configuration itself and by 300 random ordered radius vectors (`logs/pairtest.txt`);
- **chains without layers**: pivot p = (i, 0); Q = points of orbits j > i, the other points of orbit i, and the centre.
  Q lies in the open half-plane bounded by the tangent at p to the circle |z| = r_i, so the chain family and its
  proof in the docstring of `C7UPPER/gen.py` (step 4) apply verbatim; every convex octagon has a vertex of largest
  radius, so the family is complete. No layer lemma is used: the encoder covers the 3-fold case and the 5-fold case
  with centre.
- LP: maximise the normalised margin of the model's signs over ordered u with u_0 = 1. Margin > 0 gives radii (float
  check, then the exact pipeline); otherwise the Farkas support of the LP duals is added as a clause. Every LP point
  (a real configuration with these phases) and, for each new best margin above -0.05, the radii minimising the total
  hinge violation are also tested for N8 = 0 directly.
- Solver: CaDiCaL 1.9.5 through PySAT (`cadical195`). PySAT's `cadical300` ignores `set_phases`: on the 52-point
  set's own signs it returned a model differing in 255 signs, `cadical195` in 0; three early validation timeouts
  listed in `logs/summary.txt` (`pftest`, 31-33 s) are runs with `cadical300` before the switch. Decision phases of the
  chain variables are the least fixpoint for the hint's signs. Options: trust region (fix the hint's signs except the
  K least robust forms and all triples inside its octagons), re-centring.
- **Validation** (each at the set's own phases, with pair cuts): `c4_52pts_13layers` (margin 0.072), the 5-fold
  56-point set with centre (1.9e-6), the 3-fold 61-point set (1.0), SIX60 set D (2.2e-4) and `c7_64pts_small` with
  centre (8.0e-4): the first SAT model is realised in every case; the 4- and 3-fold realisations pass the exact
  pipeline at 2^30, 2^40, 2^50 (`logs/VERIFIED.tsv`). The signs of the 3-fold near miss `control_cost3_63pts` (3
  octagons) violate the formula, as they must.
- Calibration of phase sensitivity: perturbing the 52-point set's phases by sigma = 0.05 deg leaves 9 of 12 phase
  vectors realisable (CAND) and 3 undecided; for the 5-fold 56-point blow-up, sigma = 0.05 deg gives 10 of 10 UNSAT,
  sigma = 0.002 deg 5 of 8 CAND: blow-up type sets have a far thinner realisable phase region.

### 1.3 Other SAT-side tools (evidence)
`lpcegar2.py` (the six10 LP-CEGAR for general m on `gen.py` CNFs, fresh solver with root units), `trlp.py` (trust
region on the same), `altproj2.py` (alternating projections with the phase order as root units, optional trust
region), `layer_core.py`, `layer_where.py` (which layers' phase information makes the fixed-phase formula UNSAT; where
the SAT model puts a freed layer), `ext_test.py`, `core_groups.py`, `extscan.py` (fixed-phase extension by one
orbit), `template_scan.py`, `template_scan2.py`, `template_scan3.py` (phase vectors from spiral, multi-arm and cluster
templates; all radii left to the LP), `fitmodel.py`, `slp.py` (sequential LP that lets the phases move: it
linearises the forms in the phases around the LP point of a near-feasible SAT model and maximises the margin of the
model's signs over (u, phase step) with a trust region).

### 1.4 Exact verification (exact computation)
`to_pts.py` rounds a float configuration to Z[zeta_m] seeds a + b zeta at scale 2^S; `verify_mf.sh` runs the ES8SYM
pipeline (`verify_cfg.py --pts`: exact and interval signs; `cvx2`: two DPs; `cvxcheck`: DFS; `crosscheck_decimal`);
`watch_verify.sh` did this for every float N8 = 0 output at 2^30, 2^40, 2^50 (`logs/VERIFIED.tsv`).
`verify_indep.py` (written here, standard library only) is an independent exact checker for m = 3, 4, 5: integer
coordinates for m = 4 and (oblique) m = 3, exact Q(sqrt5) signs for m = 5, two differently anchored O(n^4) DPs; it
gives 7 on the 52-, 56- and 61-point sets and 8 on two near misses. `verify3.sh` adds, for 3-fold sets, ES8SYM
`verify_set.py` + `enum_convex.c` on lattice coordinates and SIX60 `dfs_convex.c`. For m = 3 the flag
`layers_are_nested_convex_orbits` of `verify_cfg.py` does not apply (no layer lemma).

## 2. Results

All numbers as of the end of the run (04:00 KST); per-directory counts in `logs/summary.txt`, raw results in
`logs/cegar/*/res_*.tsv` and `logs/runs/*/log_*.txt`. Every UNSAT / TIMEOUT below is computational evidence.

### 2.1 Fourfold, 14 layers (56 points)

- **Annealing.** 74 completed restarts (35.5 M float evaluations) at t = 14. Best N8 = 2, reached by
  four restarts from random starts (needle and spiral shapes), N8 = 3 by two more; polishing (focused moves, LNS,
  re-insertion) never went below 2. In every configuration with N8 <= 3, **every remaining convex octagon is a
  twin-square octagon**: two radially adjacent layers with radius ratio rho = r_j/r_i < 1 and phase offset D
  (|D| < 45 deg) whose eight points are in convex position, i.e. rho > 1/(cos D + sin|D|). For t = 15 the best was 21.
- **Near misses (exact computation).** `sets/c4_56pts_2octagons_A.pts`, `_B.pts` and `c4_56pts_3octagons.pts`
  (scale 2^40): the ES8SYM pipeline (0 zero orientations; `cvx2` DP1 = DP2) and SIX60 `dfs_convex.c` on the integer
  coordinates (w0 - w2, w1 - w3) give exactly 2, 2 and 3 convex 8-subsets, each a pair of squares (rotation
  invariant), and no 9 points in convex position. So there are 56-point 4-fold sets in general position with exactly
  two convex octagons. (`verify_cfg` reports `layers_are_nested_convex_orbits: False`, as it must: the two squares of
  an octagon are not nested.)
- **Phase-fixed CEGAR at annealing optima.** At the exact phases of every 4-fold annealing optimum tested (77 phase
  vectors: the restart optima with N8 <= 400 and random perturbations of them) the formula is UNSAT at the first SAT
  call, before any LP cut (`pfenc.py`; the same with `gen.py`'s CNF and root units, `lpcegar2.py`). For the N8 = 2
  configuration `a4n1_2`, dropping the phase information of layer 12 or of layer 13 (its innermost twin pair) makes the
  formula SAT, but 1D scans of theta_12 and theta_13 (0.1 deg over the full range and 0.01 deg in the windows the SAT
  model suggests; 383 vectors) are all UNSAT, as are 48 fine scans of theta_13 for `a4n5_2`; trust regions up to all
  6,930 orbit variables: UNSAT. Alternating projections with the phase order as root units: the SAT step hit its
  conflict budget or the fit left 900-1,100 wrong signs.
- **Fixed-phase extension of the 52-point set.** The 13 phases of `c4_52pts_13layers.pts`, one new layer at every
  radius rank 0..13 with phase on a 1.5 deg grid, all 14 radii free (pfenc + pair cuts): 840 of 840 vectors UNSAT at
  the first SAT call.
- **Template phase scans** (radii left to the LP): spiral template (135 vectors) and multi-arm template (426 vectors)
  at t = 14: **all UNSAT at the first SAT call**. Calibration at t = 13 (52 points exist): among 87 spiral-template
  vectors, 15 answered CAND, 40 were undecided after 30 s and 32 UNSAT; 14 of the 15 have float N8 = 0 and pass the
  exact pipeline at some scale 2^30-2^50 (`logs/VERIFIED.tsv`; new 52-point 4-fold sets), the fifteenth had LP margin
  3.6e-9, below the LP tolerance, and 164 float octagons. Perturbing the 52-point set's own phases by 0.05 deg leaves
  9 of 12 vectors realisable. So at t = 13 the same pipeline finds sets easily; at t = 14 every tested phase vector is
  refuted before any LP cut.

### 2.2 Fivefold, 12 layers (60, or 61 with the centre)

- Annealing (4.2 M evaluations): best N8 = 310 (no centre), 330 (centre). The 33 phase vectors from these optima
  (with perturbations) are UNSAT at the first SAT call (pfenc + pair cuts).
- Fixed-phase extension of the 56-point set (11 phases + centre, one new layer at every rank 0..11, phase on a 2 deg
  grid, all radii free): 432 of 432 UNSAT.
- Templates at 12 layers: spiral (with centre) 79 vectors, multi-arm 501 (with centre) and 250 (without): all UNSAT at
  the first SAT call. Calibration at 11 layers + centre: spiral template 53 of 100 vectors live after 30 s (none
  realised within 30 s), multi-arm 4 of 179 live. The 56-point set is a tiny-cluster blow-up whose realisable phase
  region is very thin (§1.2: sigma = 0.05 deg destroys it), so phase templates are a weak test for blow-up type sets.

### 2.3 Threefold, 21 orbits (63 points, or 64 with the centre)

Starting points: the exact near misses of ES8SYM, `sets4/c3_64pts_3octagons.txt` (and its 63-point subset without the
centre) and `sets3/threefold60/control_cost3_63pts.txt` (63 points, no centre). Each has exactly one rotation orbit of
convex octagons, formed by the outermost orbit's point and one point of each of the next seven orbits.
- **Remove-and-reinsert** (each orbit deleted and re-inserted on a (log r, phase) grid with local refinement): best
  N8 = 3 for both near misses; adding one orbit to the four 60/61-point sets of ES8SYM (centre removed): best N8 = 18.
  Annealing from the near misses: best N8 = 3.
- **pfenc with pair cuts at the exact phases**: both versions of the first near miss, and the cost-3 near miss with the
  centre added (64 points), are UNSAT at the first SAT call. The cost-3 near miss without centre (63 points) stays
  live for a long time: best LP margin -4.2e-3, then UNSAT after 11,562 rounds (68 min).
- **Perturbations of the cost-3 phases**: sigma log-uniform in [0.01, 3.2] deg on all orbits, 54 vectors: 8 live
  after 150 s, 46 UNSAT; sigma = 0.05 deg on orbits 0..7, 36 vectors: 24 live, 12 UNSAT. Seven live vectors were
  run to a decision: **all UNSAT**, after 1,305 to 11,562 rounds (8 to 68 min), best margins -4.2e-3 to -9.3e-2 (one of
  them, a perturbation of the 64-point near miss, without pair cuts).
- **Template scans at 21 orbits** (radii left to the LP): multi-arm template, 45 vectors without and 53 with the centre:
  6 and 3 live, the rest UNSAT. Single-arm template (outer orbit + one spiral arm of 20 orbits; drift bounded by 0.45,
  0.08, 0.03 or 0.012 of 120 deg; with and without centre): 159 vectors, 85 live (timeout or conflict budget), 74 UNSAT,
  no realisation. Four live single-arm vectors had long runs (2.2-2.5 h each), none decided: best margins
  -1.5e-4 (17,237 rounds; no centre, arm drift 0.010), -1.7e-4 (14,000 rounds, stopped at 03:43), -2.8e-4 (64 points
  with the centre, 18,222 rounds), -1.3e-3 (20,947 rounds). Calibration at 20 orbits + centre (61 points exist): 6 of
  34 multi-arm vectors live, none realised within 60 s; so the 3-fold templates are not calibrated as well as the 4-
  and 6-fold ones.
- **Phases set free** (`slp.py`) from the best SAT models of these long runs: the margin rises to about +1e-9, below
  the LP tolerance, and the corresponding radii and phases have millions of float convex octagons; the same happens
  for a model near the 5-fold 56-point set, while a 6-fold model near a realisable region stalls at -3e-6. So the
  sequential LP reaches the boundary of realisability but never a robust realisation; it is not decisive.

### 2.4 Calibration: a new 6-fold 60-point order type (exact computation)

The spiral template at m = 6, t = 10 (outer hexagon, arm of 8 layers in near-twin pairs, one inner layer; 69 random
template vectors, 30 s each) gave one realisable vector (sample 58: phi0 = 0.132, drift 0.203, in units of 60 deg;
margin 4.8e-7). Rounded at 2^40 (`sets/c6_60pts_template_calibration.pts`, SHA-256 `344463a6…`): ES8SYM pipeline
EXACT-PREP, CVX2 and CROSSCHECK PASS; SIX60 `verify60.py` (independent, two DPs): largest convex subset 7; SIX60
`dfs_convex.c`: 34,220 / 295,419 / 1,089,684 / 1,504,342 / 343,302 convex 3- to 7-subsets, no convex 8-subset. Its
convex 4-set count differs from those of the five SIX60 sets, so it is a sixth order type. The 6-fold value 60 was
already exact (SIX60); the point is that the template + phase-fixed CEGAR pipeline finds 6-fold 60-point sets from
scratch, whereas the same pipeline finds nothing at 4-fold t = 14, 5-fold 12 layers or 3-fold 21 orbits.

## 3. Status of the claims

| claim | status |
|---|---|
| the k = 8 rows 3-fold >= 61, 4-fold >= 52, 5-fold >= 56 | unchanged |
| 56-point 4-fold sets in general position with exactly 2 convex octagons (`sets/c4_56pts_2octagons_{A,B}.pts`) | exact computation (ES8SYM pipeline + `dfs_convex.c`) |
| sixth 6-fold 60-point octagon-free order type (`sets/c6_60pts_template_calibration.pts`) | exact computation (three implementations) |
| pfenc encoding (chains without layers, suffix-sum units, pair cuts) is sound | written proof (not refereed), §1.2; tested on the 4-, 5-, 6- and 7-fold record sets |
| no realisation at the scanned phase vectors (all UNSAT answers above) | computational evidence only (numerical units and cuts) |
| 4-fold 56, 5-fold 60/61, 3-fold 63/64 do not exist | **not claimed** |

## 4. Most promising next steps

- 3-fold, 63 points: the single-arm template family (outer orbit plus one almost radial arm of 20 orbits, phase drift
  at most about 0.01 of 120 deg) gives the phase vectors closest to realisable (margin -1.5e-4 after 17,237 rounds,
  undecided). Longer runs on these and a denser scan of this family are the natural next step; a joint
  phase-and-radius method that keeps general position (the sequential LP here runs into degenerate limits) would be
  needed to turn a near-feasible model into a set.
- 4-fold: the obstruction is always a twin pair; templates that forbid twins (one layer per needle position) are only
  partly covered by the multi-arm scan.
- A certified version of the negative evidence would need exact (rational) forms for the sign units and pair cuts and
  LRAT proofs checked by cake_lpr; not attempted.

## 5. Files

- `sets/`: the near misses and the calibration set (exact `.pts`, ES8SYM format), `sets/float/` the float sources;
  `sets/SHA256SUMS.txt`.
- `tools/`: everything listed in §1 (copies; `gen.py` used by `lpcegar2.py` is `C7UPPER/gen.py`, `mf.py` is a copy of
  `<six10-work-dir>/realize/p2/mfold/tools/mf.py` with the evaluator replaced, `verify_mf.sh` a copy of the six10
  script).
- `logs/`: `summary.txt` (all counts), `VERIFIED.tsv` (every exact-pipeline run of the watcher), per-run result
  tables and logs (`logs/cegar/`, `logs/runs/`), `pairtest.txt`, the exact verification logs of the sets
  (`logs/exact/`).

## Reproduction

From this directory (Python with numpy, scipy and PySAT for the search tools; standard library for the exact checks):

```sh
mkdir -p src && gcc -O3 -shared -fPIC -o src/libcvxm.so tools/cvxm.c -lm && gcc -O3 -shared -fPIC -o src/libenumk.so tools/enumk.c
# pfenc validation at the phases of the certified 52-point set (expects CAND at round 1)
python3 -c "import sys; sys.path.insert(0,'tools'); from ptsio import *; from evm import countm
lr,th,c=read_pts_cfg('../ES8SYM/sets/c4_52pts_13layers.pts',4); write_cfg('c4_52.json',4,lr,th,c,countm(4,lr,th,c)[0])"
python3 tools/pfenc.py --m 4 --out val --tag v52 --tmax 30 --pairs 1 c4_52.json; cat val/res_v52.tsv
# exact checks of the sets
sh tools/verify_mf.sh sets/c4_56pts_2octagons_A.pts 4 0 chkA     # (edit its ES8SYM path T if needed) 2 convex 8-gons
python3 tools/verify_indep.py 4 sets/c4_56pts_2octagons_A.pts 8    # largest convex subset 8
python3 ../SIX60/verify/verify60.py sets/c6_60pts_template_calibration.pts   # largest convex subset 7
```
