# SYMK8N20261113: infinitesimal (multi-scale) analysis of the symmetric k = 8 problems (13 November 2026)

**Question.** For Problem A (does a 4-fold 56-point set without a convex octagon exist?) and Problem B (3-fold 63/64,
5-fold 60/61), can an *analytic* lever give exact structure or exact searches, instead of larger SAT runs?

**Lever chosen: limit order types of multi-scale configurations.** A configuration whose parts live at separated
scales, or differ by infinitesimal displacements, is a family of points that are polynomials in a symbolic ε. Its
order type for all small ε is computed *exactly* from lowest-order coefficients (Lemma 1, §1). This turns natural
infinite families (stacks of blocks at separated scales, twin orbits, new outer or inner orbits) into **finite, exact
and complete** searches: the dependence on a direction parameter is through finitely many critical directions
(Lemma 2), so one evaluation per open arc covers every limit order type of the family.

**Outcome.**
- **Architecture (COMPUTED).** All 15 known 52-point 4-fold sets are *stacks*: an outer square and/or a two-layer
  block and an inner square are decoupled by free scale gaps from a tight core of 9 to 11 layers (§2). The 56-point
  near misses are stacks 1 | 4 | 9 or 1 | 13 with all their (twin) octagons inside the core.
- **Infinitesimal rigidity of every known extremal set (COMPUTED, exact, complete for generic directions).**
  - 4-fold: no 52-point set extends to 56 points by one infinitesimal orbit (a twin of any layer, or a new layer at
    any scale position); no "delete one layer, add two infinitesimal orbits" gives 56 points (all 15 sets; two
    orbits of different kinds, or an orbit and its own twin: 183,136 completed pairs); the near misses with one
    layer of each twin pair deleted admit no infinitesimal orbit at all. Smallest octagon counts reached: 124 (one
    added orbit), 112 (delete one, add two), 1 (near misses) (§3).
  - 3-fold: neither 61-point set nor any of the ten 60-point sets extends by one infinitesimal orbit (best: 18 and 3
    octagons); "delete one orbit, add two" on the 61-point sets: 68,628 completions, none octagon-free; near-miss
    surgery on the 63/64-point near misses (delete one orbit, add one): none (best 3) (§4).
  - 5-fold: the 56-point set extends neither by one infinitesimal orbit (best 420 octagons) nor by deleting one
    orbit and adding two (8,178 pairs, best 450) (§4).
- **Proposition N (PROVED, written; exact check).** In an octagon-free m-fold set (m ≥ 3) a *strict radial needle*
  (one arm whose orbits have finite radial gaps and infinitesimal angular spread) has at most **10** orbits: its
  planar profile B must satisfy cup(B) + cap(B) ≤ 7. For m = 3 this condition is also sufficient, and 10 is attained
  for m = 3 and m = 4 (§5). So the "single almost radial arm of 20 orbits" family suggested in LBK8SYM cannot be
  near its needle limit; its near-feasible members must contain twin-like orbit pairs. Infinitesimal refinements
  of the extremal needles stop at 16 orbits (m = 3) and 10 orbits (m = 4) (beam searches, HEURISTIC).
- **Theorem H (PROVED, written) and scale-separated maxima (COMPUTED).** s ≥ 2 generic pairwise scale-separated
  squares never have more than s + 2 points in convex position; for 2 ≤ s ≤ 6 every such configuration has exactly
  s + 2 (exact, complete). So such 4-fold configurations have at most K − 3 layers without a convex K-gon
  (K = 5, …, 8), and — the point for lever 1 of the task — **every** configuration of at most five scale-separated
  squares is octagon-free: no system of conditions on at most five layers at a time (two-layer thresholds in
  log-radii and phases included) can bound the number of layers of a 4-fold octagon-free set (§6). 3-fold
  scale-separated orbits: 3 and 5 for K = 6, 7 (with or without centre), at least 7 for K = 8.
- **No new set and no impossibility theorem.** Every search family above is negative. For the 52-point sets the
  margins are large (at least 112 octagons), so these optima are not fine-tuned boundary points of the families.

Rigor labels: **PROVED** = written proof (not refereed); **COMPUTED** = exact computation (integer arithmetic,
validated); "complete" = all limit order types of the stated family for generic directions; **HEURISTIC** = beam
search (no completeness). Nothing is committed; no file outside this directory and the work directory
`/home/jay/research/data/symk8-20261113` was changed. All runs used systemd units `nov13-sym-*` with
CPUQuota 100 % each and at most three at a time, with two short exceptions: a single-threaded foreground DFS of
about two minutes next to three units (02:40), and an overlap of a few seconds between a fourth unit and three
walks (03:37), stopped at once.

## 1. The lever: limit order types of multi-scale configurations (analysis)

**Polynomial configurations.** A point is a finite sum P(ε) = Σ_k ε^k z_k (k ∈ Z, z_k ∈ Z²) in a symbolic
infinitesimal ε > 0. A family {P_i} is m-fold symmetric if it is closed under the rotation g applied to every
coefficient: (x, y) ↦ (−y, x) for m = 4 (Gaussian integers); for m = 3 the oblique coordinates (a, b) ↔ a + bω of
ES8SYM and `verify_indep.py` (an orientation-preserving linear image of the plane), with g: (a, b) ↦ (−b, a − b);
for m = 5, Z[ζ₅] with exact signs in Q(√5) (`tools/z5.py`).

**Lemma 1 (limit order type; PROVED, elementary).** For every triple, det(P_b − P_a, P_c − P_a) is a Laurent
polynomial in ε. If none is identically zero, there is ε₀ > 0 such that for every ε ∈ (0, ε₀) the points are in
general position and every orientation has the sign of the lowest-order nonzero coefficient; likewise for
coordinate comparisons. *Proof.* A nonzero Laurent polynomial has finitely many positive roots, and near 0⁺ its sign
is that of its lowest-order term. ∎
- So the number of convex K-gons is constant on (0, ε₀) and equals what an orientation-only convex-polygon DP
  computes from the limit signs. Every evaluated configuration is a genuine point set: take ε = 2^(−s) with s large
  and clear denominators (`tools/export_cfg.py`); for m = 3, 4 it is exactly symmetric with integer coordinates.
- `tools/polyeval.c`: all limit signs exactly (__int128, coefficients below 2^60, asserted), then the DP (anchor =
  lowest point in (y, x) order, angular sort by orientation; longest-chain and counting DPs). `tools/z5.py`: the same
  for m = 5 in Z[ζ₅] (signs of X + Y√5 decided exactly), with the same DP (`tools/cvxdp.c`).
- **Validation (exact):** ES8SYM `c4_52pts_13layers`: 141,809 convex 4-sets, 45,220 convex 7-sets, 0 octagons;
  LBK8SYM near misses A, B, 3oct: 2, 2, 3 octagons; ES8SYM `c3_61pts_centre`, `c3_61pts_blowup`: largest convex
  subset 7; `c3_63pts_3octagons_nocentre`, `c3_64pts_3octagons`: 3 octagons; ES8SYM
  `c5_56pts_11layers_centre`: 27,720 / 254,660 / 1,276,831 / 3,006,175 / 2,398,345 convex 3- to 7-sets and no
  octagon, identical to its verification log.

**Lemma 2 (move families and their critical directions; PROVED, one-line expansions).**
1. *Twin orbit (doubling).* Orbit l gets twins g^k(p + ε^E d), with E above every exponent at which an orientation
   of the current configuration is decided. Then orient(p, p + ε^E d, q) = ε^E·cross(d, lead(q − p)) + higher
   order, where lead(·) is the lowest-order nonzero coefficient vector, and every other orientation keeps its sign.
   So the limit order type depends on d only through its position among the rays ±lead(q − p), q ≠ p.
2. *New scale level.* A new orbit {ε^E g^k v} with E below all exponents (outer) or above them (inner). To leading
   order its orientations with the rest are sign cross(v, lead(q₁ − q₂)) (outer; plus sign cross(v, q) for
   antipodal new vertices, m even), sign cross(v·φ, lead(q)) with φ = ζ^j − 1 an edge or diagonal factor of the new
   polygon, or φ = 1 next to the centre or antipodal points (inner), or constants. So the critical directions of v
   are those of the q₁ − q₂ (outer) and of the q·conj(φ) (inner): factors 1, 1 ± i for m = 4, 1 and 2 + ω up to units
   for m = 3, 1 and ζ^(−j) − 1 for m = 5.
- In every case the limit order type is constant on each open arc between consecutive critical directions. The
  scans evaluate **one direction strictly inside every open arc** (the sum of the two bounding directions), and are
  therefore **complete for generic directions**. The finitely many critical directions themselves, where a
  higher-order term decides, are not covered.

**Lemma 3 (scale separation; PROVED, written proof sketch, not refereed).** Let X, Y be finite, O ∉ X ∪ Y,
all directions generic, and S = X ∪ εY. A set P = P_X ∪ εP_Y with both parts nonempty is in convex position for
small ε iff (a) P_X ∪ {O} is in convex position with O a vertex (or O lies on an edge p(−p) of it, and then
|P_Y| = 1), and (b) P_Y can be ordered y₁, …, y_a so that the directions of y_{i+1} − y_i increase strictly inside
the open arc (dir(−p), dir(q)), where p, O, q are consecutive on conv(P_X ∪ {O}) (if |P_X| = 1, p = q and the arc
is a half-turn).
*Proof (sketch).* At y₁ the turn (p, εy₁, εy₂) has, to leading order, the sign of cross(−p, y₂ − y₁); at y_a that of
cross(y_a − y_{a−1}, q); the interior turns are those of Y; the turns at p and q tend to those at O; the turning
angles add up to 2π. Conversely the limit of a convex polygon is weakly convex with the εY part collapsed to the
vertex O; the εY points are consecutive on the polygon (a weakly convex limit polygon with X ∪ {O} in general
position, apart from antipodal pairs through O, visits O only once), O cannot be interior (the εY points would not
be vertices), and the same leading-order turns must be positive. ∎
- *Outer add-on* (a regular m-gon V at a larger scale than Y): S is octagon-free iff Y is, Y has no 7-chain in
  the half-turn windows (dir(−v), dir(−v) + π) of the vertices v of V, and no (8 − s)-chain in the window of any s
  consecutive vertices of V.
- *Inner add-on* (a small m-gon W inside X): for every convex polygon Q of X ∪ {O} with O as a vertex,
  (|Q| − 1) + a_W(window of Q at O) ≤ 7, with a_W the longest chain of W in that window (≤ 3 for a square).
- These "profiles" explain the architecture of §2. The computations do not depend on Lemma 3: every configuration
  is evaluated directly with Lemma 1.

## 2. Architecture of the known extremal sets (COMPUTED)

A **free cut** is a layer boundary at which an infinitesimal scale gap can be inserted without creating a convex
octagon: the outer layers X stay and the inner layers Y become εY (exact limit, Lemma 1). Tool `tools/arch.py`,
log `logs/arch.txt`.

| set (t layers) | octagons | free cuts | blocks (outer to inner) |
|---|---|---|---|
| ES8SYM `c4_52pts_13layers` | 0 | 1, 12 | 1 \| 11 \| 1 |
| 6 LBK8SYM calibration sets `s13_{29_65, 43_32, 45_74, 60_156, 74_127, 79_39}` | 0 | 1, 10, 12 | 1 \| 9 \| 2 \| 1 |
| 8 LBK8SYM calibration sets `s13_{19_10, 2_67, 27_30, 33_230, 46_30, 47_100, 54_145, 78_210}` | 0 | 10, 12 | 10 \| 2 \| 1 |
| LBK8SYM near miss B and 3-octagon near miss (t = 14) | 2, 3 | 1, 5 | 1 \| 4 \| 9 |
| LBK8SYM near miss A (t = 14) | 2 | 1 | 1 \| 13 |

- The listed cuts are also jointly free. For the ES8SYM set every other single cut creates between 4,316 and
  249,568 octagons (`tools/splits.py`).
- So **every known 52-point 4-fold set is a stack**: an outer square and/or a two-layer block and an inner square,
  decoupled by arbitrarily large scale gaps from a tight core of 9 to 11 layers. (A large radius ratio is not enough:
  `s13_78_210` has ratio 0.000 at cut 1, which is not free.)
- In `s13_29_65` and `s13_78_210` the core is a spiral of near-twin pairs (ratios 0.997 to 1.000, equal phases).
  These twins are **infinitesimal doublings**: deleting one layer of a pair and re-doubling its partner in a generic
  direction gives octagon-free 13-layer configurations (they appear among the free single moves of §3).
- All octagons of the near misses (twin octagons, i.e. failures of nesting, ALGAN §3) lie inside the core block:
  pairs (10, 11), (12, 13) of A; (7, 8), (12, 13) of B; (7, 8), (10, 11), (12, 13) of the 3-octagon set.

## 3. Problem A (4-fold, 56 points): infinitesimal extensions of every known set (COMPUTED)

Library (`sets/lib4/` of the work directory): the ES8SYM 52-point set, the 14 exact 52-point calibration sets of
LBK8SYM (for each, the first scale among 2^40, 2^50, 2^30 whose EXACT-PREP and CVX2 passed there), and the three
56-point near misses.

**3.1 One infinitesimal orbit (13 → 14 layers).** For each of the 15 sets (`tools/twostep.py`, `logs/b4a.log`,
`logs/b4b.log`), one direction per open critical arc of:
- a twin of each of the 13 layers (102 arcs per layer);
- a new square at a larger scale than the whole set (outer) and at a smaller scale (inner);
- and (`tools/addon_exact.py`, `logs/b4nm.log`) a new square at **every level position of the stretched stack** of
  §2 (free cuts made infinitesimal): above the top block, between any two consecutive blocks, below the bottom one.

Result: **no octagon-free configuration.** The smallest octagon count over all single moves is 124 to 336 per set
(always reached by a twin). New levels are much worse: on the stretched ES8SYM stack, 13,344 / 13,780 / 11,504 /
11,004 octagons at least for the four level positions; a plain outer square over the unstretched ES8SYM set at
least 1,628. In all, 4,030 single moves per set.

**3.2 Delete one layer, add two infinitesimal orbits (13 − 1 + 2 = 14).** For each set and each deleted layer
(195 bases of 12 layers):
1. all single moves on the base B (twins of every layer, outer and inner levels) are evaluated; the octagon-free
   ones are 13-layer octagon-free limit configurations (2,612 of them in all);
2. for every octagon-free first move a, the critical arcs of every *other* move family are recomputed on B + a, and
   every second move whose direction lies in an arc that was octagon-free for B alone is evaluated. Any other arc
   already gives an octagon of B + (second move), which survives in B + a + (second move).

Result: 14,728 completed pairs, **none octagon-free**; smallest octagon count 112. In all 729,690 single-move
evaluations. In 102 of the 195 bases all octagon-free first moves belong to one family (in the printed samples
mostly twins of a layer adjacent to the deleted one), so no cross-family pair exists there; 42 bases have fewer than
two octagon-free first moves. Scope: pairs from different families (twins of two different layers, a twin and a
level, an outer and an inner level), and (3.2b) a first move followed by a twin *of the new orbit*.

**3.2b Twin of the new orbit** (`tools/twin2.py`, `logs/twin2.log`): for every base and every octagon-free first
move a (a twin of a layer, or a new outer or inner square), every twin of the new orbit a, one direction per open
critical arc on B + a (a twin of a twin, or a new square together with its own twin, i.e. a two-layer block in the
twin regime at a new scale). Result: all 195 bases, 2,612 first moves, 168,408 second moves, **none
octagon-free**; smallest octagon count 132.

Not covered: two new orbits at the same new scale with a finite radius ratio, and three or more new points per
vertex at one scale; §3.4 explores some of these heuristically.

**3.3 Near misses.** Deleting one layer of each twin pair of A (4 choices) or B (4 choices) leaves 12 octagon-free
layers. Single moves: 27,456 evaluated, **none octagon-free** (best: 1 octagon, i.e. a twin octagon re-created).

**3.4 Beam searches in the infinitesimal regime (HEURISTIC; `tools/beam_inf.py`, `logs/misc.log`,
`logs/beam2.log`).** Moves: twins of any orbit (also of new ones), new levels at new extreme scales; beam ranked by
the number of convex 7-gons.
- From the 9-layer core of `s13_29_65` with its four twin partners deleted: 13 layers (52 points) are reached again,
  no 14th (27,102 evaluations at the last depth).
- From `s13_78_210` with its three twin partners deleted (10 layers): only 12.
- Bases with the bottom block removed (`logs/beam2.log`): ES8SYM set without its inner square (12 layers), without
  its outer and inner squares (11), `s13_29_65` and `s13_19_10` without their 3-layer bottom (10): every beam
  returns to 13 layers and stops. Rebuilding the 9-layer core of near miss B infinitesimally on top of its 5 outer
  layers reaches only 11 layers.
- From the 10-layer 4-fold strict needle of §5 (40 points): no infinitesimal orbit can be added (1,156 single
  moves, none octagon-free; `logs/needle4_beam.log`).
- Random walks (`tools/walk.py`, `logs/walk*.log`): from four of the 52-point sets (ES8SYM, `s13_29_65`,
  `s13_46_30`, `s13_33_230`), repeatedly delete a random orbit and add a random octagon-free infinitesimal orbit
  (the configurations become deep hierarchies of twins, exponents up to 16), scanning at every step all single moves
  for a 14th orbit: 146 + 183 + 40 + 25 steps, no 14th orbit; smallest octagon counts 244, 217, 116 and 212.

**Reading.** Every known 52-point 4-fold set is *infinitesimally rigid*: no infinitesimal orbit can be added, and no
delete-one/add-two modification in the scopes of 3.2 and 3.2b works; the near misses cannot be repaired
infinitesimally. The margins are large (at least 112 octagons), so this is not an artefact of a narrow window. A
56-point set, if it exists, is not an infinitesimal modification of a known 52-point set in these scopes.

## 4. Problem B (3-fold 63/64, 5-fold 60/61): infinitesimal extensions (COMPUTED)

**3-fold** (`sets/lib3/`: ES8SYM `c3_61pts_centre`, `c3_61pts_blowup`, `c3_60pts_nocentre`, `c3_60pts_nocentre_b`,
the eight `threefold60/base60_cost3_minus*`, and the near misses `c3_64pts_3octagons`,
`c3_63pts_3octagons_nocentre`, `threefold60/control_cost3_63pts`).
- **Architecture** (`tools/arch3.py`, orbits in radius order, `logs/hier.log`): the 3-fold sets are stacks too.
  Free cuts: 1, 16 (`c3_61pts_centre`); 1, 9, 16 (`c3_61pts_blowup`); 1, 18 (`c3_60pts_nocentre`); 1, 16, 18
  (`c3_60pts_nocentre_b` and six of the `base60_cost3_*`; 1, 5, 16, 18 for `minus6`; 16, 18 for `minus20`); the near
  misses 8, 11, 17, 19 (`c3_63pts_3octagons_nocentre`, `c3_64pts_3octagons`; their octagon orbit, orbit 0 with one
  point of each of orbits 1–7, lies inside the top block) and 1, 17, 19 (`control_cost3_63pts`; there the octagon
  orbit crosses the free cut 1 and survives the stretching).
- **One infinitesimal orbit** (twin of any orbit, outer or inner level; `logs/b3.log`, 116,240 evaluations; also
  `tools/double_exact.py`, `logs/double3.log`):
  - 61-point sets → 64 points: best 18 octagons;
  - 60-point sets → 63: best 189 and 192; `base60_cost3_*` → 63: best 3 (the near-miss pattern);
  - **no octagon-free extension.** (Adding the centre to a 60-point set already gives 19,026 to 28,032 octagons.)
- **Delete one orbit of a 61-point set, add two** (→ 64; 40 bases): 1,999 octagon-free first moves, 68,628
  completed pairs, **none octagon-free**; best 18.
- **Near-miss surgery** (delete one orbit of a 63- or 64-point near miss, add one infinitesimal orbit; 63 bases,
  `logs/b3nm.log`, 610,680 evaluations): deleting any of orbits 0–7 of `c3_64pts_3octagons` removes its octagon
  orbit (61 points left), but every re-addition creates at least 3 octagons again; **none octagon-free**.
- Pure arm (§5): beam searches that add twins and levels to the extremal 10-orbit needle reach 16 orbits
  (48 points), or 16 orbits and the centre (49 points), and stop (HEURISTIC).

**5-fold** (`sets/lib5/c5_56pts_11layers_centre.pts`, ES8SYM; exact Z[ζ₅] arithmetic, `tools/z5.py`).
- One infinitesimal orbit (→ 61 points): twins of the 11 orbits (best 420 octagons), new outer level (1,144 arcs,
  best 1,150), new inner level (44 arcs, best 69,180). **No octagon-free extension** (`logs/z5.log`, 2,398
  evaluations).
- Delete one orbit, add two (→ 61; `tools/z5pairs.py`, `logs/b5.log`): for each of the 11 orbits deleted, all
  single moves (1,980 per base); 358 octagon-free first moves in all (242 of them when the outer orbit is deleted);
  8,178 completed pairs, **none octagon-free** (best 450).

## 5. The strict radial-needle limit (written proof + exact check): Proposition N

**Setting.** A *strict radial needle* ("single arm"): n orbits whose representatives r_j(1 + ε e_j τ) lie on one ray
up to an infinitesimal transversal perturbation (τ ∉ R fixed), with r_j distinct and finite. Put
B = {(r_j, r_j e_j)} ⊂ R² (the planar profile), and cup(B), cap(B) for its longest x-monotone convex and concave
chains.

**Proposition N.** Let m ≥ 3.
1. If the m-fold configuration has no convex octagon, then cup(B) + cap(B) ≤ 7. By the Erdős–Szekeres cups–caps
   theorem (no k-cup and no l-cap gives at most C(k + l − 4, k − 2) points), **n ≤ max_{k+l=9} C(5, k − 2) = 10**.
2. For m = 3 and the arm alone, the converse holds: the 3n points have no convex octagon iff cup(B) + cap(B) ≤ 7;
   n = 10 is attained.

*Proof.* For points p_j = r_j + ε y_j τ of one needle (ray 0), det(p_b − p_a, p_c − p_a) =
ε·Im τ·det((r_b − r_a, y_b − y_a), (r_c − r_a, y_c − y_a)) + O(ε²): to leading order the needle is the profile B,
so convex polygons inside one needle are convex polygons of B (an 8-gon of B contains a cup and a cap with 10
points in all). For p_a, p_b on ray 0 and q on a ray at angle θ ∉ {0, π}, orient(p_a, p_b, q) =
(r_b − r_a)·|q| sin θ + O(ε). Hence, in a convex polygon that arrives on ray 0 from a ray on the side sin θ > 0 and
leaves to a ray on the same side, the chain on ray 0 runs outward: its first and last edges point away from O, and
it cannot reverse direction inside the needle (a reversal is a turn of π, and the transition turns already use a
positive amount of the total 2π).
For a polygon on two needles at angle θ = 2π/m ∈ (0, π), the chain on ray 0 is therefore an outward chain with left
turns, i.e. a **cup** of B, and the chain on ray θ (rotated back) an inward chain with left turns, i.e. a **cap**
of B. Conversely every cup and every cap can be joined: the four transition turns lie in (0, π) for all radii (the
turning angles are α₁, θ + π − α₁, α₂ − θ − π and 2π − α₂ with α₁ ∈ (θ, π), α₂ ∈ (θ + π, 2π)), and they add up to
2π. So the largest two-needle polygon has cup(B) + cap(B) vertices, which proves 1. For m = 3, a polygon visiting
all three needles has one vertex on each: a chain of two or more points on ray 0 would arrive from the ray at
−2π/3 (first edge inward) and leave to the ray at +2π/3 (last edge outward), so it would turn by π inside the
needle and the total turning would exceed 2π. So the octagons of the 3-fold arm are exactly those of 1, which proves
2. ∎

**Exact check** (`tools/needle_test.py`, `logs/needle.log`): the Erdős–Szekeres profile with cup 3, cap 4
(10 points) gives a 30-point 3-fold configuration with no convex octagon; 280 of 280 random profiles (5 to 11 points)
agree with "octagon-free iff cup + cap ≤ 7"; 50 of 50 eleven-point extensions of the 10-point profile have octagons.

**m = 4: the bound 10 is attained** (`tools/needle4.py`, `logs/needle4.log`; the search is HEURISTIC, the example is
exact). For m = 4 the two antipodal needles are *exactly* the affine image (x, εy) of B ∪ (−B), so B ∪ (−B) must be
octagon-free as well. The Erdős–Szekeres profile (cup 3, cap 4) fails this: its 40-point needle has 1,876 octagons,
938 in each antipodal pair. A hill-climbing search over profiles found octagon-free 4-fold needles with n = 4, …, 10
orbits; the 10-orbit one (cup 4, cap 3) is `sets/needle4_n10.json` (here and in the work directory). So a
strict needle holds at most 10 orbits for every m ≥ 3, with equality for m = 3 and m = 4. (The known 52-point sets use at most 5
near-aligned layers per group, ALGAN §3, so needles are not what limits them.)

**Independent exact check of the two extremal needles.** Exported with ε = 2^(−40) to integer coordinates
(`tools/export_needles.py`; `sets/needle3_es10_S40.pts`, 30 points, and `sets/needle4_n10_S40.pts`, 40 points, in
this directory) and checked with LBK8SYM's independent verifier `tools/verify_indep.py` (standard library, two
differently anchored DPs): rotation-closed, no collinear triple, largest convex subset 7 for both
(`logs/verify_needles.log`).

**Consequence for Problem B.** The single-arm templates of LBK8SYM have an arm of 20 orbits. A strict needle holds
at most 10 orbits, so the near-feasible members of that family (margin −1.5e-4) cannot be close to their needle
limit: some consecutive arm orbits must have log-radial gaps that are not large compared with their angular gaps
(the twin regime), where the leading-order needle analysis does not apply. Infinitesimal twin refinements of the
extremal 10-orbit needle (beam search, §4) stop at 16 orbits. A construction attempt in this family should be
organized around twin pairs with finite gaps between pairs, not around a needle.

## 6. Scale-separated (hierarchical) configurations (COMPUTED tables; Theorem H PROVED)

`tools/hier_dfs.py`: orbit j is a regular m-gon at scale ε^j (all scales pairwise separated), phases generic. A
depth-first search adds innermost orbits, one direction per open critical arc (Lemma 2, inner level), prunes
configurations with a convex K-gon, and so visits every limit order type of the family.

| m | centre | K = 6 | K = 7 | K = 8 |
|---|---|---|---|---|
| 4 | no | 3 layers (12 points) | 4 (16) | **5 (20)** |
| 3 | no | 3 (9) | 5 (15) | ≥ 7 (21); search not finished in 900 s |
| 3 | yes | 3 (10) | 5 (16) | ≥ 7 (22); not finished in 600 s |

- For m = 4 the maximum is K − 3 for K = 5, 6, 7, 8. For K = 8 the numbers of octagon-free configurations at depths
  1–5 are 1, 2, 8, 48, 384, which is **every** configuration of these depths (2(j − 1) arcs at depth j), and none of
  the 3,840 configurations of depth 6 is octagon-free (4,282 evaluations = 2 + 8 + 48 + 384 + 3,840,
  `logs/hier.log`; the complete enumeration `tools/hier_all.py`, `logs/hier_all.txt`, gives the same).
- **Phase independence (COMPUTED).** Combining the DFS for K = 5, …, 8 (every configuration of s = K − 2 squares
  contains a convex K-gon) with the complete enumeration (the largest convex subset over all configurations of s
  squares is 4, 5, 6, 7, 8 for s = 2, …, 6): **every** generic scale-separated configuration of s squares,
  2 ≤ s ≤ 6, has largest convex subset exactly s + 2, whatever the phases.

**Theorem H (PROVED, written proof, not refereed; uses Lemma 3).** Let s ≥ 2 and let Q_1, …, Q_s be squares
centred at O with pairwise separated scales (Q_{j+1} = o(Q_j)) and generic orientations. Then every subset of
Q_1 ∪ … ∪ Q_s in convex position has at most s + 2 points. (So the upper half of the phase independence holds for
all s; the lower half fails from s = 7 on, see below.)

*Proof.* Scale the plane so that Q_j has circumradius 1; the deeper squares collapse to O. For an open window
W = (α, β) of directions with |W| ≤ π, let C_k(W) be the largest number of points of k consecutive scale-separated
squares that form a chain whose consecutive edge directions increase strictly inside W (the shape of the part of a
convex polygon that enters the cluster with direction α and leaves it with direction β). In such a chain the points
of the largest square used are vertices w₁, …, w_a of that square, in counter-clockwise order, and by Lemma 3 the
smaller squares contribute at most one contiguous *dip*, which in the limit is the vertex O: before w₁ (sub-window
(α, φ₁)), between w_i and w_{i+1} (sub-window (φ_i + π, φ_{i+1})) or after w_a (sub-window (φ_a + π, β)), φ_i the
direction of w_i. The chord from the vertex at angle φ to the vertex at angle φ' has direction (φ + φ')/2 + π/2, so
consecutive chords of three vertices differ by at least π/2, four vertices need a window longer than π, and:
- two counter-clockwise neighbours (chord φ₁ + 3π/4) with a dip before or after need |W| > 3π/4 and leave a dip
  window of length < |W| − 3π/4 ≤ π/4;
- a dip between w₁ and the clockwise neighbour w₂ (φ₂ = φ₁ + 3π/2) has window length exactly π/2 (and |W| > π/2);
- a dip between two antipodal vertices has window length 0, so it holds one point;
- between counter-clockwise neighbours a dip would need a turn of 3π/2; three vertices fit in a window of length
  ≤ π only as two counter-clockwise steps of total angle < 2π, and then the only possible dip is the one-point dip
  between an antipodal pair (a dip before or after needs a window longer than 5π/4).
By induction on k (k = 1: at most 2 points if |W| ≤ π/2, at most 3 if |W| ≤ π):
  U(k): C_k(W) ≤ k + 1 if |W| ≤ π/2,   V(k): C_k(W) ≤ k + 2 if |W| ≤ π.
For U(k): no point of the largest square gives C_{k−1}(W) ≤ k; one vertex plus a dip gives 1 + U(k − 1) ≤ k + 1;
two vertices fit only as one chord (2 points) or as an antipodal pair with a one-point dip (3 ≤ k + 1); three
vertices need |W| > π/2. For V(k): no point gives ≤ k + 1; one vertex plus a dip gives 1 + V(k − 1) ≤ k + 2; two
vertices with a dip give 2 + U(k − 1) ≤ k + 2 (dip windows ≤ π/2 by the list above) or 3; three vertices give 3,
or 4 ≤ k + 2 with a one-point dip (a dip needs k ≥ 2).
Finally a convex polygon either avoids Q_1 (then it has at most (s − 1) + 2 points by induction on s) or meets Q_1
in one vertex (window π: 1 + V(s − 1) ≤ s + 2), in two neighbouring vertices with O between them (window π/2:
2 + U(s − 1) ≤ s + 2), in two antipodal or three vertices (O on an edge, one more point: ≤ 4), or in four vertices
(no other point). ∎

- **Random check of Theorem H** (`tools/hier_random.py`, `logs/hier_random.log`, 300 random configurations per s for
  s ≤ 8, 100 for s = 9, 10): the bound s + 2 is never exceeded. For s ≤ 6 every sample has exactly s + 2; from
  s = 7 on the phases matter: the largest convex subset takes the values {8, 9} for s = 7, {9, 10} for s = 8,
  {9, 10, 11} for s = 9 and {10, 11, 12} for s = 10. So the lower half of the phase independence is false from s = 7
  on, and for larger K scale-separated stacks can exceed K − 3 layers without a convex K-gon (a sampled
  configuration of 9 squares with largest convex subset 9 has no convex 10-gon, while K − 3 = 7). For K = 8 they
  cannot: every configuration of six squares already has an octagon.
- **Consequence (PROVED): the threshold lever cannot decide Problem A.** By Theorem H with s ≤ 5, *every* generic
  scale-separated configuration of at most five squares has at most 7 points in convex position. So a 4-fold
  configuration of t pairwise scale-separated squares, for any t, satisfies every necessary condition for
  octagon-freeness that involves at most five layers at a time (its 5-layer subsets are again scale-separated with
  generic phases). Hence no system of two-layer thresholds (ALGAN's Lemma 2 is the K = m + 1 case; for m = 4, K = 8
  the two-layer condition is nesting) or of three-, four- or five-layer conditions — in particular no LP or
  threshold system in log-radii and phases built from them — can bound the number of layers. Any proof that
  t ≤ 13 must use configurations of at least six layers at once. This is why lever 1 of the task cannot decide
  Problem A.
- Compared with 13 layers for the known sets, scale separation alone is weak: the extremal sets need tight cores
  with finite radius ratios, which is what §2 shows.

**Novelty.** Lemmas 1–3 are standard limit arguments (the scale-separation picture is the centre analogue of the
blow-ups of Baek–Balko, SoCG 2025). Proposition N and Theorem H are elementary and new in the repository records
(grep for "needle", "scale-separated", "s + 2"); they were not checked against the literature.

## 7. Status of the claims

| claim | label | where |
|---|---|---|
| Lemma 1 (limit order type), Lemma 2 (critical directions of twin and level moves) | PROVED (elementary, written) | §1 |
| Lemma 3 (scale separation; outer and inner add-on conditions) | PROVED (written proof sketch, not refereed); not used by any computation | §1 |
| the evaluator reproduces the published counts of the exact sets (m = 3, 4, 5); realizations at ε = 2^(−20), 2^(−40), 2^(−60) recounted by independent code give the limit count; 2,000 random directions never beat the arc minimum | COMPUTED | §1, `logs/crosscheck.txt` |
| architecture: every known 52-point 4-fold set is a stack (§2 table) | COMPUTED (exact) | §2 |
| no infinitesimal orbit extends any known 52-point 4-fold set (twin of any layer; new level at any position) | COMPUTED (exact, complete for generic directions) | §3.1 |
| no "delete one layer, add two infinitesimal orbits" (different families, or an orbit and its own twin) gives an octagon-free 56-point limit configuration from a known 52-point set | COMPUTED (exact, complete in that scope) | §3.2, §3.2b |
| the near misses with one layer of each twin pair deleted admit no infinitesimal orbit | COMPUTED (exact, complete) | §3.3 |
| the same rigidity for the 3-fold 61- and 60-point sets and near misses, and for the 5-fold 56-point set | COMPUTED (exact, complete in the stated scopes) | §4 |
| Proposition N: a strict radial needle of an octagon-free m-fold set (m ≥ 3) has at most 10 orbits; for m = 3, octagon-free iff cup + cap ≤ 7 | PROVED (written) + COMPUTED check (280/280) | §5 |
| the bound 10 is attained for m = 3 (Erdős–Szekeres profile) and m = 4 (profile `needle4_n10.json`, found by search) | COMPUTED (exact; both examples also pass LBK8SYM's independent verifier at ε = 2^(−40)) | §5 |
| Theorem H: s ≥ 2 generic scale-separated squares have at most s + 2 points in convex position; hence conditions on ≤ 5 layers at a time cannot bound the number of layers | PROVED (written, not refereed) | §6 |
| scale-separated maxima K − 3 (K = 5, …, 8); largest convex subset exactly s + 2 for every configuration of 2 ≤ s ≤ 6 squares | COMPUTED (exact, complete for generic phases) | §6 |
| beam searches (twins and levels from cores and needles) | HEURISTIC | §3.4, §4 |
| 4-fold maximum 52, 3-fold maximum 61, 5-fold maximum 56 | **not claimed** (evidence only) | — |

## 8. Assessment and next steps

- **Problem A.** The known optima are infinitesimally rigid with large margins, and so are the near misses. With
  LBK8SYM (no realization at any scanned t = 14 phase vector) and ALGAN (every abstract t = 14 model so far is
  refuted by symmetric final polynomials), the evidence for "4-fold maximum = 52" grows, but nothing here proves
  it. The analytic lever gives exact local information (rigidity, architecture, needle and scale-separation
  bounds) and proves that conditions on at most five layers at a time cannot decide the question (Theorem H, §6).
  A proof still needs a certified SAT run (encoder A with Y(1,2) and phase-order cubes, as in C6UPPER), which is an
  author decision because of the machine load.
- **Problem B.** Proposition N closes the strict single-arm family (at most 10 arm orbits). The 61-, 60- and
  56-point sets are rigid, so a 3-fold 63/64 or a 5-fold 60/61 set needs a different core. A construction attempt
  should search *twin-refined spirals* with finite gaps between twin pairs (the structure of the 52-point
  calibration sets `s13_29_65`, `s13_78_210`), for example template + LP as in LBK8SYM but with exact twin
  directions chosen from the critical arcs of Lemma 2.
- **Tools for reuse.** `polyeval.c` + `twostep.py` scan all infinitesimal modifications of an m-fold set (m = 3, 4)
  exactly in seconds; `z5.py` and `z5pairs.py` do the same for m = 5. They certify that a candidate set is
  "infinitesimally saturated", and can enumerate all limit configurations of a stack (Lemma 3).
- **Beyond Theorem H.** The lower bound s + 2 holds for s ≤ 6 and fails from s = 7 on (random examples with s + 1
  and even s points). The exact growth of the minimum largest convex subset of s scale-separated squares is open; it
  would give the scale-separated maximum for every K (K − 3 for K ≤ 8).

## 9. Files

Work directory `/home/jay/research/data/symk8-20261113` (`<w>`); copies of the tools and logs are in `tools/` and
`logs/` here. The input sets were copied from ES8SYM (`sets/c4_52pts_13layers.pts`, `sets2/`, `sets3/`, `sets4/`) and
LBK8SYM (`sets/`, and the calibration sets of `<lb-work-dir>/exact/*/cand.pts`) into `<w>/sets/lib{3,4,5}/`.

| file | content |
|---|---|
| `tools/polyeval.c` (`polyeval2.c`: wider exponent range) | exact limit signs of polynomial configurations + convex-polygon DP (m = 3, 4) |
| `tools/cvxdp.c`, `tools/stackeval.c`, `tools/stack.py` | DP on a sign table; monomial-only evaluator used for the first experiments and the realization check |
| `tools/double_exact.py`, `tools/addon_exact.py`, `tools/twostep.py` | complete arc scans: twins, new levels (also at every stack position), delete-one/add-two pairs |
| `tools/z5.py`, `tools/z5pairs.py` | the same for m = 5 in Z[ζ₅] |
| `tools/arch.py`, `tools/arch3.py`, `tools/splits.py` | free cuts / stack architecture (m = 4, m = 3) |
| `tools/needle_test.py`, `tools/needle4.py` | Proposition N check (m = 3); 4-fold needle search |
| `tools/hier_dfs.py`, `tools/hier_all.py`, `tools/hier_random.py` | scale-separated configurations (DFS, complete enumeration, random check of Theorem H) |
| `tools/beam_inf.py`, `tools/walk.py` | beam search and random walk over infinitesimal moves (HEURISTIC) |
| `tools/crosscheck.py`, `tools/crosscheck2.py`, `tools/export_cfg.py`, `tools/summarize.py` | realization and sampling checks, export to integer sets, log summaries |
| `tools/addon.py`, `tools/insert1.py`, `tools/replace.py` | first coarse rotation-grid scans (superseded by the exact arc scans) |
| `tools/batch*.sh`, `tools/run_double3.sh` | the unit scripts |
| `logs/arch.txt` | §2 |
| `logs/b4a.log`, `logs/b4b.log`, `logs/b4nm.log` | §3 (4-fold single moves, pairs, level positions, near misses) |
| `logs/b3.log`, `logs/b3nm.log`, `logs/double3.log` | §4 (3-fold) |
| `logs/z5.log`, `logs/z5test.log`, `logs/b5.log` | §4 (5-fold) |
| `logs/needle.log`, `logs/needle4.log`, `logs/needle4_beam.log` | §5 |
| `logs/misc.log`, `logs/beam2.log`, `logs/walk*.log` | beams and walks (HEURISTIC) |
| `logs/hier.log`, `logs/hier_all.txt`, `logs/hier_random.log` | §6 (and the 3-fold architecture, at the end of `hier.log`) |
| `logs/crosscheck.txt` | §1 validation |

## Reproduction

```sh
cd tools && gcc -O2 -shared -fPIC -o libpolyeval.so polyeval.c && gcc -O2 -shared -fPIC -o libpolyeval2.so polyeval2.c \
  && gcc -O2 -shared -fPIC -o libcvxdp.so cvxdp.c
PY=python3   # with numpy
$PY twostep.py 4 <w>/sets/lib4/es8sym_52.pts                      # 4,030 single moves, none octagon-free, best 330
$PY twostep.py 4 <w>/sets/lib4/es8sym_52.pts --remove 6 --pairs   # 12-layer base: free singles, then all pairs
$PY addon_exact.py 4 <w>/sets/lib4/es8sym_52.pts '1,12' 2         # new square between blocks of the stretched stack
$PY twostep.py 3 <w>/sets/lib3/c3_61pts_centre.txt               # 3-fold: best 18
$PY z5.py <w>/sets/lib5/c5_56pts_11layers_centre.pts both          # 5-fold: counts as in ES8SYM, then the scans
$PY needle_test.py 1                                               # Proposition N check
$PY hier_dfs.py 4 --K 8                                            # depth 5, counts 1, 2, 8, 48, 384
$PY crosscheck.py                                                  # realization at eps = 2^-20, 2^-40, 2^-60
```

## 10. Log (13 November 2026, KST; from file times)

| time | step | result |
|---|---|---|
| 02:02 | read ALGAN, LBK8SYM; chose the infinitesimal lever (ALGAN's Lemma 2 is the K = m + 1 threshold; for m = 4, K = 8 the two-layer condition is nesting, so thresholds alone say little) | — |
| 02:22 | exact DP on sign tables (`cvxdp.c`); validation on the 52- and 56-point sets | counts reproduced |
| 02:23 | free cuts of the 52-point set and the near misses; extra outer/inner square (coarse scan) | stack architecture; thousands of octagons |
| 02:28–02:31 | monomial and polynomial exact evaluators; complete arc scans (levels, twins) | ES8SYM set rigid (best 330) |
| 02:35 | 3-fold twin scans (`nov13-sym-dbl3`) | none (best 18 / 3) |
| 02:38 | scale-separated DFS | 4-fold: 3, 4, 5 layers for K = 6, 7, 8 |
| 02:48–03:15 | batches `nov13-sym-{b3, b3nm, b4a, b4b2, b4nm, z5, b5, misc, final}` (at most 3 at a time) | §3, §4 |
| 02:51 | Proposition N check | 280/280 |
| 02:54 | architecture of all 18 sets | §2 table |
| 03:15 | realization cross-check; sampling checks of arc completeness | 330 = 330 at ε = 2^(−20), 2^(−40), 2^(−60); 2,000 random directions never below the arc minimum (three families) |
| 03:29 | 4-fold needle search | octagon-free 4-fold needles up to 10 orbits; no infinitesimal extension of the 10-needle |
| 03:31 | 5-fold delete-one/add-two finished | 8,178 pairs, none |
| 03:35 | Theorem H (upper bound s + 2) written; random check up to s = 10 | bound never exceeded; lower bound fails from s = 7 |
| 03:42–04:17 | twin of the new orbit after a delete-one move (`nov13-sym-twin2`) | 168,408 second moves, none (best 132) |
| 03:34–03:57 | random walks over 13-layer limit configurations (`nov13-sym-walk{1,2,3,4}`; walk3 stopped at 03:37 to keep the cap, walk4 at 03:41 for the needle check) | 394 steps, no 14th orbit (best 116) |
