# Task C3a: compact CNF for 3-fold symmetric 33-point sets without a convex 7-gon

Nothing here is a theorem. "UNSAT" means UNSAT of one specific CNF; the encodings are
tested, not formally verified. A SAT model is an abstract signotope until it is realized
with exact coordinates and re-checked.

RESULTS_PLACEHOLDER

## The encoding (`c3cnf.py`)

Setup: S has 3m points in general position, is invariant under the rotation R by +120° about
c = 0, and c is not in S. A generic symmetric perturbation keeps the order type, so we may assume
no two points are collinear with c. Pick a line l through c that avoids S, make it the y-axis,
and map S by phi(x, y) = (y/x, 1/x) to S'. Label the points 0..3m-1 by increasing X' = y/x.

Identities used (re-checked exactly, see "Validation"):
1. R acts on labels as R(i) = (i - m) mod 3m.
2. chi_S(i,j,k) = chi'(i,j,k) · (-1)^(σi+σj+σk), where chi' is the orientation of S' (x-sorted, so
   a signotope on the labels) and σi = [x_i < 0].
3. chi'(Ri,Rj,Rk) = chi'(i,j,k) εi εj εk with εi = +1 iff i < m; and σ_{Ri} = σi xor [i ≥ m], so
   σ on the orbit (r, r+m, r+2m) is (s, ¬s, s), one free bit s per orbit.
4. For i < j let inv_ij = [Y'_i > Y'_j]. Then i is left of j in S iff inv_ij xor σi xor σj. The
   inversions of a triple form a prefix of (ij, ik, jk) if chi'(ijk) = + and of (jk, ik, ij) if −;
   σi = 0, σj = 1 forces inv_ij = 1, and σi = 1, σj = 0 forces inv_ij = 0.
5. The point reflection p ↦ −p keeps the labels (X' is unchanged) and the class, and maps
   (chi', σ, inv) to (−chi', ¬σ, ¬inv). So σ0 = 0 may be assumed. This is the only symmetry
   breaking.

Variables: chi' per R-orbit of triples (1,826 for m = 11: (5456 − 11)/3 + 11, the 11 orbit
triangles being fixed by R), 11 σ bits, 528 inv bits, 528 order bits B_ij, and chi_S per orbit
(T, 1,826), tied to chi' and σ by parity clauses.

Core clauses: the signotope axiom on chi' for every 4-set (3-term monotonicity; the 327,360
clauses collapse to 109,120 distinct ones under the orbit substitution), σ0 = 0, the prefix and
forced inversion clauses, and the parity definitions of B and T.

No convex k-gon, two variants (both one-directional, so only "a real convex k-gon forces a
contradiction" is needed for soundness):

- `--gon chain` (default; the encoding the task asked for). A convex k-gon has a leftmost vertex x
  (in the x-order of S, given by the literals B). The other k−1 vertices lie in the open
  half-plane right of x, sorted by angle about x; consecutive ones are counter-clockwise about x
  and every interior turn is a left turn. Conversely, such a chain of k−1 points right of x is
  angularly increasing inside a half-plane (span < 180°) with left turns everywhere, so with x it
  is a convex k-gon. Encoding: Y[x,b,c] ← B(x,c) ∧ ccw_S(x,b,c); W2[x,a,b] ← B(x,a) ∧ Y[x,a,b];
  W(r+1)[x,b,c] ← W r[x,a,b] ∧ Y[x,b,c] ∧ ccw_S(a,b,c); W(k−2) ∧ Y ∧ left turn → false. This is
  the Szekeres–Peters angular chain about the leftmost point, with "x is left of p" as literals.
  It is frame-dependent (tied to l), so it cannot be reduced by the rotation.
- `--gon conv` (variant). A set is in convex position iff all its 4-subsets are. conv4(Q) ← one
  of the 6 convex chi_S patterns of Q; conv_r(S) ← AND over x of conv_{r−1}(S − x); for every k-set
  OR over x of ¬conv_{k−1}(S − x). One variable per R-orbit of subsets, one clause per R-orbit of
  k-sets (chi_S is R-invariant). This is the gon layer of `symcnf.py`, placed on the compact
  signotope core instead of symcnf's CC-system axioms; it does not need the x-order at all.

Sizes for m = 11, k = 7:

| CNF | variables | clauses | sha256 |
|---|---|---|---|
| `c3cnf.py 11 7` (chain) | 168,399 | 4,154,921 | `bf0e502e…` |
| `c3cnf.py 11 7 --gon conv` | 466,697 | 2,115,323 | `023f8228…` |
| `symcnf.py 33 7 3` (results/E, E2) | about 464k | about 9.5M | `4c214b4c…` |

## Validation (step 3; all passed)

Exact arithmetic: points are generated with coordinates in Z[√3] (a base point times 4, then its
two exact rotations), every orientation of S, the x-order, and every collinearity with c are
decided exactly; S' = phi(S) is computed in mpmath at 120 digits and every sign taken from it is
asserted to exceed 10^-60 in absolute value (`c3geom.py`). General position, no two points
collinear with c, and distinct x-coordinates after the rotation are checked exactly; sets that
fail are redrawn. Point shapes: disk, ring, small clusters, and thin radial strips (the last
give sets without large convex subsets).

- **Identities 1–4 and the σ orbit pattern** (`check_identities.py`): 2,300 random symmetric
  sets with m = 1..11, 0 failures (`logs/identities.log`, `logs/identities_2000.log`).
- **3a, clause-level validation** (`validate.py`): for each set, the true value of every
  variable is computed from the coordinates (base variables exactly; chain or conv variables as
  the least fixpoint of their definitions), and every clause is evaluated. Required: all
  non-gon clauses true, and the gon clauses all true exactly when the exhaustive checker
  `convk.c` finds no convex k-set. When σ0 = 1 the set is replaced by −S with the same line l
  (item 5), and the check asserts that the labels are unchanged.
  - chain: 1,000 sets, m = 3..11, k = 5..11; 777 with a convex k-gon, 223 without; 0 failures
    (`logs/validate.jsonl`).
  - conv: CONV_VAL_PLACEHOLDER (`logs/validate_conv.jsonl`).
  - The validator catches planted bugs (`mutation_test.py`, `logs/mutation.jsonl`): wrong ε
    signs (20/20 sets fail), a wrong σ orbit pattern (20/20), and forbidding (k+1)-gons instead
    of k-gons (fails on the set that has a k-gon but no (k+1)-gon).
- **3b, controls that must be UNSAT**: m = 3, k = 5 (9 points) UNSAT, with an LRAT proof
  accepted by both lrat-check (E2 patch) and cake_lpr (`logs/control_m3k5_lrat.log`);
  m = 6, k = 6 (18 points) UNSAT, closed as 8 march cubes, each leaf dual-checked, cube coverage
  dual-checked (`controls/`). Also UNSAT: m = 4..8 with k = 5, and m = 5..8 with k = 6, in both
  encodings.
- **3c, expected SAT**: m = 2, k = 5 SAT; m = 8 and m = 9 with k = 7 SAT (3 s and 5 s).
- **3d, agreement with symcnf.py** (origin/main, `symcnf.py 3m k 3`, auxiliary centre):
  m = 2..6, k = 5, 6, 7: same answer in all 15 cases (`logs/compare_symcnf.jsonl`). chain vs conv:
  same answer on m = 2..8, k = 5..7, 21 cases (`logs/compare_chain_conv.jsonl`).
- **3e, decoded SAT models** (`decode.py`, independent of the clauses): chi' is checked against
  the signotope axiom on every 4-set and against the symmetry rule; σ0 = 0 and the σ orbit
  pattern hold; the inversion bits satisfy the prefix and forced rules and give a total x-order;
  chi_S = chi'·(−1)^σ equals the T variables and is R-invariant; `convk` finds no convex k-set.
  All models pass: m = 2..6 small cases, m = 8 and 9 with k = 7, and m = 10, k = 7 from both
  encodings (`models/`, `logs/sat_controls.log`). Every model has largest convex subset < k.
- **LRAT checkers**: the upstream drat-trim lrat-check accepts an empty clause without hints
  (found by E2; `results/E2/logs/lrat_check_soundness.md`). Every UNSAT here is checked by
  lrat-check with E2's patch AND by the CakeML-verified cake_lpr, and counts only if both
  accept. Checker controls (`logs/lrat_checker_controls.log`): a genuine proof is accepted by
  both; a SAT formula with a hintless empty clause and a truncated proof are rejected by both.

### Comparison with C3b (read only after the checks above passed)

C3b (`results/C3b/tools/gen_c3b.py`, commit 3aac870) independently built the same chain
encoding, with 4-point acyclicity clauses on chi_S added. On m = 2..8, k = 5, 6, 7 (21 cases) both
generators give the same answer (`logs/compare_c3b.jsonl`). Adding acyclicity to the conv
variant (`--acy`) did not speed it up (m = 7..9, k = 6).
