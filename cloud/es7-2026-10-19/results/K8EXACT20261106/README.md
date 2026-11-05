# K8EXACT20261106: exact check of the 7-fold 64-point sets against encoders B and A

6 November 2026 (KST; the logs carry UTC times). Computer-assisted. Modelled on the 4 November exact 6-fold re-check
(`C6C7REVIEW/tests/certified54.py`, `C6UPPER` §5). The encoder-A part was added on 6 November after review.

## Result

**Exact computation.** The eight 7-fold 64-point files cover the seven order types listed in `PRIMEFOLD` §3. Each
is a centre plus 9 heptagons. For each file, both the set and its mirror image were taken. The centre was dropped,
giving 9 nested regular heptagons (63 points). For those 16 configurations:

- all 41,664 orientation signs of the 64-point set (39,711 triples of the 63 points and 1,953 triples through the
  centre) are nonzero, computed exactly;
- the geometric assignment was derived exactly: the orientation of each of the 5,673 triple-orbit representatives,
  the 28 phase-order variables Y(i,j) and the 8 half-sector variables H(i);
- **encoder B** (`C6UPPER/encb/gen_b2.py 7 8 9`, SHA-256 `67cd613d…`): with the chain variables set to their least
  model, the full assignment satisfies **every one of the 1,765,351 clauses**. There are **0 violations** in each of
  the four families, in all 16 cases;
- **encoder A** (`C7UPPER/gen.py 7 8 9`, SHA-256 `bb85a966…`, the recorded 9-layer formula, regenerated here and
  matching): the same holds. With A's own variable map and the chain variables at their least model, **every one of
  the 1,765,351 clauses** is satisfied, with **0 violations** in each family, in all 16 cases;
- a separately written clause checker (`satcheck.py`) confirms 0 unsatisfied clauses for all 32 dumped assignments
  (16 for B, 16 for A);
- **H(1) flips** between each set and its mirror, in all 8 files. In fact every H(i) flips and every Y(i,j)
  reverses, as the reflection argument predicts (theta_i to 2pi/7 − theta_i);
- **A with the unit H(1).** The certificate formula is A(7,8,10) plus the unit clause H(1). At 9 layers, for each of
  the 8 files exactly one of the set and its mirror satisfies A(7,8,9) together with the unit H(1): the mirror for
  the four `c7_*` files, and the set itself for the other four.

**Exact computation (hash checks).** The generators were run again under the one-core cap. They reproduce the
recorded formulas byte for byte:
- `gen_b2.py` (SHA-256 `3d47459a…`, as recorded in `C6UPPER/SHA256SUMS.txt`):
  - `B_m7K8t10` `b4d290176cb675c6…` (`p cnf 80080 2748538`);
  - `B_m6K8t9` `9f63854369a76998…` (`p cnf 42728 1040348`).
- `gen.py` (`4564e7f0…`) and `addunits.py` (`c6654fa5…`), both as recorded in `C7UPPER/SHA256SUMS.txt`:
  - `A_m7K8t9` `bb85a9666902ab91…` (`p cnf 58136 1765351`), the formula checked above;
  - `A_m7K8t10` `1a7c0e706f2a7fb5…` (`p cnf 80080 2748538`);
  - `A_m7K8t10` + unit 7857 `fa297b5bd6608d29…` (`p cnf 80080 2748539`), the certificate formula. gen.py's meta file
    shows that variable 7857 is H(1) at 10 layers.

The regenerated CNFs were deleted afterwards. Only their hashes are kept (`logs/regen_hashes.log`,
`logs/regen_hashes_A.log`, `logs/gen_A_m7K8t9.log`).

**Scope.** This is a finite validation of encoders A and B at 9 layers on 16 real configurations. Real
octagon-free configurations must satisfy a sound encoding, and these do. It is not a soundness proof of either
encoding, which remains a written proof (Lean-checked in part, `LAYERLEAN`). `C7UPPER` §4 had tested these sets
against encoder A's 9-layer formula in floating point (float64, and 150-digit Decimal for three sets). Here both
encoders are checked in exact arithmetic. No SAT solver or proof checker is used here, and no file outside this
directory was changed.

## The sets

`PRIMEFOLD` §3 lists seven pairwise non-equivalent order types in eight files. `p7_two_orbit_64` has the same
orientation table as `p7_compound_64`, and both files were checked. The five `ES8SYM/sets` copies are byte-identical
to the `PRIMEFOLD/sets/k8` files (`logs/sets.txt`). The 63-point set `ES8SYM/sets/c7_63pts_9layers.pts` is not a
64-point set and was not checked here.

| file (`PRIMEFOLD/sets/k8/`) | SHA-256 | H(1..8) orig / mirror | psi order orig | min \|det\| | B chain vars true orig / mirror | A chain vars true orig / mirror | violations B / A |
|---|---|---|---|---:|---:|---:|---:|
| `c7_64pts_small` | `ebe028f6…` | 00000000 / 11111111 | 0<8<7<…<1 | 1.46 | 17,713 / 16,682 | 16,682 / 17,713 | 0 / 0 |
| `c7_64pts_9layers_centre` | `23e1389d…` | 00000000 / 11111111 | 0<8<7<…<1 | 2.16e17 | 17,708 / 16,714 | 16,714 / 17,708 | 0 / 0 |
| `c7_64_own_s1000` | `c9942cc1…` | 00000000 / 11111111 | 0<8<7<…<1 | 2.64 | 17,645 / 16,991 | 16,991 / 17,645 | 0 / 0 |
| `c7_64pts_9layers_centre_own` | `ec481469…` | 00000000 / 11111111 | 0<8<7<…<1 | 3.07e4 | 17,612 / 17,011 | 17,011 / 17,612 | 0 / 0 |
| `p7_compound_64` | `ef50ee00…` | 11111111 / 00000000 | 0<1<2<…<8 | 1.00e9 | 16,686 / 17,852 | 17,852 / 16,686 | 0 / 0 |
| `p7_two_orbit_64` | `9a55f245…` | 11111111 / 00000000 | 0<1<2<…<8 | 9.99e9 | 16,686 / 17,852 | 17,852 / 16,686 | 0 / 0 |
| `rule_p7_64pts` | `bb38d29a…` | 11111111 / 00000000 | 0<1<2<…<8 | 2.36e13 | 16,928 / 17,957 | 17,957 / 16,928 | 0 / 0 |
| `m7_x2_G9s_centre` | `ac524df7…` | 11111111 / 00000000 | 0<1<2<…<8 | 1.13e22 | 16,330 / 18,255 | 18,255 / 16,330 | 0 / 0 |

"violations B / A" counts both cases (set and mirror) of each file.

Notes on the columns:
- "min |det|" is the 200-digit Decimal value of the smallest orientation determinant among the 63 layer points (in
  the file's coordinates). It is evidence only; the signs themselves are exact.
- In every case the phases are monotone in the layer index, and all H(i) are equal. The mirror's phase order on
  layers 1..8 is the reverse of the original's.
- Y(1,2) equals H(1) in every case here.
- Each mirror is psi_i -> pi/7 − psi_i.
- **Observation (not used for any claim).** In all 16 cases, the number of chain variables in A's least model equals
  the number in B's least model on the mirror image. Both counts are exact computations. A's counts on the
  originals also equal `_chainvars_true` in the float64 run `C7UPPER/logs/repro_validation.log` for the same file
  names: 16682, 16714, 16991, 17011, 17852, 17852, 17957, 18255. The A/B match is consistent with the expectation
  that a reflection, followed by reversing the order of each chain, turns A's chains into B's. That correspondence
  has not been proved or checked here.

## Method

### Arithmetic and geometry (`k8exact.py`)

**Arithmetic (exact computation).** A point is w = (w_0, …, w_6), meaning Σ w_j ζ^j with ζ = e^{2πi/7}. This is the
format of the set files.
- Sums, products and conjugates are computed in Z[ζ]. Equality is tested after subtracting w_6·(1, …, 1).
- Every sign that is needed is the sign of Im(a) or Re(a) for some a in Z[ζ]. With c = ζ + ζ^{-1} = 2cos(2π/7):
  - a − ā = (ζ − ζ^{-1})·(d_1 + d_2 c + d_3 (c² − 1)), where d_j = a_j − a_{7−j} and ζ − ζ^{-1} = 2i·sin(2π/7)
    with sin(2π/7) > 0 (elementary: 0 < 2π/7 < π);
  - 2Re(a) = (2a_0 − 2s_2 + s_3) + (s_1 − s_3) c + (s_2 − s_3) c², where s_j = a_j + a_{7−j}.
- The identities behind these formulas are verified exactly in Z[ζ] at start-up. They are:
  - f(c) = 0, where f = x³ + x² − 2x − 1;
  - ζ^2 − ζ^{-2} = (ζ − ζ^{-1})c and ζ^3 − ζ^{-3} = (ζ − ζ^{-1})(c² − 1);
  - ζ^2 + ζ^{-2} = c² − 2 and ζ^3 + ζ^{-3} = −c² − c + 1;
  - ω = −ζ^4 satisfies ω² = ζ and ω^7 = −1, and Re ω > 0, Im ω > 0. So ω = e^{iπ/7}.
  - The start-up assertion Im ζ > 0 is a consistency check only: it is the premise sin(2π/7) > 0 of the Im
    formula itself, so it proves nothing.
- **Isolating c.** 0 < 2π/7 < π/3 gives 1 < c < 2. The polynomial f has exactly one root in [1, 2], because f(1) < 0
  < f(2) and f′ > 0 there. An interval [L, L+1]/2^N containing it is found by integer bisection, with the exact checks
  f(L/2^N) < 0 < f((L+1)/2^N).
- **Certified sign.** The sign of q_0 + q_1 c + q_2 c² is read off an exact integer interval enclosure over that
  interval. Each term is monotone in c > 0. If the enclosure contains 0, N is doubled.
  - This terminates: f has no rational root, so it is irreducible, and 1, c, c² are linearly independent.
  - So the value is 0 only for q = 0, which is returned as sign 0, and only where 0 is expected. There are 11 such
    calls per normalisation: the Im of the 9 real squared radii, and the two layer-0 points lying exactly on the
    sector boundaries at angles 0 and 2π/7. That gives the `exact_zero: 77` in the log, for 7 normalisations per
    case. Every sign that enters the assignment is asserted nonzero.
  - Precision used: at most 512 bits (for `m7_x2_G9s_centre`, with coordinates near 10^30).

**Conventions** (shared by `C6UPPER/encb/gen_b2.py` and `C7UPPER/gen.py`, odd m).
- **Layers.** Layer 0 is outermost; orbits are sorted by exact squared radius |p|² = p·p̄, all distinct.
- **Angles.** Point (i, k), id 7i + k, has angle θ_i + 2πk/7, with θ_0 = 0 and θ_i ∈ [0, 2π/7). The representative
  of layer i is the unique orbit point q with q·p̄_0 in that sector. The sector test is Im(z) ≥ 0 and Im(z ζ̄) < 0.
- **H and psi.** H(i) = [θ_i < π/7] = [Im(z_i ω̄) < 0]. psi_i = arg(u_i) with u_i = z_i or z_i ω̄. It is checked to lie
  in (0, π/7).
- **Y.** Y(i,j) = [Im(ū_i u_j) > 0].
- **Choice of layer-0 point.** The phases (H, Y) were recomputed for all 7 choices of the layer-0 point put at angle
  0, and are identical.

### Encoder B (`k8exact.py`)

- **Orbit variables.** An orbit variable is true iff orient(c_0, c_1, c_2) > 0 for its canonical triple c from B's
  map file.
- **Families.** The formula is split by B's emission order: 112 transitivity, 49,957 angular (1,637 units and 48,320
  conditional), 252 nesting and 1,715,030 chain clauses. The split was checked against the clause contents: chain
  clauses are exactly those with a chain variable.

### Encoder A (`k8exact_a.py`)

`k8exact_a.py` loads `k8exact.py` and uses its sign routines, normalisation, orientation table and clause
evaluation unchanged. Only the variable map and the family split are A's own.
- **Orbit variables.** V(C) = [orient(C) = +] for the canonical triple C of each rotation orbit. C is the
  lexicographically least sorted rotation of the triple. The variables are numbered 1, 2, … in order of first
  appearance over all triples of the 63 points in lexicographic order (`gen.py` docstring and constructor). The map is
  derived from that definition in `k8exact_a.py`. It is then compared with the generator's own table (`gen.Enc`,
  constructor only) and agrees: 5,673 orbits of exactly 7 triples each.
- **Y and H.** These come from gen.py's meta file (`A_m7K8t9.cnf.json`) and agree with `gen.Enc`. They are
  variables 5,674–5,701 and 5,702–5,709, and H(1) is variable 5,702.
- **Families.** These come from the meta file's clause ranges: 112 order (Y-transitivity), 49,957 angular (1,637
  units), 252 nesting and 1,715,030 chain clauses. The split was checked against the clause contents. Non-chain
  clauses use only the 5,709 geometric variables; every chain clause has a chain variable; transitivity clauses are
  ternary in Y; nesting clauses are orbit-variable units.
- **Unit H(1).** For each case the log records whether the assignment also satisfies the unit clause H(1)
  (`satisfies_A9_plus_unit_H1`). The script fails unless exactly one of each set and its mirror does.

### Clause evaluation (both encoders)

- **Chain variables.** Once the geometric variables are fixed, the remaining clauses are Horn in the chain variables.
  The chain variables get their least model; all others are false. Every clause is then evaluated.
  - Zero violations means the full assignment satisfies the CNF.
  - A violation would mean that no extension exists, because every model contains the least model.
- **Dump.** The full assignment is written out and re-checked by `satcheck.py`, which shares no code with
  `k8exact.py` or `k8exact_a.py`.
- **Exit status.** `k8exact.py`, `k8exact_a.py` and `satcheck.py` exit with status 1 on any violated clause, a
  missing H(1) flip, a failed assertion, or (for A) a file where not exactly one of set and mirror satisfies the
  unit H(1). `run.sh` records every step's exit status in `logs/exit_status.json` and exits 0 only if all are 0.

**Cross-checks** (all passed, all 16 cases):
1. Rotation invariance of all 39,711 orientation signs, (i, k) → (i, k+1). Exact.
2. All 41,664 signs agree with `PRIMEFOLD/check64/z7exact.py`. That is separately written code for the same
   identities, with a fixed 320-bit bracket and an explicit error bound. Exact. This was run in both the B and the A
   check.
3. A 200-digit Decimal recomputation (Machin π, Taylor series) of all orientations, H and Y: 0 disagreements and 0
   undecided. Evidence only. This is in the B check only; the A check uses the same geometry code.
4. Negative controls on each original set, for both encoders. One geometric value is flipped at a time, and the
   numbers are the clauses then violated, over the 8 files.
   - Flipping the first angular-unit variable gives 1. That is its own unit clause, so this only checks the
     bookkeeping.
   - The following flips test whether the evaluation responds to the geometry:
     - H(1): 56–111 (the same for A and B);
     - Y(1,2): 8–21;
     - H(8): 0–7 (0 for the four files with H = 11111111);
     - five orbit variables picked with a fixed seed: 0–16,215 for B and 0–16,630 for A.
   - A flip with 0 violations is not a failure: the flipped assignment can still be a model. Only the unit flip is
     asserted to be detected.

**Self-tests** (`test_signs.py`, `logs/test_signs.json`):
- the identities;
- 40,000 float64 comparisons on well-separated values (evidence only);
- 20,000 comparisons with `z7exact.py`, including near-cancelling inputs;
- exact zeros of real and imaginary elements;
- 1,153 continued-fraction convergents p/q of c and c², with q up to 2^1000. These have the known signs (−1)^n and
  needed 951 precision doublings in total, so they exercise the refinement path.

## Files

| file | content |
|---|---|
| `k8exact.py` | exact derivation of the geometric assignment, encoder B's map, clause evaluation (stdlib only) |
| `k8exact_a.py` | encoder A's map and family split on top of `k8exact.py` (stdlib only) |
| `satcheck.py` | separate minimal clause checker for dumped assignments |
| `test_signs.py` | self-tests of the sign routines |
| `regen_hashes.sh` | regenerates `B_m7K8t10` and `B_m6K8t9`, compares with the recorded hashes, deletes them |
| `regen_hashes_a.sh` | regenerates `A_m7K8t10` and `A_m7K8t10` + unit H(1), compares with the recorded hashes, checks that 7857 is H(1), deletes them |
| `run.sh` | the whole run (every heavy step under a one-core, 12 GB cap at idle priority) |
| `logs/sets.txt` | hashes of the eight set files; ES8SYM copies identical |
| `logs/gen_m7K8t9.log` | generation of B (7,8,9): `p cnf 58136 1765351`, CNF `67cd613d…`, map `e7dee023…` (no earlier recorded hash exists) |
| `logs/gen_A_m7K8t9.log` | generation of A (7,8,9): CNF `bb85a966…`, `MATCH` with `C7UPPER/SHA256SUMS.txt`; meta file `48698d3f…` |
| `logs/exact_check.jsonl` | B: one line per case, per-file mirror flips and a final `"status": "PASS"` |
| `logs/exact_check_A.jsonl` | A: one line per case, per-file mirror flips and unit-H(1) case, final `"status": "PASS"` |
| `logs/satcheck.jsonl` | B: 16 × `"unsatisfied_clauses": 0` |
| `logs/satcheck_A.jsonl` | A: 16 × `"unsatisfied_clauses": 0` |
| `logs/test_signs.json` | self-tests, `"status": "PASS"` |
| `logs/regen_hashes.log` | the two recorded B hashes reproduced: `MATCH`, `MATCH` |
| `logs/regen_hashes_A.log` | the two recorded A 10-layer hashes reproduced: `MATCH`, `MATCH`; unit 7857 is H(1) |
| `logs/exit_status.json` | exit status of every step of `run.sh` (all 0) |

All `.jsonl` and `.json` logs are strict JSON (one object per line). Standard error of each Python step goes to
`logs/<step>.stderr`, which is removed when empty; none is present.

The regenerated CNFs, the map/meta files and the 32 assignment files were deleted after the run (they are
reproducible). Their hashes are in the logs.

**Resources.** The logged run took 137 s of wall-clock time at one core. `k8exact.py` took 50.7 s with peak RSS
624 MB, and `k8exact_a.py` took 49.2 s with peak RSS 601 MB. The previous B-only run, before the review fixes, took
101 s and gave the same encoder-B results.

## Left open

- **Finite validation.** This checks 16 real configurations at 9 layers. It is not a soundness proof of either
  encoding. Soundness remains a written proof (the `C7UPPER/gen.py` docstring; B is a separate implementation of
  the same clause families, `C7UPPER` §2 and `C6UPPER`), Lean-checked in part (`LAYERLEAN`).
- **The 10-layer formulas** (the certificates) cannot be tested this way: by the theorem itself no real
  configuration of 10 such layers exists. They are tied to this check only through being the output of the same
  generators (hashes reproduced here).
- **Reflection argument.** It is confirmed here on A's and B's variables for these 8 sets: each H(i) flips, each
  Y(i,j) reverses, and exactly one of each set and its mirror satisfies A(7,8,9) with the unit H(1). The argument
  that the unit H(1) loses no generality remains a written proof (`C7UPPER` §2).
- **The 63-point set** `ES8SYM/sets/c7_63pts_9layers.pts` was not included.

## Reproduction

From `cloud/es7-2026-10-19/results`:

```sh
bash K8EXACT20261106/run.sh <scratch work dir>     # about 2-3 minutes at one core; rewrites logs/; exit 0 = all PASS
```

Python 3.14.4 was used, with no third-party modules.
