# Soundness of every clause family used in LBK9OCT20261111 (written proofs, not refereed)

Status: written proofs, not refereed and not reviewed independently (a second reading only). The families (a)–(c) are
new; every implementation was also tested against exact and random real configurations (README §2, §3 gate).

## 0. Setting and the hypotheses H, G, N

Let m = 8 and t >= 1. A **configuration** is S = L_0 ∪ … ∪ L_{t-1}, where L_i is a regular octagon about a point O
with circumradius r_i, and

- **(H)** every L_j with j > i lies in the interior of conv(L_i) (strict nesting of the convex layers; it implies
  r_0 > r_1 > … > r_{t-1} > 0), O ∉ S, and S is in general position (no three points collinear).
- **(H0)** the weaker condition r_0 > r_1 > … > r_{t-1} > 0, O ∉ S, general position.

By the layer lemma (`LAYERLEAN`, Lean-checked: `layers_are_orbits`, `strict_nesting`, `centre_not_mem_of_even`), every
8-fold symmetric set of 8t points in general position without 9 points in convex position is a configuration with (H).

**Labelling** (encoder A, `C7UPPER/gen.py`). Rotate so that one vertex of L_0 has angle 0. Then L_i has vertices at
the angles theta_i + 45°·k with theta_i in [0°, 45°), theta_0 = 0; psi_i := theta_i. Point (i, k) is the vertex of
L_i with angle in [45°k, 45°(k+1)). Y(i, j) := [psi_i < psi_j] for 1 <= i < j.

- **(G)** psi_1, …, psi_{t-1} are pairwise distinct and none is 0 or 22.5° (for B = 4 also none is 11.25° or
  33.75°).
- **(N)** S has no 9 points in convex position.

**Perturbation lemma.** Every configuration with (H) has a configuration with (H) and (G), obtained by changing only
the phases by arbitrarily little, with the same orientation of every ordered triple (corresponding points). Proof:
each orientation is a continuous function of the phases and nonzero at the start (general position), so a small
change keeps every orientation; the strict nesting of (H) is a set of such orientation conditions (each vertex of L_j
strictly left of each edge of L_i), and the radii do not change; changing a phase that is 0 to a small positive value
keeps the labelling. The same order type means the same subsets in convex position, so (N) is kept too. If psi_1, …, psi_{t-1} was weakly increasing
(or weakly decreasing), the perturbation can be chosen strictly increasing (decreasing): separate equal values in the
required order and move the value 0 to a small positive one.

**Variables and their intended values.** For a configuration with (H) and (G): every triple-orbit variable gets the
true orientation of its canonical triple (rotation preserves orientation); Y(i, j) its truth value; Z(i, b) :=
[psi_i < b·45°/B]; the chain variables of encoder A their least fixpoint. "A family is sound under X" means: for every
configuration with X, this assignment satisfies every clause of the family.

## 1. The families

| family | file / generator | sound under | argument |
|---|---|---|---|
| order (Y transitivity) | gen.py `fam_order` | H0, G | Y is a strict order |
| angle | gen.py `fam_angle` | H0, G | docstring of gen.py, step 2 |
| nest | gen.py `fam_nest` | H | docstring of gen.py, step 3; `LAYERLEAN` `strict_nesting` |
| chain | gen.py `fam_chain` | H, G, N | docstring of gen.py, step 4; `LAYERLEAN` chain lemma (Lean-checked) |
| chord | `chord_rules_m.py` | H0, G | `CHORD20261105` §1 (holds even without nesting) |
| (a) cone rules | `cone_rules.py` | H0, G | §2 below |
| (b) threshold-order rules | `thr_rules2.py` | H0, G | §3 below |
| (c) cell rules, B = 2 and 4 | `cell_rules.py`, `cell_thr.py` | H0, G | §4 below |
| bin-order clauses | `binorder.py` | H0, G | definitions of Y and Z |
| Y(1,2) unit (not in the certificate) | reflection | H, G, N, up to reflection | `C6UPPER` §2 |
| the increasing cube (105 units Y(i,j)); partial versions (units Y(i,j) for a <= i < j <= b) | a case | psi increasing (on [a, b]) | §5 below |
| the Z cubes | a case split | — | §5 below (cover) |

Only the chain family uses (N). Only the nest and chain families use the strict nesting of (H); every other family
needs only the radius order (H0) together with (G). This is visible in the random checks: random configurations that
satisfy (H0) but not (H) violate nest units (and nothing else), while configurations filtered for (H) violate nothing
(`logs/rand_check_*.log`).

## 2. Cone rules

**Polar formula** (`ES8SYM` Lemma 1). For points p, q, s at distances r_p, r_q, r_s from O and directions b_p, b_q,
b_s, 2 area(p, q, s) / (r_p r_q r_s) = u_p sin(b_s - b_q) + u_q sin(b_p - b_s) + u_s sin(b_q - b_p) with u = 1/r.
So orient(p, q, s) = sign F(u), F(u) = sum_x c_x u_{L(x)} (L(x) = layer of x), with coefficients c_x that depend only on
the phases.

**Cone lemma.** Let D = {d_1 < … < d_s} be the layers of the triple. By (H0), (u_d)_{d in D} ranges exactly over the
open cone C = {0 < u_{d_1} < … < u_{d_s}} (any such values extend to a strictly increasing u). Put
g_r = sum_{d >= d_r, d in D} e_d. Then C = {sum_r lambda_r g_r : all lambda_r > 0} (lambda_r = u_{d_r} - u_{d_{r-1}},
u_{d_0} = 0). Hence F > 0 on all of C iff G_r := F(g_r) >= 0 for every r and G_r > 0 for some r (if some G_r < 0, a
large lambda_r makes F negative; if all are 0, F = 0). G_r is the sum of c_x over the points x on layers >= d_r.

**Product forms.** With A_0 = b_2 - b_1, A_1 = b_0 - b_2, A_2 = b_1 - b_0 (so A_0 + A_1 + A_2 = 0) and c_x = sin A_x:
one point: G = sin A; two points: sin A + sin B = 2 sin((A+B)/2) cos((A-B)/2); three points:
sin a + sin b + sin c = 4 sin((a+b)/2) sin(a/2) sin(b/2) = -4 sin(a/2) sin(b/2) sin(c/2). Every factor is
sin(pi·phi) with phi affine in the phases of D (in units of pi; cos x = sin(x + pi/2)) and rational constants.

**Cells.** Fix the order of psi on the free layers D \ {0} (layer 0 has theta = 0). Under (G) those phases lie in the
open simplex 0 < psi_{p_1} < … < psi_{p_n} < 45°. A non-constant affine function maps this open simplex onto the open
interval between its smallest and largest value at the simplex's n + 1 vertices; sin(pi·x) has constant sign on an
open interval without integers. So each factor, hence each G_r, has a sign that is constant on the cell and is
computed exactly (`factor_sign`, rational arithmetic). If the sign pattern of (G_r) satisfies the cone lemma, the
orientation is the same for every configuration whose phases lie in the cell, and the clause
(not pattern) or (literal) holds. The pattern is written with the Y literals of consecutive layers of the order, which
imply the whole order together with the transitivity clauses (as in gen.py's `fam_angle`).

## 3. Threshold-order rules

Fix layers i < j and an orbit variable v whose three points lie on exactly these two layers: F = a u_i + b u_j. By
(H0), (u_i, u_j) ranges over 0 < u_i < u_j; up to a positive factor this is w(t) = (1 - t)(1, 1) + t (0, 1),
t in (0, 1), and F(w(t)) = (1 - t) P + t Q with P = F(1, 1) = G_1 and Q = F(0, 1) = G_2 (§2). F depends on the phases
only through d = theta_j - theta_i; on the pair's cell (i = 0: d in (0°, 45°); i >= 1: psi_i < psi_j gives
d in (0°, 45°), psi_i > psi_j gives d in (-45°, 0°)) the signs of P and Q are computed exactly as in §2.

For a literal l = s·v (s = ±1) put p = sP, q = sQ. If p > 0 > q on the cell, l is true exactly for t < t*(l) =
p/(p - q) ("small side"); if p < 0 < q, exactly for t > t*(l) ("large side"); at t = t* the orientation is 0, which
general position excludes. For two literals on the same side, t*(l1) <= t*(l2) iff Delta := p1 q2 - p2 q1 >= 0 (multiply by
(p1 - q1)(p2 - q2) > 0). Hence, if Delta < 0 on the whole open cell and both are small-side literals, l2 implies l1;
if Delta > 0 and both are large-side literals, l2 implies l1. Literals on different sides never imply each other.
The clause is (not cell premise) or (not l2) or l1.

**Sign of Delta on the open interval** (`thr_rules2.verify`). Delta is s1 s2 (P_a Q_b - P_b Q_a), a sum of two
products of sines of affine functions of d. At each endpoint e the values Delta(e) and Delta'(e) are computed
**exactly** in Q(zeta_16) (all arguments are multiples of pi/8 there; elements are vectors over Q in the basis
1, zeta, …, zeta^7 with zeta^8 = -1, so the zero test is exact). If Delta(e) = 0, the inward derivative D1 must be
nonzero with the required sign; then |Delta(e + x)| >= |D1| x - L2 x^2/2 > 0 for 0 < x < 2|D1|/L2, where L2 bounds
|Delta''| (product rule; |(prod_k sin(pi(c_k d + e_k)))''| <= pi^2 (sum |c_k|)^2). If Delta(e) != 0 its sign must be
the required one. On the rest, a bisection accepts [x0, x1] (centre c, width w) when
sigma Delta(c) - |Delta'(c)| w/2 - L2 w^2/8 > 1e-9 (Taylor with the bound L2). Delta(c) and Delta'(c) are evaluated in
double precision; their absolute error is below 1e-13 (at most 8 bounded factors per product), far below the margin.
**This one step is a floating-point computation with explicit error bounds, not exact arithmetic.** Candidates that
fail any test are dropped (dropping a clause is always sound).

## 4. Cell rules and bin-order clauses

Z(i, b) := [psi_i < b·45°/B] (b = 1..B-1; for B = 2, Z_i := Z(i, 1) = [psi_i < 22.5°]). Under (G) each psi_i lies in
exactly one open bin (b·45°/B, (b+1)·45°/B). A cell is an order pattern of the free layers of a triple (or pair)
together with a bin for each of them; its phase region is the open polytope "order chain ∩ open bin boxes". `cell_rules.py`
enumerates the vertices of its closure exactly (every choice of n active constraints, exact rational solve,
feasibility test) and checks that the open polytope is nonempty (its vertex centroid satisfies every constraint
strictly). The argument of §2 then applies verbatim with these vertices (the image of an open convex polytope under a
non-constant affine map is the open interval between the extreme vertex values). `cell_thr.py` applies §3 on the open
d-interval of the cell (endpoints multiples of 45°/B; exact endpoint algebra in Q(zeta_{16B})). The bin premise of a
clause is the negation of the bin literals (Z(L, b+1) if b < B-1, not Z(L, b) if b > 0). Ladder clauses
Z(i, b) => Z(i, b+1) and bin-order clauses [psi_j < psi_i] and Z(i, b) => Z(j, b) hold by the definitions.

## 5. The case split of the certificate

**Reflection.** The map (x, y) -> (x, -y) sends a configuration with (H), (N) to one with (H), (N): it keeps each
octagon (a regular octagon about O goes to one), each radius, general position and convex position. It fixes the
reference vertex of L_0 (angle 0), and sends the vertex of L_i at angle psi_i to angle -psi_i ≡ 45° - psi_i
(mod 45°), so psi_i becomes 45° - psi_i for psi_i in (0°, 45°). Hence a strictly decreasing psi_1 > … > psi_15
becomes strictly increasing. (Checked on exact data: the mirror images of the six monotone exact sets, four 120-point
sets and two 128-point near misses, have the decreasing order, `logs/controls2.log`.)

**The increasing cube.** If psi_1 < … < psi_15 then Y(i, j) is true for all 1 <= i < j <= 15: the 105 units of BASE.

**The Z cover** (`tools/verify_cover_mono.py`, enumeration of all 2^15 assignments). For a sequence of Booleans
Z_1..Z_15 let r + 1 be the index of the first false one (r = 15 if none). Then the assignment lies in the cube c_r and
in no other cube. Hence BASE ∧ c_r UNSAT for all r implies BASE UNSAT.

**Conclusion (Theorem 1).** If a 128-point 8-fold set without 9 points in convex position had a monotone phase
sequence, then by the layer lemma, the perturbation lemma and the reflection it would give a configuration with (H),
(G), (N) and an increasing sequence; its intended assignment would satisfy BASE (§1–§4) and one cube c_r. All 16 are
unsatisfiable (cake_lpr).

**Partially monotone sequences (Theorems 2–4).** For layers a <= b, "increasing on [a, b]" means
psi_a < psi_{a+1} < … < psi_b, with no condition on the other phases. The reflection maps "decreasing on [a, b]" to
"increasing on [a, b]" (it acts on every phase by psi -> 45° - psi). The base formula is encoder A + the same
families + the units Y(i, j) for a <= i < j <= b (Theorem 2: a = 2, b = 14, 78 units, `cnf/mono2to14.units`;
Theorem 3: a = 3, b = 13, 55 units; Theorem 4: the windows 1..12 and 4..15, 66 units each). The
cubes are the decision list on Z_a, …, Z_b: d_r = (Z_a … Z_{a+r-1} true, Z_{a+r} false) for r = 0 … b-a, and
d_{b-a+1} = (Z_a … Z_b true); the other Z are free. `tools/verify_cover_mono.py BASE DIR (b-a+1) (a-1)` checks the cover
by enumeration and the cube hashes. The perturbation lemma keeps "weakly increasing on [a, b]" strictly increasing on
[a, b] after perturbation, as in §0.
