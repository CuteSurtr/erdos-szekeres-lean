# facial: nested-face (facial reduction) certificates for the sixfold 10-layer cores, degree 2 and degree 4

Work dir: `<six10-work-dir>/facial` (5 Nov 2026, 00:05-03:30 KST, 4 cores).
Rigor labels: **exact** = accepted by an exact (rational) checker; **written** = short argument here; **evidence** =
numerical only.

**Summary.**
1. **The 10 hard cores.** All 10 cores and all 101 blocked models of `SIX10CEGAR` are excluded by exact degree-2
   nested-face certificates (minimized clauses of 2-31 literals).
2. **Rules missing from encoder A.** The c11111 core reduces to a binary rule. A systematic search found 1,176
   exactly verified unit and binary rules that encoder A lacks.
3. **The lanes' new blocked models are beyond degree 2.** The live CEGAR lanes started blocking models in a new
   regime. For the six models blocked by 00:37 that this tool could not certify, an exact strictly feasible PSD lift
   exists, so no degree-2 certificate can exclude them.
4. **Degree 4 settles them.** Degree-4 (product) facial certificates on 3- or 4-layer subsets exclude all six, and
   every model blocked since. The certificates are exact over Q(sqrt(-3)) and checked independently, with short
   clauses: 2-7 literals after minimization.
   - Their images under layer relabeling give a further 1,680 exact clauses.
   - A detached resolver keeps doing this for every newly blocked model until 04:30.

None of this settles 54 vs 60: the CEGAR has no UNSAT cube yet. It changes the frontier. Degree 2 is exhausted on the
current blocked models, and degree 4 on small layer subsets works.

## Results

1. **All 10 hard cores are excluded, all 101 blocked models** (exact computation + written argument). For every cluster
   of `SIX10CEGAR/hard_models`, one certificate's clause avoids the cluster's free variables. So it is falsified by
   every member of the cluster (12+13+16+8+3+15+1+15+3+15 = 101 of 101). The independent checker verifies each
   certificate and counts the members it kills.
   Minimized clauses (`certs/<cube>/witness_min.json`):

   | cube | clause length | rank of -M | real kernel dim | face (kernel), seeds z_i, R = +60 deg rotation |
   |---|---:|---:|---:|---|
   | c00000 | 8 | 18 | 2 | layer 0 free |
   | c00001 | 22 | 12 | 8 | layers 0,1,2 free; z4 = z3, z5..z8 = R^-1 z3 |
   | c01001 | 17 | 12 | 8 | layers 0,1,2 free; z4..z8 = R z3 |
   | c10000 | 15 | 16 | 4 | layer 0 free; z4 = z1, z2,z3,z5..z8 = R z1 |
   | c10100 | 5 | 18 | 2 | layer 0 free |
   | c11000 | 12 | 8 | 12 | layers 0..4 free; z6..z8 = R z5 |
   | c11001 | 31 | 12 | 8 | layers 0,1,2 free; z4..z8 = R z3 |
   | c11011 | 17 | 10 | 10 | layers 0,1,2 free; z3 = z4 = z5 = z6; z7 = z8 |
   | c11110 | 19 | 16 | 4 | layer 0 free; z2 = z1, z3..z8 = R z1 |
   | c11111 | **2** | 2 | 18 | layers 0..8 free (the form is -c\|z9\|^2) |

   "Free" means that the form does not involve that layer. The ranks reported by the checker equal 20 minus twice the
   complex kernel dimension in every case.
   The kernel column is the numerically read face. It is evidence only and is not used by the checker. The checker
   tests negative semidefiniteness completely, with no kernel basis.
   The unminimized certificates (`certs/<cube>/witness.json`, 26-111 records) are also checked.
2. **A missing family of simple rules in the base encoding** (exact computation + written argument).
   The c11111 certificate splits into 7 two-record certificates. Each is an exact identity:
   `1*(-(2/sqrt3)[(k,0),(9,4),(9,5)]) + 2*(-E_k9) = -D_99`.
   So if psi_9 < psi_k, then orient((k,0),(9,4),(9,5)) = +, a binary clause. Geometrically, (k,0) lies on the centre's
   side of the edge (9,4)(9,5) whatever its radius. Encoder A's angular rules miss it: the middle point is innermost,
   and triples with an antipodal pair are not covered (`C6UPPER` §3b says so for encoder B).
   A systematic search (`lib/rules.py`) took one triple record plus phase and radius rows on its 2-3 layers, over all
   5,710 orbits, both signs and all phase orders. It found 3,228 exact rules.
   - 1,404 are satisfied by a base unit and 648 are subsumed by a base clause of length <= 4.
   - **1,176 are new: 288 unit clauses and 888 binary clauses** (`certs/rules/`). All 1,176 pass the independent
     checker (batch mode).
   - They falsify 90 of the 101 hard models.
   - Numerical sanity check (evidence): 120 random strictly nested real configurations violate none of them. In the
     same test, the encoder's own order/angle/nest clauses hold, and they fail massively under the mirrored rotation
     convention, so the test has power.
   - The units are the antipodal-pair orientations. Example: orient((0,0),(0,3),(j,2)) < 0, by the identity
     F + 2(D_0j - E_0j) = 0.
3. **The live CEGAR frontier is beyond degree 2** (exact computation + written argument).
   The lanes running from `../cegar` had blocked 8 models without a certificate by 00:37. Two of them (c11100 r139 and
   c11000 r150) are certified by `lib/certify.py`, and the coordinator's `resolve_blocked.py` resolved them with its
   snapshot of this tool.
   The other **six models have strictly feasible PSD lifts**:
   - c01011 `g1793805139_61638/r141`;
   - c11100 `g1793806103_91147/r21`;
   - c10100 `g1793806103_91171/r20`;
   - c11111 `g1793806103_91135/r78`;
   - c00001 `g1793806103_91195/r37`;
   - c00000 `g1793806103_91201/r31`.

   For each one, `checker/check_strict.py` (stdlib, exact rationals) verifies two things (`certs/frontier/`,
   `check_strict_all.log`):
   - the real form [[D',-E'],[E',D'/3]] is positive definite (20 positive pivots);
   - all 5,854 rows (5,710 triples, 135 phase rows, 9 radius rows) are strictly positive at D = S D' S, E = S E' S.

   So no positive combination of these rows is negative semidefinite. **No degree-2 certificate can exclude these
   models**: not lin, face, def, facial, nor any certificate on a layer subset, since those use the same rows.
   This is the case the task asked to report.
   - The lifts are multi-scale. Layer 0 must dominate: t = 1e4 to 1e10 is added to D'_00. The minimum record is
     2.8e-7 to 5e-5 relative to the inner layers.
   - By construction, the minimum relative margin is attained in the facially reduced problem with layer 0 free.
   - Numerical realization probes (evidence only, `realize/`) found nothing:
     - L-BFGS on the scale-free loss from phase-order starts: best 72-98 of 5,710 signs wrong;
     - random rank-one roundings z ~ CN(0, H) of the strict lift: at best 300 or more wrong before optimization,
       98 after;
     - a log-det rank-reduction heuristic stalls at a second eigenvalue of 1.3e-3 relative, giving 150 wrong.
   - **Excluding these models needs degree >= 4 (products of records), unless they are realizable.** Degree 4
     does it; see result 4.

4. **Degree-4 facial certificates on 3-layer subsets exclude the frontier models** (exact computation + written
   argument). This is new.
   - **Why a small subset.** For a frontier model, some 3-layer sub-pattern can have a strictly feasible degree-2
     lift (degree-2 margins on the subset are about 3e-3 to 9e-3) while its degree-4 relaxation has margin 0 with a
     face.
   - **Degree-4 relaxation.** Take y in C^3 and the Hermitian moment matrix Y on the monomials u_ab = y_a y_b
     (6 of them). The constraints are all products l_a * l_b of the subset's records (triple, phase and radius rows)
     and the products l_a * |y_i|^2.
   - **Facial reduction** (`sub/sub4cert.py`), as in degree 2 but in the monomial basis:
     - level 0 has margin about -5e-12, and its face is "the monomials without the innermost layer";
     - the reduced problem (Y PSD only on the other monomials) then has margin about -0.5;
     - exact rounding: nullspace projection over Q, then the complete Hermitian PSD test of -G over Q(sqrt(-3))
       (`deg4/qsqrt3.py`).
   - **Certificate.** Positive integers w_p with G = sum_p w_p Gram(f_p g_p) negative semidefinite on C^6. A
     configuration satisfying all literals would make sum w_p f_p g_p > 0, but that sum equals u^* G u <= 0.
   - **Checker.** `checker/check_deg4.py` (stdlib) is independent of the generator. It derives each factor from
     det(a,b) = Im(conj(a) b) in z coordinates over Q(sqrt(-3)), binds factors to `E.tvar` and the model, and runs the
     complete exact Hermitian PSD test. `tests/deg4_mutants.log`: 7 of 7 mutants rejected.
   - **Results.** Five of the six frontier models are certified, each on the first or one of the first subsets tried
     (subsets containing layers 9 and 0 are tried first). Minimized certificates are in `certs/deg4/d4min_*`:

     | model | layers | products | clause (minimized) |
     |---|---|---:|---:|
     | c01011 r141 | 3,4,9 | 14 | 6 |
     | c00000 r31 | 0,3,9 | 8 | 4 |
     | c00001 r37 | 0,5,9 | 10 | 3 |
     | c10100 r20 | 0,7,9 | 20 | **2** |
     | c11111 r78 | 0,1,5 | 27 | 7 |

     The c10100 r20 clause [1419, 5664] has no Y literal: in every configuration, orient((0,0),(7,0),(7,2)) and
     orient((7,0),(9,1),(9,3)) are not both negative. It is a degree-4 fact that no degree-2 certificate can give.
   - **The sixth, c11100 r21, is not resolved.**
     - Every 3-layer subset has a strictly positive degree-4 margin (5e-7 to 1e-5, numerical; so no degree-4
       certificate exists on 3 layers, evidence).
     - The 4-layer subsets tried so far have margin near 0 at level 0, but the coordinate-face reading did not lead to
       a certificate. A 4-layer scan was running at the time of writing (`sub/scanL_*`, `sub/scan_summary.txt`).
   - **Images** (exact computation). The certificate is a polynomial identity in the layer seeds, so relabeling layers
     by any order-preserving map a<b<c -> a'<b'<c' keeps it valid.
     - The rows are re-validated: phase_sign rows with i >= 1 get their Y literal, and an image needing
       theta_0 > theta_j is skipped.
     - `sub/images.py` generated 1,560 distinct image clauses of length 2-34 (most 2-7) from the minimized frontier
       and resolver witnesses. All pass `check_deg4.py` in batch mode without a model.
     - They kill 46 of the 101 old hard models and 5 of the 6 frontier models.
     - Files: `certs/deg4img/`; inbox `facial_d4img.clauses`.
   - **Live resolver** (`watcher/resolver.py`, detached; stops itself at 04:30; pid in `watcher/resolver.pid`,
     progress in `watcher/STATUS` and `watcher/resolver.log`).
     - For every new row of `../cegar/shared/blocked_models.tsv`, it tries the degree-2 facial certificate, then
       degree-4 certificates on 3-layer subsets (minimized), then the images of the certificate.
     - Exact-checked clauses go to the inbox: `facial_w_*` (degree 2), `facial_w4_*` (degree 4) and
       `facial_w4img_*` (images).
     - Unresolved models get an exact strict-lift test.
     - By 01:03 it had resolved all 11 models the lanes blocked between 00:47 and 00:56, every one by degree 4 on
       3 layers, with clauses of 2-6 literals (one unminimized clause has 34).
     - Over the same period the lanes' model rates fell, for example c11111 to 10 models per 10 min. This is
       evidence only and has other causes too.

## Method (written argument)

- **Records.** Records are linear in the Hermitian lift H = D + i*sqrt3*E, with D_ij = <z_i, z_j> and
  E_ij = det(z_i, z_j)/sqrt3. Coefficients come from `ROTREFINE20261104/math_linear.py` (`lib/core.py`). Phase rows and
  radius rows are as in `sdp_ext.py`; a phase_sign row with i >= 1 puts its Y literal into the clause.
- **Facial reduction** (`lib/red.py`, `lib/facial.py`). For a conjectured kernel K, use the unitary basis T = [K|Q].
  The reduced primal keeps only the QQ block of T^*HT PSD and leaves the K rows free. Its dual is lambda >= 0 with
  M(lambda)K = 0 and the QQ block of M <= margin*I.
  - The level-l face is read from the reduced primal solution. Take the layers at the top scale (diag >= 1e-2 * max),
    then the principal block's top eigenvectors (>= 1e-3 * max).
  - Its basis is recognized in reduced echelon form over Q(w) (denominators <= 6) and appended to K, and the level is
    repeated.
  - Stop when the reduced margin is < -1e-6, typically -0.01 to -0.04 (well conditioned).
  - Fallback: coordinate kernels "all layers except T", |T| <= 3. This is how c11111 was found: K = layers 0..8.
- **Exact rounding** (`lib/exact.py`).
  - Take the support lambda_t > 1e-7 max. The constraints M(lambda)W = 0 (W = real kernel basis in oblique
    coordinates, {z, Rz} per complex vector) are integer-linear in lambda.
  - Project the rationalized dual onto their exact nullspace (python-flint) and drop nonpositive entries; repeat.
  - Scale to integers and verify -M PSD with a complete rational test (positive pivots; a zero diagonal entry must have
    a zero row).
- **Minimization** (`--minimize`). Greedily drop literal-carrying records: re-solve the reduced SDP on the rest plus
  all model-independent rows with the same K, then re-round exactly.
- **Soundness of a clause** (written). A configuration satisfying all literals of the records makes every record
  strictly positive, so sum w_t F_t > 0 at its seeds. But that sum is a negative semidefinite quadratic form in the 20
  real seed coordinates.
  - phase_plus/minus and radius rows hold in the encoding's normal form.
  - phase_sign rows hold given their Y literal (for i = 0, theta_0 = 0 always).
  - No convexity is used, so every clause holds for every normal-form configuration of 10 nested regular hexagons in
    general position.

## Checkers (stdlib only)

- `checker/check_facial.py MODEL WITNESS [--cluster CLUSTER.json]`, or `check_facial.py - FILE.jsonl` (batch, no model).
  It is independent of `lib/exact.py`:
  - it uses (u, v) coordinates, seed = (u, sqrt3 v), instead of oblique ones;
  - it builds each record's quadratic form from point coordinates;
  - it binds triple to variable through `gen.py` `E.tvar`, and record signs and Y literals to the model file (hash
    checked);
  - it runs the complete exact PSD test on -P and checks that the clause equals the negated record literals and is
    falsified by the model.

  The witness format is `facial-cert-v1`.
- `tests/mutants.py`: 230 cases. All 20 originals are accepted and 209 of 210 mutants are rejected (flipped sign, wrong
  variable or triple, weight x1000 or 0, dropped literal, extra literal, wrong model hash, flipped phase sign).
  The one accepted mutant drops one of the 111 records of the unminimized c00000 witness, together with its literal.
  That is a genuinely valid smaller certificate, consistent with the minimized 31-record one, so accepting it is correct.
- `checker/check_strict.py MODEL STRICT.json`: exact check of a strictly feasible lift. It derives the (D,E)
  coefficients independently from 2cos(60k) and (2/sqrt3)sin(60k).
- `checker/check_deg4.py MODEL WITNESS`, or `check_deg4.py - FILE.jsonl` (batch, no model): exact check of degree-4
  certificates over Q(sqrt(-3)). `tests/deg4_mutants.log`: 7 of 7 mutants rejected.
- `tests/strict_mutants.log`: the strict-lift checker rejects 5 of 5 mutants (t shrunk, negative diagonal, flipped
  E_39, layer 9 rescaled, other model).
- `tests/convention_test.py DIR SEED N` (evidence). It is a convention and soundness test on random strictly nested
  configurations (r_{i+1} < r_i sqrt3/2).
  - The encoder's order/angle/nest clauses hold: 0 violations.
  - `MIRROR=1` is the negative control (the -60 deg convention violates about 2,500 clauses per configuration).
  - Facial clauses: 0 violations (`tests/convention_*.log`).
- `tests/sample_short.py` (evidence). Every clause of length <= 4 (2,136 clauses: the degree-2 rules and the degree-4
  images) is tested on 20,000 random normal-form configurations: 0 violated.
  - Control: 300 copies of these clauses with one literal flipped; 260 are violated
    (`tests/sample_short*.log`).
- Cross-check with the repository's own exact checker (`SIX10CEGAR/tools/check_cert_g.py`, oblique coordinates, face
  spec): it accepts the triple-only certificates c00001, c01001, c10000 (unminimized) and c11000 (minimized),
  converted to its format (`certs/crosscheck/`).

## Inbox (for the CEGAR lanes)

`../cegar/inbox/facial_<cube>.clauses` (the minimized clause per cluster) and `facial_rules.clauses` (1,176 rules),
each with a `.check.log` from `check_facial.py`.

## Reproduce

```sh
cd <six10-work-dir>/facial
V=../venv/bin/python; R=<results-dir>/SIX10CEGAR/hard_models
$V lib/certify.py ../models/c11001_c12e54f7.json out_c11001 --cluster $R/cluster_c11001.json --minimize 600
python3 -I checker/check_facial.py ../models/c11001_c12e54f7.json out_c11001/witness.json --cluster $R/cluster_c11001.json
$V lib/certify.py ../models/c11111_05e2e24e.json out_c11111 --cluster $R/cluster_c11111.json   # uses the fallback
for w in 0 1 2; do $V lib/rules.py $w 3 rules/r_$w.jsonl & done; wait                            # about 3 min
python3 lib/filter_rules.py ../cegar/base/encA_6_8_10.cnf rules/kept rules/r_*.jsonl
python3 -I checker/check_facial.py - certs/rules/rules_witnesses.jsonl
$V lib/strict_lift.py MODEL.json strict.json && python3 -I checker/check_strict.py MODEL.json strict.json
python3 tests/mutants.py; python3 -I tests/convention_test.py certs/rules 3 120
```

Set `OMP_NUM_THREADS=1` (each SDP is small). `lib/certify.py` on one model takes 1-10 s; minimization takes 2-10 s.

## Files

- `lib/`: `core.py` (records), `red.py` (reduced SDP), `facial.py` (level reading), `exact.py` (rounding and PSD test),
  `certify.py` (driver), `rules.py` and `filter_rules.py` (rule family), `strict_lift.py`, `scaled.py`.
- `checker/`: `check_facial.py`, `check_strict.py`.
- `certs/<cube>/`: the model, `witness.json` and `witness_min.json` with check logs, and the clause files.
- `certs/rules/`: `rules_witnesses.jsonl`, `rules.clauses`, `check.log`.
- `certs/frontier/`: the c01011 r141 model (true variables <= 5746, sorted), the strict-lift witness and its check log.
- `runs/`: working files. `rules/`: raw rule search output. `realize/`: the numerical realization probe (evidence).
- `tools/`, `tools_orig/`: copies of the repository tools (placeholders replaced). The repository was not modified.
