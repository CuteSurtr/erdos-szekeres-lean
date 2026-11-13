# THEORY310N20261113: structural routes below ES(8) ≤ 310 (night of 13 November 2026)

Theory fork of the 13 November session, 02:10–05:40 KST. **No new bound is claimed.**
This record lists candidate lemmas aimed at the composition
|S| ≤ 1 + n_H + n_R ≤ 1 + 187 + 121 that do not just add residual rows. Each lemma
has a status:
- **PROVED**: a written proof, plus an exact or empirical check where stated.
- **REFUTED**: an explicit counterexample or a negative computation.
- **OPEN**: with evidence.

Work directory: `/home/jay/research/data/theory310-20261113/` (abbreviated W). The small
scripts and outputs are copied to `tools/` and `data/` here; CNF and LRAT files stay in
W. All computations ran in systemd user units capped at one core each, at most two at a
time. Nothing is committed.

## Notation

Notation follows `math.md` §2–3.
- P is the chart of an octagon-free set S at a hull vertex a: no 7-cap, no 8-gon.
- U, L, G, H = L ∪ G and R = U \ G come from the minimum-slope partition.
- Residual labels are (6 − F₋, E₊ − 1) ∈ [1..4] × [1..6]. Balanced labels are
  (E₋ − 1, E₊ − 1) ∈ [1..5]².
- f_a is the height of column a (the cap coordinate) of an incoming state.
- **N(cap ≤ α, cup ≤ β)** is the largest real point set (distinct x, general position) in
  which every cap has at most α points, every cup at most β points, and no 8 points are
  in convex position. "cup ≤ 7" is automatic.
- **ETV** is the Erdős–Tuza–Valtr conjectured value. It is Σ_{i=8−b}^{a−2} C(6, i) for
  "no a-cap, no b-cup, no 8-gon". It is proved only for a = 4 or b = 4 (Baek).

## 1. Summary: what would break 310

The one structural lever found is **capacity rows from ETV-type statements on level sets
of the two catalogs**.
- Lemma A: the owners of residual states with f₁ ≥ 5 form a 5-cap-free octagon-free set.
- Lemma B: a balanced set splits into two pieces, one with no 6-cap and no 7-cup, the
  other the y-mirror case.
- Combined with the existing rows, weak forms of the ETV conjecture already break 310:

| sufficient statement | ETV says | how it is used | consequence |
|---|---|---|---|
| **(W1)** N(cap ≤ 4) ≤ 57: every **58**-point set with no 5-cap has a convex octagon | 42 | row h(F) ≥ 27 on the 84 states with f₁ ≥ 5, plus the 2,650 rows and h₀ = 0. **Exact branch-and-bound tree**: 1,327 nodes, 664 integer leaves, minimum margin 1, replayed by `scripts/omission_tree.check_tree` (§3). Sharp: capacity 58 admits an exact 33-hole vector | residual holes ≥ 34, n_R ≤ 120, **ES(8) ≤ 309** |
| **(W1⁺)** N(cap ≤ 4) ≤ 56: every **57**-point set with no 5-cap has a convex octagon | 42 | row h(F) ≥ 28. Exact tree for budget 34: 8,879 nodes, 4,440 leaves, margin ≥ 1. Sharp: capacity 57 admits an exact 34-hole vector | holes ≥ 35, n_R ≤ 119, **ES(8) ≤ 308** |
| N(cap ≤ 4) ≤ 49 | 42 | row h(F) ≥ 35; exact LP dual bound 121/3 | holes ≥ 41, ES(8) ≤ 302 |
| **(W2)** N(cap ≤ 5, cup ≤ 6) ≤ 93: every 94-point set with no 6-cap and no 7-cup has a convex octagon | 56 | Lemma B alone: n_H ≤ 2N | n_H ≤ 186, **ES(8) ≤ 309** |
| N(cap ≤ 5, cup ≤ 6) ≤ 92 | 56 | Lemma B alone | n_H ≤ 184, ES(8) ≤ 307 |
| N(cap ≤ 5, cup ≤ 6) ≤ 78 | 56 | Lemma B alone, or the single row h(f₁=5) ≥ 48 with the 3,131 rows (exact dual bound 65.48) | n_H ≤ 156, ES(8) ≤ 279 |
| both ETV values (42 and 56) | – | Lemmas A and B | n_R ≤ 106 (LP 47⅓ with the rows), n_H ≤ 112, ES(8) ≤ 220 |

How much room there is:
- (W1) is 15 points weaker than the ETV value, (W1⁺) 14 and (W2) 37.
- Both residual thresholds are exact and sharp over the present Lean rows:
  - capacity 57 forces 34 holes, and capacity 58 admits an exact 33-hole vector;
  - capacity 56 forces 35 holes, and capacity 57 admits an exact 34-hole vector.
- The present catalogs implicitly allow about 61 owners for (W1): the four known 33-hole
  residual vectors occupy 61, 60, 61 and 62 of the 84 states of F. So any capacity
  c ≤ 59 already kills all four.
- They allow about 90 owners for each balanced half (the 71/72-hole vectors).
- Real 64-point octagon-free sets have |R₆| ≤ 9 and |H₆| ≤ 1 in all 26 charts tried (§4).

None of these statements is proved tonight. Plain CaDiCaL does not decide them, nor even
the heptagon analogue (§5).

## 2. Level-set lemmas (PROVED)

**Lemma A (residual split).** Let R be residual (no 6-cap, no 8-gon, no junction). Let
R₆ be the set of points of R at which a 6-cup of R ends; equivalently, the owners of
states with f₁ ≥ 5. Let R₇ be the set where a 7-cup ends (f₁ = 6). Then:
- (i) R₆ has no 5-cap;
- (ii) R \ R₆ has no 6-cup (and no 6-cap);
- (iii) no 4-cap of R starts at a point of R₇;
- (iv) R₆ \ R₇ has no 7-cup.

Hence n_R ≤ N(cap ≤ 4) + N(cap ≤ 5, cup ≤ 5) and |O ∩ F| ≤ N(cap ≤ 4), where F is the set
of 84 states with f₁ ≥ 5.

*Proof.*
- (i) A 5-cap inside R₆ starts at a point that ends a 6-cup of R. That is a junction.
- (ii) and (iv): the last vertex of a 6-cup (7-cup) inside the set would end a 6-cup
  (7-cup) of R.
- (iii) Let c₁…c₆v be a 7-cup ending at v and v z₁ z₂ z₃ a 4-cap. If (c₆, v, z₁) were a
  cup, c₁…c₆ v z₁ would be an 8-cup, hence an octagon. So it is a cap, and c₆ v z₁ z₂ z₃
  is a 5-cap (consecutive triples negative). It starts at c₆, which ends the 6-cup
  c₁…c₆. That is a junction.
- f₁(v) is (length of the longest cup of R ending at v) − 1, which gives the state
  description. ∎

Part (iii) is the geometric content of row 973: exactly the 28 states with f₁ = 6,
demand 6, Baek capacity 22, and it is derivable from label domains. All 23 existing block
rows lie inside F: they are Baek two-level compressions inside the 5-cap-free family.
(W1) is the three-level analogue covering all of F. Splitting F further with (iv) does
not help: N(cap ≤ 4, cup ≤ 6) has ETV value 41, but the four vectors already occupy only
38–40 of the 56 states with f₁ = 5.

**Lemma B (balanced split).** Let H be balanced (no 7-cap, no 7-cup, no 8-gon). Let H₆
be the set where a 6-cup of H ends (states with f₁ = 5). Let H⁶ be the set where a 6-cap
ends (f₅ ≥ 1). Then:
- H₆ has no 6-cap;
- H \ H₆ has no 6-cup;
- H⁶ has no 6-cup;
- the junction set G of the partition lies in H \ H⁶. Points of U end no 6-cap of P,
  because caps ending in U extend to the right.

Hence n_H ≤ N(cap ≤ 5, cup ≤ 6) + N(cap ≤ 6, cup ≤ 5) = 2·N(cap ≤ 5, cup ≤ 6), by
y-reflection.

*Proof.* Let y₁…y₆ be a cap in H₆ and c₁…c₅y₁ a 6-cup of H. If (c₅, y₁, y₂) were a cup,
c₁…c₅y₁y₂ would be a 7-cup. So it is a cap, and c₅y₁…y₆ is a 7-cap. The other claims are
the mirror argument and the last-vertex argument. ∎

These splits are the cup–cap recursion that the 5 November memo calls "fed by ETV
values". The new point tonight is quantitative: through the existing rows, a statement
far weaker than ETV suffices, and §3 gives an exact certificate.

**Family sweep.** W/families.py takes every upper set {f₁ ≥ t₁, …} of both catalogs. For
each it derives the forbidden chain lengths from the label domains and finds the largest
capacity c* that still gives LP > 33 (residual) or > 65 (balanced). See
data/families_out.json.
- The best small targets are F (c* = 56, slack 14 over ETV 42) and its subfamilies
  {f₁ ≥ 5, f₂ ≥ 1} (55, 13) and {f₁ ≥ 5, f₂ ≥ 2} (53, 11).
- Balanced single-family targets have c* = 59–68 at slack 3–12. Lemma B, at slack 37, is
  the better balanced target.
- The domain-only families {f₁ = f₂ = 5} (no 5-cap) and {f₅ ≥ 2} (no 5-cup) give LP
  55.81 and 55.79 at their ETV value 41, against the base 55.

## 3. Conditional consequences (exact certificates)

Residual: with the 2,650 rows, h₀ = 0 and h(F) ≥ 84 − c, the LP value is 89⅓ − c for
42 ≤ c ≤ 60. It is 28.40 at c = 61 and 27.74 at c = 62; the base is 27. The Lo family
(70 states with f₁ ≤ 4) needs c ≤ 54 against ETV 50.

Balanced:
- One row h(f₁ = 5) ≥ 126 − c gives LP 65.49 at c = 78 and 66.96 at c = 76.
- The two rows given by Lemma B give exactly 252 − 2c.

Exact rational duals for the key claims are in data/exact_dual.out (W/exact_dual.py).

The main thread's coupled-core rows do not move these thresholds. Its 47,173 new rows
(snapshot of `res33-20261113/newrows.json`, 03:07 KST; 49,823 rows in all) leave the base
LP at 27.0 and the F threshold at c ≤ 56: the LP values are 33.33, 32.33, …, 28.40 for
c = 56, …, 61 (W/cap_with_cegar.py, read-only). Those rows cut integer points only, so
(W1) and the CEGAR are complementary. A capacity c in 57–59 combined with them might still
give 34 holes, but that needs a branch-and-bound.

**Integer thresholds. Warning: HiGHS MIP optima are not reliable here.**
W/cap_mip.py runs HiGHS branch-and-bound on the 2,650 rows, h₀ = 0 and h(F) ≥ 84 − c. It
reported "optimal 35" at c = 57 (5,867 nodes, 64 s). The project's exact solver
(`experiments/omission-final313-2026-10-11/search/pbb_strong.py`, extra row h(F) ≥ 27,
budget 34) then returned a **34-hole witness**, data/pbb_witness34_c57.json. Checked
exactly: 34 holes, state 0 occupied, 0 of 2,650 rows violated, 57 F-states occupied. So
HiGHS's c = 57 claim is false; floating-point MIP optima are not evidence. What remains
valid:

| capacity c | holes forced | how known |
|---|---|---|
| 59 | 33 is attained (no gain) | HiGHS incumbent; also implied by the row below |
| 58 | 33 is attained (no gain) | exact vector data/cap_mip58_sol.json: 33 holes, 58 F-states, 0 violations |
| **57** | **≥ 34, and 34 is attained** | exact pbb_strong tree at budget 33: 16 contexts, 1,310 search nodes, 28 s on 2 cores; assembled tree of 1,327 nodes and 664 leaves, minimum margin 1, replayed exactly. The witness above attains 34. **ES(8) ≤ 309** |
| **56** | **≥ 35** | exact pbb_strong tree at budget 34: 8,862 search nodes, 129 s; assembled tree of 8,879 nodes and 4,440 leaves, minimum margin 1, replayed exactly. The LP alone gives only ≥ 34 (100/3; one-leaf certificate below). **ES(8) ≤ 308** |
| 55 | ≥ 35 | exact LP dual 103/3. ES(8) ≤ 308 |
| 54 / 53 / 52 | ≥ 36 / 37 / 38 | HiGHS LP value 89⅓ − c, rounded up; floating point, exact duals only for 56, 55, 49. ES(8) ≤ 307 / 306 / 305 |
| 49 | ≥ 41 | exact LP dual 121/3. ES(8) ≤ 302 |
| 42 (ETV) | ≥ 48 | LP 47⅓. ES(8) ≤ 295 |

The two trees are data/tree_c57_b33.json.gz (SHA-256 `ddcf84e9…`) and
data/tree_c56_b34.json.gz (`4e89f051…`), with extra-row files data/extra_F27.json
(`9a561566…`) and data/extra_F28.json (`5e002fb5…`). Each tree has the 313 record's
layout: the root branches on state 0, and the one pending child (state 0 missing) is
discharged by `OmissionResidualZeroState.zero_mem_residualOccupied`. They were built with
`experiments/omission-final313-2026-10-11/search/pbb_strong.py` (K_TOP 16, D_TOP 8,
K_LOW 4, 2 processes) and assembled and replayed with `search/assemble.py`. The replay is
`scripts/omission_tree.check_tree`, which recomputes every leaf margin in unbounded
integers. They are certificates over the 2,650 Lean rows plus the hypothetical capacity
row; they are not Lean-checked yet.

For c ≤ 55 the HiGHS optima (35, 36, 37, 38) coincide with these LP roundings. The
MIP logs are kept in data/ only as a record of the false claim.

The main thread's CEGAR rows kill the exact c = 58 vector: 7 of its 50,183 rows are
violated, one of them cake_lpr-certified (read-only check of
`res33-20261113/newrows.json` and `certified.jsonl`). So the capacity row and the CEGAR
rows combine; an exact branch-and-bound over both, at c = 57–62, would show how weak the
capacity statement can get.

**One-leaf certificate for (W1) ⇒ residual budget 33** (W/dual_weights.py,
data/w1_leaf_certificate.json). Multiplied by 6, the rational dual (denominators 1, 2, 3
and 6) gives integer weights on 11 rows:
- the capacity row h(F) ≥ 28, weight 6;
- rows 475, 507, 542, 583, 625 and 632 (8-state cycle rows, demand 1), weight 1 each;
- row 730, weight 3;
- row 1234 (demand 2), weight 2;
- row 1627 (demand 3), weight 1;
- row 1798 (demand 4), weight 4.

Every column load is ≤ 6, with column 0 fixed occupied. The weighted demand is D = 200,
and leaf test (3.3) with C = 6 gives 6·33 = 198 < 200. So budget 33 is excluded by one
leaf, with no branching. Once the capacity row is a theorem, ES(8) ≤ 309 needs only this
leaf and the existing `Final310Compact` composition.

## 4. Negative and neutral results

- **L1, the root's +1 is intrinsic. PROVED.** S is octagon-free iff P has no 7-cap and no
  8-gon.
  - (⇐) An octagon through a gives a 7-cap of P: X ∪ {a} is convex iff X is a cap in the
    chart.
  - Conversely, every such P lifts back: translate it to y < 0 and invert Φ_a.
  - So max|S| = 1 + max|P| exactly. No argument about P recovers the +1, and P's first
    point (in R, state 0) is already used.
- **L2, the partition is canonical given the chart. PROVED.** Put α(u) = min over x < u
  of slope(x, u) and β(u) = min over y > u of slope(u, y). A neighbour extending every cap
  ending at u must lie to the right with slope < α(u); one extending every cup starting
  at u must lie to the left with slope < β(u). So u ∈ U ⟺ β(u) < α(u).
  - The max-slope rule is the min-slope rule of the mirror chart.
  - The four classes U∩U′, U∩L′, L∩U′ and L∩L′ have cup–cap catalogs
    126 + 84 + 126 + 126 = 462 (Pascal), with no junction saving.
- **L3, fan monotonicity. PROVED; REFUTED as a source of rows.** Exact labels satisfy:
  for p < q < r, if (p,q,r) is a cup then E₊(p,r) ≥ E₊(p,q), E₋(p,r) ≤ E₋(p,q) and
  F₋(p,r) ≤ F₋(q,r); the inequalities reverse for a cap.
  - Proof: replace the last (or first) vertex of an attaining chain and use 4-point
    transitivity. It also holds for signotopes.
  - Empirical check (W/fan_check.py): 0 violations in 30,735 triples.
  - Six-order check with fan rules (W/fan.py; the base reproduces model.py's table
    exactly):
    - residual: 167,805 → 167,805 forced list triples, though 7,271 more chronological
      orientations are forced;
    - balanced: 557,898 → 557,898, with 31,066 more.
  - Coupled model (October rank-search model.py plus fan clauses, W/fan_coupled.py):
    71 of 71 recorded "necessary-model SAT" supports stay SAT.
- **L4, junction at owners. PROVED but implied.** f₁(u) ≥ 5 ⇒ every outgoing label of u
  has cap coordinate ≥ 2, and E₊(v) ≥ 7 ⇒ F₋(v) ≤ 3. Both follow from state separation,
  the excluded label (1, 6) and the restriction f₁ = 6 ⇒ f₂ = 6.
- **L5, internal omission bounds. REFUTED as a route.** These apply the omission method
  to the sub-problems themselves, with lazy separation: W/cap5_omission.py uses cycle
  rows and the simple Baek blocks; W/omission_gen2.py uses cycle rows only. Each loop ended with no violated list, so the values are
  exact optima of those row systems:
  - N(cap ≤ 4) ≤ 71 (13 of 84 holes);
  - N(cap ≤ 5, cup ≤ 6) ≤ 104 (22 of 126 holes).
  - Both are far from 56 and 93, and cuts cannot help, since integer vectors attain these
    optima.
- **L6, no new Baek block supports among upper and lower sets. REFUTED**
  (W/block_search.py).
  - Residual: only the f₁ = 6 family and its subsets compress, and all are implied by
    row 973.
  - Balanced: no upper or lower set of more than 22 states admits a two-level cap or cup
    compression.
  - Targeted search inside the four 33-hole vectors (W/block_augment.py,
    W/block_greedy.py):
    - each of the 23 existing blocks keeps 22 occupied states, as its row requires, and
      in no case can a further occupied state be added while a two-level cap compression
      survives;
    - greedy removal from the occupied F-states finds nothing larger than 6.
    - So no violated Baek row of this local kind exists for these vectors. The compression
      test reproduces all 23 existing blocks: 0 conflicts.
- **L7, joint H/R rows. OPEN.**
  - There are no cross-part labels: H- and R-states are computed inside their parts, so
    no orientation of a mixed triple is forced, and octagons with vertices in both parts
    are never used.
  - **In/out double injection with Hall's theorem (W/hall.py, W/hall_witness.py).
    PROVED as a valid joint constraint; REFUTED as a cut.**
    - Every balanced point v has an in-state I(v) and an out-state O(v). The out-states
      are the in-states of the x-reversed configuration, which is balanced, so they
      satisfy all 3,131 rows.
    - For u < v < w the triple is a cap or a cup. Concatenating the chains through v
      gives a + a′ ≤ 5 or b + b′ ≤ 5 for every in-cell (a, b) of I(v) and out-cell
      (a′, b′) of O(v).
    - So the occupied in-states and out-states are perfectly matched inside this
      compatibility graph (density 0.31).
    - The LP with both vectors, equal population and the 650 Hall rows for X = {I ⊇ C},
      |C| ≤ 2, stays at 55.
    - The exact matching condition does not cut the known 72- and 71-hole witnesses
      either: HiGHS finds a feasible out-vector with a perfect matching for each.
  - The 26 real charts below show that (|H|, |R|) swings from (36, 27) to (6, 57) with the
    root.
  - No valid joint inequality between H and R was found. The Hall constraint above couples
    two injections of the same part, not H and R.
- **L8, real 64-point sets (W/real_sets.py, data/real_sets_out.json).** Four octagon-free
  64-point sets (saturation witness 8, ot0000, ot0001m, ot0002), each at all 7 hull roots:
  - All Lemma A/B checks hold.
  - Maxima over the charts: |H| 36, |R| 57, |R₆| 9, |R₇| 2, |H₆| 1, |G| 1.
  - Side remark: witness 8 at root (62, −6399444) has G = ∅ and a 57-point residual part.
    This shows D₈ ≥ 57, against the floor 50 quoted from Schroeder in
    `docs/RELATED_WORK_2026-10-14.md`; the same note says ETV would give D₈ ≤ 57.
  - That residual part was re-checked independently (W/residual57.py, exact
    rationals): it has longest cap 5, no junction, and largest convex polygon a heptagon.
    The last uses the exact criterion max over endpoint pairs of (cap + cup) = 9. The 57
    chart points are in data/residual57_points.json.
  - So the balanced-plus-residual scheme can never go below C₈ + D₈ + 2 ≥ 62 + 57 + 2 = 121.
- **L9, Baek capacity 21 for row 973 under attainment. OPEN.** Not attempted beyond
  Lemma A(iii).
- **L10, a split of P that bypasses the partition. PROVED, but the target is too large.**
  Let P₇ be the points of P at which a 7-cup ends.
  - P \ P₇ is balanced (no 7-cup, no 7-cap), so it has at most 187 points.
  - P₇ has no 6-cap: in a 6-cap y₁…y₆ of P₇ with 7-cup c₁…c₆y₁, the triple (c₆, y₁, y₂)
    must be a cap, or an 8-cup appears; then c₆y₁…y₆ is a 7-cap.
  - Hence |S| ≤ 1 + 187 + N(cap ≤ 5). So "every 121-point set with no 6-cap has a convex
    octagon" also gives ES(8) ≤ 309. ETV says 58 points suffice (slack 63), but a
    121-point SAT instance is out of reach.
  - Under ETV the balanced class has C₈ = ETV(8,7,7) = 62, and N(cap ≤ 5) = 57. Both this
    split and the partition then give |S| ≤ 1 + 62 + 57 = 120, which is exactly the floor
    121 of L8. Lemma B is lossy by comparison: under ETV it gives n_H ≤ 112, not 62.
- **Capacity that kills the four known 33-hole vectors.** Their F-occupancies are 61, 60,
  61 and 62, so N(cap ≤ 4) ≤ 59 ("every 60-point 5-cap-free set has a convex octagon")
  would exclude all four. N(cap ≤ 4) ≤ 56 excludes every 33-hole vector.

## 5. SAT experiments on the capacity statements

The encoder is W/etv_sat2.py.
- Signotope axioms on all 4-tuples.
- Caps and cups tracked from their first point by their last pair.
- Every octagon type (a-cap, b-cup) on common endpoints with a + b = 10 is forbidden.
- It is a sound relaxation of real point sets: UNSAT at n proves N ≤ n − 1.
- CaDiCaL 2.1.3, one core, `-q`.

| instance | result |
|---|---|
| no 4-cap, n = 22 | SAT (positive control) |
| no 4-cap, n = 23 (Baek's theorem), first encoder W/etv_sat.py | UNSAT in 10 min 49 s, no certificate kept |
| no 4-cap, n = 23, **certified control** with W/etv_sat2.py (13,915 vars, 138,391 clauses; CNF SHA-256 `b6328e84…`, encoder `ecc8a4e9…`) | UNSAT (`--lrat --no-binary`, 1.6 GB proof), then cake_lpr **s VERIFIED UNSAT**; 9 min 51 s CPU in all |
| no 5-cap, n = 30 | SAT (positive control) |
| heptagon analogue: no 5-cap, no 7-gon, n = 26 (ETV value) | SAT in 0.09 s |
| heptagon, n = 27 / 34 / 40 | no verdict in 240 / 120 / 120 s |
| no 5-cap, n = 50 (would give ES(8) ≤ 302) | no verdict in 12.5 CPU-min (stopped) |
| no 5-cap, n = 57 = (W1⁺) (245,252 vars, 6.19 M clauses) | two runs, default and `--unsat`; see §7. (W1) itself would be the n = 58 instance |
| **(W2)**: no 6-cap, no 7-cup, n = 94 (1.10 M vars, 46.96 M clauses) | no verdict in 11 CPU-min (6.3 GB peak, swapping under the 6.5 GB cap); stopped to give the core to a second (W1) run |

The heptagon rows matter: 14 points of slack over ETV did not make the problem easy in
two minutes. Plain CDCL is not the right tool at these sizes.

Counting alone does not reach these instances either. The internal omission optimum
(cycle rows only) of the heptagon analogue is 10 holes of 56, so up to 46 points pass,
against ETV 26 (W/omission_gon.py). Adding omission lemmas as redundant clauses would
therefore still leave the geometric search to the solver.

## 6. Next step

1. **Prove (W1)**: every 58-point set with no 5-cap has a convex octagon (SAT instance
   n = 58), or (W1⁺) at 57 points. Either is the cheapest route below 310. The arithmetic
   side is already certified by the exact trees of §3 (1,327 and 8,879 nodes).
   - Option a: a Schroeder-style whole-catalog coupled SAT on the 84 internal states,
     with occupancy indicators, at least 57 occupied, and cycle rows as clauses. This is
     the method of his (7,5,6) ETV certificate.
   - Option b: cube-and-conquer with symmetry breaking on the signotope instance
     (march_cu is not built here).
2. In parallel, (W2) (94 points) is the balanced counterpart; it would give n_H ≤ 186
   with no rows at all.
3. The pipeline itself is certified: Baek's n = 23 instance from the same encoder is
   VERIFIED UNSAT by cake_lpr (§5). A proof of (W1) from this encoder would therefore be
   checkable as is. What remains is the encoder's soundness (real points ⇒ signotope and
   chain clauses), which is a short Lean lemma in the style of ENCBLEAN.
4. Lemma A(i), Lemma B and the one-leaf certificate are small Lean additions on top of
   `SlopePartition` / `ResidualStates` and `OmissionCertificates`. Do them only once a
   capacity statement is proved. Concretely, for (W1):
   - State the capacity as a hypothesis on configurations: `CapW1 : ∀ m (d : Configuration m),
     ¬ d.HasCap 5 → ¬ HasConvexNGon 8 (univ.image d.point) → m ≤ 57`.
   - Apply it to the restriction of a residual configuration c to the owners of F.
     Lemma A(i) supplies no 5-cap; `Subsets.restrict` keeps general position and octagon
     avoidance. This gives the row h(F) ≥ 27 for `c.residualOccupied`.
   - The exact tree data/tree_c57_b33.json.gz (1,327 nodes) proves
     `Excludes(2650 + 1)Zero 33`. With h(F) ≥ 28 the one-leaf certificate does the same, and
     data/tree_c56_b34.json.gz gives budget 34. The proof of
     `residual_bound_of_excludes2650` then gives `Partition.ResidualBound 120`.
   - `PopulationBounds.forces_of_population_bounds` with
     `Compact310.balanced_population_187` gives `ForcesConvexNGon 309 8`, conditional only
     on `CapW1`.

## 7. Status at stop time

### 7a. Main-thread note (as written into this file at about 04:45 KST)

*Written by the main thread at about 04:45 KST.* This fork stopped at its turn limit at about 04:00,
before writing this section. The outcomes of its background jobs, read from
`/home/jay/research/data/theory310-20261113`:

| job | outcome |
|---|---|
| `cap_mip.py 59` (2,650 rows + h(F) ≥ 25, HiGHS, mip_rel_gap 0) | **COMPUTED: optimum exactly 33** (132,690 nodes, 1,111 s, `cap_mip59b.log`). Capacity 59 with the base rows does **not** force 34 holes. Main-thread follow-up (RES33N20261113 `capvec.jsonl`): the 33-hole vector found under capacity 59 occupies 59 F-states and violates 6 of the main thread's new coupled rows. |
| `cap_target.py 34 800 1 57` (CP-SAT, capacity 57, budget 34) | UNKNOWN after 800 s (`cpsat57_b34.log`) |
| `cap4_n57` (W1 signotope SAT, no 5-cap, n = 57; default and `--unsat`) | no verdict while running. Partial LRAT files `cap4_n57.lrat` (0.8 GB) and `cap4_n57u.lrat` were kept; they are useless without a verdict and can be deleted with the author's OK. The units end by their own timeouts (about 05:00 and 05:20 KST) or are stopped by the main thread at 05:35. |
| `baek23_v2` (Baek control, n = 23) | cake_lpr **s VERIFIED UNSAT** (§5) |

What remains open from this record: any proof of N(cap ≤ 4) ≤ c with c ≥ 56 (or of (W2)). This is the
cheapest structural route to ES(8) ≤ 309. With the main thread's new rows, c = 59 may already suffice:
the main thread's capacity-capped CP-SAT search (all rows + h(F) ≥ 25) found no 33-hole vector. That is
evidence, not proof (see RES33N20261113).

### 7b. Fork update (written by the theory fork, 04:50–05:25 KST)

The fork did not stop at 04:00; it kept working until 05:25, and the main thread's note
above predates the following.

- **Exact arithmetic thresholds (§3).** Over the 2,650 Lean rows with state 0 occupied:
  - h(F) ≥ 27 (capacity 57) forces Σh ≥ 34. The pbb_strong tree has 1,327 nodes and 664
    leaves, margin ≥ 1, replayed by `check_tree` in exact integers.
  - h(F) ≥ 28 (capacity 56) forces Σh ≥ 35 (8,879 nodes, 4,440 leaves).
  - Both are sharp: exact witnesses exist at 58 F-states (33 holes) and at 57 F-states
    (34 holes).
  - So **(W1): every 58-point 5-cap-free set has a convex octagon ⇒ ES(8) ≤ 309**, and
    **(W1⁺): every 57-point one ⇒ ES(8) ≤ 308**. Over the Lean rows alone, capacity 58 or 59
    is not enough.
- **HiGHS gave a false optimum.** `cap_mip.py 57` reported "optimal 35", but the exact solver
  found a 34-hole vector (data/pbb_witness34_c57.json, checked exactly). MIP status lines
  from HiGHS are therefore not used as evidence anywhere in this record. The "optimum
  exactly 33" at c = 59 in the note above is consistent with the exact c = 58 vector
  (33 holes), which also satisfies h(F) ≥ 25.
- **SAT.** All runs were stopped by the fork without a verdict:
  - (W1⁺) instance n = 57, default: 1 h 47 min CPU;
  - (W1⁺) instance n = 57, `--unsat`: 8 min CPU, paused most of the time to give the core
    to the exact runs;
  - (W2) instance n = 94: 11 min CPU.
  - The partial LRAT files are useless without a verdict and can be deleted with the
    author's OK.
- **Capacity plus the main thread's cake_lpr-certified rows.** Exact pbb_strong at budget 33
  with the 2,650 rows, all 492 cake_lpr-certified coupled rows (snapshot 04:49, including the
  8 cores refuting vector N5) and h(F) ≥ 25 (capacity 59). It was restarted at 04:50 when
  the coordinator reported the 8 new rows.
  - **Result: WITNESS** at about 05:20, after one context had closed with 43,387 nodes.
  - It is a 33-hole vector with exactly 59 F-states occupied (data/pbbcombo_c59_witness.json).
  - Checked exactly: state 0 occupied; 0 of 2,650 rows violated; 0 of the 492 certified rows
    violated, and the capacity row holds.
  - It does violate 5 of the main thread's 50,568 rows, which are not all certified.
  - So capacity 59 plus the certified rows is not enough. To use the main thread's evidence
    that c = 59 suffices with all its rows, one of those 5 rows covering this vector must
    be certified. This vector is a concrete next target for the coupled CEGAR.
- All units of this fork are stopped (05:22).
