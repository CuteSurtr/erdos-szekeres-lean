# six_model0090: semidefinite (face-reduced) exclusion of `model0090`

4 November 2026, 09:19-09:58 KST. Scope: realizations with the prescribed Euclidean sixfold action of the
m6K8t10 encoding (point id `x = 6*i + k` is `R^k z_i`, `R` = counterclockwise rotation by 60 degrees).
Inputs (read-only): review archive `proof-archives/es8-rot-refine-2026-11-04/` (below `ARCH`), review results
`ROTREFINE20261104/` (encoder `C7UPPER/gen.py`, `math_linear.py`). `model0090` SHA-256
`62b5c1d0ba4c9fb6d9b19a65c86d87f427853af388cf65d470dd73cae1f19f21` (`ARCH/m6/models/model0090.json`, hash checked).

## 1. Result

**Exact computation.** There are 36 orientation triples `r` (touching all ten layers), required signs `s_r`
read from `model0090`, and positive integers `w_r` (from 3.1e16 to 9.28e18) such that

    P(z) = sum_r w_r * s_r * (2/sqrt3) * [a_r b_r c_r](z)

is a negative SEMIdefinite quadratic form in the 20 real seed coordinates. Certificate: `P` vanishes on the
explicit rational 4-dimensional subspace

    W = { z_1 = z_2 = z_3 = z_4 = R z_5,  z_5 = z_6 = z_7 = z_8,  z_9 = 0,  z_0 free },

i.e. `P*W = 0` exactly, and `-P` restricted to the 16 coordinates other than `(Re, Im)` of `z_0` and `z_5` is
positive definite (16 positive exact rational LDL pivots). `W` restricted to the 4 dropped coordinates is the
identity, so `P` is congruent to `diag(0, P_CC)` with `P_CC` negative definite; hence `P <= 0` everywhere.

**Written proof (not refereed).** If a general-position configuration with the prescribed rotation realized
these 36 signs, every term `w_r s_r [a_r b_r c_r]` would be strictly positive, so `P(z) > 0`, contradicting
`P(z) <= 0`. Hence `model0090` is not realizable with the prescribed sixfold rotation. Only the rotation formulas
and the 36 signs are used (no nesting, phase-order, GP or K-gon clauses). Semidefiniteness suffices: the
contradiction needs only `P <= 0` and strict positivity of the left side.

**Evidence only (why the review's negative-definite search failed).** The numerical PSD relaxation (orientation
rows, Hermitian Gram `[[D,-E],[E,D/3]] >= 0`, trace 1) has maximum margin `-1.2e-8`. Its optimum is a rank-2
degenerate Gram matrix lying in `W` (layers 1-8 collapsed onto one hexagon orbit, layer 9 collapsed to the
centre) that satisfies every row weakly, so every dual certificate vanishes there and none can be definite.
Adding valid phase-order rows (`sign(theta_j-theta_i) E_ij > 0`, `D_ij +- E_ij > 0`) and radius rows left the
margin at `-8.6e-9` and the same face; these rows were not used in any certificate.

## 2. Method and commands (`V` = research venv python, used only for numerical search; checks are stdlib)

Scripts read the review results directory from `$ES_RESULTS` (and `loop.sh` the venv python from `$ES_VENV_PY`);
the final checks were re-run after this path edit and pass.

1. `V -I -B sdp_ext.py --model M --out run_full_base --no-phase --no-radius` (Clarabel SDP; dual, primal saved).
2. `V -I -B analyze.py run_full_base M` (evidence): Gram eigenvalues `0.915, 0.085, 0 (x8)`; `|C_ij| = 1` on
   layers 1-8 with relative phases in `{0, pi/3}`; `D_99 = 0`; dual matrix has a 4-dimensional numerical kernel.
3. `V -I -B face_sparse.py M sparse0090 4`: reweighted-L1 SDP over `lambda >= 0` with `Q_lambda W = 0`,
   `-Q_lambda[C,C] >= I`; support 91 -> 43 -> 40 -> 36.
4. `V -I -B face_cert.py sparse0090 M 1e-8 face_sparse0090`: rounds lambda, projects it EXACTLY onto
   `{Q_lambda W = 0}` (rational solve of `B B^T y = -B lambda0`), requires all weights positive, re-checks
   `Q W = 0` and the LDL pivots of `-Q[C,C]`, using the review's dot/cross table (`math_linear.form`).
5. `python3 -I -B check_cert.py M face_sparse0090/face_witness.json`: independent checker. It binds every record
   to the encoder's canonical triple variable and to the model sign, expands every determinant directly in
   oblique coordinates `z = a + b*omega`, `R(a,b) = (-b, a+b)`, `det = (sqrt3/2)(p_a q_b - p_b q_a)`, rebuilds `P`,
   and checks `P*W = 0` and the 16 pivots. Output `ok: true, records 36, complement_pivots_positive 16`.
6. `python3 -I -B float_sanity.py <witness>` (evidence): true complex coordinates `omega^k z_i`, 2000 random and
   near-`W` samples; normalised weighted sum `<= -1.1e-7`, consistent with NSD and the sign convention.

A first, denser certificate (support 1,884; `face_1e5/`) also passes both exact checkers.

## 3. CNF cut and re-solve

Cut = negation of the 36 signs (`cut_model0090_sparse.clauses`; falsified by `model0090`, checked):
`-677 684 -715 -842 1648 1654 1714 1725 1875 -2198 2214 2284 2894 -2936 -2942 3029 -3061 -3168 3491 3790 3888 -4149 4626 4638 4730 4852 5059 5065 5071 5095 -5179 5218 -5278 5305 5368 5478 0`
Its soundness is the written proof of section 1 (single clause; no family lifting applied).

Refined formula = final review CNF `ARCH/m6/current.cnf` (SHA-256 `4281bf37...d041`, 9,198,581 clauses, hash
verified) plus cuts: `(echo "p cnf 58626 <n>"; tail -n +2 current.cnf; cat cuts) > refined.cnf`, then
`cadical -t <s> --seed=<k> refined.cnf`.

* Dense 1,884-literal cut: **SAT** in 7.65 s (`solve.log`). Next model `model_next.json` (SHA-256
  `5f18821567edf3107180c4380d24162f76c03ddf1d48fe276bc92d9b8e553523`) differs from `model0090` in one orientation
  variable (1366, triple `0,39,45`) and 3 auxiliary variables. **Exact computation:** it satisfies all
  9,198,582 clauses of the refined CNF (`verify_sat.py`, `verify_next.json`, 0 violated, CNF SHA-256
  `fcd17ed994cbad293e97d054a117a8721faa9a3121dd240910fe8c2d89c6d117`). It is excluded by the same face method
  (`face_next/`, both checkers pass). **Exact computation:** it passes the full GP test (`gp_next/`, 27,307,560 relations, 0 violated).
* Sparse-cut loop `loop.sh`: section 4.

No UNSAT was obtained, so no LRAT proof is kept (the one written for the dense-cut SAT run was deleted).

## 4. Refinement loop (`loop/log.txt`)

Loop: start from the final review CNF plus the 36-literal cut; each round solves with CaDiCaL (`-t 240`), runs
`face_sparse.py` + `face_cert.py` + `check_cert.py`, and appends the new 1-clause cut. 55 rounds, 09:29-09:49.
Per-round table: `loop_table.txt`; all cuts: `loop/cuts.clauses` (55 clauses).

* **Exact computation.** Every round was SAT. All 55 models pass the full GP test (27,307,560 relations,
  0 violated; review checker `gpcheck`, SHA-256 `7bb2e153...3c6c`, via `m6_full_gp.py`). Exact clause-by-clause
  satisfaction was verified for model 14 (`verify_loop14.json`) and model 55 (`verify_loop55.json`, 9,198,636
  clauses, 0 violated).
* **Exact computation.** Models 1-54 are each excluded by a face-reduced semidefinite certificate on the SAME
  face `W`, with 25-35 terms; both exact checkers pass for all 54 (`loop/face<k>/`, `loop/check<k>.log`).
* **Exact computation.** Model 55 (SHA-256 `f2499707ba1098aaa8a53055bdad61705f28af9f71b97723b91300b0a4f61772`)
  leaves the face: its PSD margin is `-1.46e-3` (evidence only), and a 55-term NEGATIVE-DEFINITE certificate on
  layers 0-8 exists (`loop/sdp55/witness.json`, SHA-256 `f3f88262...1199`), checked by the exact LDL in `sdp_ext.py` and
  independently by `check_def.py` (18 positive pivots; its printed `kernel_dim_checked` field is a stale label,
  no kernel is used). Its cut was not added and no further solve was run (deadline).
* **Evidence only.** The refined formula is still SAT after 55 cuts; the loop is a chase of nearby models. The 576 layer relabelings that preserve `W` (permutations within
  `{1..4}` and within `{5..8}`) of the model0090 certificate falsify none of the loop models
  (`family_probe.py`), so that family does not speed the chase.
* A first loop with the dense 1,884-literal cuts (`loop_dense_partial/`) was stopped after one round in favour
  of sparse cuts.

## 5. Files (this directory) and SHA-256

| file | SHA-256 |
|---|---|
| `face_sparse0090/face_witness.json` (36-term certificate) | `6747891d5d525ba81cf50b0e8c6c8ae13fc1f995f132dff51f65a3d29a2db5a1` |
| `cert36_model0090.txt` (readable triples, signs, weights) | `9f93943a275d2c9f9cc0a4a02fff49d12c6d02b14a279d5dcc5c761a48ad74a8` |
| `cut_model0090_sparse.clauses` | `8acfca54ad69e9edf91d2b7734380c56cd761a5d5284c212e8e32e7d814bfbf4` |
| `face_1e5/face_witness.json` (1,884-term certificate) | `0f46700521a6a172ce7eb00221948b4d659a1124e0299cd32ebca2817e610478` |
| `cut_model0090.clauses` (1,884 literals) | `4667ba2ab0df3cec40dc05fc730f20ab4d5eb641fcd0ff164621b5c1576658f1` |
| `face_next/face_witness.json` (next model) | `114a253bfdb79e36a39e7e6f98b4c81841e7892ffc0e710f71625e0b3ddd3a0e` |
| `model_next.json` | `5f18821567edf3107180c4380d24162f76c03ddf1d48fe276bc92d9b8e553523` |
| `check_cert.py` (independent checker) | `9e8365ad9a4d570b206948d2cc7bd87b30036e142547cd100d265d1a92dd51f3` |
| `face_cert.py` | `96ddd2491a79aca98310da7f2d44620546c9dab49871d3cf0c0ccbe0134683ea` |
| `face_sparse.py` | `a97a1b93b7804e4314cda5d09f9372cb6f6dfe77297976569d2f64229ef1e85f` |
| `sdp_ext.py` | `02b8a2ff00caef715b152b6b41a035ee8dc3c15a017e8868f793e2999d441226` |
| `float_sanity.py` | `d6154bfebc476094e52abdab857ef3795c9006f4a81f19c30b0c86b78cd61cd7` |
| `check_def.py` (definite-certificate checker) | `31f1054681a76e7270847fc5944318f5d7236ecc90a00a4fa470b5804ff56f7e` |
| `loop/cuts.clauses` (55 cuts) | `2c59979647de3e7613de4625698cf2fe9f86952fadb1186397ae1c7778bd4725` |
| `loop_table.txt` | `dad6e8e2dd113fbf551b49507585deae7b8c6e690f7a78bc668abe29b602d6d9` |
| `loop/model55.json` | `f2499707ba1098aaa8a53055bdad61705f28af9f71b97723b91300b0a4f61772` |
| `loop/sdp55/witness.json` | `f3f882628de79de05b5988d78ecc77a788448679eb74c362c6eb7c0843d71199` |
| `verify_sat.py`, `loop.sh` | `ac947f9a...286b`, `19fab8d6...553b` |

Large intermediate CNFs were deleted after hashing; rebuild them with the command above.

## 6. Open issues

* Each cut is one clause. Lifting to an orbit-injection/shift family (substituting `z_i -> R^{s_i} z_{f(i)}`
  keeps `P <= 0`; direction and global sign must be coupled as in `quadratic_bounds.md`) was not done, so the
  solver keeps finding nearby models (one or a few sign flips) on the same degenerate face.
* The certificates have not been reviewed by a second person. The two exact checkers share the encoder's
  variable/triple map but not the determinant expansion or the subspace arithmetic.
* One transient helper text file was written to and deleted from the system temporary directory (rule slip).
* The sixfold maximum remains 54 or 60: the refined formula is still SAT; no UNSAT and no 60-point
  realization. No matching prior result was found in the sources inspected for this face-reduced use of a
  semidefinite certificate in the campaign; priority is not claimed.
