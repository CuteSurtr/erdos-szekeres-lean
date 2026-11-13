# C7UPPER: the largest 7-fold symmetric octagon-free set has exactly 64 points

2–3 November 2026 (UTC). Computer-assisted.

**Statement.** Every configuration of 10 nested regular heptagons about a common centre, in general position (the
centre not included), contains 8 points in convex position. Hence L(7,8) = 9: every 7-fold rotationally symmetric set
of at least 65 points in general position contains a convex octagon, and the largest 7-fold symmetric set in general
position with no convex octagon has exactly 64 points. This is the 7-fold case of ES(8) = 65.

**Status.**
- Encoding soundness: a written proof (the docstring of `gen.py`), checked step by step by an independent review that
  found no gap. Since 4 November three parts are Lean-checked (`LAYERLEAN`): the layer lemma, the mathematical
  soundness of the chain family, and the angular rules in polar form. The classification of phase patterns and the
  step from code to clauses are not.
- Two separately implemented encoders give UNSAT at 10 layers. Each LRAT proof is accepted by lrat-check (re-checked by
  an independent check) and by cake_lpr (heap 8,000 MB, about 33 s each; `logs/cake_A.out`, `logs/cake_B.out`).
- Lower bound: the certified 64-point sets (9 layers plus the centre) of `ES8SYM` and `PRIMEFOLD`.
- No matching prior result was found in the sources inspected: the symmetric literature (arXiv:2506.00224 and the
  Mackey thesis) stops at k = 7, and the searches recorded in `PRIMEFOLD` and `ES8SYM` found no rotational results for
  k = 8.

## 1. Reduction

Lean-checked since 4 November (`LAYERLEAN`, `sevenfold_octagon`): the statement follows from `Sevenfold70` (every
centre-free 70-point sevenfold set in general position has a convex octagon). That is the content of the certificate.

By the layer lemma (`SYM5/README.md` §2; a special case is stated in arXiv:2506.00224 §3.2), a 7-fold symmetric set in
general position with no convex octagon (K = 8 <= 2·7) consists of nested regular heptagons, plus possibly the
centre. A set of at least 65 points therefore has at least 10 layers (7·9 + 1 = 64), and its 10 outermost layers,
without the centre, form an octagon-free configuration of the kind excluded here.

## 2. The encoding (`gen.py`, `gen_b.py`)

- **Variables.** One per rotation orbit of triples (7,820 for 10 layers), phase-order variables Y(i,j) = [psi_i < psi_j]
  with psi = theta mod pi/7, and H(i) = [theta_i < pi/7], plus chain variables.
- **Angular rules.** For a triple, the circular order of the directions and their antipodes is a function of the phase
  order of its layers. If the centre lies inside the triangle, the orientation is the cyclic angular order. If the
  triple lies in an open half-plane through the centre and the angularly middle point is in the outermost of its
  layers, it is a left turn. Proof: the polar orientation formula (`ES8SYM`, Lean-checked there) and
  sin x + sin y > sin(x + y).
- **Nesting.** Each inner layer lies strictly inside the hull of the previous one.
- **No convex octagon.** No 7-point convex chain in angular order around a pivot point (i, 0) among the points of
  layers >= i. By rotation this covers every convex octagon: take its outermost layer as i.
- **Symmetry breaking (`gen.py` only).** theta_0 = 0 and, in the certificate, the unit H(1) (theta_1 < pi/7), which
  loses nothing because reflecting in the x-axis keeps theta_0 = 0 and swaps H(1).

`gen_b.py` is a separate implementation of the same families (exact integer circular orders instead of sampling) with
no symmetry breaking beyond theta_0 = 0. Both produce `p cnf 80080 2748538` at 10 layers.

## 3. Certificates

| | CNF (SHA-256) | proof (bytes, SHA-256) | lrat-check | cake_lpr |
|---|---|---|---|---|
| encoder A + H(1) | `fa297b5b…` (base `1a7c0e70…`) | 1,702,278,368, `c750a805…` | VERIFIED | VERIFIED UNSAT |
| encoder B | `b4d29017…` | 1,630,259,870, `75f9bd35…` | VERIFIED | VERIFIED UNSAT |

CaDiCaL 3.0.1, UNSAT in 833 s and 802 s (1.6–1.7 GB). Proofs and CNFs are in the local archive
`es8-c7-octagon-2026-11-03` (outside Git). Full hashes: `SHA256SUMS.txt`.

## 4. Validation (`tests/`, `logs/`)

- All nine known 7-fold 63- and 64-point octagon-free sets satisfy every clause of the 9-layer CNF (float64, and
  150-digit Decimal for three of them). The 9-layer CNF is SAT in 3.7 s.
- 78 random nested 10-layer configurations: no violated clause outside the chain family. All 73,784 angular clauses
  were tested on 221,352 random instances: no failure.
- Encoders A and B agree on all 185,549 orbit-pattern pairs of the non-chain part.
- Chain family against brute force over all 8-subsets (random 2- and 3-layer configurations) and against a per-pivot
  dynamic program (30 random 10-layer configurations, 300 pivot cases): no unsound or inexact case.
- Calibration: for (m, K) = (3,4), (4,5), (5,6), (6,7) the same encoding is SAT exactly at the known maximum number of
  layers and UNSAT one layer beyond (LRAT proofs accepted by lrat-check; `logs/calib_*.log`).

## 5. Scope

- The statement concerns Euclidean 7-fold rotations; affine 7-fold symmetries reduce to it by the averaging argument
  of `SYMLEAN` (a 7-fold affine symmetry is conjugate to a rotation).
- The layer lemma (including strict nesting), the chain family's mathematical soundness and the angular rules in polar
  form are Lean-checked (`LAYERLEAN`, added 4 November). The rest of the encoding's soundness is a written proof (reviewed, not Lean-checked).

## Reproduction

```sh
S=<scratch directory with resolve/bin/{cadical,lrat-check}> bash C7UPPER/repro.sh        # validation (~90 s)
S=<...> bash C7UPPER/repro.sh solve                                                      # re-solve and check
```

`logs/repro_validation.log` was produced in the original host layout. On 6 November 2026 the paths of `repro.sh` were
adjusted for a checkout of the repository: tools from `$S/resolve/bin`, test scripts from `tests/` (with `C7UPPER` on
`PYTHONPATH`, since they import `gen.py`), point sets from `../ES8SYM/sets` and `../PRIMEFOLD/sets/k8`, outputs to
`$S/repro`. The message of the `S` check was quoted, because its unquoted `}` appended `}` to `S`, and `cd` now exits
on failure. The first validation run (no `solve`, 2-minute limit, `nice -n 19`, 4 GB memory cap, machine under full
load) stopped at the time limit during the A/B comparison (`logs/repro_validation_20261106.log`). It ran before the
quoting fix, so its outputs went to the shell's working directory, outside the repository. A second run of the adjusted
script (no `solve`, absolute `S`, CaDiCaL 2.1.3, same caps, 15-minute limit) completed with exit 0 in 2 min 35 s. Its
output equals `logs/repro_validation.log` apart from the point-set paths (`logs/repro_validation_20261106b.log`). The
`solve` branch has not been re-run. The "~90 s" above is the original timing. After the second run, `B` (the tool
directory) is set after `cd "$S"`, so that a relative `S` also works; for an absolute `S`, as in that run, the
behaviour is unchanged.
