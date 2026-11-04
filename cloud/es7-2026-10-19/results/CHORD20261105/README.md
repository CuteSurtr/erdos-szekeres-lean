# CHORD20261105: the chord lemma — orientation signs fixed by phases alone (5 November 2026)

**Summary.** The angular rules of `C7UPPER/gen.py` miss a simple family of orientation facts. When two of the three
points lie on one layer, a radius-free lemma fixes the sign from phases alone. This record states and proves the
lemma (written proof, not refereed) and generates its clauses for any m. For m = 6 it certifies each clause exactly,
and an independent reviewer verified the family by a second exact method. It also shows that, for the sixfold
10-layer encoding, the lemma is all the local degree-2 information that matters.

## 1. Lemma

Setting and conventions are those of `C7UPPER/gen.py`. The configuration is t nested regular m-gons about O, with
vertex (i,k) at angle theta_i + 360k/m and theta_0 = 0.
- **Even m:** theta_i = psi_i in (0, 360/m).
- **Odd m:** theta_i = psi_i + (0 if H_i else 180/m), with psi_i in (0, 180/m).
- In both cases Y(i,j) = [psi_i < psi_j].

**Lemma.** Let q1 = (j,k) and q2 = (j,k+d) be vertices of one layer, with ccw separation phi = 360d/m <= 180. Let p be
any other point.

1. **Chord (phi < 180).** Let n be the unit normal of the line q1q2 pointing away from O. If the direction of p makes
   an angle of at least 90 degrees with n, then orient(q1, q2, p) = +.
2. **Diameter (phi = 180, even m).** orient(q1, -q1, p) = sign(p . n), where n is q1/|q1| rotated by -90 degrees.

**Proof.**
1. The chord's line is {x : x . n = rho_j cos(phi/2)} with rho_j cos(phi/2) > 0, so O lies on its left side. If
   p . n <= 0, then p lies on the same side.
2. orient(q1, -q1, p) = det(-2 q1, p - q1) = -2 det(q1, p) = 2 |q1| (p . n). QED.

The angle between p = (i,l) and n is delta + 360(l - k)/m - phi/2 for a chord, and the same with +90 in place of
-phi/2 for a diameter. Here delta = theta_i - theta_j. Given the condition literals Y(i,j), H_i and H_j, delta ranges
over an open interval with rational endpoints in degrees. Whether the hypothesis holds is therefore decided exactly
by rational interval arithmetic. **No radius enters**: the clauses even hold without the nesting order.

`tools/chord_rules_m.py m t OUT` emits one clause per prime implicant of the condition region:
(orientation literal) OR (negated condition literals). It merges rules that hold under every case into units and
drops clauses subsumed by a unit. For m = 6 it reproduces the hand-derived `tools/chord_rules.py` family exactly as
a set: 976 clauses, `data/chord_m6t10.clauses`.

## 2. Exact certificates and checks (m = 6)

- **A degree-2 certificate for every clause** (`tools/chord_certs.py`, `data/chord_m6t10_certs.jsonl`).
  - The records are the opposite orientation plus the phase rows of the two layers: s E_ij bound to the Y literal,
    and D_ij +- E_ij > 0, which hold because |theta_i - theta_j| < 60.
  - The mixed part of the orientation form is cancelled exactly by a nonnegative combination of phase rows (a 2-D
    Farkas step solved in rationals).
  - What remains is a nonpositive multiple of D_jj, or 0 for diameters.
  - `tools/clausecert_check.py` rebuilds every form in oblique coordinates and shares no code with the generator. It
    runs a complete exact PSD test and checks clause polarity: 976/976 pass, and 200/200 corrupted copies are
    rejected.
- **Real configurations.**
  - `tools/chord_validate.py` and `chord_validate_m.py`: 0 violations on 1,260 random sixfold configurations, with radii
    down to e^-16 and phases within 1e-6 of every boundary. Also 0 violations on 150 random configurations each for
    m = 4, 5, 7.
  - `tools/chord_check_sets.py` (80-digit): every applicable clause holds on the certified sets
    `ES8SYM/sets/c6_54pts_9layers` (780 clauses), `sets3/c5_56pts_11layers_centre` (1,472) and
    `sets/c4_52pts_13layers` (745).
  - Every clause holds on both exact 60-point sets of `SIX60`.
- **Independent review** (`review/`; a separate agent was asked to refute the claim).
  - The reviewer checked the written proof and the soundness of every row type.
  - It proved each of the 976 clauses by its own exact method, `review/check_angles.py`: sign tests of sinusoids at
    interval endpoints in Q(sqrt3), with no certificate and no radius assumption.
  - It re-checked the certificates in Cartesian Q(sqrt3) arithmetic (`review/check_certs_cart.py`).
  - It ran 20,144 adversarial 80-digit configurations: 6,000 random in six modes and 14,144 targeted at interval ends.
  - It found no violation, and negated clauses were all caught.
  - Verdict: **survives**.

## 3. What the lemma adds to the encoding

- **Sixfold, t = 10.**
  - The family has 976 clauses (544 units, 432 binary). Of these, 524 are new against the base CNF
    (`data/chord_m6t10_new_vs_base.clauses`): 352 diameter, 162 edge and 10 short-chord. The encoder gives no clause
    for a triple containing an antipodal pair ("degenerate").
  - 90 of the 101 "hard" models of `SIX10CEGAR` violate the family.
  - The last uncertified cluster, c11111 (15 models), falls to one instance: orient(4.0, 9.4, 9.5) with
    theta_9 < theta_4, found as a 2-record degree-2 certificate.
  - The `SIX10CEGAR` lanes always ran their SDP with `--no-phase --no-radius`, so these certificates were invisible
    to them.
- **5-fold, t = 13:** 2,126 clauses (`data/chord_m5t13.clauses`), of which 882 are new to `gen.py 5 8 13`
  (90 units, 396 binary, 396 ternary).
- **4-fold, t = 17:** 1,313 clauses (`data/chord_m4t17.clauses`), of which 801 are new to `gen.py 4 8 17`
  (321 units, 480 binary).
- No chord unit contradicts a base unit in any case.

## 4. The lemma is all the local degree-2 information (m = 6, t = 10)

An independent agent (`localrules/`, its own code) decided every (orbit triple, sign, phase order of its <= 3
layers) case. It used degree-2 certificates over triple, phase, radius and nesting records supported on those layers.
- **Exact.** 3,268 certificates (1,108 unit, 1,656 binary, 504 four-literal), all accepted by
  `tools/clausecert_check.py`. 0 cases were left uncertified and 0 conflicts were found.
- **Complete for this row family** (evidence with a clear gap, `localrules/margin_summary.json`). Over all 46,412
  cases the best achievable maximal eigenvalue is <= 1e-6 when certified and >= (sqrt2 - 1)/4 otherwise.
- **New beyond base + chord:** exactly 672 three-layer binary clauses (`localrules/local_rules_new.clauses`). The
  facial workstream's independent sweep found the identical set. They cut 0 of the 101 hard models and 0 of 400 CEGAR
  models.
- **Units.** Three independent sweeps were compared: linear-lift (`nfunits`), degree-2 facial, and this lemma. They
  give 928 distinct forced units with no contradiction. The 308 units absent from the base CNF are exactly the chord
  lemma's new units.

## 5. Other checks in `tools/`

- `gpcheck_indep.py` independently re-checks the 436 Grassmann–Plücker cuts produced in the campaign.
- `facial_indep.py` independently re-checks the facial-reduction certificates of the ten `SIX10CEGAR` clusters, in
  oblique coordinates and bound to the original cluster files. All 101 models are excluded.
- These certificates matter for history only, since `SIX60` settles the sixfold question by a construction.

## 6. Independent review of the general-m generator (m = 5, 4; `review_m/`)

A second reviewer, asked to refute `tools/chord_rules_m.py`, found no unsound clause (verdict: **survives**).
- **Line-by-line check** of the odd-m phase model (theta = psi + (0 if H else 180/m)), the Y and H polarities, layer
  0, the prime implicants (every Y/H combination is realizable) and the merging.
- **An exact verifier sharing no code with the generator** (`review_m/verify_exact.py`). For two-layer triples,
  orient / r_J^2 = sin(c0) + lambda [sin(delta + c2) - sin(delta + c1)] for all lambda > 0. The zeros of the bracket
  are located in rationals and signs are evaluated with 80-digit intervals.
  - All 2,126 (m = 5, t = 13) and 1,313 (m = 4, t = 17) clauses are proved, including every clause added to the
    threshold formulas.
  - Every mutated control is rejected: flipped orientation, dropped or negated condition literal.
- **Stress tests.** 12,000 random configurations (20.6M clause evaluations) and 1.8M corner evaluations, with phases
  within 1e-14 of every boundary and radius ratios from 1e-12 to 1e12: 0 violations.
- **Certified sets, in exact arithmetic.** The 5-fold 56-point set (Q(sqrt5) signs) satisfies all 552 applicable
  clauses, and the 4-fold 52-point set (Gaussian integers) all 481.
- **Consistency with the base formulas.** No conflict with the units of `gen.py 5 8 13` or `gen.py 4 8 17`. The 36
  cube files contain exactly the reviewed clauses plus their units.
- **Caveat stated by the reviewer.** The cube cover (reflection unit and phase-order split) was not part of this
  review. It follows `ROT456`/`C7UPPER` §2. The 40 + 20 transitivity-violating patterns were refuted again with the
  chord clauses added, with LRAT proofs accepted by lrat-check (5 November).

## Reproduction

Run from this directory; `ES_RESULTS` defaults to the parent results directory.

```sh
python3 tools/chord_rules_m.py 6 10 out.clauses        # set-equal to data/chord_m6t10.clauses
python3 tools/clausecert_check.py data/chord_m6t10_certs.jsonl
python3 tools/chord_validate_m.py 5 5 150 1           # m t configurations seed
python3 tools/chord_check_sets.py ../ES8SYM/sets3/c5_56pts_11layers_centre.pts 5   # needs mpmath
```
