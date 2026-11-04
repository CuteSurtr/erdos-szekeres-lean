# altcert: non-degree-2 certificates for the sixfold 60-point hard cores (5 Nov 2026, night)

Question: is the largest 6-fold octagon-free set in general position 54 or 60 points? The SIX10CEGAR run left 101
blocked "hard" abstract 10-layer models (10 clusters, one per cube; `SIX10CEGAR/hard_models`, decoded into
`<six10-work-dir>/models/`) that no degree-2 (PSD) certificate excluded.
This directory tried certificate types that are not degree-2 PSD forms.

Rigor labels: **exact** = accepted by an exact (integer/rational) checker; **written argument** = proof sketch here or
in a tool docstring (not refereed); **evidence** = numerical / floating point.

## Results in one paragraph

**All 101 hard models are excluded by exactly checked certificates** (`verify_all.tsv`; see the numbers at the end).
- **c11000 (15 of 15 models) and 3 of the 8 c10000 models violate the 3-term Grassmann-Pluecker (GP) relation**
  (324 and 112 violated relations respectively). The SIX10CEGAR lanes never ran the full GP scan. [exact]
- **Every other cluster is excluded by a biquadratic final polynomial (BFP, Bokowski-Richter)** on 3 layers
  (c00000, c00001, c01001, c10000, c10100, c11001, c11011, c11110) or 4 layers (c11111). The certificates avoid
  the cluster's free triple variables, so one clause excludes every member. The shortest is 36 literals
  (c10000, layers 2,5,9, 11 GP comparisons). [exact; two independent checkers; corruption tests]
- The complete directed product graph (all 4,551,260 rotation-reduced GP identities) is **acyclic** for all 83
  GP-consistent hard models, so plain product cycles cannot do it. The BFP log-LP is strictly stronger and is
  infeasible already on 3 layers. [exact for acyclicity; LP infeasibility certified by the extracted exact weights]
- Degree-4 Lasserre (U(1)-invariant, all localizing matrices): on the 3-layer subsets where BFP succeeds, degree 2
  has margin +2.0e-3 / +8.9e-4 and degree 4 still has positive margin (+1.2e-5 / +1.8e-8). So in these instances the
  degree-4 PSD relaxation does not separate, while BFP does. [evidence]
- A cut service (`daemon/`) runs BFP on the live CEGAR's blocked models and on fresh lane models, appending exactly
  checked clauses to `cegar/inbox/altcert_bfp.clauses`, until 04:35 KST.

## 1. GP relations (exact)

Identity (polynomial identity in the coordinates; verified symbolically with sympy in `gp/check_gp.py --selftest`):
`[abc][ade] - [abd][ace] + [abe][acd] = 0`. In general position all six brackets are nonzero, so the three terms
cannot all have the same sign.

- `gp/gp_scan.py`: all 10 * C(59,4) = 4,551,260 rotation-reduced relations (pivot a = vertex 0 of a layer).
- Violations: c11000 all 15 models (324 relations each); c10000 members 08e6fb6f, da3f2287, fac9ca3d (112 each);
  none elsewhere. The 324 c11000 clauses avoid the cluster's free variables.
- 436 distinct clauses -> `cegar/inbox/altcert_gp.clauses`. Each clause = negation of the model's six bracket literals.
- Checker `gp/check_gp.py` (stdlib; independent re-implementation of the orbit-variable semantics, cross-checked against
  `gen.py`): accepts all 436 witnesses and the per-model witness files with model binding (`gp/check_gp.log`).
  Corruption test (`gp/corrupt_test.log`): flipped literal 50/50 rejected, dropped literal 50/50, replaced variable
  50/50. Swapping b and c in the quintuple is (correctly) still accepted: it gives the same relation up to sign.

## 2. Product graph (exact, negative result)

`prod/run_full.py` + `tools/m6_full_products.c` (review's exact checker, unchanged): for each of the 101 models, all
4,551,260 identities, 9,102,520 edges, 9,848,610 product vertices. 83 models: graph **acyclic** (indegree pruning
removes every vertex). 18 models: the checker stops at the first GP violation (the 18 GP-violating models above).
So product cycles cannot exclude the cores (consistent with the review).

## 3. Biquadratic final polynomials (exact certificates)

**Certificate type** (written argument). For each GP relation with model signs, the odd-sign ("minority") term T_m
satisfies |T_m| = |T_j| + |T_j'| > |T_j| for both other terms j. Each term is a product of two brackets, and bracket
magnitudes are constant on rotation orbits (the sixfold rotation preserves areas). Take positive integer weights w_k on
such comparisons with sum_k w_k (e(T_m,k) - e(T_j,k)) = 0, where e(T) is the exponent vector of T in the orbit
magnitudes. Then prod |T_m|^w > prod |T_j|^w, yet both sides are the same monomial: contradiction. The certificate
uses only the GP identity, rotation invariance of magnitudes and general position: no radius order, phase or
convexity information. It is valid for every sixfold configuration in general position. The clause is the negation
of all bracket literals of the used relations.

**Search.**
- (evidence) Full 10-layer log-LP (9,097,072 distinct rows, 5,710 unknowns L = log|bracket orbit|): minimising
  sum max(0, 1 - A L)^2 with L-BFGS gives a stationary point (|A^T r|/|r| ~ 1e-6) with loss ~1.8e6-2.5e6 for all 9
  GP-consistent cluster representatives (`lp/batch_lbfgs.log`, `lp/dual_c11110.log`). On models of real random
  configurations the same code reaches loss 0 (`lp/sanity_lbfgs1.log`), and the true log-magnitudes satisfy all
  9.1M rows (`lp/sanity_real.py`, min row value > 0).
- (evidence) Layer subsets (`lp/subset_hinge.py`): for c11110_47b85004 all 2-layer subsets are feasible; 18 of the
  120 3-layer subsets and 64 of the 210 4-layer subsets are infeasible (all 3-layer ones contain layer 9).
- (exact) `lp/bfp_lib.py`: on a layer subset, the dual LP `y >= 0, A^T y = 0, sum y = 1` is solved by HiGHS. Then
  the exact integer kernel of A^T on the vertex support is computed with python-flint, giving positive integer
  weights. `lp/cluster_driver.py` does this for every 2-/3-layer subset (4-layer for c11111), keeping only the
  relations that avoid the cluster's free triple variables.

**Certificates** (`lp/certs/bfp_<cube>_L<layers>.json`, 6 per cluster with the shortest clauses):

| cluster | members | layers of shortest | comparisons | clause length |
|---|---|---|---|---|
| c00000 | 12 | 0,4,9 | 65 | 116 |
| c00001 | 13 | 0,1,7 | 26 | 68 |
| c01001 | 16 | see certs | - | 117-134 |
| c10000 | 8 | 2,5,9 | 11 | 36 |
| c10100 | 3 | 3,6,9 | - | 58 |
| c11001 | 1 | 1,3,5 | - | 98 |
| c11011 | 15 | 1,3,6 | - | 125 |
| c11110 | 3 | 0,3,9 | 92 | 127 |
| c11111 | 15 | 4-layer (see `lp/drv_c11111_k4.log`) | - | 218+ |
| c11000 | 15 | GP (section 1) | 1 relation | 6 |

**Checkers.**
- `lp/check_bfp.py`: stdlib; own orbit semantics; checks that the clause variables equal the bracket variables, the
  minority under the clause-falsifying assignment, the exact exponent cancellation, and the model binding.
- `lp/check_bfp2.py`: written separately. It takes literal semantics from `gen.py` (`E.o`) and re-derives the GP
  coefficients (1,-1,1) by symbolic expansion.
- Both accept all 49 + 6 cluster certificates. `inbox/altcert_bfp_clusters.checker.log` lists each certificate, checked
  without a model and against every member model of its cluster.
- Corruption tests (`lp/test_controls.json`, `lp/corrupt_bfp2.log`): 20/20 rejected for each of: weight +1, literal
  flip, dropped comparison, wrong minority, wrong other term, changed point. check_bfp2: 10/10 for each of five
  corruption kinds.

**Negative controls** (exact for the stated instances). Models of 8 real random sixfold configurations, 4 of them
multi-scale (radii log-uniform in [1e-6, 1]): 135 subset LPs each (all 3-layer subsets plus 15 four-layer ones) gave
**0 certificates** (`lp/test_controls.json`). This is required, since a real configuration admits none.

**Independent consistency check** (evidence). `sanity/grid_cert.py`: 24M random sixfold configurations of the
certificate's 3 layers (any phases; radii log-uniform down to 1e-8). None matches all literals of the c10000 L259 or the
c00001 L017 certificate; the minimum number of mismatches is 1. `sanity/grid3.py`: a 70^4 grid plus refinement on
layers 0,3,9 of c11110 finds no realization of the 138-orbit sub-pattern (minimum mismatch 1).

**Worked example** (c10000, all 8 members; layers 2, 5, 9; 36 literals; weights 1 except two of weight 2).
`lp/certs/bfp_c10000_L259.json` lists the 11 quintuples (a; b,c,d,e) with the minority and the other term index.
The product of the 11 weighted strict inequalities |T_m| > |T_j| has identical monomials on both sides.

## 4. Degree-4 relaxation (evidence only)

`las/las3.py`: complex seeds z in C^n on a layer subset, U(1)-invariant homogeneous level-2 moments (M2 = E[(z z)(z z)^*]
Hermitian PSD, M0 = E[vec(z z^*) vec(z z^*)^*] PSD), localizing E[s_t Q_t z z^*] PSD for every record, margin
E[s_t Q_t |z|^2] >= m, E|z|^4 = 1. Clarabel.

| instance | records | deg-2 margin | deg-4 margin (localizing) | deg-4 + all pair products |
|---|---|---|---|---|
| c11110_47b85004, layers 0,3,9 | 138 | +2.0e-3 | +1.2e-5 | see `las/las_c11110_039_prod.log` |
| c10000_4abab3b8, layers 2,5,9 | 138 | +8.9e-4 | +1.8e-8 | not run |

Degree 4 lowers the margin a lot but does not make it negative. The BFP certificates on the same sub-patterns are
exact. No degree-4 certificate was extracted.

## 5. BFP cut service for the live CEGAR (`daemon/`)

`daemon/bfp_daemon.py` (pid in `daemon/daemon.pid`, status in `daemon/STATUS`, log `daemon/daemon.log`; stops
itself at 04:35 KST) watches `cegar/shared/blocked_models.tsv` and the newest lane models. It runs
`lp/bfp_model.py` (all 2-/3-layer subsets, 4-layer fallback for blocked models with no 3-layer certificate),
re-checks every certificate with `check_bfp.py` (model-bound), and appends accepted clauses to
`cegar/inbox/altcert_bfp.clauses`, one log line per certificate in `altcert_bfp.checker.log`. Certificates are in
`daemon/certs/<tag>/`.

**Note for the coordinator.** Every blocked model processed so far received a BFP cut. So the lanes' blocked
assumptions can be replaced by certified cuts (see `daemon/daemon.log`, lines tagged BLOCKED). A lane method "BFP
on all 3-layer subsets" costs 2-30 s per model (`lp/bfp_model.py`). It would let the lanes stop blocking models
altogether.

## Reproduce

```
P=<six10-work-dir>/venv/bin/python
cd altcert/gp && $P gp_scan.py $(cat ../prod/all_models.txt) && $P make_gp_certs.py && python3 -I check_gp.py gp_all_witness.jsonl
cd altcert/prod && $P run_full.py $(cat all_models.txt)            # needs tools/m6_full_products (gcc -O2)
cd altcert/lp && KMAX=3 $P cluster_driver.py c00000 c00001 c01001 c10000 c10100 c11001 c11011 c11110
cd altcert/lp && KMAX=4 $P cluster_driver.py c11111
cd altcert/lp && python3 -I check_bfp.py certs/bfp_c10000_L259.json --model ../../models/c10000_4abab3b8.json
cd altcert/lp && $P -I check_bfp2.py certs/bfp_c10000_L259.json --model ../../models/c10000_4abab3b8.json
cd altcert && $P verify_all.py                                     # the 101-model table
cd altcert/lp && $P bfp_model.py MODEL.json OUTDIR --k 3            # cuts for any new model
```

## Files

- `tools/`: copies of `gen.py`, `m6_full_products.c` (+binary), `math_linear.py`, `sdp_ext.py`, and `common.py`.
- `gp/`: GP scan, witnesses, clause file, checker, logs.
- `prod/`: full product-graph runs.
- `lp/`: BFP code. Core: `bfp.py`, `bfp_lib.py`, `cluster_driver.py`, `bfp_model.py`, `check_bfp.py`,
  `check_bfp2.py`. Also: certificates in `certs/`, controls, corruption tests, hinge experiments, logs.
- `las/`: degree-4 relaxation experiment.
- `sanity/`: random and grid realization searches on certificate layers.
- `daemon/`: the cut service.
- `verify_all.py`, `verify_all.tsv`: final per-model table.
